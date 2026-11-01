-- Read-only shared HUD usage probe. Pair with warp.lua and CLICK=45.
-- The ANM-part pool (EXE 0x8001B07C) has a base at 0x8008C4F0, count at
-- 0x8008C46C, stride 0x20: ANM pointer +0, selected item +6.
-- Capture first use of each Japanese-bearing small HUD item, after 120
-- frames for the fade. Presence in RAM is discovery, not visual proof.
local mem = PCSX.getMemPtr()
local function r16(a) a = a & 0x1FFFFF; return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local function valid(a) return a >= 0x80000000 and a < 0x80200000 end
local wanted = { [20]=true, [31]=true, [32]=true, [33]=true, [34]=true,
  [42]=true, [48]=true, [49]=true, [73]=true, [77]=true, [78]=true,
  [79]=true, [85]=true }
local seen, pending = {}, {}
L.on_frame(function(n)
  for item, due in pairs(pending) do
    if n >= due then L.shot(string.format('hud_%02d.png', item)); pending[item] = nil end
  end
  if n % 15 ~= 0 then return end
  local anm
  for slot = 0, 31 do
    local a = 0xA3DE0 + slot * 8
    local base = r32(a)
    if r16(a + 4) == 350 and valid(base) then
      local candidate = base + r32(base + 8)
      if valid(candidate) and r32(candidate) == 0x004D4E41 and r32(candidate + 4) == 87 then
        anm = candidate
      end
    end
  end
  if not anm then return end
  local base, count = r32(0x8008C4F0), r32(0x8008C46C)
  if not valid(base) or count > 4096 then return end
  for i = 0, count - 1 do
    local part = base + i * 0x20
    if r32(part) == anm then
      local item = r16(part + 6)
      if wanted[item] and not seen[item] then
        seen[item], pending[item] = true, n + 120
        L.log(string.format('HUD item %d f%d part %08X', item, n, part))
      end
    end
  end
end)
