-- Exec watch over EXE ranges tools/deadcode.py calls unreached (candidate space for relocated code strings).
--   emu.py CUE --debugger --script tools/lua/deadwatch.lua ...   logs "DEADHIT <range> pc=<pc>" once per range
-- Ranges = engine.RELOC_FREE (keep in step).
local RANGES = DEAD_RANGES or { {0x80058A98, 0x80059118}, {0x8006F778, 0x8006FF08} }
local keep, hit = {}, {}
for i, r in ipairs(RANGES) do
  keep[#keep + 1] = PCSX.addBreakpoint(r[1], "Exec", r[2] - r[1], "deadwatch", function()
    if not hit[i] then
      hit[i] = true
      L.log(string.format("DEADHIT %08X pc=%08X", r[1], PCSX.getRegisters().pc))
    end
    PCSX.resumeEmulator()
    return true
  end)
end
