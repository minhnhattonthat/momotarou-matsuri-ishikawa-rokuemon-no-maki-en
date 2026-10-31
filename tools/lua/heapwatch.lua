-- Log heap A use (docs/re/disc.md §Heap): bytes in use now/peak and the heap bounds, whenever they change.
--   emu.py CUE --out DIR --script tools/lua/heapwatch.lua      (or warp_all.py --probe tools/lua/heapwatch.lua)
-- gp = 0x8008C0B8: gp+0x2F0 bytes in use, gp+0x300 peak since the last heap init, gp+0x2E8 highest block end.
-- Bounds: start 0x8008C474, size 0x8008C4AC (set per game mode by 0x8001ED4C / 0x8001ED7C).
-- Line: "HEAP f<frame> use=<n> peak=<n> top=<addr> start=<addr> size=<n> free=<size - peak>".
local mem = PCSX.getMemPtr()
local function r16(a) a = a & 0x1FFFFF; return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local last = ""
L.on_frame(function(n)
  if n % 10 ~= 0 then return end
  local use, peak, top = r32(0x8008C3A8), r32(0x8008C3B8), r32(0x8008C3A0)
  local start, size = r32(0x8008C474), r32(0x8008C4AC)
  local key = string.format("peak=%d top=%08X start=%08X size=%d", peak, top, start, size)
  if key ~= last then
    last = key
    L.log(string.format("HEAP f%d use=%d %s free=%d", n, use, key, size - peak))
  end
end)
