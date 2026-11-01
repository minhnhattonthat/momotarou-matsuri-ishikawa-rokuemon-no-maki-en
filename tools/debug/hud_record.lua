-- Opt-in stress fixture for the object-count HUD's four-digit record.
-- EXE 0x80042514 reads game 15's record at 0x800BDBF0 + 15*28, field +8
-- (story) or +24 (trial). Seed both before OVLM15 0x800CDA3C reads it.
-- Writing the HUD's cached record after creation leaves its old dash objects
-- across the digits. This fixture uses the real initial record-loading path.
-- RAM only; no memory-card writes, digit objects or textures are changed.
local mem = PCSX.getMemPtr()
L.on_frame(function()
  if HUD_RECORD and mem[0x8C490] == 17 then
    for _, offset in ipairs({8, 24}) do
      for i = 0, 3 do mem[0xBDBF0 + 15 * 28 + offset + i] = (HUD_RECORD >> (i * 8)) & 255 end
    end
  end
end)
