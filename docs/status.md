# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** **8 in progress** (QA in the emulator), then 9 (release).
- **Done (phase 8 so far, 2026-11-01):**
  - Phase 6 review (`.harness/reviews/...-phase6.md`) fixed, commit 5aedd55: Momotaro/Kintaro full names where the
    slot fits (by_id), 花 = Flower in Q301/Q345, M580D/19 Poverty God / Fortune God. Lint now (a) needs every row
    of a glossary-waived unit listed in glossary_ok.txt by id, (b) rejects identical English for different JP in
    one choice menu. Quiz choice layouts 5/6 widened to 88 px (engine.CHOICE_EXE + CURSOR; windows.md).
  - Graphics pipeline: `tools/gfx.py` (gfx/en/FILE_ENTRY.png -> TIM pixels, ECD, archive; insert + verify_build
    hooked; tests/test_gfx.py), `tools/gen_gfx.py` (LABELS rect -> English, Fredoka OFL, colours from the JP
    lettering, writes every byte-identical copy; `boxes`), `tools/gfxfind.py` (same pixel rows in other images).
    Done: title press-start prompt (CI0D:3 + TITLE0D:3), shot in game (work/qa/title8c f3030); Game Album menu
    labels (NAME0D:0 + PREM0D:0 + YUGI0D:0: Game Album / Rank Details / Quick Match! / Name Entry), checked in the
    image only: the screen needs a memory-card save (below).
  - Text tour started on the en build of 5aedd55 (before any redraw): `work/qa/tour8` (warp_all --hold 1500
    --click 45 --every 60 --probe textlog, log work/qa/tour8.log). When result.tsv is complete: `sheet.py` per
    scene dir (--changed 0.02), `qa_gate.py init work/qa/manifest.tsv work/qa/tour8 --glob "*sheet*.png"`, the
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
  - Graphics text (D5: all of it; docs/re/gfx_survey.tsv, 200 rows): title logo pieces (CI0D:3/TITLE0D:3,
    YUGI0D:1, HOUGEN0D:2, FILESL0D:1), NAME0D:0 mode menu, STATUS0D:0, M990D:0/1 HUD + result words, banners
    (M010D:4, M110D:0, M140D:0, M560D/M590D, GV02000D:2, GV13000D:2...), HOUGEN0D:0 card album, credits EVT600D:2-4,
    100 dialect cards HCARD*, signs. Per image: `gfx.py export`, find each sprite's rect (in-game the sprite rect
    can be narrower than the JP atlas row: shoot it), add LABELS, `gen_gfx.py`, build `--out build/g8.bin`, shoot.
    STATUS0D:0 (next): ステータス (0,55)-(111,77) red; grey embossed 総段位/段/巻 (y 83-105) and 免許皆伝 (y 112-130);
    beige panel rows 総カード枚数/プレイ時間/歩数/お金 (x 0-105, y 129-215, bg='fill'); unit glyphs 枚/歩/両 at
    x ~222-240 sit under the rank plates; 4 rank plates 桃太郎/名人/達人/仙人 (x 113-223, y 80-208) have patterned
    backgrounds: clear only the lettering pixels, not the rect (gen_gfx needs a mode for that).
  - Memory-card save for Status / Game Album / trial money: none yet. Make one headlessly (new game -> first save
    point, `--state-out`, keep the card emu.py writes) and add it to tools/routes or work/saves.
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
