-- Read-only placeholder-portrait trace; requires --debugger.
-- Use with warp.lua SCENE='map_gv3100_294', HOLD=600.
-- Texture upload is not proof of a displayed sprite. Trace both the animated
-- and static sprite bind APIs (dialogue portraits use the static one).
local function reg(n) return tonumber(PCSX.getRegisters().GPR.r[n]) end
for _, address in ipairs({0x8001E160, 0x8001E224}) do
  L.on_exec(address, function()
    local file, entry = reg(6), reg(7)
    if file == 476 then
      L.log(string.format('PORTRAIT_BIND f%d api=%08X file=%d entry=%d', L.frame, address, file, entry))
    end
  end)
end
L.on_exec(0x8001C604, function()
  if reg(4) == 475 then
    L.log(string.format('PORTRAIT_UPLOAD f%d file=475 entry=%d', L.frame, reg(5)))
  end
end)
