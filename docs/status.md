# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 1 (research and recon) done 2026-10-31; next is phase 2 (debug tool). No build yet.
- **Done (phase 1):** notes in `docs/re/` (index README.md):
  - disc.md: EXE LBA file table (EXE 0x6F1B0, 1,606 start/end pairs; rebuild must rewrite it), load addresses
    (EXE 0x80010000, all OVL*.BIN at 0x800CB338), offset-table archives (`tools/arc.py`), ECD = LZSS variant
    (`tools/ecd.py`, all 2,313 entries decode; encoder roundtrips), free-space candidates.
  - text.md: Shift-JIS verified on screen; codes KG/KP/KN, bb..ww colours, MM name, R0-R3 numbers; message
    block `u16 a, 2, 1, voice, lines`; `message_open(file, entry)` EXE 0x8002B864 -> stand-alone messages are
    archive entries. ~190k JP chars incl. duplicates: GSV 101k, M 52k, GSF 21k, EVT, GDEF, GSS, code overlays.
  - graphics.md + gfx_survey.tsv: 953 unique TIMs swept (`tools/gfxdump.py` -> `work/gfx/`), 200 Japanese rows
    (100 dialect cards, 57 town signs, banners, logos, menus, credits images). Font FONT0D = 2-bit glyph pages,
    ~1,000 glyphs, no Latin letters.
  - Tools: iso.py, arc.py, ecd.py, tim.py, gfxdump.py, ramfind.py, re.py; tests/test_formats.py (5 pass).
- **Next (phase 2):** debug tool. A New game (circle on 初めて) goes straight to おためし対戦 (trial minigame,
  Daruma otoshi); board mode (GSV scripts) not reached yet. Find the game-mode/scene state in RAM (EXE switch at
  0x80020F40 on [0x8008C490], 99 cases, looks like the top-level mode), build `tools/debug/warp.lua` +
  `scenes.txt` (title, each minigame M00-M59, board areas, events EVT, ending/credits EVT600-620, status,
  card album). Then read-watch a loaded GSV entry to find the script interpreter and settle whether script
  bytecode holds byte offsets (text.md "Open"); needed before phase 4/5.
- **Open bugs:** none.
- **Waiting on the user:** GUI keyboard input in `tools/pcsx/` not proven by hand (headless-only runs; default
  keyboard bindings copied to `tools/pcsx/pcsx.json` from `tools/emu-config/pcsx.json`). Non-blocking; check when
  playtesting.
