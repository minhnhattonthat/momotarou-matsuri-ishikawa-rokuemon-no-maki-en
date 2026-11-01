-- Cold menu-header coverage. Controller navigation after the existing warp or
-- saved-Status route; only the album's native played flag is seeded in RAM.
assert(TITLE_CASE == 'album' or TITLE_CASE == 'quick' or TITLE_CASE == 'name'
    or TITLE_CASE == 'saved_details', 'unknown title case')
local mem = PCSX.getMemPtr()
local function r16(a) return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local expected = TITLE_CASE == 'quick' and 0x50 or TITLE_CASE == 'name' and 0x51 or 0x4F
local state = expected == 0x50 and 0xE2ABC or expected == 0x51 and 0xE2D78 or 0xE27FC
local loaded, seeded, entered, ready
FRAMES = 20000
L.on_frame(function(n)
  if n > 19000 then L.fail('menu title timeout: ' .. TITLE_CASE); return end
  local mode = mem[0x8C490]
  if mode == 0x4A then loaded = true end
  if loaded and not seeded and mode == 0x49 then
    -- One played game enables Album without changing the record or rank.
    mem[0xBDBF0], mem[0xBDBF1], mem[0xBDBF2], mem[0xBDBF3] = 1, 0, 0, 0
    seeded = true
  end
  if (TITLE_CASE == 'album' or TITLE_CASE == 'saved_details')
      and seeded and mode == 0x4E and L.route_done() and not entered then
    assert(r32(0xE2610) == 0, 'Status cursor is not on the first icon')
    L.shot('status_before.png')
    if TITLE_CASE == 'album' then
      L.press('cross', 6); L.press('-', 300)
      L.press('left', 6); L.press('-', 90)
    end
    L.press('circle', 6); L.press('-', 900)
    entered = true
  end
  if mode == expected and r16(state) == 1 and L.route_done() then
    ready = ready or n
    if n - ready >= 600 then
      if TITLE_CASE == 'album' or TITLE_CASE == 'saved_details' then
        assert(entered, 'header reached without requested menu navigation')
      end
      local context = mem[0xA3F40 + mode]
      if TITLE_CASE == 'saved_details' then assert(context == 4) end
      if TITLE_CASE == 'name' then assert(context == 3) end
      L.shot('title.png')
      L.log(string.format('MENU_TITLE %s mode=%d context=%d state=1 f%d',
        TITLE_CASE, mode, context, n))
      L.finish(0)
    end
  else ready = nil end
end)
