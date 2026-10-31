-- Log the top-level game mode [0x8008C490] (EXE switch 0x80020F40) and the loaded overlay each time either changes.
-- usage: emu.py ... --script tools/debug/modelog.lua [--var "WATCH={0x8008C490,0x8008C494}"]
local mem = PCSX.getMemPtr()
local function u32(a) a = a & 0x1FFFFF; return mem[a] + mem[a + 1] * 256 + mem[a + 2] * 65536 + mem[a + 3] * 16777216 end
local words = WATCH or { 0x8008C490 }
local last = {}
L.on_frame(function(n)
  local cur = {}
  for i, a in ipairs(words) do cur[i] = string.format("%08X=%X", a, u32(a)) end
  cur[#cur + 1] = string.format("ovl=%08X", u32(0x800CB338 + 0x10))  -- overlay fingerprint
  local ids = {}  -- loaded-file slots 0x800A3DE0 {u32 base, u16 id} (docs/re/text.md); names: tools/fileids.py
  for i = 0, 31 do
    local a = 0x800A3DE0 + i * 8
    if u32(a) ~= 0 then ids[#ids + 1] = string.format("%d", (u32(a + 4) & 0xFFFF)) end
  end
  cur[#cur + 1] = "files=" .. table.concat(ids, ",")
  local s = table.concat(cur, " ")
  if s ~= last.s then L.log(string.format("%6d %s", n, s)); last.s = s end
end)
