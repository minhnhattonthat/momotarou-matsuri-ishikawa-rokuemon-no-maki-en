-- Native op-26 capture during warp.lua OPS, with a temporary origin-field fixture.
local mem = PCSX.getMemPtr()
local function r16(a) a = a & 0x1FFFFF; return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local first, captured, origin
L.on_frame(function(n)
  if captured or mem[0x8C490] ~= 1 then return end
  -- EXE 80034D50 gates captions on the incoming-map field (<37, or a
  -- special 126/139 pair). The new-game opening carries no world-map origin.
  -- Reproduce origin 0 in RAM so the existing native caption handler opens.
  local pc = r32(0xBF7BC)
  if not origin and pc >= 0x80000000 and pc < 0x80200000 and r16(pc) == 0x26 then
    origin = r32(0x8C510)
    for i = 0, 3 do mem[0x8C510 + i] = 0 end
    L.log('CAPTION_ORIGIN previous=' .. origin .. ' fixture=0')
  end
  if r16(0xBF7FC) ~= 0x26 then return end
  local object = r32(0xBF7D8)
  if object < 0x80000000 or object >= 0x80200000 or r16(object) == 0 then return end
  first = first or n
  if n - first == 10 then
    local x, y = r16(object + 4), r16(object + 6)
    L.log(string.format('CAPTION x=%d y=%d glyphs=%d f%d', x, y, r16(object + 2), n))
    L.shot('caption.png')
    for i = 0, 3 do mem[0x8C510 + i] = (origin >> (8 * i)) & 255 end
    captured = true
  end
end)
