# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 7 done (2026-11-01) -> next is **phase 8** (QA in the emulator), then 9 (release).
  Phase 7 done-when met: lint 0 errors (widths, pages, control codes, glossary); `tools/verify_build.py` on the
  en build: 342 files changed, 0 errors; check.py green (31 tests).
- **Done (phase 7):**
  - `tools/verify_build.py [CUE]` (AGENTS.md "Verify"): reads every file from both disc images; unchanged files
    identical; changed files == insert.files(); code files (EXE, OVL*) pass `romdiff.check` with allowed = string
    slots (+ refs for RELOC), hook sites + hook area, money sites, LBA/size tables; archives: same entries,
    non-script entries identical, each script entry reverted to its JP text gives the original bytes; FONT0D: only
    the glyph page; LBA/size tables match the built image; no original branch lands inside a hook span.
    `tests/test_verify.py` runs the per-file checks on insert's output (no disc build) + negative cases.
  - Relocation guard: `insert.patch_code` only moves a string into a hole with the same lui half and errors
    otherwise (OVLXTTL 0x800DAF10 pairs with a second lui in a branch delay slot that codestr does not see).
  - Trial money templates OVLXTTL@800CD1A4/450 now `[20]x12 + ryo`, relocated (lint lets RELOC rows exceed max).
    In game only with a memory-card save (`tools/routes/status.txt` stops at "no save file"); English is narrower
    than the JP (75 vs 84 px at the same x).
  - Map captions (op 26): 19 captions had inherited capped code-string short forms ("Tabidachi", "Capital",
    "Island"); `script/by_id.tsv` gives them the glossary names ("Tabidachi Village", "Capital of Hope",
    "Onigashima"). Centring hook verified in game: x = 160 - width/2 (warp.lua `OPS` + `tools/debug/caption_ops.py`).
  - Map 284: not a translation bug. The dir-2 arrival (GSD0000D) is a CD-timing race in the warp (flips with
    sector shifts of the map files, docs/re/debug.md); dir 0 (GSF0000D, the game's own route) loads in both
    builds. scenes.txt now uses it.
  - Heap A/B bounds and malloc found (docs/re/disc.md §Heap); `tools/lua/heapwatch.lua`.
- **Next (phase 8):**
  - Text tour (`warp_all.py --hold 1500 --click 45 --probe tools/lua/textlog.lua`, then `tools/textlog.py`),
    `jp_left.py` on the build, visual-QA sheets + `qa_gate.py` verdicts (in-session `visual-qa` agents, D9),
    graphics-text rows in zoomed cold-boot shots (docs/re/graphics.md).
  - Captions: 27 rows; shoot each with `OPS` (`caption_ops.py ID`) for the sheets.
  - Weak short forms to revisit in polish: EXE fireworks items named bare "Dog"/"Monkey"/"Momotaro", 7-byte key
    items "Island" (鬼ヶ島), "Prism" (虹の玉), "Steps" (歩数計).
- **Open bugs / gaps:**
  - 9 maps hang when warped (9, 29-31, 34, 187, 201, 204, 294; debug.md): their text needs another way in for
    phase 8. Story flags not mapped (warped maps show default state). `tools/deadcode.py` output is not safe hook
    space without an exec watch (`tools/lua/deadwatch.lua`, `warp_all.py --debugger`).
  - Status / Game Album screens (trial money, records) need a memory-card save; none made headless yet.
- **Waiting on the user:**
  - (resolved, D9) reviews: the run brief allows a fresh read-only pass, so the repo's in-session `reviewer` /
    `visual-qa` agents do the phase 6/8/9 verdicts.
  - Quiz keys M510D/227, 229, 238 look factually off in the JP (kept; game scores .0). Non-blocking.
  - GUI keyboard input in `tools/pcsx/` not proven by hand (headless-only runs).
  Non-blocking; check when playtesting.
