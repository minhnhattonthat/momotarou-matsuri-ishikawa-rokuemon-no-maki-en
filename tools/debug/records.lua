-- Opt-in QA fixture: mark the first minigame played so Game Album can open on a new save.
-- EXE 0x800435F4 scans 70 records at 0x800BDBF0, stride 0x1C; nonzero first word enables the album.
-- Use with --script tools/debug/records.lua --var RECORDS=true and the saved-record cold-boot route.
-- RAM only: never included in the built disc or applied to the source memory card.
if RECORDS then
  local mem = PCSX.getMemPtr()
  L.on_frame(function()
    mem[0xBDBF0] = 1
  end)
end
