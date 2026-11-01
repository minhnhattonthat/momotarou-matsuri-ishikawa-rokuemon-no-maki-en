-- Controller-only entry into Slippity Slide's left course after a cold warp.
-- The entry room needs movement into a course, not repeated Circle presses.
local mem = PCSX.getMemPtr()
local entered
L.on_frame(function(n)
  if mem[0x8C490] ~= 21 then return end
  entered = entered or n
  local age = n - entered
  if age == 800 then L.press('left', 60) end
  if age == 900 then L.press('up', 8) end
  if age == 930 then L.press('left', 120) end
  if age == 1100 then L.press('up', 120) end
  if age > 1400 and age % 60 == 0 then L.press('circle', 6) end
end)
