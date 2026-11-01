-- Native M50 countdown and Start cue. Pair with warp.lua, HOLD=-1.
-- Read game state, advance instructions and optionally time a Circle response.
-- No RAM writes, sprite substitutions or outcome edits.
local mem = PCSX.getMemPtr()
local function r16(a) return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local entered, previous, since, cue_previous, cue_since
local captured = {}
local answered, result_since
assert(TIMING_OUTCOME == nil or TIMING_OUTCOME == 'success' or TIMING_OUTCOME == 'early')
L.on_frame(function(n)
  if n > 18000 then L.fail('native timing countdown timeout'); return end
  if mem[0x8C490] ~= 0x2E then return end
  entered = entered or n
  if n - entered < 180 then return end
  local state, cue = r16(0xCC77C), r32(0xCC638)
  if TIMING_OUTCOME and n % 6 == 0 then L.shot(string.format('actor_%06d.png', n)) end
  if state ~= previous then
    previous, since = state, n
    L.log(string.format('TIMING state=%d cue=%d f%d', state, cue, n))
  end
  if cue ~= cue_previous then
    cue_previous, cue_since = cue, n
    L.log(string.format('TIMING cue=%d item=%d f%d', cue, r32(0xCC640), n))
  end
  if (state == 1 or state == 4) and n - since >= 120 and n % 45 == 0 then
    L.press('circle', 6)
  end
  if cue >= 1 and cue <= 4 and n - cue_since == 15 and not captured[cue] then
    assert(r32(0xCC640) == cue - 1, 'native cue item disagrees with countdown')
    assert(r32(0xCC644) == 2, 'unexpected cue ANM')
    L.shot(string.format('countdown_%d.png', cue))
    L.log(string.format('TIMING_CAPTURE cue=%d item=%d state=%d f%d', cue, cue - 1, state, n))
    captured[cue] = true
    if cue == 4 then
      assert(captured[1] and captured[2] and captured[3], 'missing native countdown step')
      if not TIMING_OUTCOME then L.finish(0) end
    end
  end
  if TIMING_OUTCOME and state == 5 and cue == 0 and not answered then
    local target = r32(0xCC784) * (TIMING_OUTCOME == 'success' and 60 or 30)
    if r32(0xCC760) >= target then
      L.log(string.format('TIMING_PRESS %s timer=%d target=%d f%d',
        TIMING_OUTCOME, r32(0xCC760), target, n))
      -- The original disc's early test can take 18 frames to sample the pad.
      -- Hold across that gap; still require the actual early result below.
      L.press('circle', TIMING_OUTCOME == 'early' and 30 or 6)
      answered = n
    end
  end
  if answered and n - answered <= 36 then
    L.log(string.format('TIMING_INPUT age=%d held=%04X new=%04X timer=%d state=%d',
      n - answered, r16(0x8C410), r16(0x8C420), r32(0xCC760), state))
  end
  if state == 6 then
    local result = r32(0xCC774)
    if not result_since then
      L.log(string.format('TIMING_EVALUATED %s result=%d target_seconds=%d f%d',
        TIMING_OUTCOME, result, r32(0xCC784), n))
    end
    result_since = result_since or n
    assert(answered, 'result reached without timed controller response')
    assert(result == (TIMING_OUTCOME == 'success' and 1 or 2), 'unexpected timing result')
    if n - result_since == 180 then
      assert(captured[4], 'result reached without complete countdown')
      L.log(string.format('TIMING_RESULT %s result=%d f%d', TIMING_OUTCOME, result, n))
      L.shot('result.png')
      L.finish(0)
    end
  end
end)
