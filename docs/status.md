# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 5 (engine spike + marker build) done 2026-11-01; next is phase 6 (translate).
- **Done (phase 5):** `docs/re/engine.md`, `docs/re/windows.md`.
  - Engine: digraph VWF (two ASCII chars per u16 unit `0x8000|c1<<7|c2`), hooks in the EXE (`tools/engine.py`,
    armips; drawer 0x80029AC4 -> dead code 0x80028A38), English 12 px font `fonts/en12.txt` in FONT0D cells
    0x12A0+. Japanese still renders (13 px advance).
  - Insert: `tools/insert.py` (`build_archive`; modes en/marker/qa), `build.py --marker / --qa / --qa-file`.
    Archives regrow (16-aligned entries) and **the EXE size table (0x6C9D8, data id d = index d+63) is rewritten**:
    a stale size overran the next RAM buffer (black screen). Code strings in place (`max`), relocation not built yet.
  - Marker build: boots; 452/452 scenes reach without flat frames (`work/qa/mk_tour`); line probe
    (`tools/lua/textlog.lua` + `tools/textlog.py`) finds no leftover Japanese except the game's own JP names.
    Excluded non-text: memory-card/save-title strings (must stay full-width SJIS), money templates keep digit slots.
  - Width gate: `tools/windows.py` gives every item a budget: message 228 px, portrait 192, memcard 180, op-41
    choice box 72 (fixed layouts from the op 04 switch; one 200 px top box), EXE choices 26, main menu 112/92,
    captions 116 (from code), code strings = JP width (in-place byte cap keeps English inside it).
- **Done (phases 1-4):** RE notes `docs/re/`, warp tool (452 scenes), byte-identical rebuild, 7,678 items in
  `script/` with roundtrip tests.
- **Next (phase 6):** translator batches from `script/*.json` (`en` field), glossary from `glossary.md` +
  `../momotarou-densetsu-en`; lint per `windows.budget()`. Then phase 7:
  - caption centring (0x80034DC0 `160 - units*6`) assumes 12 px/unit: add a px-width helper;
  - money box: `ryo` overruns the frame ~3 px (box 0x80033DC0, move left ~6 px);
  - code-string relocation + repointing for strings longer than `max`.
- **Open bugs / gaps:** 9 maps hang when warped (9, 29-31, 34, 187, 201, 204, 294; debug.md): their text needs
  another way in for phase 8. Story flags not mapped (warped maps show default state).
- **Waiting on the user:** GUI keyboard input in `tools/pcsx/` not proven by hand (headless-only runs).
  Non-blocking; check when playtesting.
