-- Native Fortune God reward route after warp.lua. No RAM writes.
local mem = PCSX.getMemPtr()
local function r16(a) return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local entered, previous, since
local seen = {}
L.on_frame(function(n)
  if n > 18000 then L.fail('Fortune God route timeout'); return end
  if mem[0x8C490] ~= 0x2D then
    if entered then
      assert(seen[1] and seen[2] and seen[3] and seen[4], 'missing native reward states')
      L.log(string.format('FORTUNE_RETURN mode=%02X f%d', mem[0x8C490], n))
      L.shot('return.png')
      L.finish(0)
    end
    return
  end
  entered = entered or n
  if n - entered < 180 then return end
  local state = r16(0xCD580)
  if previous ~= state then
    previous, since = state, n
    seen[state] = true
    L.log(string.format('FORTUNE state=%d sub=%d amount=%d f%d', state, r16(0xCD582), r32(0xCD57C), n))
  end
  if (state == 1 or state == 2) and n - since == 60 then
    L.shot(string.format('context_%d.png', state))
  end
  if state == 4 and n - since == 180 then L.shot('reward.png') end
  if n % 3 == 0 then L.shot(string.format('actor_%06d.png', n)) end
  if (state == 1 or state == 2 or state == 4) and n % 90 == 0 then L.press('circle', 12) end
end)
