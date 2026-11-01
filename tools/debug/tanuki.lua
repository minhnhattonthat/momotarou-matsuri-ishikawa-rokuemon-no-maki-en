-- Both controllers roll through native Even Tanuki rounds. No RAM writes.
-- Pair with warp.lua and two_player.lua, HOLD=6000 and no CLICK.
local mem = PCSX.getMemPtr()
local pad2 = PCSX.SIO0.slots[2].pads[1]
local circle = PCSX.CONSTS.PAD.BUTTON.CIRCLE
local entered
L.on_frame(function(n)
  if mem[0x8C490] ~= 0x10 then
    pad2.clearOverride(circle)
    return
  end
  if not entered then
    assert(mem[0x8C580] == 1, 'Even Tanuki needs native 2P selection')
    entered = n
    L.log(string.format('TANUKI players=2 selector=1 f%d', n))
  end
  if n % 90 == 0 then L.press('circle', 12) end
  if (n + 45) % 90 < 12 then pad2.setOverride(circle) else pad2.clearOverride(circle) end
end)
