-- Controller-only Rabbit-Turtle Race route after warp.lua enters game_m23_19.
-- It picks distinct runners, confirms, watches the race and advances results.
-- Use HOLD=10000 and --shot-every 60; no score, position or outcome edits.
local entered
local mem = PCSX.getMemPtr()
L.on_frame(function(n)
  if mem[0x8C490] ~= 25 then return end
  entered = entered or n
  local age = n - entered
  if age >= 650 and age < 1800 and age % 60 == 0 then L.press('circle', 6) end
  if age >= 1800 then
    if age % 180 == 0 then L.press('down', 6)
    elseif age % 180 == 60 then L.press('circle', 6)
    elseif age % 180 == 120 then L.press('circle', 6) end
  end
end)
