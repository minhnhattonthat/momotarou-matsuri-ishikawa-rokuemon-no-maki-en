-- Cold-boot card navigation; pair with warp.lua SCENE='card_album', HOLD=-1.
-- The warp enables collectibles in RAM. This probe uses the controller to open
-- the album and turn pages; the game's loader chooses every card and palette.
-- A RAM-only input latch clears Right once the next index arrives. Disc loads
-- can preserve the old pad snapshot and turn several pages after one tap.
local mem = PCSX.getMemPtr()
local function r16(a) return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local entered, opened, due, count, retries = nil, false, nil, 0, 0
L.on_frame(function(n)
  if mem[0x8C490] ~= 0x4C then return end
  entered = entered or n
  if opened and r32(0xE2324) >= count then
    -- held / newly pressed PS1 pad bits, EXE 0x8008C410 / 0x8008C420.
    mem[0x8C411] = mem[0x8C411] & 0xDF
    mem[0x8C421] = mem[0x8C421] & 0xDF
    for i = 0, 3 do mem[0xE2328 + i] = 0 end
  end
  if n - entered == 600 then L.shot('album.png') end
  if n - entered == 700 then L.press('circle', 6); opened = true; due = n + 240 end
  if not opened or n < due then return end
  local index = r32(0xE2324)
  -- A short press can land inside a CD-load stall. Retry only the unchanged
  -- preceding page; never accept a skip or relabel an old screenshot.
  if count > 0 and index == count - 1 and r16(0xE232C) == 7 and retries < 3 then
    retries = retries + 1
    L.log(string.format('CARD retry %d -> %d f%d', index + 1, count + 1, n))
    L.press('right', 8)
    due = n + 240
    return
  end
  if index ~= count or r16(0xE232C) ~= 7 then
    L.fail(string.format('card navigation failed: expected %d, got %d, state %d',
        count, index, r16(0xE232C)))
    return
  end
  L.log(string.format('CARD %03d state %d f%d', index + 1, r16(0xE232C), n))
  L.shot(string.format('card_%03d.png', index + 1))
  retries = 0
  count = count + 1
  if count >= (CARD_COUNT or 100) then L.shot('final.png'); L.finish(0); return end
  L.press('right', 8)
  due = n + 180
end)
