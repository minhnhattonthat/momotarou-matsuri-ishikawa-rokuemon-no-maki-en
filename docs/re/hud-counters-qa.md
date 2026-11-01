# Shared HUD counters and layout checks, 2026-11-01

**Phase 8 remains incomplete.** This checkpoint translates twelve more small
HUD words, checks eight natural minigame contexts and a four-digit record,
and fixes the layouts exposed by those checks. It does not approve the full
graphics survey or every natural use of these shared words.

## Graphics and geometry

M990D TIM 0 now has whole English labels in previously transparent, unreferenced
pixels `(48,192)..(160,216)`. `tools/gfx_hud.py` draws the existing MIT
`credits7.txt` font and changes only UV, dimensions and vertical offsets in
the following M990D ANM 2 items:

| Item | Japanese | English |
|---|---|---|
| 20 | 計 | Total |
| 31 / 32 | 勝 / 負 | Win / Loss |
| 33 / 85 | 分 / 秒 | min / sec (time units) |
| 34 | 階 | Floor |
| 48 | 後 | later |
| 49 | ボーナス | Bonus |
| 73 | 勝負 | Match |
| 77 | 回 | times |
| 78 | コ | items |
| 79 | 本 | pieces |

The old pixels remain intact. In particular, the 8x8 fragment at `(128,0)`
and the announcement strip at `(144,0,8,24)` must not be overwritten when
replacing Win/Loss or the small Bonus. Whole-archive ANM scans guard the new
space; palette, page, flags, record counts, scales and timings stay unchanged.
Original M990D ANM 2 SHA-1: `1aa343767e38cad3fdb959eb84e8854a0ebf78d6`.

The natural M34 counter panel was too narrow for `times`. M340D TIM 1's
48x32 panel at `(192,152)` is now 56x32, extending into eight unused columns.
The generator duplicates eight interior columns and shifts the complete right
border; the left border and both corner designs are preserved. ANM 7 item 9
changes only its width, retaining its left edge. Original ANM SHA-1:
`b7588abd46fc698482e28f3e53599fe032b9dda1`.

## Executable layout fixes

`engine.HUD_LAYOUT` pins every original instruction before changing it. The
disc verifier includes these five four-byte sites in the allowed ranges:

| Address | Change | Reason |
|---|---|---|
| `80040C0C` | object-count record unit x280 -> 276 | complete 19px `items` stays inside x296 |
| `8003D918` | absent-record dashes x256 -> 252 | gap before the full unit |
| `80040B7C` | Record heading x216 -> 200 | four digits at x240..271 remain unobscured |
| `80041880` | Floor label x40 -> 24 | put the English label before its number |
| `8003DAE8` | floor digits x24 -> 48 | `Floor 2`, with room for two digits and the timer |

The first review caught the right-hand `items` crossing the panel border;
the left-hand copy was already readable, so a global template search alone
had incorrectly passed that screen. The runner now checks the right unit
inside `(264,16,32,32)` independently. Bounded scans skip the emulator's 1x1
display-off frames; a regression test includes one before the valid frame.

The record stress route also exposed the old Record/digit collision. Its
first RAM fixture changed the HUD cache after the absent-record dashes had
been created, leaving those dashes across `9999`. This was a fixture error,
not a font defect. `hud_record.lua` now seeds game 15's actual record fields
at `0x800BDBF0 + 15*28 + {8,24}` before the normal getter at `0x80042514`
loads them (OVLM15 call `0x800CDA3C`). No memory-card file, glyph object or
texture is edited by this fixture.

## Routes and reproducible checks

`hud.lua` is a read-only discovery probe. It scans the ANM-part pool whose
base is at `0x8008C4F0`, count at `0x8008C46C`, stride 0x20, ANM pointer +0,
selected item +6 (EXE `0x8001B07C`). Presence in this pool is **not** visual
proof: the ice-tower and target-toss objects exist while their HUDs are hidden.
The original discovery sweep reached all 60 minigame scenes; the first 14
were repeated after correcting the probe's pool address.

`hud_units.py` verifies complete pixels and palettes in actual cold captures:

- Fixture: all twelve listed items through the real paused renderer.
- M05 and M14: Total in the target-toss result and dice sum.
- M15 and M22: object counts, including both M15 units.
- M19: Floor in the ice tower. `ice.lua` steps around the Snow Oni, crosses
  under the dividing wall, and walks into the left course with controller
  input. Repeated Circle alone stays in the entrance room.
- M20 and M28: firewood and candle quantities retain their object icons.
- M34: action count and its expanded panel.
- M15 stress: `9999` loaded through the game's ordinary record path.

```powershell
python -X utf8 tools/gen_gfx.py --only M990D.BIN:0 M340D.BIN:1
python -X utf8 tools/build.py
python -X utf8 tools/debug/hud_units.py --out work/qa/hudunits8_final3 --jobs 3
python -X utf8 tools/debug/hud_units.py --original --out work/qa/hudunits8_original --jobs 3
python -X utf8 tools/debug/hud_units.py --check-only --out work/qa/hudunits8_final3 --jobs 3
python -X utf8 tools/debug/hud_units_review.py work/qa/hudunits8_final3 --original work/qa/hudunits8_jp --out work/qa/hudunits8_review3
```

The original fixture and six ordinary contexts are in `work/qa/hudunits8_jp`;
the successful original M05/M19 routes are in `work/qa/hudunits8_jp_complete`;
the corrected original record fixture is in `work/qa/hudunits8_record_jp_clean`.
Rejected exploratory runs are not release evidence.

## Fresh read-only review and validation

After the panel and record-fixture corrections, a fresh D10 pass read all five
enlarged sheets without changing the implementation or artwork. The scoped
gate is **5/5 ok**, at `work/qa/hudunits8_review3/manifest.tsv` with its sibling
`verdicts/review.tsv`. These hashes preserve the evidence identity in git:

| Sheet | SHA-1 |
|---|---|
| fixture_sheet | `ceb07ca77361dc7e275ee861db6aaf7e2dd07535` |
| contexts1_sheet | `c680d437d976e5cfdd563d656c3a4fbfd0899e11` |
| contexts2_sheet | `8863bbc3a273e63d36276fc7282cc0ff685dfba1` |
| contexts3_sheet | `5c58230e23e6fd4909ada52cd0422a927e1a261e` |
| record_sheet | `5c0acf8c7c38e3fe0032b37208420798c4584fe9` |

- Final cold run `work/qa/hudunits8_final3`: **12/12 fixture labels**, all
  **8 natural minigame contexts** and the **9999 record case** pass coverage.
  M15's absent and populated record units additionally pass the right-edge
  bounded search. The corrected record capture has no overlaid dash sprites.
- `tools/check.py`: **68 tests passed**, lint **0 errors**.
- `tools/verify_build.py`: **363 changed files**, **0 errors**.
- Cold smoke: `work/qa/hudunits8_final3_smoke`, passed.
- `tools/textlog.py work/qa/hudunits8_final3`: **0 Japanese lines**, **0 markers**
  in 10 logs; graphics are outside this logger's detection.
- Main disc: **182,498,736 bytes**, **2026-11-01 05:57:34 UTC**, SHA-1
  **`e7ff120deca2a8d4b5ec6fe4203af61dca82f363`**.

The in-game M14 wall scroll is still Japanese and remains separate graphics
scope; the accepted Total-label verdict does not approve that background.
Earlier `hudunits8_final2` sheets were rejected for the narrow Times panel
and stale-dash fixture. Only `hudunits8_review3` is the final scoped verdict.

## Remaining scope

Natural Win/Loss/min/sec/later/Match/small-Bonus contexts remain to be found.
The partial item 42 and announcement items 19/20 retain their original pixels
and require runtime classification; this checkpoint does not certify them as
English or unused. More nonzero record categories, versus outcomes, signs,
card illustrations, retained-logo classification, menu/rank states, captions,
nine hanging-map routes and the phase-wide visual manifest remain open.
No owner-only decision blocks that work, and no release was created.
