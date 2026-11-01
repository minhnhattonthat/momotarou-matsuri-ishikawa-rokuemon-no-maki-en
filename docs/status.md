# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** **8 in progress** (QA in the emulator), then 9 (release).
- **Done (phase 8 so far, 2026-11-01):**
  - Credits checkpoint: all **101 lines / 22 ANM items** redrawn, including full names and Product Managers
    omitted by an online transcription. `gfx/credits.tsv`, `tools/gen_credits.py`, new MIT `fonts/credits7.txt`.
    Whole-archive duplicate sweep updates **18 atlases** (entries 2-4 in EVT600D through EVT650D).
    An early build only translated the first three screens; regression test now guards every ending reload.
  - `tools/debug/credits_qa.py` finds complete credit items from cold-boot screenshots: rejected build 3/22,
    final build **22/22**. Fresh read-only visual pass accepts four enlarged sheets; scoped gate **4/4 ok** at
    `work/qa/credits8_review`. Names with unconfirmed readings remain a polish item; ending-art Japanese is
    separate from credit lettering. Commands, sources, limitations: `docs/re/credits-qa.md`.
  - Latest validation: **45 tests passed**, lint 0; verifier **352 changed files / 0 errors**; cold smoke
    `work/qa/credits8_final_smoke` passed; credits textlog 0 Japanese lines. Main disc: 182,571,648 bytes,
    **2026-11-01 02:06:24 UTC**, SHA-1 **4031eba32228dbfe896eb6222fa86c63a4a943d1**.
    Phase 8 remains incomplete: the scoped credits gate does not cover the remaining graphics or full tour.
  - Minigame graphics checkpoint: eight new atlas redraws (M010D:4, M030D:3, M110D:0, M140D:0, M560D:1,
    M590D:0/6, M990D:0). `tools/anm.py` decodes actual sprite rectangles; corrected narrower award/Lose
    bounds and excluded a Bonus region with a partial sprite user. `tests/test_anm.py` guards HUD fragment use.
    Small HUD words use the new MIT `fonts/hud7.txt`; a tiny rounded Record label failed review and was replaced.
  - `tools/debug/janken.lua` selects seven hands from a cold warp using controller input. The final fresh
    read-only review accepts Ready/Go/Win/Lose/Draw and Score/Record in game; scoped gate **1/1 ok** under
    `work/qa/banners8_review`. Other new atlas redraws still need outcome/palette routes; do not count them as
    phase-wide visual approvals. Reproduction, exact bounds and remaining work: `docs/re/minigame-graphics-qa.md`.
  - Previous banner validation: **42 tests passed**, lint 0; verifier 346 changed files / 0 errors; cold smoke
    `work/qa/banners8_final2_smoke` passed; `banners8_final2_janken` textlog 0 Japanese lines.
    Build: `build/momotarou-matsuri_en.bin`, 182,839,776 bytes, 2026-11-01 01:50:59 UTC,
    SHA-1 `e4ccf3f32f96fcc03e2834d2716a0a97e4261ce3`. **Phase 8 cannot advance yet**; this is a scoped checkpoint.
  - Resumed save/Status QA: `tools/debug/save_fixture.py` now creates and verifies a game-written save without
    a playthrough. Seed card must be empty; the emulator edits a copy. Fixture: `work/qa/save_fixture_checked/memcard1.mcd`.
    `save_menu` is a new debug scene (453 entries now); `tools/routes/status_saved.txt` cold-boots, loads slot 1,
    and opens Status. `tools/debug/records.lua --var RECORDS=true` enables the first minigame in RAM for album QA.
  - The saved-record route exposed **11 omitted number templates** (rank, hours, minutes, points, counts, colon),
    including both copies in OVLXTTL. `codestr.py` now recognises referenced digit-slot templates with short units;
    all eleven are translated in script/OVLXTTL.json. Whole-code-file sweep and regression tests cover the form.
    The earlier 452-scene text tour did not cover these saved-record screens.
  - STATUS0D:0 redrawn: title, rank/mastery labels, four rank plates, panel labels, counter suffixes. Grey-letter
    removal preserves coloured plate backgrounds. Main Status screen compared cold against the original;
    hidden step-count question marks are original behaviour. Three higher rank plates still need in-game shots.
    Review and commands: `docs/re/status-menu-qa.md`; scoped evidence: `work/qa/status8_review/`.
  - Previous Status/save validation: **40 tests passed**, lint 0; disc verifier 345 changed files / 0 errors; cold smoke
    `work/qa/smoke8_final` passed; `status8_final_cold` textlog 0 Japanese lines; scoped visual gate 2/2 ok.
    Build: `build/momotarou-matsuri_en.bin`, 2026-11-01 01:29:27 UTC,
    SHA-1 `a3db1fb15d377b7933560c661b1fdf4b3344896e`. These checks do **not** complete phase 8.
  - Phase 6 review (`.harness/reviews/...-phase6.md`) fixed, commit 5aedd55: Momotaro/Kintaro full names where the
    slot fits (by_id), 花 = Flower in Q301/Q345, M580D/19 Poverty God / Fortune God. Lint now (a) needs every row
    of a glossary-waived unit listed in glossary_ok.txt by id, (b) rejects identical English for different JP in
    one choice menu. Quiz choice layouts 5/6 widened to 88 px (engine.CHOICE_EXE + CURSOR; windows.md).
  - Graphics pipeline: `tools/gfx.py` (gfx/en/FILE_ENTRY.png -> TIM pixels, ECD, archive; insert + verify_build
    hooked; tests/test_gfx.py), `tools/gen_gfx.py` (LABELS rect -> English, Fredoka OFL, colours from the JP
    lettering, writes every byte-identical copy; `boxes`), `tools/gfxfind.py` (same pixel rows in other images).
    Done: title press-start prompt (CI0D:3 + TITLE0D:3), shot in game (work/qa/title8c f3030); Game Album menu
    labels (NAME0D:0 + PREM0D:0 + YUGI0D:0: Game Album / Rank Details / Quick Match! / Name Entry), checked in the
    image only for the three mode labels; the Game Album title has now been seen in `work/qa/album8_unlocked`.
  - Text tour on the en build of 5aedd55 (before any redraw): `work/qa/tour8` (warp_all --hold 1500 --click 45
    --every 60 --probe textlog): **452/452 ok, textlog.py: 0 Japanese lines, markers 0**. Per-scene sheets
    (`sheet.py DIR --changed 0.02`) made for 88 of 452 only, and the JP reference tour `work/qa/tour_jp` reached
    ~296 scenes: both background jobs were killed by Claude Code for low system memory (2026-11-01). Rerun them
    with fewer jobs (`--jobs 3`), then: `qa_gate.py init work/qa/manifest.tsv work/qa/tour8 --glob "*sheet*.png"`, the
    same tour on rom/ into work/qa/tour_jp, `qa_gate.py todo ... --size 30`, `visual-qa` agents (<= 4 at once),
    `textlog.py work/qa/tour8` for Japanese still drawn.
  - Gotcha: `build.py --out` needs a `.bin` name (`--out build/g8.bin`); building the default image while a tour
    runs on it fails (mkpsxiso, file locked): build QA images under another name.
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
  - Heap A/B bounds and malloc found (docs/re/disc.md §Heap); `tools/lua/heapwatch.lua` + `tools/heaplog.py`.
    All 452 scenes on the en build (`warp_all.py --probe tools/lua/heapwatch.lua --hold 300`): least heap-A free
    156,128 bytes (game_m25/m70-72 minigames), so English growth (a few KB per file) is far from the limit.
    15 runs of that sweep died with emulator exit -1 while other emulators ran; all 15 passed on a rerun.
- **Next (phase 8):**
  - Finish runtime coverage of the new minigame redraws: awards need nonzero-score routes; M14/M56/M59
    banners need the relevant outcome/versus states. Circle-only tours do not reach all those sprites.
    M990D big announcement words and most other HUD fragments remain Japanese; use `anm.py` to check their
    composition before editing pixels. Small Bonus at (136,16,40,16) has overlapping fragment users and is untouched.
  - Graphics text (D5: all of it; docs/re/gfx_survey.tsv, 200 rows): classify retained title logos under D5
    (CI0D:3/TITLE0D:3, YUGI0D:1, HOUGEN0D:2, FILESL0D:1); NAME0D:0 mode-menu shots,
    STATUS0D:0 higher rank shots, remaining M990D:0/1 HUD + result words, remaining banners
    (GV02000D:2, GV13000D:2...), HOUGEN0D:0 card album, ending-art signs/emblems,
    100 dialect cards HCARD*, signs. Per image: `gfx.py export`, find each sprite's rect (in-game the sprite rect
    can be narrower than the JP atlas row: shoot it), add LABELS, `gen_gfx.py`, build `--out build/g8.bin`, shoot.
  - Saved-record QA: exercise all record categories with nonzero scores, not only the newly translated file
    selector. Use the new fixture and records probe; get actual mode-menu/rank-detail/name-entry coverage.
    `work/qa/album8_*` exploratory states are from earlier builds: regenerate cold before accepting verdicts.
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
  - Phase 8 remains incomplete: most of the 200-row graphics survey, the full visual manifest, caption tour,
    and nine hanging-map routes remain open. Do not advance to phase 9 on the scoped Status/save verdicts.
- **Waiting on the user:**
  - (resolved, D9) reviews: the run brief allows a fresh read-only pass, so the repo's in-session `reviewer` /
    `visual-qa` agents do the phase 6/8/9 verdicts.
  - Quiz keys M510D/227, 229, 238 look factually off in the JP (kept; game scores .0). Non-blocking.
  - GUI keyboard input in `tools/pcsx/` not proven by hand (headless-only runs).
  Non-blocking; check when playtesting.
