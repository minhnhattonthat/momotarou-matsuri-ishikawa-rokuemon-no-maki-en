# Text boxes and width budgets (phase 5 width gate)

Machine-readable: `tools/windows.py` (`variants()`, `budget(row, variant)`); `python -X utf8 tools/windows.py`
prints counts per variant and tag. Widths are sums of `engine.widths()` advances (fonts/en12.txt: caps 6 px,
lower case 5 px, i/l 2 px, space 4 px; Japanese chars and `　` 12 px). Budgets are for the **sum of advances**.
Stress lines: `tools/debug/widthgate.json` (`build.py --qa-file ...`), runs in `work/qa/wg_*` (ruler digits are
5 px: group k starts at x0 + 50k), read off 3-6x zoomed shots (`sheet.py --crop --zoom`).

## Measured (verified in-game, 2026-11-01)
| Variant | Items | Text x | Right limit | Budget | Lines | Evidence |
|---|---|---|---|---|---|---|
| message (op 02, no voice) | 3,967 | 48 | gold frame inner edge x=282 (left inner 37) | **228 px** | 3 visible; a 4th line scrolls the box up (the Japanese does this too: 1,063 four-line pages) | event00 f4110 (GSV0001D/6/013A), game_m00_02 (PREM0D/14) |
| message with portrait (voice != 0xFFFF) | 927 | 90 | same frame, 282 | **192 px** | 3 visible | event00 f4005 (GSV0001D/6/0004) |
| memory-card messages (`{KK}` lines, `{KE}` end) | 25 | 72 | frame inner 258 | **180 px**, <= 64 bytes/line, no `KK`/`KE` byte pair in text | 3 | continue f3340 (SLPM 80018550/98) |
| main menu items (OVLXTTL 800CB504-34) | 4 | 62 / 184 | next column 184 / frame 282 | **112 / 92 px** | 1 | game_m00_02 f2970 |
| EXE choice boxes (はい/いいえ/遊ぶ/やめる/泊まる/休む/売る/買う/説明/N人/ふつう) | 15 | 260 | frame ~288 (box 0x8002CD58: x=0xEE w=0x38) | **26 px** | 1 | game_m00_02 f3510 |
| title New/Continue line (OVLXTTL 800CB4E4) | 1 | 48 | layout: items must start at x=108 and x=192 (peach cursor at fixed x); pad with `　` (12 px) and spaces (4 px) | 228 | 1 | game_m00_02 f2490 |

Vertical: line pitch 14 px (y = 170, 184, 198) in the message box, 16 px in the memory-card box.
Record limit (all variants): <= 32 units per line incl. codes (`windows.LINE_UNITS`); 228 px of English is
~50 chars = ~26 units, so the px budget binds first.

## Guess (Japanese design width, 12 px per JP char of the longest line; measure before shortening)
- **op 41 choices** (1,601 items, quiz/choice answers, shuffled by the handler 0x800306BC): drawn at x=232 in the
  M510 quiz; the answers registered but were not on screen in the frames shot (wg2_m51), so not measured yet.
- **op 26 captions** (27 place names): build_line, frame (0x5F, 0x34, w 0x82 = x 95..225), text centred as
  `x = 160 - units * 6` (0x80034DC0): assumes 12 px per unit, so VWF English sits left of centre. Phase 7: a
  `line_width(obj)` helper and repointing the centring sites (also check other `count * 6` sites).
- **other code strings** (1,118: OVLGMAIN board UI, items, cards; OVLM minigame HUD; OVLXTTL trial screens):
  many sit in fixed layouts (e.g. trial info panel: label x=48, values at 85/160/216). Measure per screen in
  phase 8 when a LONG line hits a guessed budget; in-place space (`max` bytes) is a hard cap until relocation.
- Money templates (`[20]x7 + 両`, `－x6 + 両`): put_number (0x8002A004) writes digit glyphs into the first records,
  so keep the leading `[20]` slots exactly; the suffix (`両` -> `ryo`) may grow. **Measured** (marker build,
  event00 f4260, field money box at text x=216): digits (10 px) + `ryo` (15 px) overrun the frame by ~3 px; the
  box (0x80033DC0: frame x=0xD0 w=0x60, text x=0xD8) needs to move/widen ~6 px left in phase 7 (or shorter suffix).
