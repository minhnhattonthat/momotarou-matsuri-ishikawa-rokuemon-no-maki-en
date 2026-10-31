# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 4 (extract) done 2026-11-01; next is phase 5 (engine spike + marker build).
- **Done (phase 4):** script VM decoded (`docs/re/script.md`): 0x69 ops, lengths from the EXE handlers, jumps =
  byte offsets in 05-0A (if-blocks) and 0D-13 (branches), message/caption/menu text ops 02/26/41. `tools/text.py`
  extracts 7,678 items (4,894 msg, 1,601 menu items, 27 captions from 1,975 script entries; 1,156 code strings
  from EXE + overlays via `tools/codestr.py`) into `script/<FILE>.json` (346 files; 5,885 unique jp, ~225k chars).
  `text.rebuild(entry, texts)` rewrites an entry with new text and relocates jumps. Tests (`tests/test_text.py`):
  every script entry rebuilds byte-identical, grown text keeps every jump on its op (>500 entries), disc-wide
  Shift-JIS coverage (only 8 frozen noise runs), code strings roundtrip, script/ jp == fresh extraction.
- **Done (phase 3):** `tools/build.py`: dumpsxiso once into work/disc, changed files (`patched_files()`, empty)
  to build/files/, EXE LBA table rewritten from mkpsxiso's layout; output sha1 == rom.sha1 (tests/test_build.py).
- **Done (phases 1-2):** RE notes `docs/re/` (disc, text, graphics + gfx_survey.tsv, debug); warp tool reaches
  452 scenes from a cold boot (`tools/debug/`, `docs/re/debug.md`).
- **Next (phase 5):**
  1. Insert path: `build.patched_files()` writes archives whose script entries are rebuilt with
     `text.rebuild` (archive header offsets rewritten, arc.py; entries 16-aligned), code strings in place when
     they fit (`max`), else relocate + repoint every ref (codestr refs: ptr words, lui/addiu pairs).
  2. Font/encoding decision: the renderer takes u16 SJIS glyph codes (8-byte glyph records, 0x80029DF4); options:
     full-width SJIS Latin (no code change, wide) vs a half-width/VWF hook. Measure box widths (width gate).
  3. Marker build: every item -> `[id]` marker text; boot, warp to scenes, confirm ids show, find leftover JP
     (code-built strings, single-char code strings like 両 that codestr rejects as noise).
  - Possible buffer limits: data files load whole into heap buffers (disc.md: PREM0D at 0x8010D150 etc.);
    grown archives may overrun the next buffer. Check in the marker build.
- **Open bugs / gaps:** 9 maps hang when warped at any arrival point (9, 29-31, 34, 187, 201, 204, 294; debug.md):
  their text needs another way in for phase 8. Story flags not mapped (warped maps show default state).
  No text lint yet (check.py runs tests only); add EN control-code/width lint with phase 6/7.
- **Waiting on the user:** GUI keyboard input in `tools/pcsx/` not proven by hand (headless-only runs; default
  keyboard bindings copied to `tools/pcsx/pcsx.json` from `tools/emu-config/pcsx.json`). Non-blocking; check when
  playtesting.
