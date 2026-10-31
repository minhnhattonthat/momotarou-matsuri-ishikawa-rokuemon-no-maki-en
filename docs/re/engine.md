# English text engine (phase 5)

Code: `tools/engine.py` (codec, font, hooks), `tools/insert.py` (script/ -> disc files), `tools/build.py`
(`--marker`, `--qa ID=TEXT`). Tests: `tests/test_engine.py`, `tests/test_build.py`.

## Text drawing path (verified: static read + the marker build draws through it)
- `build_line(str a0, x a1, y a2, ot a3)` = EXE 0x80029DF4 turns one text line (u16 units, ends at a unit whose
  low byte is 0) into a **line object** from the pool at `gp+0x514` (count `gp+0x51C`, allocated by 0x8002AACC):
  0x10C bytes = `{u16 used, u16 count, u16 x, u16 y, 32 x 8-byte records, u32 ot at +0x108}`. **32 records per
  line, unchecked** (a 33rd overwrites +0x108): text units + control units (KG/KP/KN, colours) together.
- Each unit is first looked up in the control table at 0x800829A8 (21 x `{u16 code, u16 value}`: `　` 0x8140,
  two spaces, KG KP KN, R0-R4 (value 0xF000: number), MM QQ UU II ZZ (0xFF00: name/string insert via 0x80029C1C),
  ww rr gg bb oo dd (value = colour index 0-5)). Controls are stored as a record with the raw code.
- Other units go to `append(code, obj, colour)` = 0x80029AC4: linear search of the SJIS table at 0x80081BE0
  (1,766 u16 big-endian SJIS codes; not found -> index 0xB8) -> glyph record `{tpage 0x1E + idx/882,
  clut colour*2 (+1 on odd pages), u, v}` with page = idx/441, cell = idx%441, u = cell%21*12, v = cell/21*12.
- `draw_lines` = 0x8002A174 draws every object: a record with first word < 0x20 is a glyph: one 12x12 sprite
  (0x8001D14C, then 0x8001D2F4, 0x8001D210), x += 12 (10 for the digits row of page 0); a control record:
  0x8140 x += 12, two spaces x += 10, others nothing.
- Font: FONT0D.BIN entries 0/1 = 4bpp TIMs at VRAM (896,256) and (960,256); each holds two pages in the
  nibble bits (even page = bits 2-3, odd page = bits 0-1, matching the even/odd CLUT). All 1,764 cells are
  Japanese glyphs (ink value 3, no shadow).

## English (verified: marker build boots, title menu and opening captions draw markers)
- **Digraphs**: an English unit = two ASCII bytes (0x20-0x7F, first char in the low byte), so 32 records hold up
  to ~62 letters + the line end code. `engine.encode_ascii` pads odd runs with PAD (0x7F, width 0) and puts PAD
  before a char whose pair would equal a control code (`bb`, `KG`, `MM`, two spaces ...).
- **append hook** (EXE 0x80029AC4 -> 0x80028A38): a digraph unit becomes the record `{code, clut = colour*2+1}`.
- **drawer hook** (0x8002A210: "code not in the control table" branch -> `digraph_draw`): draws both chars from
  FONT0D page 1 cells (row (c-0x20)>>4, column (c-0x20)&15; those cells held kanji), sprite width = advance
  from the width table, space advances only. Uses the drawer frame's free word sp+0x2C.
- Hook space: 0x80028A38-0x80028DD4, unreferenced debug/leaf functions (`tools/deadcode.py`: no jal, j, pointer
  word or lui/addiu pair in the EXE or any overlay reaches any address inside). EXE zero runs are not free:
  0x800840CD.. and 0x800851D0.. are written at runtime, 0x80085360 is a 512-byte buffer (0x80052B30),
  0x80086A38 the GTE matrix stack.
- Font: `fonts/en12.txt` (from the sibling repo, MIT), rows 2-11 of the cell.

## Disc: the second file table (verified: GDEF0D grown by the marker build hung at boot until fixed)
- The loader 0x8001F3B0 allocates `(size[d] - offset)` rounded up to 2 KB from a **u32 byte-size table per data
  id** at EXE RAM 0x8007C1D8 (file offset 0x6C9D8, 1,543 entries = files 63..1605 of the LBA table, all equal
  to the ISO sizes), then reads the sectors from the LBA table. A grown file with a stale size overran the next
  buffer (GDEF0D 21,120 -> 24,576 bytes: black screen after the logos). `build.rewrite_lba_table` now rewrites
  both tables (`tests/test_build.py`).
