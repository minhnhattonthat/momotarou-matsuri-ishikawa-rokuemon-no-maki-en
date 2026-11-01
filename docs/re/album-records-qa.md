# Game Album and Quick Match record panels, 2026-11-01

Phase 8 remains incomplete. This checkpoint covers the record panels, not the
full graphics survey, story interactions, Rank Details or Name Entry.

## Reproduction

Use the game-written card from `tools/debug/save_fixture.py`; the default is
`work/qa/save_fixture_checked/memcard1.mcd`. Each command cold-boots, loads a
copy of that card through the normal saved-Status route, seeds records in RAM
after loading, exits Status and navigates through the real menus/controller.
The source memory card is checked unchanged. No texture, glyph, display-object
coordinate, record getter or executable instruction is substituted by the probe.

```powershell
python -X utf8 tools/debug/album_records.py --out work/qa/records8_final
python -X utf8 tools/debug/album_records.py --out work/qa/records8_original --original
python -X utf8 tools/debug/album_records.py --out work/qa/records8_empty --empty
python -X utf8 tools/debug/album_records.py --out work/qa/trial8_final --trial
python -X utf8 tools/debug/album_records.py --out work/qa/trial8_original --trial --original
python -X utf8 tools/debug/album_records.py --out work/qa/trial8_empty --trial --empty
```

Each album run passes **43/43** pages in order; each Quick Match run passes
**6/6**. The helper requires both the ordered RAM/page log and every screenshot;
these are navigation checks, not an image-template matching oracle. The visual
pass below checks the actual rendered content. `--check-only` rechecks artifacts.
No scores were earned by playing, and these are not gameplay completion tests.

## Native layout and discovered bug

Records start at `0x800BDBF0`, stride `0x1C`, 70 entries. Story fields are played
`+0`, rank `+4`, record `+8`; Quick Match uses `+16`, `+20`, `+24`. The native
getter `0x80042514` selects the record field according to mode/context. A record
of `0xFFFFFFFF` means no score. The fixture retains empty player-name fields.

Game Album is mode `0x4F`; page index `0x8008C5C0`, UI state `0x800E27FC` (u16).
The 43 rows at `0x800E077C` contain category, illustration index and record ID;
the signed bytes at `0x800E0AD8` select record format:

| Type | Format | Fixture | Pages |
|---|---|---|---|
| 0 | Four-digit points | 9999 | Most pages |
| 1 | Four-digit items | 9999 | 14 |
| 2 | Time | 359999 frames, displayed 99:59:99 | 17-20, 22, 24, 27, 37 |
| 3 | Six-digit money | 999999 ryo | 23 |
| 4 | Five-digit points | 99999 | 30 |
| -1 | No record | No record line, also on original | 16, 21, 28, 35 |

Quick Match is mode `0x50`; page index `0x8008C5B8`, UI state `0x800E2ABC` (u16).
Its **six**, not eight, 12-byte rows at `0x800E0C48` use record IDs
0, 4, 6, 13, 16, 38. All six use four-digit points. Pointer tables follow the
six rows; treating them as additional records gives invalid IDs.

The first populated cold tour (`work/qa/records8_probe`) exposed English
**points/items clipped by the panel's right edge**, including the five-digit
score. `Record` and the adjacent number also appeared crowded; money lacked a
space before ryo. Empty-record tours had concealed this: ASCII dashes are much
narrower than the game's unchanged 12px digits.

`engine.RECORD_LAYOUT` checks and replaces **26 original MIPS instructions** in
OVLXTTL: the two Record headings move from x160 to x136, numeric fields and
placeholders start at x184, and time's three fields start at x184/214/244.
The native panel, digit writer, rank text, graphics, palettes and frame borders
are unchanged. Full Mastery ends at x128, Record at x167; the widest five-digit
points string ends at x274 inside the x280 inner edge. Money now includes the
space before ryo and ends at x275. Both copies of the empty score labels use
the full word **points** instead of **pts**.

The second renderer shares branches for all five formats, so the same checked
layout changes cover those branches too; only its four-digit branch is reached
by the six native Quick Match entries. Do not claim runtime proof for the
second renderer's other branches. Range checks allow only these explicit sites;
the existing verifier also requires built bytes to match insertion output.

`tests/test_record_layout.py` checks complete translated templates, maximum
numeric widths/gaps, revision guards and unchanged bytes outside the sites.

## Fresh read-only review (D10)

After the final build and all six tours completed, opened every sheet below in
a separate read-only pass. All 49 populated panels and 49 empty panels fit;
the original comparisons preserve numeric values and intentional blank record
pages. All game names, rank labels, units and frame edges are complete. Quick
Match's empty Name line remains intentional; entered-name rendering is untested.

| Sheet under `work/qa/records8_review/` | SHA-1 | Verdict |
|---|---|---|
| populated_sheet.png | 2fdd0451c9688708c13e654c0a0dc3201d1c8055 | ok, album 0-11 |
| populated_sheet_2.png | 1277cf9485a31ed2c4e06d1771dea1fe24f3c866 | ok, album 12-23 |
| populated_sheet_3.png | df49c2b0caced4d10a4e207a8064ba4b191e189a | ok, album 24-35 |
| populated_sheet_4.png | e6ebae587f74d60d63346e7a6abc8b309feb3907 | ok, album 36-42 |
| empty_sheet.png | bd084a6e8c1ab50d3a42dd2d87649b251951f14f | ok, album 0-11 |
| empty_sheet_2.png | b491e927fafa7d703e337396b7f55ba2400cd240 | ok, album 12-23 |
| empty_sheet_3.png | f847db2eee3dbb165c06e509226d1ffc4cd7b9e2 | ok, album 24-35 |
| empty_sheet_4.png | 418dd613476fda9e2a4e9e9a25ee378f84b2f161 | ok, album 36-42 |
| trial_sheet.png | a800e6b0203163415d654ed8335350e899f77f65 | ok, six populated Quick Match panels |
| trial_empty_sheet.png | 78440e3689ddf903866b07dc1e9db2e08a97dda9 | ok, six empty Quick Match panels |

The local manifest and `verdicts/review.tsv` pass **10/10**. These are deliberately
cropped panel verdicts; they do not approve minigame illustration lettering,
other menu modes or the phase-wide visual tour. Generate their sheets with
`sheet.py 'work/qa/records8_final/record_*.png' --compare work/qa/records8_original
--crop 32,176,256,48 --zoom 2 --cols 1 --max 12 --out <existing-dir>/populated_sheet.png`.
For empty panels, compare `records8_empty` against `records8_final`. For Quick
Match, use `trial8_final`/`trial8_original`, then `trial8_empty`/`trial8_final`,
with crop `32,160,256,64` and `--max 6`.

## Validation and continuation

- `tools/check.py`: **82 tests passed**, lint **0 errors**.
- `tools/verify_build.py`: **369 changed files**, **0 errors**.
- All four English tour textlogs: **0 Japanese lines**, four nonempty logs total.
- Cold smoke: `work/qa/records8_smoke`, **smoke ok**.
- Main disc: `build/momotarou-matsuri_en.bin`, **182,491,680 bytes**,
  **2026-11-01 07:51:14 UTC**, SHA-1 **3d7ddc6c7ae4442d2671dda01c40a9ef81da66b2**.

Rank Details, Name Entry, entered player names and natural game-to-record
progression remain open. Name Entry's top-level mode is `0x51`, native init
`OVLXTTL:0x800DF8A4`; its exit returns to Quick Match. Its atlas NAME0D:1 still
needs investigation, not just relabelled kana keys. The full corrected map
interaction tour, remaining signs/card illustration text and the other graphics
requirements in `docs/status.md` also remain open. **Do not advance to phase 9.**
