-- Cold saved-record Rank Details tour. Only native record fields are seeded;
-- navigation, context selection, graphics loading and rendering are native.
local mem = PCSX.getMemPtr()
local function r16(a) return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local function w32(a, v)
  for i = 0, 3 do mem[a + i] = (v >> (8 * i)) & 255 end
end
local loaded, seeded, status, entered, ready, leaving, last_press
local target = 0
L.on_frame(function(n)
  if n > 95000 then L.fail('Rank Details timeout at page ' .. target); return end
  local mode = mem[0x8C490]
  if mode == 0x4A then loaded = true end
  if loaded and not seeded and mode == 0x49 then
    for i = 0, 69 do
      local a = 0xBDBF0 + 28 * i
      w32(a, 1); w32(a + 4, DETAIL_EMPTY and 0 or i % 11)
      w32(a + 8, DETAIL_EMPTY and 0xFFFFFFFF or 9999)
    end
    seeded = true
    L.log('DETAIL_SEEDED empty=' .. tostring(DETAIL_EMPTY or false))
  end
  if seeded and mode == 0x4E then status = true end
  if status and not entered and L.route_done() then
    assert(r32(0xE2610) == 0, 'Status cursor is not on Rank Details')
    L.shot('status_before.png')
    L.press('circle', 6); L.press('-', 900)
    entered = true; FRAMES = 100000
  end
  if entered and not leaving and mode == 0x4F and L.route_done() then
    assert(mem[0xA3F8F] == 4, 'not the native saved-Status Rank Details context')
    local page = r32(0x8C5C0)
    if page > target then L.fail('Rank Details skipped a page'); return end
    if page ~= target or r16(0xE27FC) ~= 1 then
      if page == target - 1 and r16(0xE27FC) == 1 and last_press and n - last_press > 900 then
        L.log(string.format('DETAIL_RETRY %d -> %d f%d', page, target, n))
        L.press('right', 6); L.press('-', 300); last_press = n
      end
      return
    end
    ready = ready or n
    if n - ready < 240 then return end
    local id = r32(0xE077C + target * 12 + 8)
    local rank = r32(0xBDBF0 + id * 28 + 4)
    assert(rank == (DETAIL_EMPTY and 0 or id % 11), 'record rank changed')
    L.shot(string.format('detail_%02d.png', target))
    L.log(string.format('DETAIL_PAGE %d record=%d rank=%d context=4 f%d', target, id, rank, n))
    if target == 42 then
      L.press('cross', 6); L.press('-', 900); leaving = true
    else
      target = target + 1
      L.press('right', 6); L.press('-', 300); last_press = n
    end
    ready = nil
  end
  if leaving and mode == 0x4E and L.route_done() then
    ready = ready or n
    if n - ready >= 240 then
      assert(r32(0xE2610) == 0, 'return lost Status selection')
      L.shot('status_return.png'); L.log('DETAIL_RETURN status cursor=0')
      L.finish(0); return
    end
  end
end)
