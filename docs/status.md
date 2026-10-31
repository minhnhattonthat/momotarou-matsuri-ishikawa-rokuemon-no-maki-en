# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 6 (translate) — all 78 batches translated and merged except the EXE/OVLM byte-cap shortening
  (b003/b005/b007-b009, in progress); then phase 7 (layout fixes) and 8 (QA tour).
- **Done (phase 6):**
  - Pipeline: `tools/batches.py` split/check/merge/terms/todo, `tools/lint.py` (in check.py), `tools/layout.py`
    (wrap, pages), brief `docs/translator-brief.md`, `docs/style-reference.md`, `docs/synopsis.md`, `glossary.md`
    (Avoid column enforced). Reviewed glossary exceptions: `script/glossary_ok.txt`.
  - `script/by_id.tsv`: per-id English for rows whose same-JP twin means something else (quiz answers like
    タイ Sea bream / Thailand; answers shared with code strings). Merge applies it last; such rows are their own unit.
  - Quizzes (M510D/M530D/M580D): answers kept in the 72 px op-41 box; kanji quizzes glossed ("Live+Start").
  - Money box: text x 0xD8 -> 0xD0, frame x 0xD0 (`engine.patch_money`, EXE + overlay sites); `208,26 ...ryo` fits.
  - Code-string relocation (OVLGMAIN, OVLXTTL): `insert.patch_code` (docs/re/script.md).
- **Next:**
  - Merge b003/b005/b007-b009 once shortened; build; boot smoke; title menu (OVLXTTL@800CB4E4, relocated).
  - Phase 7: caption centring hook (`engine.py`, op 26) not yet seen in-game (captions fire on world-map entry,
    not after a warp); trial-screen money templates OVLXTTL@800CD1A4/450 keep 両 (12 digit slots + 2 free bytes,
    `ryo` needs 4); save titles full-width `ＭＯＭＯＴＡＲＯ　＃n`.
  - Phase 8: text tour (`warp_all.py --hold 1500 --click 45 --probe tools/lua/textlog.lua`), leftover-JP scan,
    visual QA sheets.
- **Open bugs / gaps:** 9 maps hang when warped (9, 29-31, 34, 187, 201, 204, 294; debug.md): their text needs
  another way in for phase 8. Story flags not mapped (warped maps show default state). `tools/deadcode.py` output
  is not safe hook space without an exec watch (`tools/lua/deadwatch.lua`, `warp_all.py --debugger`).
- **Waiting on the user:** GUI keyboard input in `tools/pcsx/` not proven by hand (headless-only runs).
  Non-blocking; check when playtesting.
