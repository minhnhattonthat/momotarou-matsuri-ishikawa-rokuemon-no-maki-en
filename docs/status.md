# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** **8 in progress** (QA in the emulator), then 9 (release).
- **Done (phase 8 so far, 2026-11-01):**
  - Attract-portrait prop checkpoint: both fans now say the complete Festival (FEST / IVAL); Rokuemon's ten
    stylized six badges use 6, with the eight partial badges clipped by their original coat edges/folds.
    Explicit masks preserve fan ribs/handles, coloured cloth, borders and all sprite/animation data.
    Regression checks caught two rib pixels and the narrow numeral's lower-loop clipping; both are fixed.
  - Natural cold original and English runs each pass **5/5 complete character/name pairs**, including every
    prop pixel. Fresh read-only D10 review accepts **3/3 scoped full-screen comparisons**;
    `docs/re/character-props-qa.md` records reproduction and verdict hashes. Survey rows #1/#2 portrait
    lettering are covered; separate ending/card festival marks and GCV0310 tags are not.
  - Latest validation: **76 tests passed**, lint 0; verifier **369 changed files / 0 errors**; cold smoke
    `work/qa/props8_smoke` passed. Intro textlog emits no lines, so 0 logs is not text coverage.
    Main disc: **182,491,680 bytes**, **2026-11-01 07:11:40 UTC**, SHA-1
    **6fd935950a81755dcc5a37796150790508af9c6c**. **Phase 8 remains incomplete; do not advance to release.**
  - Character-introduction checkpoint: Momotaro, Kintaro, Urashima, Yashahime and the full Ishikawa Rokuemon
    name are English in CHR0D:1/2. Yashahime was three fragments of one name, not two copies; the composite
    redraw and regression test preserve every character pixel and all ANM data.
  - `tools/debug/character_intro.py` waits through the natural title attract sequence, with no input, save
    or RAM substitutions. Original and English runs each pass **5/5 complete character/name pairs in the same
    frame**; fresh read-only review accepts **5/5 scoped sheets** (`docs/re/character-intro-qa.md`).
    Festival-fan lettering and costume marks remain open; the name-label verdicts do not approve them.
  - Latest validation: **75 tests passed**, lint 0; verifier **369 changed files / 0 errors**; cold smoke
    `work/qa/names8_smoke` passed. The intro has no textlog output, so its 0-log result is not text coverage.
    Main disc: **182,494,032 bytes**, **2026-11-01 06:57:03 UTC**, SHA-1
    **3f33c5f80f72f7b7288ca70c74a417f49c46b85c** (`build/names8.bin` is identical).
    **Phase 8 remains incomplete; do not advance to release.** Full graphics, visual and story-state gates remain.
  - Field-sign/map-warp checkpoint: both Pun Contest board atlases translated with the full glossary name;
    Men's Bath / Women's Bath curtains updated in all three atlas copies. Original and English cold routes
    each pass **7/7 lettering checks** across four maps, including the alternate red/blue palettes.
    Fresh read-only review accepts **4/4 scoped comparison sheets** (`docs/re/field-signs-qa.md`).
    The split GV02000D board still lacks runtime proof; other town signs and the tiny bath-counter placard remain open.
  - **Critical QA correction:** map warps always ran **GSF0000D:60**, the world-map initializer, after loading
    every destination. Backgrounds could render without town NPCs/decorations, and some coordinates hung.
    `gen_scenes.py` now derives each destination's real initializer from the original scripts; every map row
    carries it, and the warp refuses an implicit fallback. Queued Circle input during loading is also fixed.
    **Earlier map tours do not establish actor/dialogue/animated-decoration coverage.**
  - All **nine previously excluded maps** now load. Eight need their correct initializer; map 294 additionally
    needs the setup surrounding its normal GSF0000D:25 entry, now retained in its row. Map 294 passes on both
    discs at its original coordinates. The list now contains **464 scenes**. Replacement cold sweep:
    **358/358 maps ok**, **0 Japanese lines in 358 logs**, in `work/qa/mapinit8_all`.
    This is load/initialization coverage, not a phase-wide visual or NPC-interaction approval.
    Details and exact op sequences: `docs/re/map-initializers.md`.
  - Main disc: **182,498,736 bytes**, **2026-11-01 06:27:20 UTC**, SHA-1
    **4493a392249171d9e12b467c1cfba74522e49a30** (`build/signs8.bin` is identical).
    **74 tests passed**, lint 0; verifier **368 changed files / 0 errors**; cold smoke `work/qa/signs8_smoke`
    passed; four sign-route logs and all nine recovered-map logs have 0 Japanese lines (graphics excluded).
    **Phase 8 remains incomplete; do not advance to release.**
  - HUD-counter checkpoint: twelve additional M990D words translated (Total, Win, Loss, min, sec, Floor,
    later, small Bonus, Match, times, items, pieces). Whole words use unused pixels; shared old fragments
    remain intact. M34's counter panel extended by eight pixels without losing its borders.
  - Natural cold routes cover **8 minigames**, plus a true **9999 record** loaded before HUD creation;
    the assembly fixture covers **12/12 labels**. Fixed right-edge items clipping, Record/9999 overlap,
    Floor/number order, and the Times panel. Fresh read-only review: **5/5 scoped sheets ok**.
    The first stress fixture left old dashes over digits; the corrected fixture seeds the actual record
    fields. Details, exact addresses, original comparisons and verdict hashes: `docs/re/hud-counters-qa.md`.
  - Latest validation: **68 tests passed**, lint 0; verifier **363 changed files / 0 errors**; cold smoke
    `work/qa/hudunits8_final3_smoke` passed; final 10 logs have 0 Japanese lines (graphics excluded).
    Main disc: **182,498,736 bytes**, **2026-11-01 05:57:34 UTC**, SHA-1
    **e7ff120deca2a8d4b5ec6fe4203af61dca82f363**. **Phase 8 remains incomplete; do not advance to release.**
  - Minigame label/race checkpoint: Jackpot!, Level 1-3 and four speech bubbles, One away!, Miss,
    Rabbit-Turtle Race, Start and the shared Race suffix translated. M230D's sprite-built text is now English:
    all **30 runner names** use full glossary romanizations; rank dot, Lane, Time, Hit and ryo replace five
    kana units. These ANM glyph strings were invisible to the text logger. Original glyph atlas stays intact.
  - Cold original and English fixtures each cover **48/48 complete states** (18 labels + 30 names);
    fresh read-only review accepts **10/10 scoped sheets**. Natural controller-only race covers betting,
    racing, standings, zero payout and Good Work. Review caught seven names with unordered glyph records:
    anchor by minimum x, cap width at 50, preserve the Lane separator. The tiny-dot oracle now has a bounded
    search to reject panel-corner false matches. Details/reproduction: `docs/re/minigame-labels-qa.md`.
  - Previous label validation: **64 tests passed**, lint 0; verifier **363 changed files / 0 errors**; cold smoke
    `work/qa/labels8_final4_smoke` passed; nine fixture logs and one natural-race log have 0 Japanese lines.
    Main disc: **182,496,384 bytes**, **2026-11-01 05:21:18 UTC**, SHA-1
    **4ca27d7a3651f537adcaf74d27d913cc7d7dd992**. **Phase 8 remains incomplete; do not advance to release.**
  - Shared HUD/outcome checkpoint: Weather, Forecast, Race Result, Entry, Slow and M03 Which? translated.
    Cold checks cover **13 shared HUD states + 11 outcome/prompt states**, with **6/6 scoped visual sheets ok**.
    M14 Streak now has a readable outlined pixel font. Fixed M59's `Loseけ!` by relocating the complete
    Lose! sprite; its old tail shared actor pixels, which regression tests preserve.
  - New `sprite_fixture.lua` uses loaded ANM selectors when a game lacks the shared Pause banner;
    `announcements.lua` can substitute a natural Game Start item. These prove assembly and palettes,
    **not natural outcomes or positioning**. M59's alternate TIM 6 / ANM 16 and the natural Which? route remain open.
    The screenshot gate now rejects solid-panel false matches, and the ANM renderer rejects ambiguous
    reused VRAM pages. Reproduction, original comparisons and verdict hashes: `docs/re/hud-outcomes-qa.md`.
  - Previous HUD validation: **60 tests passed**, lint 0; verifier **363 changed files / 0 errors**; cold smoke
    `work/qa/outcomes8_final_smoke` passed; eight targeted textlogs contain 0 Japanese lines (graphics excluded).
    Main disc: **182,491,680 bytes**, **2026-11-01 04:37:10 UTC**, SHA-1
    **86480010b723c6376450b9181d30cd6b85c544ae**. **Phase 8 remains incomplete; do not advance to release.**
  - Mask Maker controls and Mask Album title translated: **6/6 complete control sprites + 1/1 title** match
    cold captures, **3/3 scoped visual sheets ok**. Fixed preview icons covering English instructions and
    dialogue by reserving 48 pixels on every relevant line; original comparison confirms the layout.
    New `mask_editor` shop fixture (455 scenes) and state-aware `masks.lua` select all six parts and reach
    confirmation and accept it, returning to Story on both discs. Error/redo/continue branches covered;
    memory-card persistence and populated album navigation remain wider QA scope.
    `docs/re/masks-qa.md` records evidence and 8bpp ANM support added to the screenshot oracle.
  - Previous mask validation: **56 tests passed**, lint 0; verifier **363 changed files / 0 errors**; cold smoke
    `work/qa/mask8_smoke` passed; mask-fixture textlog 0 Japanese lines. Main disc: **182,491,680 bytes**,
    **2026-11-01 04:02:28 UTC**, SHA-1 **bd6ff6ca1786b31afe0695b328a3a05af2c741b2**.
    **Phase 8 remains incomplete.** Remaining graphics, outcome/menu routes and full visual tour prevent release.
  - Shared result banners: M990D:0 and 40 ANM states now show Round/Try/Question 1-10, individual and paired
    winners with full names, Win and Lose. `tools/gfx_results.py` repacks English words into old large-letter
    regions; `gfx_layout.py` checks 743 geometry fields while preserving palettes, flags, scales and counts.
    Tests guard every other archive's sprite users, atlas boundaries and English word order.
  - Final cold fixture: **40/40 complete result states**, **5/5 scoped visual sheets ok**; original comparison
    under `work/qa/results8_original`. The extra M51 route is a one-question encounter and does not cover the
    question-counter banners. Natural result progression remains in the wider QA scope. `docs/re/results-qa.md`.
  - Previous result-banner validation: **54 tests passed**, lint 0; verifier **363 changed files / 0 errors**; cold smoke
    `work/qa/results8_smoke` passed; result-fixture textlog 0 Japanese lines. Main disc: **182,496,384 bytes**,
    **2026-11-01 03:39:19 UTC**, SHA-1 **2423760e259876a8dfce16a26db5ca994aa7557b**.
    **Phase 8 remains incomplete.** Remaining graphics, outcome/menu routes and full visual tour prevent release.
  - Marginal card phrases: `gfx/card_words.tsv` and `tools/gen_card_words.py` redraw the brown dialect
    captions on **all 100 cards**. English follows the existing vertical margins clockwise; all card numbers,
    prefecture strips, palettes and ANM records stay intact. Narrow erase regions protect nearby figures,
    leaves and props; the pixel/TIM tests reject edits outside the declared areas.
  - Cold review found four phrases blending into background art; added a one-pixel white keyline and
    regenerated the build/tour. `tools/debug/card_words_review.py` makes five scoped phrase sheets with the
    skill's sheet.py. Fresh read-only review accepts **5/5 scoped sheets**, all **100/100** complete cold-boot
    card captures match, and textlog reports **0 Japanese lines** (excludes graphics). Full-card comparison
    restored four clipped props; new regression checks protect them. Details: `docs/re/card-words-qa.md`.
    **Illustration SFX, signs, clothing emblems and the red new-card notice remain open.** This is not whole-card
    approval and phase 8 cannot advance to release on it. Original card 001 art/gloss mismatch is documented.
  - Previous card-phrase validation: **52 tests passed**, lint 0; verifier **363 changed files / 0 errors**; cold smoke
    `work/qa/words8_smoke4` passed. Main disc: **182,503,440 bytes**, **2026-11-01 03:25:16 UTC**, SHA-1
    **f7b8c56da2e6026b7d154cb3a8496b0806e3f60b**. Final tour: `work/qa/words8_final4`; scoped review:
    `work/qa/words8_review`. Phase 8 remains incomplete; do not advance to release.
  - Card Album checkpoint: title, seven region names and counters in HOUGEN0D:0 redrawn; all **100 prefecture
    captions** in HCARD00D through HCARD90D redrawn within the actual 120x16 name-strip sprite. Card numbers,
    illustrations, palettes and ANM records preserved at that checkpoint. Marginal dialect words are now
    translated above; illustration SFX and the fragmented red new-card tag remain Japanese.
  - New `card_album` scene (454 entries) enables only collectible bits 0-99 in RAM and enters mode 0x4C.
    `tools/debug/cards.lua` visits all 100 pages through the real loader. CD loads can lose/retain a timed tap;
    the probe retries unchanged pages and clears cached Right input once each target arrives. It fails on skips.
    `cards_qa.py` matches each complete illustration and caption: **100/100 on both original and English**.
  - Fresh read-only D10 review: **5/5 scoped sheets ok** (overview + 100 caption strips), under
    `work/qa/cards8_review`. Final tours: `work/qa/cards8_captions3`, `work/qa/cards8_jp_all3`; runtime textlog
    **0 Japanese lines** (excludes graphics). Commands, verified RAM addresses and limits: `docs/re/cards-qa.md`.
  - Previous prefecture-caption validation: **50 tests passed**, lint 0; verifier **363 changed files / 0 errors**; cold smoke
    `work/qa/cards8_final_smoke` passed. Main disc: **182,543,424 bytes**, **2026-11-01 02:52:33 UTC**, SHA-1
    **dcd7600ce28f778f642cd81b7908ae947d753591**. Phase 8 remains incomplete; do not advance to release.
  - Shared announcements checkpoint: M990D:1 redrawn (New Record, Level Up, Full Mastery, Game Start,
    Good Work, Pause, Draw, Finish). `gfx_layout.py` validates 26 specific u16 ANM edits to rejoin Start's
    fragments and centre level numbers; the disc verifier rejects every other ANM edit. M010 Perfect's
    duplicate exclamation fixed after comparison with the original. No new engine code or palette changes.
  - `tools/debug/announcements.lua` selects real loaded ANM items in RAM after a cold boot. Screenshot gate
    `announcements_qa.py`: **16/16** shared announcement states (15 paused + Full Mastery through the result
    animation), **5/5** M010 awards. Fresh read-only review: **6/6 sheets ok** in `work/qa/announcements8_review`.
    M03/M14/M56/M59 fixture attempts stayed in dialogue and are **not approved**. Full reproduction and limits:
    `docs/re/announcements-qa.md`. The full graphics survey and phase-wide visual tour remain open.
  - Previous announcements validation: **48 tests passed**, lint 0; verifier **352 changed files / 0 errors**; final cold smoke
    `work/qa/announcements8_release_smoke` passed; announcement/natural/mastery textlogs 0 Japanese lines.
    Main disc: **182,564,592 bytes**, **2026-11-01 02:34:07 UTC**, SHA-1
    **c84d1a018c9649a1468efa45564c88475b4e4cb8**. Phase 8 has not met its done-when; do not advance to phase 9.
  - Credits checkpoint: all **101 lines / 22 ANM items** redrawn, including full names and Product Managers
    omitted by an online transcription. `gfx/credits.tsv`, `tools/gen_credits.py`, new MIT `fonts/credits7.txt`.
    Whole-archive duplicate sweep updates **18 atlases** (entries 2-4 in EVT600D through EVT650D).
    An early build only translated the first three screens; regression test now guards every ending reload.
  - `tools/debug/credits_qa.py` finds complete credit items from cold-boot screenshots: rejected build 3/22,
    final build **22/22**. Fresh read-only visual pass accepts four enlarged sheets; scoped gate **4/4 ok** at
    `work/qa/credits8_review`. Names with unconfirmed readings remain a polish item; ending-art Japanese is
    separate from credit lettering. Commands, sources, limitations: `docs/re/credits-qa.md`.
  - Previous credits validation: **45 tests passed**, lint 0; verifier **352 changed files / 0 errors**; cold smoke
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
  - Character names, fan lettering and coat numerals now have natural attract-mode proof. The four small
    name tags in GCV0310D:13 are separate outstanding work. `character-intro-qa.md` and
    `character-props-qa.md` record exact bounds, preservation tests and cold routes.
  - Re-run the full text/visual tour with the corrected destination initializers. Older map shots lacked the
    proper actors and cannot support complete dialogue, animated decoration or story-state coverage. Use
    `map-initializers.md` and `work/qa/mapinit8_all/result.tsv` for the 358 passing cold entries; add interaction
    and later-story routes rather than treating that arrival count as full text coverage.
  - Field signs: locate the runtime consumer of GV02000D:2's split contest board; classify the restored tiny
    bath-counter placard (GV16090D:1, (128,0), 32x24, palette 2; GV16091D:3 ANM item 2).
    Other wooden shop/stall signs remain Japanese. `signs_tour.py` reproduces the
    accepted contest and three bath contexts; `fieldmap.py` is a navigation preview, never QA evidence.
  - Shared HUD counters: natural Win/Loss/min/sec/later/Match/small-Bonus contexts remain unproved;
    partial M990D:2 item 42 and M990D:3 items 19/20 retain original pixels and need runtime classification.
    `hud_units.py` reproduces the accepted 12-label fixture, 8 natural contexts and record stress case;
    `ice.lua` now reaches the left ice-tower course with controller input. Broader versus/record states remain.
  - Minigame labels: M05/M08/M18/M50 have complete sprite-assembly proof, but natural Jackpot, near-win,
    Miss and Start positioning still needs routes. Race Hit/nonzero payout remain fixture-only; the normal
    story return remains untested (both original and English direct warps return to the debug system menu).
    `tools/debug/minigame_labels.py` reproduces all 48 states; `race.lua` advances the natural race screens.
  - Cards: all 100 prefecture captions and marginal dialect phrases are English. Use the cold-boot tour and
    `cards_qa.py` meaning-ID report for the remaining black illustration SFX, signs and clothing emblems;
    the scoped phrase gate is not a whole-card verdict. Locate/render the fragmented red new-card tag.
    HOUGEN0D ANM 5/6 does not reference its visible atlas fragments; the runtime draw path is still unknown.
  - Finish natural outcome/versus routes. M03 Perfect, M14/M56 and M59 story banners now have scoped cold
    sprite-assembly proof (`hud-outcomes-qa.md`); M59's alternate TIM 6 / ANM 16 remains unapproved, and
    Which? has fixture proof only. M010 awards and M990D:1 announcements also have full-sprite cold proof.
    The pause fixture does not work while other games are in dialogue, so its exit code alone is not coverage.
    M990D:0's 40 large winner/ordinal states are now translated and cold-rendered (`results-qa.md`);
    normal gameplay progression still needs tour coverage. Small Bonus now uses a separate English sprite;
    its original overlapping fragment users remain intact and unclassified. See `docs/re/hud-counters-qa.md`.
  - Graphics text (D5: all of it; docs/re/gfx_survey.tsv, 200 rows): classify retained title logos under D5
    (CI0D:3/TITLE0D:3, YUGI0D:1, HOUGEN0D:2, FILESL0D:1); NAME0D:0 mode-menu shots,
    STATUS0D:0 higher rank shots, remaining M990D fragment/context classification, remaining banners
    (GV02000D:2, GV13000D:2...), HOUGEN0D:0 new-card tag, ending-art signs/emblems,
    illustration SFX/signs on HCARD* cards. Per image: `gfx.py export`, find each sprite's rect (in-game the sprite rect
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
  - The nine historical map hangs are resolved by correct initialization and map 294's entry setup;
    story flags remain unmapped (warped maps show default state). `tools/deadcode.py` output is not safe hook
    space without an exec watch (`tools/lua/deadwatch.lua`, `warp_all.py --debugger`).
  - Phase 8 remains incomplete: most of the 200-row graphics survey, the full visual manifest, caption tour,
    and the corrected map interaction tour remain open. Do not advance to phase 9 on scoped graphics verdicts.
- **Waiting on the user:**
  - (resolved, D9) reviews: the run brief allows a fresh read-only pass, so the repo's in-session `reviewer` /
    `visual-qa` agents do the phase 6/8/9 verdicts.
  - Quiz keys M510D/227, 229, 238 look factually off in the JP (kept; game scores .0). Non-blocking.
  - GUI keyboard input in `tools/pcsx/` not proven by hand (headless-only runs).
  Non-blocking; check when playtesting.
