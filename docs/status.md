# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** **8 in progress** (QA in the emulator), then 9 (release).
- **Done (phase 8 so far, 2026-11-02):**
  - Paper Fan Chop's countdown cue now reads **Duel**, matching both instruction pages, and is centred
    in its original panel. Cold solo/versus checks pass on both discs; fresh D10 review accepts **5/5**
    scoped sheets. `duel-cue-qa.md` records native player-count checks and rejected timing/alignment probes.
    `two_player.lua` now selects 2P through native menu states, with controller port 2 connected in the
    emulator config; `call_contexts.py` preserves the static MIPS call-context helper.
  - Latest validation: **131 tests / lint 0**, verifier **400 changed files / 0 errors**, cold
    `work/qa/duel8_centered_smoke` passed; `duel8_centered_en` has **0 Japanese lines in 2 logs**
    (graphics excluded). Main disc **182,449,344 bytes**, **2026-11-01 18:09:17 UTC**, SHA-1
    **cbadc82590fd4cfb81d78ddca889a293d47faebe**. **Phase 8 remains incomplete.**
  - Card-notice static follow-up: another HOUGEN loader exists at OVLXTTL **0x800D8350**, with no
    direct JAL callers. The album background table uses only y=0/16 and cannot draw the red fragments.
    These are limited static exclusions; native/dynamic consumers remain open (`card-full-art-qa.md`).
  - EVT220D's split village banner now reads **Welcome!!**. Native event15, run without
    automatic clicks, shows three complete scrolling placements on both discs; fresh D10 review
    accepts **6/6** context/detail sheets. `welcome-banner-qa.md` records source geometry,
    preservation tests, disc-sourced oracle and the skipped-animation pitfall. Survey row #141 closed.
  - Latest validation: **131 tests / lint 0**, verifier **400 changed files / 0 errors**, cold
    `work/qa/welcome8_smoke` passed; `welcome8_natural_en` has **0 Japanese lines in 1 log**
    (graphics excluded). Main disc **182,449,344 bytes**, **2026-11-01 17:44:05 UTC**, SHA-1
    **c9b124f5f466d4e4473e081d68163e4385d72ea0**. Snow placards, gold-prop and game-hall
    marks remain unresolved after enlarged inspection. **Phase 8 remains incomplete.**
  - Card notice follow-up: original OVLXTTL's collected/missing branch selects ANM6 items 3/4;
    both mode-entry context branches call the same initializer. Exact native addresses are in
    `card-full-art-qa.md`; neither path supplies the red notice's runtime consumer. It remains open.
  - Card063's final margin defect is repaired: complete top falling-leaf contour and no upper/right
    caption fringe. Fresh D10 cold review accepts the changed five-card sheet and enlarged margin;
    nineteen other sheets exactly match accepted hashes. **Full album 20/20 accepted; detail 1/1**.
    `card063-qa.md` records source changes, commands, hashes and scope. Earlier card063 issues are superseded.
  - Latest validation: **129 tests / lint 0**, verifier **399 changed files / 0 errors**, cold
    `work/qa/card063_smoke` passed; `card063_cold` has **100/100 complete captures**, **0 Japanese lines**
    (graphics excluded). Main disc **182,449,344 bytes**, **2026-11-01 17:25:34 UTC**, SHA-1
    **30553cd86663b6a9af287ff00e626d2771e25c85**. **Phase 8 remains incomplete; phase 9 has not started.**
  - Event classification rechecked on that disc: `snow_classify8_en` / `gold_classify8_en`, native
    oracle **5/5**, textlog **0 Japanese lines in each run** (graphics excluded). Three enlarged
    original/English comparisons remain **issue**, with no missing/stale verdicts: tiny placard marks
    could be grain or schematic writing; the gold emblem still has no confident reading.
    `event-props-qa.md` records exact crops/hashes. No owner decision is required and no exception is assumed.
  - Illustrated card-margin follow-up: **13 repaired margins accepted** on
    **007/026/033/039/044/054/075/079/082/087/093/094/098**. Grey drawing components and
    coloured backgrounds are preserved; card093 moves left to keep both falling leaves.
    A fresh D10 pass rejected three remaining fragments, now corrected and cold rechecked.
    Full-album gate **19 ok / 1 issue**, margin details **13 ok / 1 issue**; no missing/stale verdicts.
    **Card063 remains open**: incomplete top falling-leaf outline and faint upper/right caption fringe.
    `card-background-qa.md` / `card-background-verdicts.tsv` record scope, hashes and rejected candidates.
  - Latest main validation: **129 tests passed / lint 0**, verifier **399 changed files / 0 errors**;
    cold `work/qa/card_repair8_final_smoke` passed; `work/qa/card_repair8_final_cold` has **100/100
    complete captures**, **0 Japanese lines in one textlog** (graphics excluded). Main disc
    **182,449,344 bytes**, **2026-11-01 17:14:04 UTC**, SHA-1 **7015ad07c73b0721d0ab3526f2d4a26075088df2**.
    Earlier `card_repair8_cold` is superseded. **Phase 8 remains incomplete; phase 9 has not started.**
  - Full 100-card artwork audit: **20 whole-card sheets reviewed**; eight masks repaired on
    **034/038/049/059/076/077/078/084**, preserving monkey/oni/staff/hand edges and removing old strokes.
    Final D10 details **8/8 ok**; full album **7 ok / 13 issue sheets**, with no missing/stale verdicts.
    `card-full-art-qa.md` and `card-full-art-verdicts.tsv` record rejected candidates and fourteen remaining
    card defects. The red notice's cross-archive ANM scan supplies leads only; its runtime path remains open.
  - Previous main validation: **127 tests passed / lint 0**, verifier **399 changed files / 0 errors**;
    cold `work/qa/cards_full8_final_smoke` passed; `work/qa/cards_full8_final_cold` has **100/100 complete
    captures**, **0 Japanese lines in one textlog** (graphics excluded). Main disc **182,454,048 bytes**,
    **2026-11-01 16:39:00 UTC**, SHA-1 **5b1f3ee68331bd006fc9c1c7e0e49010a4a16816**.
    Earlier `cards_full8_cold` and `cards_full8_accepted_cold` are rejected intermediate candidates.
    **Phase 8 remains incomplete; the full-album gate is red and phase 9 has not started.**
  - Menu headers: **4/4 cold routes on both discs**, complete ANM/TIM pixel matches for Game Album,
    Quick Match! and Name Entry; saved-Status viewing also uses Game Album on the original. Fresh D10
    review **8/8 sheets ok**. `menu-titles-qa.md` and `tools/debug/menu_titles.py` record contexts,
    named-disc verification and stale-capture rejection. The separate Rank Details atlas consumer remains open.
  - Card caption masks corrected on **003/011/022/045/085/086**: complete old strokes and pale fringe removed,
    ear/breath-puff/heart preserved. Enlarged review rejected two grey fill-donor streaks; explicit blank-paper
    bounds remove them without the broad candidate's shoreline/smoke damage. Final fresh D10 review **8/8 ok**;
    `card-margin-polish-qa.md` records commands, rejected evidence, final hashes and limited scope.
  - Earlier caption-polish validation: **126 tests passed / lint 0**, verifier **399 changed files / 0 errors**;
    cold smoke `work/qa/card_polish8_accepted_smoke` passed, album **100/100 complete captures**, and
    **0 Japanese lines in its textlog** (graphics excluded). Main disc **182,454,048 bytes**,
    **2026-11-01 16:07:41 UTC**, SHA-1 **6ba02079bfa79409b99ce78d063942d6266eccdd**.
    Accepted album run: `work/qa/card_polish8_accepted_cold`; earlier `card_polish8_*cold` candidates are superseded.
    **Phase 8 remains incomplete; no phase-9 or release work is authorized by these scoped verdicts.**
  - Event artwork: Kintaro's snow-statue initial is now **K** across EVT110D's 240-pixel texture seam,
    and all three EVT620D orange fans read **Festival** (FEST / IVAL). Exact component masks preserve
    the statue oval and fan ribs; the first fresh review caught six cream fringe pixels, now removed
    and regression-tested. The disc-sourced oracle handles EVT620D:1 overwriting :0's shared CLUT.
    `event-props-qa.md` records routes, masks and limits. Tiny snow placards and the ending's black
    gold-prop mark remain unclassified; **phase 8 cannot advance**.
  - Final event-prop validation: **5/5 complete regions on both discs**, fresh D10 **4 detail sheets ok /
    2 context sheets with issues**; no missing/stale verdicts. **125 tests / lint 0**, verifier **399 changed
    files / 0 errors**, **0 Japanese lines in 2 logs** (graphics excluded); cold main smoke passed.
    Main disc: **182,454,048 bytes**, built **2026-11-01 15:32:34 UTC**, SHA-1
    **d20bb64a57a110da58795477de0bf197effcc0de**. `build/event_props8.bin` is an older rejected candidate.
  - Medicine now uses full **Medicine** on maps143/144, preserving Items in the same atlases. A hash-checked,
    unreferenced diagnostic checker cell supplies the third tile when transparent space runs out.
    Both discs pass **4/4** complete Medicine/Items placements; fresh D10 review **8/8 ok**.
    `medicine-plaques-qa.md` records allocation, preservation, commands and verdict hashes.
  - Current validation: **123 tests / lint 0**, verifier **398 changed files / 0 errors**, **0 Japanese
    lines in 4 sign logs** (graphics excluded); cold `medicine8_smoke` and `medicine8_main_smoke` passed.
    Main disc is byte-identical to `build/medicine8.bin`, **182,454,048 bytes**, built
    **2026-11-01 15:08:17 UTC**, SHA-1 **d0552aced38bba6aed45e37620cf76e7ddff331d**.
  - Symbol follow-up: **7/7 cold routes on both discs**, fresh D10 **5 ok / 4 issues**. Shrine papers are
    abstract dots/bars and torii-like pictograms; event01's old snow-placard note was a review error (the
    historical frame also shows the bath). Actual EVT110D snow art remains open. Round banners remain
    unresolved, now located at GV02070D:2 (128,180)-(144,196), CLUT13, with **30 exact texture matches**.
    `symbol-classification-qa.md` preserves details; historical verdicts stay unchanged.
    **Phase 8 cannot advance: remaining graphics, full visual and story/NPC coverage gates remain open.**
  - Large bath plaques now read **Bath** in **five cold placements on both discs**: map180 and both
    bathhouses in maps320/321. `gfx_signs.py` reassembles map180's split right column; all board edges,
    mounting posts, palettes and layouts are preserved. M220D:3's duplicate is regenerated, but its
    natural minigame placement remains unproved. Fresh D10 review accepts **10/10** scoped sheets;
    `bath-boards-qa.md` records hashes, sources and limits.
  - Current validation: **121 tests / lint 0**, verifier **398 changed files / 0 errors**, **0 Japanese
    lines in 5 logs** (graphics excluded); cold main smoke `bath_boards8_main_smoke` passed. Main disc:
    **182,454,048 bytes**, **2026-11-01 14:50:28 UTC**, SHA-1
    **161e5adff5fae2c79cd691b2a86cc9cfbcd59b28** (identical to `build/bath_boards8.bin`).
    **Phase 8 cannot advance: remaining graphics, phase-wide visual and story/NPC gates are still open.**
  - Earlier Medicine allocation lead is resolved above. `field_label_plan.py` excludes all existing English
    plaque allocations when listing candidates; maps143/144 retain their native CLUT31488/page5.
  - Narrow plaques now show full **Flowers / Items** in **six cold contexts on both discs**:
    maps99/100, 143/144 and 237/238. `gfx_field.py` uses isolated atlas tiles and hash-checked
    front-grid/record edits; source tiles, rear grids, native palettes and attributes are preserved.
    The rain oracle uses captured CLUTs with disc-sourced pixels and requires an unoccluded full label.
    Fresh D10 review accepts **12/12** context/detail sheets; `narrow-plaques-qa.md` records proof and limits.
  - Current validation: **120 tests / lint 0**, verifier **398 changed files / 0 errors**, **0 Japanese
    lines in 6 logs** (graphics excluded); cold main smoke `narrow8_main_smoke` passed. Main disc:
    **182,454,048 bytes**, **2026-11-01 14:28:34 UTC**, SHA-1
    **3231d03e8188cf2631110dc4f4f8d2b5a3618c8f** (identical to `build/narrow8_final.bin`).
    **Phase 8 cannot advance: remaining graphics, phase-wide visual and story/NPC gates are still open.**
  - Equipment plaques: map45 now shows full **Weapons / Armor / Shoes**, with **3/3 complete
    matches on both discs** and a fresh D10 gate of **6/6 ok** (one scene, three detail pairs).
    Weapons expands the wood interior within the original 32-pixel tile pair; no map/code edits.
    Complete engraved-mask sweeps find these three glyph forms only in GV01000D:0.
    `equipment-signs-qa.md` records preservation, source coordinates, routes and verdict hashes.
  - Narrow-plaque investigation: the Flowers/Items maps draw only a central 16-pixel tile even
    when the atlas shows a wider board. `field_label_plan.py` now prints qualified native neighbors
    and conservative allocation candidates. Maps99/100, 237/238 and 143 are mapped in the report;
    mixed-palette/layer neighbors need verified tile-layout or renderer work, not a wider PNG alone.
  - Latest validation: **111 tests / lint 0**, verifier **394 changed files / 0 errors**, cold main smoke
    `equipment8_main_smoke` passed; **0 Japanese lines in one log** (graphics excluded). Main disc:
    **182,451,696 bytes**, build **2026-11-01 14:08:30 UTC**, SHA-1
    **49e632d7417e4901ca0bfb0bc872b18eb65ab6bd** (identical to `build/equipment8.bin`).
    **Phase 8 cannot advance: its phase-wide graphics/visual gates remain incomplete.**
  - Games/Produce/Fish Shop checkpoint: **20 sign placements in 18 atlases** translated; complete mask
    sweeps cover seven new Games, nine Produce and four Fish Shop textures. **24/24 cold placements
    pass on both discs** (10 Games, 10 Produce, 4 Fish Shop). Read-only D10 review accepts all 24 detail
    pairs; Games gate **20/20 ok**, shop gate **22 ok / 6 issues** for other plaques/banners.
    `shop-boards-qa.md` and two verdict TSVs record sources, exact hashes, routes and limits.
  - Maps99/100's native initializer starts Dog's event and moves Momotaro to the southern entrance.
    Their Produce routes use native op2B to set only flags 0x6F=0 and 0x90=3 before the full initializer;
    these are explicit graphics fixtures, not story-progress verdicts. Map208's Fish Shop copy remains
    runtime-unproved. Flower, footwear/weapon/armor, item/medicine and bath plaques still need work.
  - Latest validation: **111 tests / lint 0**, verifier **394 changed files / 0 errors**, cold main smoke
    `shop_boards8_main_smoke` passed; **0 Japanese lines in 24 logs** (graphics excluded). Main disc:
    **182,451,696 bytes**, build **2026-11-01 13:39:20 UTC**, SHA-1
    **1af379e36d3a23e8bc65b2ec8f131508afc16f9d** (identical to `build/shops8.bin`).
    **Phase 8 has not met its done-when; do not advance to phase 9.**
  - Tea/Bank plaques: **28 Tea + 23 Bank placements across 28 atlases** translated, including M220D.
    Both engraved variants were swept by complete pixel masks. Bank uses a 16-pixel source span,
    preserving the complete word and all surrounding art; night Tea uses the existing CLUT-1 fix.
    **26 Tea + 22 Bank cold placements pass on both discs**. Reframed maps99/100 after review caught
    off-screen plaque edges despite a passing English lettering match. Fresh D10 review accepts all
    **48/48 detail pairs**; whole-scene gate is **78 ok / 18 issues** across 96 pairs, with no missing
    or stale verdicts. Other signs/emblems remain; `tea-bank-signs-qa.md` and its verdict TSV record scope.
  - Latest validation: **109 tests / lint 0**, verifier **394 changed files / 0 errors**, cold smoke
    `tea_bank8_smoke` passed, **0 Japanese lines in 48 logs** (graphics excluded). Main disc:
    **182,451,696 bytes**, **2026-11-01 13:11:23 UTC**, SHA-1
    **5061f496f11a4fa0be71e1c4bf936bfb181e2b7d**. **Phase 8 still has not met its done-when.**
  - Inn signs: both engraved forms now read **Inn**, **34 placements / 28 atlases** including M220D.
    Cold original/English routes cover **26 field placements**, including snow, rain and night variants.
    The first night redraw lost strokes because CLUT 0 aliases wood/ink; a new regression caught it,
    and GV30002D now imports through distinct CLUT-1 colours. Fresh D10 review: **26/26 Inn details ok**;
    whole-scene gate **45 ok / 7 issues** (other Tea/と signs, purple-banner and ground-placard classification).
    `inn-signs-qa.md` / `inn-signs-verdicts.tsv` record the routes, hashes and unproved copies. Map208 has
    no known native initializer; unreferenced/underlying plaques and the M22 duplicate remain runtime gaps.
  - Current validation: **107 tests / lint 0**, verifier **394 changed files / 0 errors**, cold smoke
    `inn_final8_smoke` passed; **26/26 complete plaques / 0 Japanese lines in 26 logs**. Main disc:
    **182,451,696 bytes**, **2026-11-01 12:46:24 UTC**, SHA-1
    **7e5908a7bc3a4b2d6b85346a18da1cb050d1c3b1**. Phase 8 still has not met its done-when.
  - Additional Games boards: **GV16000D:3 / GV22000D:1**, plus identical **M220D:3**, translated.
    Five cold field placements cover bath town and both island boards in sunny/rainy states. The island
    board's split right edge was fixed after visual rejection; weather matching requires an exact full
    pixel pattern under a one-to-one palette remap. Fresh D10 review: **10/10 scoped sheets ok**.
    Reproduction/hashes/limits: `games-signs-qa.md`. M22's duplicate still lacks a visible natural placement.
  - Map284 regression isolated to a **SEQ tempo divide-by-zero**, Cause 0x24 / EPC 8006D494, rather than
    a loader wait. The warp now retains GSF0000D:23's native pre/post transition/music ops. **Two cold
    passes each on original, frozen and current discs**, with the unchanged arrival check; no delay added.
    `map284-regression.md` records the failing negative fixture, diagnostic controls and scoped verdict.
    The upstream zero-tempo cause remains untraced; this fixes the tested warp, not the game audio library.
  - Current validation: **105 tests / lint 0**, verifier **375 changed files / 0 errors**, cold smoke
    `games_more8_smoke` passed; **5/5 complete signs / 0 Japanese lines in 5 logs**. Main disc:
    **182,454,048 bytes**, **2026-11-01 12:10:14 UTC**, SHA-1
    **a55a142561d6bb35cd67b479a08e9692f57434c3**. Phase 8 still has not met its done-when.
  - Games-board checkpoint: **five atlases / six cold placements** now say Games. Actual CLUT ink and
    clean-wood sampling were corrected after rejected captures; every pixel outside lettering is preserved.
    Fresh read-only D10 review accepts **12/12 scoped context/detail sheets** (`games-signs-qa.md`).
    Survey rows #448/#456/#468/#547/#556 updated; other Games and roof-sign variants remain open.
  - Current validation: **103 tests / lint 0**, including the final wood repair's preservation test.
    Verifier **373 changed files / 0 errors**,
    cold smoke `games_signs8_fixed_smoke` passed, **6/6 complete signs / 0 Japanese lines in 6 logs**.
    Main disc: **182,454,048 bytes**, **2026-11-01 11:40:47 UTC**,
    SHA-1 **606ce85331274eff4e3e495021c391f1f2e29112**.
  - Corrected-initializer tour finished: frozen card-prop disc **464/465 scenes**, **0 Japanese lines in
    464 logs**; map284 failed. A clearly recorded current-build retry supplies its visual pair. Fresh
    read-only review covers **78 arrival/final sheets / 465 pairs**, with **0 missing verdicts, 25 not ok**.
    `corrected-tour-qa.md` and `corrected-tour-verdicts.tsv` preserve build hashes, scene order, sheet hashes
    and findings. This mixed-build audit does not approve all intermediate text, NPC dialogue or story flags.
  - Map284's dir-0 workaround is not reliable across builds: frozen tour + two isolated retries stall on
    op001D; original and two current-build runs pass. `map_watch.lua` is a read-only diagnostic. Root cause
    remains unresolved; do not weaken the warp's completion check or claim the new graphics fixed loading.
  - Static consumer lookup now follows paired map-table archives and page/CLUT identity. GV02000D:2's
    split contest board has **0 static tile/ANM matches** in paired map59/GV02001D; this narrows the search,
    not proof of native/story unreachability. Known GV13000D:2 board gives nine tile matches as a control.
  - Card-prop checkpoint: **20 sign/emblem placements on 18 cards** translated (Sake, 1000 ryo,
    Dumplings, Puffer fish, K/P initials and E crown marks), with **five marginal-caption fringe fixes**.
    `gfx_card_props.py` preserves blue curtain waves and adjacent object borders; added K/P to MIT hud7.
    Fresh read-only D10 review accepts **9/9 scoped sheets**; `docs/re/card-props-qa.md` records hashes/limits.
    Older marginal fringes elsewhere and the red Card Album notice remain open. **Phase 8 is incomplete.**
  - Latest validation: **102 tests passed**, lint 0; verifier **369 changed files / 0 errors**; cold smoke
    `work/qa/card_props8_smoke` passed; **100/100 complete cards** and **0 Japanese lines in 1 text log**
    at `work/qa/card_props8_cold6`. Main disc: **182,458,752 bytes**, **2026-11-01 11:03:30 UTC**,
    SHA-1 **1ff27c30c241edca355a724a9fce8e56d94f36cf**.
  - Card-art checkpoint: **56 sound-effect placements on 36 cards** translated; all 100 cards still have
    complete cold screenshot coverage. `gfx/card_art.tsv` and `gfx_card_art.py` preserve adjacent actors,
    chair/door edges, motion lines and underwater colour. Added generated-PNG consistency and prop regressions.
    Fresh read-only D10 review accepts **8/8 sound-effect sheets**, after correcting cramped Hop lettering,
    a Pshh stroke remnant and Twang/sweat-drop overlap. Small signs, clothing/crown marks, older marginal-caption
    remnants and the red album notice remain open; `docs/re/card-art-qa.md`. **Phase 8 remains incomplete.**
  - Latest validation: **101 tests passed**, lint 0; verifier **369 changed files / 0 errors**; cold smoke
    `work/qa/card_art8_main3_smoke` passed; **100/100 complete cards** and **0 Japanese lines in 1 text log**
    at `work/qa/card_art8_final3_cold` (graphics excluded from textlog). Main disc: **182,458,752 bytes**,
    **2026-11-01 10:46:26 UTC**, SHA-1 **d6c06dcc9a39d45fd49692aae423407608e33366**.
  - Caption/Rank Details checkpoint: **27/27 captions on both discs**, with exact textlog and native
    centering checks; **43/43 saved-Status record pages** on original, populated English and empty English,
    including all **11 rank values**, and controller return to Status. Source memory card unchanged.
    Fresh read-only D10 review accepts **3 caption + 10 record sheets** (`docs/re/captions-rank-details-qa.md`).
  - Added an optional warp closing-input delay: the original opening-frame Circle could dismiss a caption
    before capture. Rank Details retries only a missed press on the previous ready page, rejecting skips.
    This native saved-Status route uses **context 4** and the **Game Album title on both discs**; it does
    not prove display of the separate Rank Details atlas lettering. Caption fixtures prove layout, not
    all destinations' natural story entrances. The red Card Album notice remains unresolved and unchanged.
  - Latest validation: **99 tests passed**, lint 0; verifier **369 changed files / 0 errors**; cold smoke
    `work/qa/caption_details8_smoke` passed; **0 Japanese lines in 29 English logs** (graphics excluded).
    QA-only changes: existing main disc retained, **182,482,272 bytes**, **2026-11-01 09:45:58 UTC**, SHA-1
    **81f569029bc195b8ea7e8bdb725b1de469099a43**. **Phase 8 remains incomplete; do not advance to release.**
  - Small-prop checkpoint: sushi menu now has all five full food/price pairs in a horizontal layout above
    the actors; bath placards say **Private Today** in all three atlas copies; the swimming victory flag
    reads **First** in a natural cold win. Fixed retained brown Japanese antialiasing, actor occlusion,
    the egg label's x=240 texture seam, and the placard's inverted CLUT-2 ink. Added pixel digits 0-4 and
    preservation/palette/fit regressions. Fresh read-only D10 review accepts **8/8 scoped sheets**, after
    rejecting and correcting the flag's initially wrong erase bounds. **9/9 complete labels** match cold
    captures. One race rerun exited -1 after the win; the final cold retry exits 0. `docs/re/small-props-qa.md`.
  - The four product-logo families (CI0D/TITLE0D, YUGI0D, HOUGEN0D, FILESL0D) are now explicitly classified
    **kept Japanese under D5**, including title subtitles/furigana. The separate press-start instruction
    remains English; this exception does not cover signs, emblems or other lettering (`docs/re/graphics.md`).
  - Latest validation: **97 tests passed**, lint 0; verifier **369 changed files / 0 errors**; cold smoke
    `work/qa/smallprops8_main_smoke` passed. Six final targeted textlogs have **0 Japanese lines** (graphics excluded).
    Main disc: **182,482,272 bytes**, **2026-11-01 09:45:58 UTC**, SHA-1
    **81f569029bc195b8ea7e8bdb725b1de469099a43**; `build/props_final9.bin` is identical.
    **Phase 8 remains incomplete; do not advance to release.**
  - Name persistence checkpoint: four- and one-character names now pass native save/overwrite and a
    **separate cold reload on both discs**. All eight name bytes, including FF padding, are checked;
    source cards remain unchanged. `name_save.py` uses controller input after the existing Name Entry warp.
    Fresh read-only D10 review accepts **6/6 scoped sheets** (`docs/re/name-persistence-qa.md`).
  - Fixed the overwrite warning's missing **OK**: the native memory-card scanner treats every uppercase
    K byte as control syntax, while the old lint rejected only KK/KE pairs. The prompt now says **Is that
    okay?**. All **25 memory-card messages** were swept; seven regression cases cover literal K, a line
    beginning E after KK, termination space and valid text. Native code and graphics are unchanged.
  - Latest validation: **91 tests passed**, lint 0; verifier **369 changed files / 0 errors**; cold smoke
    `work/qa/persist8_smoke` passed; the four accepted English save/load logs have **0 Japanese lines**.
    Main disc: **182,482,272 bytes**, **2026-11-01 08:36:29 UTC**, SHA-1
    **dca819a139f5c9ccba906a1e083f764e46077269**. **Phase 8 remains incomplete; do not advance to release.**
  - Name Entry checkpoint: **80 Latin/symbol glyphs** replace the kana font in NAME0D:1 and PREM0D:1;
    checked selection-table edits give ordered D-pad navigation. Native four-character limit, ANM data,
    save structure, palettes, arrows and panel artwork are preserved. Existing Japanese record-name IDs
    now display Latin characters; the release README must explain this compatibility limit.
  - New `name_entry` cold scene (**465 scenes**) and `tools/debug/name_entry.py` cover **80/80 complete glyphs
    on each disc**, four-letter entry, rejection, back/edit/accept and the exact returned record bytes.
    Both discs also pass one-letter entry via Start. Fresh read-only D10 review accepts **4/4 sheets**;
    it caught the font's @ heart icon, replaced by an actual asterisk before the final build and tour.
    Reproduction, state addresses, verdict hashes and limits: `docs/re/name-entry-qa.md`.
  - Latest validation: **84 tests passed**, lint 0; verifier **369 changed files / 0 errors**; cold smoke
    `work/qa/name8_final_smoke` passed; both English name-tour logs have **0 Japanese lines**.
    Main disc: **182,482,272 bytes**, **2026-11-01 08:20:36 UTC**, SHA-1
    **8781edd1b47f4a947cb90197dbb65e9ac6730b17**. **Phase 8 remains incomplete; do not advance to release.**
  - Saved-record checkpoint: cold tours cover **43/43 Game Album pages** and **6/6 Quick Match pages**
    on original, populated English and empty-record English. `tools/debug/album_records.py` loads the
    game-written save, seeds records only in RAM, and navigates real menus; source card stays unchanged.
  - Maximum values exposed clipped points/items and crowded money units. Both record renderers now use
    checked x-coordinate edits that fit full units and native-width digits; empty scores say points, and
    six-digit money has a space before ryo. Fresh read-only D10 review accepts **10/10 panel sheets**.
    Reproduction, exact state addresses, verdict hashes and coverage limits: `docs/re/album-records-qa.md`.
  - Latest validation: **82 tests passed**, lint 0; verifier **369 changed files / 0 errors**; cold smoke
    `work/qa/records8_smoke` passed; all four English record tours have **0 Japanese lines**.
    Main disc: **182,491,680 bytes**, **2026-11-01 07:51:14 UTC**, SHA-1
    **3d7ddc6c7ae4442d2671dda01c40a9ef81da66b2**. **Phase 8 remains incomplete; do not advance to release.**
  - Status rank/counter checkpoint: all **six rank illustrations** and four English plates now have cold
    proof, plus a populated panel (rank 610, mastery 61, 100 cards, 99:59, seven-digit steps and money).
    Original and English each pass **7/7 complete picture matches**. `tools/debug/status_ranks.py` loads
    the game-written save, seeds real RAM record fields, and lets the game select/construct the UI.
  - Stress review fixed Money/card-label overlap; enlarged original comparisons also exposed old erasures
    cutting panel borders and leaving a Steps suffix fragment. Restored exact edges/blank backgrounds,
    tightened redraws to ANM bounds, preserved every digit/question mark, and retained full Money/ryo labels.
    The previously unlisted Hermit staff's 仙 is now full HER/MIT; silhouette and other character art preserved.
    Fresh read-only D10 re-review accepts **7/7 scoped sheets**. Reproduction/hashes: `docs/re/status-ranks-qa.md`.
  - GCV0310's four labelled portraits are dormant placeholders, not ordinary name tags: IDs 123-126 have
    **0 references in 4,894 parsed messages**. Cold Moon trace uploads the atlas but neither sprite binder
    uses those portraits. `portrait_audit.py`, `portrait_trace.lua`, and `docs/re/portrait-audit.md` record the
    exact evidence and limits; they remain unchanged, and must be reopened if a future route displays them.
  - Latest validation: **80 tests passed**, lint 0; verifier **369 changed files / 0 errors**; cold smoke
    `work/qa/ranks8_final_smoke` passed; `ranks8_final2` textlog has **0 Japanese lines in 7 logs**.
    Main disc: **182,491,680 bytes**, **2026-11-01 07:39:16 UTC**, SHA-1
    **fcca7fe2b700c03a8be3012b24a24f71d02d87ce**. **Phase 8 remains incomplete; do not advance to release.**
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
  - Character names, fan lettering and coat numerals have natural attract-mode proof. `character-intro-qa.md`
    and `character-props-qa.md` record exact bounds and cold routes. GCV0310's four placeholders have no
    literal message references (`portrait-audit.md`); reopen if runtime evidence ever displays them.
  - Finish the corrected tour's **25 historical non-ok sheets** using `corrected-tour-verdicts.tsv`;
    supplement with the shrine-paper classification/event01 correction in `symbol-classification-qa.md`.
    EVT110D's snow initial is now K with cold event07 proof; its tiny placards remain open. Three EVT620D
    Festival fans are translated; the ending's separate gold-prop mark near (164,53) needs classification.
    The round banner emblem and other signs/costume marks remain open.
    Map284 now has six passing native-setup retries (`map284-regression.md`). Review
    intermediate text frames and add NPC interaction/later-story routes: 465 arrival/final pairs are not
    complete dialogue or story-state coverage. Older pre-initializer shots remain superseded.
  - Field signs: locate the runtime consumer of GV02000D:2's split contest board. The restored tiny
    bath-counter placard is now Private Today, verified under palette 2 in all three contexts (`small-props-qa.md`).
    Five Games atlases now have six accepted cold placements (`games-signs-qa.md`); other Games variants
    #481/#514 Games boards are now accepted in five more contexts; #562 still needs classification,
    and other equipment/shop and sprite-strip signs remain Japanese. Both Inn glyph families now have
    26 accepted cold placements (`inn-signs-qa.md`); seven context findings keep their gate red.
    Static/underlying copies and map208 remain unproved.
    Tea/Bank glyph families now have 48 accepted cold placements (`tea-bank-signs-qa.md`); their broader
    views exposed Games boards in maps80/81 and 263 plus Produce/Fish Shop boards, now covered by
    `shop-boards-qa.md` (24 cold placements). Map45's equipment plaques now have cold proof
    (`equipment-signs-qa.md`); Flowers/Items now have six accepted widened placements
    (`narrow-plaques-qa.md`). Large Bath boards now have five accepted cold placements (`bath-boards-qa.md`);
    small underlying/unplaced ゆ copies and other equipment/medicine sprite forms remain.
    Medicine and Items at maps143/144 now have cold proof; unplaced/rear-grid copies remain unproved.
    GV01000D:0 medicine records 102/103 have no default grid placement in map45; locate their native consumer.
    Follow the five unresolved issues in `shop-boards-verdicts.tsv` and the unresolved portions of the 18 older
    whole-scene issues in `tea-bank-signs-verdicts.tsv`. Historical verdicts are not retroactively changed.
    `plaque_consumers.py tea|bank` gives static navigation leads; `signs_tour.py --only tea* / bank*`
    means the explicit named cases in its CASES table (the CLI does not expand wildcards).
    `gfxfind_rect.py --indices 12 13` finds complete engraved-glyph copies; `inn_consumers.py` lists their
    static map consumers. `signs_tour.py --only` reproduces the
    new Games, accepted contest and bath contexts; `fieldmap.py` is a navigation preview, never QA evidence.
  - Shared HUD counters: natural Win/Loss/min/sec/later/small-Bonus contexts remain unproved;
    item 73 is now **Duel**, with accepted natural solo/versus timer-expiry proof (`duel-cue-qa.md`).
    partial M990D:2 item 42 and M990D:3 items 19/20 retain original pixels and need runtime classification.
    `hud_units.py` reproduces the accepted 12-label fixture, 8 natural contexts and record stress case;
    `ice.lua` now reaches the left ice-tower course with controller input. Broader versus/record states remain.
  - Minigame labels: M05/M08/M18/M50 have complete sprite-assembly proof, but natural Jackpot, near-win,
    Miss and Start positioning still needs routes. Race Hit/nonzero payout remain fixture-only; the normal
    story return remains untested (both original and English direct warps return to the debug system menu).
    `tools/debug/minigame_labels.py` reproduces all 48 states; `race.lua` advances the natural race screens.
  - Cards: all 100 prefecture captions and marginal dialect phrases are English; **56 sound-effect placements
    on 36 cards** are now translated (`card-art-qa.md`). Four signs and 15 costume/crown marks now have
    cold proof (`card-props-qa.md`, 20 placements because the curtain uses two panels). Caption fringes
    on 028/036/046/081/099 are fixed. Follow-up `card-margin-polish-qa.md` now corrects
    003/011/022/045/085/086 with eight accepted cold sheets; the older 045 no-op is superseded.
    Full follow-up `card-full-art-qa.md` corrects 034/038/049/059/076/077/078/084 and reviews all 100 cards.
    Follow-up `card-background-qa.md` accepts thirteen more margins. Its **last card defect, 063**,
    is now fixed by `card063-qa.md`: complete top falling-leaf contour and
    upper/right fringe removed. The current full-album gate is **20/20 accepted**, with the enlarged
    card063 detail also accepted; thirteen unchanged margin details retain their accepted observations.
    Locate/render the fragmented red new-card tag.
    HOUGEN0D ANM 5/6 does not reference its visible atlas fragments; the runtime draw path is still unknown.
    `tools/debug/atlas_refs.py` scans cross-archive ANM leads by page/depth/CLUT, but cannot prove runtime
    use or disuse; the report records the three fragment bounds and a working control region.
  - Finish natural outcome/versus routes. M03 Perfect, M14/M56 and M59 story banners now have scoped cold
    sprite-assembly proof (`hud-outcomes-qa.md`); M59's alternate TIM 6 / ANM 16 remains unapproved, and
    Which? has fixture proof only. M010 awards and M990D:1 announcements also have full-sprite cold proof.
    The pause fixture does not work while other games are in dialogue, so its exit code alone is not coverage.
    M990D:0's 40 large winner/ordinal states are now translated and cold-rendered (`results-qa.md`);
    normal gameplay progression still needs tour coverage. Small Bonus now uses a separate English sprite;
    its original overlapping fragment users remain intact and unclassified. See `docs/re/hud-counters-qa.md`.
  - Graphics text (D5: all of it; docs/re/gfx_survey.tsv, 203 rows): product-title logo variants are now
    explicitly retained under D5 (`graphics.md`). Remaining work: the native Rank Details title consumer
    (Game Album/Quick Match!/Name Entry have cold proof in `menu-titles-qa.md`),
    remaining M990D fragment/context classification, remaining banners
    (GV02000D:2, GV13000D:2...), HOUGEN0D:0 new-card tag, ending-art signs/emblems,
    illustration SFX/signs on HCARD* cards. Per image: `gfx.py export`, find each sprite's rect (in-game the sprite rect
    can be narrower than the JP atlas row: shoot it), add LABELS, `gen_gfx.py`, build `--out build/g8.bin`, shoot.
  - Saved-record QA: Status covers all rank pictures and wide counters (`status-ranks-qa.md`); all five
    Game Album record formats and six Quick Match pages now have populated/empty cold proof
    (`album-records-qa.md`). Name Entry now has all 80 glyphs, editing/confirmation and returned-name proof
    (`name-entry-qa.md`); name memory-card persistence now has four passing original/English cases
    (`name-persistence-qa.md`). Saved-Status Rank Details now has 43 populated/empty pages, all rank values
    and return proof (`captions-rank-details-qa.md`); natural record-setting remains.
    Name Entry mode 0x51 needs its native context byte set to 3 when warped, to return to Quick Match;
    `SCENE='name_entry'` and `tools/debug/name_entry.py` do this. Use the existing save fixture for reload QA.
    `work/qa/album8_*` exploratory states are from earlier builds: regenerate cold before accepting verdicts.
  - Text tour (`warp_all.py --hold 1500 --click 45 --probe tools/lua/textlog.lua`, then `tools/textlog.py`),
    `jp_left.py` on the build, visual-QA sheets + `qa_gate.py` verdicts (in-session `visual-qa` agents, D9),
    graphics-text rows in zoomed cold-boot shots (docs/re/graphics.md).
  - Captions: all 27 rows now have original/English cold op-26 captures and exact text/centering checks
    (`caption_tour.py`, `captions-rank-details-qa.md`). Natural destination/story entrance coverage remains.
  - Weak short forms to revisit in polish: EXE fireworks items named bare "Dog"/"Monkey"/"Momotaro", 7-byte key
    items "Island" (鬼ヶ島), "Prism" (虹の玉), "Steps" (歩数計), and OVLGMAIN@800CB5D4 "Flower" (花屋).
- **Open bugs / gaps:**
  - Map284's bare warp is a retained negative regression case: frozen disc 1ff27c30... raises a sequence
    tempo divide-by-zero. Native transition setup now passes twice on all three discs. Preserve the frozen
    build, `map284_bare.txt` and failure evidence; investigate audio lifetime if a natural route reproduces it.
  - The nine historical map hangs are resolved by correct initialization and map 294's entry setup;
    story flags remain unmapped (warped maps show default state). `tools/deadcode.py` output is not safe hook
    space without an exec watch (`tools/lua/deadwatch.lua`, `warp_all.py --debugger`).
  - Phase 8 remains incomplete: much of the 203-row graphics survey, the full visual manifest,
    and the corrected map interaction tour remain open. Do not advance to phase 9 on scoped graphics verdicts.
- **Waiting on the user:**
  - (resolved, D9) reviews: the run brief allows a fresh read-only pass, so the repo's in-session `reviewer` /
    `visual-qa` agents do the phase 6/8/9 verdicts.
  - Quiz keys M510D/227, 229, 238 look factually off in the JP (kept; game scores .0). Non-blocking.
  - GUI keyboard input in `tools/pcsx/` not proven by hand (headless-only runs).
  Non-blocking; check when playtesting.
