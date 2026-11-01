-- Read-only map-load diagnostic. Pass alongside warp.lua; no debugger needed.
local mem = PCSX.getMemPtr()
local function r16(a) a = a & 0x1FFFFF; return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
L.on_frame(function(n)
  if n < 3300 or n % 300 ~= 0 then return end
  L.log(string.format('MAPWATCH f%d map=%d script=%08X pc=%08X op=%04X', n,
    r16(0x8008C570), r32(0x800BF7B8), r32(0x800BF7BC), r16(0x800BF7FC)))
  local regs = PCSX.getRegisters()
  local sp = tonumber(regs.GPR.r[29])
  local stack = {}
  for offset = 0, 124, 4 do
    local value = r32(sp + offset)
    if value >= 0x80010000 and value < 0x800F5000 then
      stack[#stack + 1] = string.format('+%02X=%08X', offset, value)
    end
  end
  L.log(string.format('MAPWATCH cpu=%08X ra=%08X sp=%08X %s',
    tonumber(regs.pc), tonumber(regs.GPR.r[31]), sp, table.concat(stack, ' ')))
  local ok, detail = pcall(function()
    return string.format('MAPWATCH status=%08X cause=%08X epc=%08X badvaddr=%08X',
      tonumber(regs.CP0.r[12]), tonumber(regs.CP0.r[13]),
      tonumber(regs.CP0.r[14]), tonumber(regs.CP0.r[8]))
  end)
  L.log(ok and detail or 'MAPWATCH CP0 unavailable')
  if MAPWATCH_DUMP and n == 4200 then L.dump_ram('mapwatch_ram.bin') end
end)
