# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 3 (identity build) done 2026-11-01; next is phase 4 (extract).
- **Done (phase 3):** `tools/build.py`: check dump, dumpsxiso once into work/disc (pristine), changed files
  (`patched_files()`, empty) to build/files/, build/layout.xml points those entries there, EXE LBA table rewritten
  from mkpsxiso's computed layout, mkpsxiso repack (~1 s). Output sha1 == rom.sha1; `tests/test_build.py` checks
  identity and a grown-file build (table matches ISO directory). Smoke ok; grown build plays the story opening.
- **Done (phase 1):** notes in `docs/re/` (index README.md): disc.md (EXE LBA table 0x6F1B0, archives, ECD
  LZSS codec), text.md (Shift-JIS, control codes, message block, text locations), graphics.md + gfx_survey.tsv
  (200 Japanese graphics rows, font FONT0D). Tools: iso.py, arc.py, ecd.py, tim.py, gfxdump.py, ramfind.py, re.py.
- **Done (phase 2):** `tools/debug/warp.lua` + `scenes.txt` (gen_scenes.py): 5 menus, 38 OVLEVT events (19 =
  opening, 20 = ending + credits), 60 minigame modes, 349 field maps; all 452 reached from a cold boot by
  `tools/debug/warp_all.py` (proof shots `work/qa/warp_all/shots/`, result.tsv), no `--debugger` needed (~12 s
  each, 10 in parallel). RE in `docs/re/debug.md` (mode 0x8008C490, event 0x8008C4F9, map 0x8008C570, script VM
  0x800BF7B8 with next-op at +4, interpreter EXE 0x8003698C). Helpers: fileids.py (file ids -> names), maps.py
  (map table), find_arrivals.py, modelog.lua; `tools/routes/story.txt` (cold boot -> story mode).
- **Next (phase 4):** first disassemble script op handlers from EXE 0x8003698C (op lengths, any offset operands;
  text.md Open), then extract text to `script/` with a roundtrip + coverage test; insertion plugs into
  `build.patched_files()` (archive entries can grow: rewrite the archive header, disc.md).
- **Open bugs / gaps:** 9 maps hang when warped at any arrival point (9, 29-31, 34, 187, 201, 204, 294; debug.md):
  their text needs another way in for phase 8. Story flags not mapped (warped maps show default state).
- **Waiting on the user:** GUI keyboard input in `tools/pcsx/` not proven by hand (headless-only runs; default
  keyboard bindings copied to `tools/pcsx/pcsx.json` from `tools/emu-config/pcsx.json`). Non-blocking; check when
  playtesting.
