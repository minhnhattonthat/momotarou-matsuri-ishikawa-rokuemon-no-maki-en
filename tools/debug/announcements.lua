-- Cold-boot shared-announcement fixture. Use with warp.lua, SCENE='game_m11_0d'.
-- Opt in with ANNOUNCEMENTS=true. Pause via the controller, then select each
-- M990D:3 item through the pause item's RAM table pointer. Optional source:
-- ANNOUNCEMENT_SOURCE={file=294,entry=18,items={0,1,2,3,4}} for M010D awards.
-- ANNOUNCEMENT_MODE=3, ANNOUNCEMENT_PAUSE=2500, ANNOUNCEMENT_CLICKS=true can
-- reach a different minigame's paused gameplay before showing its own sprites.
-- No pixels, ANM records,
-- code or disc data are changed. The real renderer uses each item's own palette,
-- dimensions and anchors. This verifies assembly, not score/rank gameplay logic.
-- ANNOUNCEMENT_REPLACE={from=7,to=10} substitutes one natural result instead of
-- opening Pause; pair with janken.lua to show Full Mastery without a pause menu.
local mem = PCSX.getMemPtr()
local function r16(a) a = a & 0x1FFFFF; return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local function w32(a, v)
  a = a & 0x1FFFFF
  for i = 0, 3 do mem[a + i] = (v >> (8 * i)) & 255 end
end
local entered, tableptr, offsets, started, last, sharedanm, sourceoffsets
local order = ANNOUNCEMENT_SOURCE and ANNOUNCEMENT_SOURCE.items
    or { 15, 13, 18, 16, 11, 14, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 }
L.on_frame(function(n)
  if not ANNOUNCEMENTS or mem[0x8C490] ~= (ANNOUNCEMENT_MODE or 0x0D) then return end
  entered = entered or n
  if not tableptr then
    for slot = 0, 31 do
      local a = 0xA3DE0 + slot * 8
      local base = r32(a)
      if r16(a + 4) == 350 and base >= 0x80000000 and base < 0x80200000 then
        local anm = base + r32(base + 12)
        if r32(anm) == 0x004D4E41 and r32(anm + 4) == 71 then
          tableptr = anm + r32(anm + 8)
          sharedanm = anm
          offsets = {}
          for i = 0, 70 do offsets[i] = r32(tableptr + i * 4) end
          L.log(string.format('ANNOUNCEMENTS table %08X', tableptr))
        end
      end
    end
  end
  local age = n - entered
  if ANNOUNCEMENT_REPLACE then
    if tableptr then
      local from, to = ANNOUNCEMENT_REPLACE.from, ANNOUNCEMENT_REPLACE.to
      local sources = type(from) == 'table' and from or { from }
      for _, item in ipairs(sources) do
        assert(offsets[item] and offsets[to], 'announcement replacement out of range')
        w32(tableptr + item * 4, offsets[to])
      end
      if not last then
        L.log(string.format('ANNOUNCEMENT replace %s -> %d', table.concat(sources, ','), to))
        last = to
      end
    end
    return
  end
  if tableptr and not sourceoffsets then
    if not ANNOUNCEMENT_SOURCE then sourceoffsets = offsets
    else
      for slot = 0, 31 do
        local a = 0xA3DE0 + slot * 8
        local base = r32(a)
        if r16(a + 4) == ANNOUNCEMENT_SOURCE.file and base >= 0x80000000 and base < 0x80200000 then
          local anm = base + r32(base + ANNOUNCEMENT_SOURCE.entry * 4)
          if r32(anm) == 0x004D4E41 then
            local tab = anm + r32(anm + 8)
            sourceoffsets = {}
            for _, item in ipairs(order) do
              assert(item >= 0 and item < r32(anm + 4), 'source item out of range')
              sourceoffsets[item] = (anm + r32(tab + item * 4) - sharedanm) % 0x100000000
            end
            L.log(string.format('ANNOUNCEMENTS source %d:%d at %08X',
                ANNOUNCEMENT_SOURCE.file, ANNOUNCEMENT_SOURCE.entry, anm))
          end
        end
      end
    end
  end
  local pause = ANNOUNCEMENT_PAUSE or 1500
  if ANNOUNCEMENT_CLICKS and age >= 700 and age < pause - 120 and age % 60 == 0 then L.press('circle', 6) end
  if age == pause then L.press('start', 6); started = n + 120 end
  if not started or n < started or not tableptr then return end
  if not sourceoffsets then L.fail('announcement source was not loaded'); return end
  local step = math.floor((n - started) / 90) + 1
  if step > #order then
    w32(tableptr + 15 * 4, offsets[15])
    L.log('ANNOUNCEMENTS fixture complete')
    L.finish(0)
    return
  end
  local item = order[step]
  w32(tableptr + 15 * 4, sourceoffsets[item])
  if item ~= last then
    L.log(string.format('ANNOUNCEMENT item %d f%d', item, n))
    last = item
  end
  if (n - started) % 90 == 60 then L.shot(string.format('announcement_%02d.png', item)) end
end)
