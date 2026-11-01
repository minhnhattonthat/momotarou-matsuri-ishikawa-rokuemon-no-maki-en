-- Cold-boot Janken 7 result coverage. Use alongside warp.lua, SCENE='game_m11_0d', HOLD=6000.
-- Pick seven rock panels with ordinary controller input, then confirm OK. No game code/RAM is patched.
local mem = PCSX.getMemPtr()
local entered
L.on_frame(function(n)
  if mem[0x8C490] ~= 0x0D then return end
  entered = entered or n
  local age = n - entered - 1500
  if age >= 0 and age < 7 * 90 then
    if age % 90 == 0 then L.press('up', 6) end
    if age % 90 == 45 then L.press('right', 6) end
  elseif age >= 7 * 90 and age % 45 == 0 then
    L.press('circle', 6)
  end
end)
