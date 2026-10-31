# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 6 done (2026-11-01) -> next is **phase 7** (insert, fit, check; romdiff ranges), then 8 (QA).
  Reviewer pass: 26 in-session read-only `reviewer` agents (D9), one per `work/qa/review/pairs/gNN.txt`.
  0 Critical; all Important fixed (list in `work/qa/review/important.md`: glossary -sama slips on Kannon of
  Hope / Lord Water Dragon, "Let's Pillow Fight!", Grandpa "dear" -> "my boy", elder じゃ voice on signposts and
  Mashira, Pun Contest plant puns, "Mr. Turtle/Rabbit/Tanuki" -> "-san" sweep, OVLXTTL glossary entries, quiz
  decoy U-D-L-R). Cap-forced keeps ticked in `docs/polish.md`. All Minors are in `docs/polish.md` (one pass
  before release). All batches check 0 errors; check.py green; build smoke ok.
- **Text tour (en build, 2026-11-01):** 451/452 scenes ok, 0 Japanese lines drawn (`tools/textlog.py
  work/qa/tour`). Fails: `map_gv2500_284` (see Open bugs).
- **Done (phase 6):**
  - Pipeline: `tools/batches.py` split/check/merge/terms/todo, `tools/lint.py` (in check.py), `tools/layout.py`
    (wrap, pages), brief `docs/translator-brief.md`, `docs/style-reference.md`, `docs/synopsis.md`, `glossary.md`
    (Avoid column enforced). Reviewed glossary exceptions: `script/glossary_ok.txt`.
  - `script/by_id.tsv`: per-id English for rows whose same-JP twin means something else (quiz answers like
    タイ Sea bream / Thailand; answers shared with code strings). Merge applies it last; such rows are their own unit.
  - Quizzes (M510D/M530D/M580D): answers kept in the 72 px op-41 box; kanji quizzes glossed ("Live+Start").
  - Money box: text x 0xD8 -> 0xD0, frame x 0xD0 (`engine.patch_money`, EXE + overlay sites); `208,26 ...ryo` fits.
  - Code-string relocation (OVLXTTL only): `insert.patch_code` (docs/re/script.md). EXE, OVLM*, OVLGMAIN
    strings fit in place (short forms, `script/glossary_ok.txt`). Title menu `　x5 New Game　x3 Resume`
    (full-width spaces keep the JP columns; checked in a cold-boot shot).
- **Next:**
  - Weak short forms to revisit in polish: EXE fireworks items named bare "Dog"/"Monkey"/"Momotaro", 7-byte key
    items "Island" (鬼ヶ島), "Prism" (虹の玉), "Steps" (歩数計).
  - Phase 7: caption centring hook (`engine.py`, op 26) not yet seen in-game (captions fire on world-map entry,
    not after a warp); trial-screen money templates OVLXTTL@800CD1A4/450 keep 両 (12 digit slots + 2 free bytes,
    `ryo` needs 4); save titles full-width `ＭＯＭＯＴＡＲＯ　＃n`.
  - Phase 8: text tour (`warp_all.py --hold 1500 --click 45 --probe tools/lua/textlog.lua`), leftover-JP scan,
    visual QA sheets.
- **Open bugs / gaps:**
  - **Map 284 (GV2500, shore facing the Capital of Hope) never loads when warped in the English build**; the
    original and the marker build load it. The VM sits on op 0x1D (change map) with MAP=284; loader calls
    (`EXE 0x8001C334`, exec probe) show GV25000D/1, SVBM14D, GCV0250D (215 KB at 0x80140CA0, right after the
    loaded map scripts) and GCV0251D, then nothing. Reverting all GSV+GSF+GSS text to JP fixes it; reverting GSV
    alone, GSF+GSS alone, GSV2500D, or GSV00/GSV0x-1x/2x/3x ranges does not. Suspect memory/timing (the warp
    hijacks map 41's script at 0x80140304). Next: find the real entry to map 284 (its only arrival 19,11 comes
    from one script) and test that route; check RAM limits above 0x80175000.
  - 9 maps hang when warped (9, 29-31, 34, 187, 201, 204, 294; debug.md): their text needs
  another way in for phase 8. Story flags not mapped (warped maps show default state). `tools/deadcode.py` output
  is not safe hook space without an exec watch (`tools/lua/deadwatch.lua`, `warp_all.py --debugger`).
- **Waiting on the user:**
  - (resolved, D9) reviews: the run brief allows a fresh read-only pass, so the repo's in-session `reviewer` /
    `visual-qa` agents do the phase 6/8/9 verdicts.
  - Quiz keys M510D/227, 229, 238 look factually off in the JP (kept; game scores .0). Non-blocking.
  - GUI keyboard input in `tools/pcsx/` not proven by hand (headless-only runs).
  Non-blocking; check when playtesting.
