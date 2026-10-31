-- Log every text line the game draws through build_line (docs/re/engine.md), once per distinct (x, y, text).
--   emu.py CUE --out DIR --script tools/lua/textlog.lua [--var TEXTLOG_EVERY=5]
-- Reads the line-object pool (base gp+0x514, count gp+0x51C; gp = 0x8008C0B8) every TEXTLOG_EVERY frames.
-- Line form: "TEXT f<frame> <x>,<y> <text>": digraphs as ASCII, Japanese glyphs as {XXXX} (Shift-JIS, from the
-- glyph table at 0x80081BE0), controls as {KG} etc. tools/textlog.py decodes and summarises the logs.
local mem = PCSX.getMemPtr()
local function r16(a) a = a & 0x1FFFFF; return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local POOL, COUNT, GLYPHS = 0x8008C5CC, 0x8008C5D4, 0x80081BE0
local every = TEXTLOG_EVERY or 5
local seen = {}

local function rec_text(r)
  local c = r16(r)
  if c < 0x20 then  -- glyph: tpage, clut, u, v -> table index -> SJIS
    local page = (c - 0x1E) * 2 + (r16(r + 2) & 1)
    local idx = page * 441 + math.floor(r16(r + 6) / 12) * 21 + math.floor(r16(r + 4) / 12)  -- LuaJIT: no //
    if idx < 0 or idx >= 1766 then return "{?}" end
    local s = r16(GLYPHS + 2 * idx)
    return string.format("{%04X}", s)
  end
  local lo, hi = c & 0xFF, c >> 8
  if lo >= 0x20 and lo <= 0x7F and hi >= 0x20 and hi <= 0x7F and c ~= 0x2020 then
    local s = ""
    for _, b in ipairs({ lo, hi }) do if b ~= 0x7F then s = s .. string.char(b) end end
    if c == 0x474B or c == 0x504B or c == 0x4E4B then return "" end  -- KG KP KN
    return s
  end
  if c == 0x4081 then return "{8140}" end
  if c == 0x2020 then return "  " end
  return ""
end

L.on_frame(function(n)
  if n % every ~= 0 then return end
  local base, cnt = r32(POOL), r32(COUNT)
  if base < 0x80000000 or base >= 0x80200000 or cnt == 0 or cnt > 256 then return end
  for i = 0, cnt - 1 do
    local o = base + i * 0x10C
    local k = r16(o + 2)
    if r16(o) ~= 0 and k > 0 and k <= 40 then
      local parts = {}
      for j = 0, k - 1 do parts[#parts + 1] = rec_text(o + 8 + j * 8) end
      local t = table.concat(parts)
      local key = string.format("%d,%d %s", r16(o + 4), r16(o + 6), t)
      if t ~= "" and not seen[key] then
        seen[key] = true
        L.log(string.format("TEXT f%d %s", n, key))
      end
    end
  end
end)
