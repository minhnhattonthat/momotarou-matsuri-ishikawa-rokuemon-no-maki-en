-- Select 2P through Quick Match's native player-count menu before warp.lua
-- redirects the selected game. Pair with a game scene; no RAM edits.
-- Both emulator controller ports must be connected (tools/emu-config/pcsx.json).
-- State waits accommodate Japanese/English message typing times.
WARP_GAME_INPUT = false
local mem = PCSX.getMemPtr()
local entered, chosen, checked, previous, since
local function r32(a)
  return mem[a] + mem[a + 1] * 256 + mem[a + 2] * 65536 + mem[a + 3] * 16777216
end
L.on_frame(function(n)
  local mode = mem[0x8C490]
  if entered and mode >= 2 and mode <= 0x3D and not checked then
    -- EXE 0x800428F0 reads this selector; M16 copies it to 0x800D1104.
    assert(chosen and r32(0x8C580) == 1, 'native 2P selection was not retained')
    L.log(string.format('TWO_PLAYER verified mode=%02X selector=1 f%d', mode, n))
    checked = true
  end
  if mode ~= 0x50 then return end
  entered = entered or n
  assert(n - entered < 3000, '2P menu timed out')
  local state = mem[0xE2ABC] + mem[0xE2ABD] * 256
  if state ~= previous then
    previous, since = state, n
    L.log(string.format('TWO_PLAYER menu state=%d f%d', state, n))
  end
  local age = n - since
  if state == 1 and age == 180 then L.press('circle', 6) end
  if state == 2 then
    assert(r32(0xA3DD4) ~= 0, 'connect emulator controller port 2 before this route')
    if age == 180 then
      assert(not chosen, '2P menu unexpectedly reopened')
      L.press('down', 6)
      chosen = true
    end
    if age == 220 then L.shot('two_player_menu.png') end
    if age == 240 then L.press('circle', 6) end
  end
  assert(state ~= 3, 'native controller-presence check failed')
  if state == 4 and age == 180 then L.press('circle', 6) end
end)
