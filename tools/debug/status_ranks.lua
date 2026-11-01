-- Cold saved-Status fixtures. Seed record values AFTER the game's save load;
-- the unmodified Status code selects its rank/illustration and builds counters.
-- No ANM selectors, glyphs, screen coordinates or save files are modified.
assert(STATUS_RANK and STATUS_RANK >= 0 and STATUS_RANK <= 610)
local mem = PCSX.getMemPtr()
local function r32(a)
  return mem[a] + mem[a + 1] * 256 + mem[a + 2] * 65536 + mem[a + 3] * 16777216
end
local function w32(a, v)
  for i = 0, 3 do mem[a + i] = (v >> (i * 8)) & 255 end
end
local loaded, seeded, entered
L.on_frame(function(n)
  local mode = mem[0x8C490]
  if mode == 0x4A then loaded = true end
  if loaded and not seeded and mode == 0x49 then
    local remaining = STATUS_RANK
    for i = 0, 69 do
      local rank = math.min(10, remaining)
      remaining = remaining - rank
      local record = 0xBDBF0 + i * 0x1C
      w32(record, rank > 0 and 1 or 0)
      w32(record + 4, rank)
    end
    if STATUS_STRESS then
      -- 100 real card flags; retain the following five noncollectible bits.
      for i = 0, 11 do mem[0xBD9F8 + i] = 255 end
      mem[0xBDA04] = mem[0xBDA04] | 15
      w32(0x8C504, 9999999) -- money
      w32(0x8C50C, 9999999) -- steps
      w32(0x8C560, (99 * 60 + 59) * 3600) -- playtime in 60 Hz frames
      -- The step counter is visible only with item 8 (pedometer) in the
      -- key-item list, scanned by EXE 800328F4(category 1, item 8).
      local added = false
      for i = 0, 63 do
        local a = 0xBDAE0 + i * 2
        local value = mem[a] + mem[a + 1] * 256
        if value == 8 then added = true; break end
        if value == 65535 then mem[a], mem[a + 1] = 8, 0; added = true; break end
      end
      assert(added, 'no free key-item slot for the pedometer fixture')
    end
    seeded = true
    L.log(string.format('STATUS_SEEDED rank=%d stress=%s f%d', STATUS_RANK, tostring(STATUS_STRESS), n))
  end
  if seeded and mode == 0x4E then
    entered = entered or n
    if n - entered == 550 then
      local rank, tier = r32(0xE2630), r32(0xE27BC)
      assert(rank == STATUS_RANK, 'Status did not read seeded ranks')
      if STATUS_STRESS then
        assert(r32(0xE262C) == 100 and r32(0xE27C0) == 9999999
          and r32(0xE27C4) == 9999999 and r32(0xE27B8) == (99 * 60 + 59) * 3600,
          'Status did not read the complete counter stress fixture')
      end
      L.log(string.format('STATUS_RESULT rank=%d tier=%d cards=%d money=%d steps=%d time=%d',
        rank, tier, r32(0xE262C), r32(0xE27C0), r32(0xE27C4), r32(0xE27B8)))
      L.shot('status.png')
    end
  end
end)
