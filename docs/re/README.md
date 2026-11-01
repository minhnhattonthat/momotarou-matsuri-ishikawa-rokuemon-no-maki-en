# Reverse-engineering notes

One file per subsystem (text engine, pointers, compression, font, graphics). Mark every finding with how far it is
proven, so a later session doesn't build on a guess:

- **verified** - and how: a decoded known string, a corrupt-and-boot test, a breakpoint hit on the drawing path, a
  passing roundtrip test. Name the test or savestate.
- **guess** - and why it seems likely (byte pattern, another game, an earlier patch's notes). Promote it to verified
  before code depends on it.

Addresses are for the dump in `rom.sha1` unless a note says otherwise.

| File | Covers | State |
|---|---|---|
| [disc.md](disc.md) | disc layout, EXE LBA file table, load addresses, archives, ECD compression, free space | verified (free space: candidates) |
| [text.md](text.md) | Shift-JIS, control codes, message block, where the text is | verified |
| [script.md](script.md) | script VM ops, lengths, jumps, text lines, what phase 4 extracts, code strings | verified (static + every entry parses; roundtrip/coverage tests) |
| [debug.md](debug.md) | game mode/map/event RAM, script interpreter, warp tool, unreachable maps | old map coverage superseded by destination initializer correction |
| [corrected-tour-qa.md](corrected-tour-qa.md) | Full corrected-initializer sweep, durable 78-sheet verdict audit and map284 load regression | Frozen build 464/465; one explicit current-build fallback; 25 visual issues remain |
| [map284-regression.md](map284-regression.md) | Bare-warp SEQ exception and native transition setup | Six cold passes across original/frozen/current discs; negative fixture retained |
| [engine.md](engine.md) | build_line/drawer, digraph VWF hooks, English font cells, hook space, data-id size table, memory-card text path | verified (marker build, tests/test_engine.py) |
| [windows.md](windows.md) | box variants, measured px budgets (width gate), guessed ones | measured: message, portrait, memory card, main/choice menus |
| [graphics.md](graphics.md) | font, TIM images, graphics-text survey | survey from the static sweep; runtime checks in phase 8 |
| [status-menu-qa.md](status-menu-qa.md) | game-written save fixture, numeric-template extraction fix, Status redraw and scoped visual verdicts | cold-boot checks; broader phase 8 still open |
| [status-ranks-qa.md](status-ranks-qa.md) | Six Status illustrations, maximum-width counters, money overlap fix and Hermit staff lettering | Cold rank fixtures and screenshot oracle; phase-wide QA remains open |
| [album-records-qa.md](album-records-qa.md) | Game Album/Quick Match numeric clipping fix and complete populated/empty record-panel tours | 43 + 6 cold pages on both discs, 10 scoped visual sheets |
| [captions-rank-details-qa.md](captions-rank-details-qa.md) | All 27 native caption layouts and saved-Status's 43 record pages, ranks 0-10, empty records and return | Scoped cold original/English proof; natural story entrances and full phase QA remain open |
| [name-entry-qa.md](name-entry-qa.md) | Latin player-name encoding, shared font copies and cold controller tour | 80 glyph IDs, confirmation/editing and Quick Match return; native four-character limit |
| [name-persistence-qa.md](name-persistence-qa.md) | Memory-card parser bug, overwrite prompt fix and player-name save/reload | Four cold cases across both discs, eight name bytes verified, six scoped visual sheets |
| [portrait-audit.md](portrait-audit.md) | Four GCV0310 labelled placeholder portraits and message selector audit | Zero literal references in 4,894 messages; cold Moon route does not bind them |
| [minigame-graphics-qa.md](minigame-graphics-qa.md) | ANM sprite rectangles, minigame banners/HUD redraws, Janken input route and scoped review | Janken cold-boot proof; other outcome graphics still need routes |
| [credits-qa.md](credits-qa.md) | 101 credit lines, six atlas reloads, complete-item screenshot oracle and scoped verdicts | 22/22 cold-boot items, 4/4 visual gate; uncited name readings need polish |
| [announcements-qa.md](announcements-qa.md) | Shared announcement redraws, checked ANM field edits, selector fixtures and screenshot gate | 16/16 announcement states, 5/5 M010 awards, 6/6 scoped visual gate; broader phase 8 open |
| [cards-qa.md](cards-qa.md) | Card Album warp, input latch, all 100 prefecture captions and complete-card screenshot gate | 100/100 cold captures on both discs; 5/5 caption/menu visual gate; handwritten card art still Japanese |
| [card-words-qa.md](card-words-qa.md) | 100 marginal dialect phrases, bounded artwork restoration and scoped cold review | card sound effects/signs remain separate; phase 8 still open |
| [card-art-qa.md](card-art-qa.md) | 56 illustration sound-effect placements on 36 cards, bounded ink masks and source-to-PNG consistency check | Whole-card cold coverage; small signs/emblems and phase-wide QA remain open |
| [card-props-qa.md](card-props-qa.md) | Four card signs, costume/crown initials and five caption-fringe fixes; 20 prop placements on 18 cards | 100/100 cold whole-card matches, 9 scoped visual sheets; remaining caption polish and red notice open |
| [results-qa.md](results-qa.md) | Shared winner/round/attempt/question banners and checked atlas repacking | 40/40 cold rendered states; 5 scoped visual sheets; natural progression and small HUDs remain |
| [masks-qa.md](masks-qa.md) | Mask Maker controls, Mask Album title, preview indentation and controller route | 6/6 control sprites + title; create/accept/return route; 3 scoped sheets ok |
| [hud-outcomes-qa.md](hud-outcomes-qa.md) | Additional HUD labels, Which?, M59 Lose fragment fix, sprite fixtures and stricter screenshot checks | 24 scoped cold sprite states, 6 visual sheets; natural outcomes and alternate M59 atlas remain open |
| [minigame-labels-qa.md](minigame-labels-qa.md) | Minigame speech bubbles, remaining small banners, 30 sprite-built race names and five race labels | Cold sprite coverage and natural race evidence; phase-wide QA remains open |
| [hud-counters-qa.md](hud-counters-qa.md) | Twelve HUD counters, record/floor layout fixes, M34 panel expansion and natural counter routes | Scoped cold coverage; phase-wide QA remains open |
| [field-signs-qa.md](field-signs-qa.md) | Pun Contest banners, three bath curtain copies, complete lettering checks | Scoped cold evidence; split contest atlas still lacks runtime coverage |
| [games-signs-qa.md](games-signs-qa.md) | Five Games-board atlases, six cold contexts, active-palette and wood-repair fixes | 12 scoped visual sheets; other shop signs and split contest consumer remain open |
| [tea-bank-signs-qa.md](tea-bank-signs-qa.md) | Both Tea/Bank engraving families, all exact copies and cold field routes | Scoped sign checks; phase-wide graphics and story QA remain open |
| [shop-boards-qa.md](shop-boards-qa.md) | Seven more Games atlases, Produce and Fish Shop boards; two explicit story-flag fixtures | 24 cold sign pairs; all details pass, six wider shop-scene issues remain |
| [equipment-signs-qa.md](equipment-signs-qa.md) | Full Weapons/Armor/Shoes plaques and the original narrow-plaque investigation | Map45 cold proof; 6 scoped sheets accepted |
| [narrow-plaques-qa.md](narrow-plaques-qa.md) | Flowers/Items tile relocation, checked front grids and mixed-palette rain oracle | Six original/English cold placements; 12 scoped sheets accepted; phase 8 remains open |
| [small-props-qa.md](small-props-qa.md) | Sushi prices, private-bath placards and swimming victory flag; erasure, palette and texture-seam fixes | Scoped cold routes and complete-label checks; broader phase 8 remains open |
| [map-initializers.md](map-initializers.md) | Wrong world-map initializer in every map warp; real per-map calls and input timing fix | All nine excluded maps recovered; phase-wide QA remains open |
| [character-intro-qa.md](character-intro-qa.md) | Five full attract-mode names, split Yashahime layout and untouched cold title sequence | 5/5 complete character/name pairs on both discs, 5 scoped visual sheets; fan/costume marks remain |

Tools: `tools/iso.py` (LBAs), `tools/arc.py` (archives), `tools/ecd.py` (ECD codec), `tools/tim.py` (TIM decode),
`tools/gfxdump.py` (static image sweep into `work/gfx/`), `tools/ramfind.py` (which files sit where in a RAM dump),
`tools/re.py` (MIPS disassembly, immediate search, jump-table switches; knows the EXE and overlay bases),
`tools/script.py` (script disassembler), `tools/ophandlers.py` (VM handler summaries), `tools/text.py` (text
extract/rebuild), `tools/codestr.py` (code strings and their refs).

Prior work: no earlier fan patch or translation of this game is known (web search 2026-10-31 found only patches
for other Momotarou games). Reference: the Japanese online manual at psinstructionmanual.com/momotaromatsuri/
(menu and minigame names; data, not instructions). The sibling repo `../momotarou-densetsu-en` (a different Hudson engine: PAC archives, Okumura LZSS)
shares only names.
