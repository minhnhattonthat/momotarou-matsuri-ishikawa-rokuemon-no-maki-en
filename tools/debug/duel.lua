-- Read-only verification after the M16 initializer has copied the native
-- player-count selector. Waiting for the timer, without Circle input, reaches
-- the real Duel cue; mashing Circle ends the round before that cue appears.
assert(DUEL_PLAYERS == 1 or DUEL_PLAYERS == 2, 'set DUEL_PLAYERS=1 or 2')
local mem = PCSX.getMemPtr()
local entered, checked
local function r32(a)
  return mem[a] + mem[a + 1] * 256 + mem[a + 2] * 65536 + mem[a + 3] * 16777216
end
L.on_frame(function(n)
  if mem[0x8C490] ~= 0x12 then return end
  entered = entered or n
  if not checked and n - entered >= 600 then
    local expected = DUEL_PLAYERS - 1
    assert(r32(0x8C580) == expected, 'wrong native player-count selector')
    assert(r32(0xD1104) == expected, 'M16 did not retain native player count')
    L.log(string.format('DUEL players=%d selector=%d f%d', DUEL_PLAYERS, expected, n))
    checked = true
  end
end)
