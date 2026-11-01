-- Cold saved-record tour. Seed record fields after save load, then navigate all
-- 43 Game Album pages (or six Quick Match pages with ALBUM_TRIAL=true)
-- using the real controller and loaders. RAM only.
local mem = PCSX.getMemPtr()
local function r32(a)
  return mem[a] + mem[a + 1] * 256 + mem[a + 2] * 65536 + mem[a + 3] * 16777216
end
local function w32(a, v)
  for i = 0, 3 do mem[a + i] = (v >> (8 * i)) & 255 end
end
local loaded, seeded, status, entered, page_at, last_press
local target = 0
L.on_frame(function(n)
  local mode = mem[0x8C490]
  if mode == 0x4A then loaded = true end
  if loaded and not seeded and mode == 0x49 then
    for i = 0, 69 do
      local a = 0xBDBF0 + 28 * i
      for _, offset in ipairs({0, 16}) do w32(a + offset, 1) end
      for _, offset in ipairs({4, 20}) do w32(a + offset, 10) end
      for _, offset in ipairs({8, 24}) do w32(a + offset, ALBUM_EMPTY and 0xFFFFFFFF or 9999) end
    end
    -- These are the record ids used by the money, five-digit score and time pages.
    if not ALBUM_EMPTY then
      for _, offset in ipairs({8, 24}) do
        w32(0xBDBF0 + 23 * 28 + offset, 999999)
        w32(0xBDBF0 + 31 * 28 + offset, 99999)
        for _, id in ipairs({18, 60, 19, 20, 22, 24, 27, 39}) do
          w32(0xBDBF0 + id * 28 + offset, 359999)
        end
      end
    end
    seeded = true
    L.log('ALBUM_SEEDED empty=' .. tostring(ALBUM_EMPTY or false))
  end
  if seeded and mode == 0x4E and not status then status = n end
  if status and not entered and L.route_done() then
    L.press('cross', 6); L.press('-', 300); L.press('left', 6); L.press('-', 90)
    if ALBUM_TRIAL then L.press('up', 6); L.press('-', 90) end
    L.press('circle', 6); L.press('-', 900)
    entered = true
    FRAMES = 100000
  end
  if entered and mode == (ALBUM_TRIAL and 0x50 or 0x4F) then
    local page = r32(ALBUM_TRIAL and 0x8C5B8 or 0x8C5C0)
    local state = r32(ALBUM_TRIAL and 0xE2ABC or 0xE27FC) & 65535
    if page == target and state == 1 and L.route_done() then
      page_at = page_at or n
      if n - page_at >= 240 then
        L.shot(string.format('record_%02d.png', page))
        L.log(string.format('ALBUM_PAGE %d f%d', page, n))
        if target == (ALBUM_TRIAL and 5 or 42) then L.finish(0); return end
        target, page_at = target + 1, nil
        L.press('right', 6); L.press('-', 300); last_press = n
      end
    elseif page > target then
      L.fail('album skipped page ' .. target .. ' to ' .. page)
    elseif L.route_done() and last_press and n - last_press > 900 then
      L.press('right', 6); L.press('-', 300); last_press = n
    end
  end
  if n > 90000 then L.fail('album tour timed out at ' .. target) end
end)
