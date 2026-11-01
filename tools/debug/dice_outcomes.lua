-- Cold M56/M59 outcome coverage after warp.lua; HOLD=-1 and no CLICK.
-- Only the M59 encounter selector is set, once before its native initializer.
-- All rolls, RNG, outcomes, sprites and return transitions are game-controlled.
local mem = PCSX.getMemPtr()
local function r16(a) return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local game = assert(DICE_GAME)
assert(game == 56 or game == 59)
local opponent = DICE_OPPONENT or 0
assert(opponent >= 0 and opponent <= 5)
local mode = game == 56 and 0x34 or 0x37
local state_at = game == 56 and 0xCCFE8 or 0xCE514
local dice_at = game == 56 and 0xCCFCC or 0xCE4F4
local result_state = game == 56 and 6 or 7
local banner = game == 56 and 0xCCE68 or 0xCE390
local entry = game == 56 and 4 or (opponent < 5 and 9 or 16)
local period, offset = DICE_PERIOD or 90, DICE_OFFSET or 0
assert(period >= 30 and offset >= 0)
local entered, previous, since, selected, rounds, returned = nil, nil, nil, false, 0, false
L.on_frame(function(n)
  if n > 20000 then L.fail('dice encounter timeout'); return end
  if mem[0x8C490] ~= mode then
    if entered and not returned then
      assert(rounds > 0, 'encounter exited without a result')
      returned = true
      L.log(string.format('DICE_RETURN game=%d mode=%02X rounds=%d f%d', game, mem[0x8C490], rounds, n))
      L.shot('return.png')
      L.finish(0)
    end
    return
  end
  if not selected then
    -- OVLM59 800CCC14 reads 8008C540 when the native entry context is 1.
    -- warp.lua has just redirected mode 02; the M59 initializer runs next.
    if game == 59 then
      for i = 0, 3 do mem[0x8C540 + i] = i == 0 and opponent or 0 end
    end
    selected = true
    entered = n
    L.log(string.format('DICE_ENTRY game=%d opponent=%d period=%d offset=%d f%d', game, opponent, period, offset, n))
  end
  if n - entered < 180 then return end
  if game == 59 then assert(r32(0xCE508) == opponent, 'native opponent initializer disagrees') end
  local state = r16(state_at)
  if state ~= previous then
    previous, since = state, n
    L.log(string.format('DICE_STATE state=%d sub=%d dice=%d,%d f%d', state, r16(state_at + 2), r16(dice_at), r16(dice_at + 2), n))
    if state == result_state then rounds = rounds + 1 end
  end
  if state == result_state and n - since == 12 then
    local player, rival = r16(dice_at), r16(dice_at + 2)
    assert(player >= 1 and player <= 6 and rival >= 1 and rival <= 6, 'invalid native dice')
    local item = player > rival and 0 or (player < rival and 1 or 2)
    assert(r32(banner + 0x10) == item and r32(banner + 0x14) == entry, 'native banner selector disagrees with dice')
    L.log(string.format('DICE_RESULT round=%d item=%d entry=%d player=%d rival=%d f%d', rounds, item, entry, player, rival, n))
    L.shot(string.format('result_%02d_%d.png', rounds, item))
  end
  if (state == 8 or state == 9) and n - since == 120 then
    L.shot(string.format('dialogue_%d.png', state))
  end
  -- Match warp.lua's 600-frame arrival delay, then vary only pad timing.
  if n - entered >= 600 and (n - entered - 600 + offset) % period == period - 1 then
    L.press('circle', 6)
  end
end)
