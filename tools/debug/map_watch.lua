-- Read-only map-load diagnostic. Pass alongside warp.lua; no debugger needed.
local mem = PCSX.getMemPtr()
local function r16(a) a = a & 0x1FFFFF; return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
L.on_frame(function(n)
  if n < 3300 or n % 300 ~= 0 then return end
  L.log(string.format('MAPWATCH f%d map=%d script=%08X pc=%08X op=%04X', n,
    r16(0x8008C570), r32(0x800BF7B8), r32(0x800BF7BC), r16(0x800BF7FC)))
end)
