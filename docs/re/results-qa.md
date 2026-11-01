# Shared winner and ordinal banners, 2026-11-01

**Phase 8 is incomplete.** This checkpoint translates 40 shared M990D result states. It does not approve
the remaining small HUD glyphs, minigame-specific outcomes, card illustrations, signs or full visual tour.

## Implementation

`tools/gfx_results.py` assigns dedicated atlas rectangles to English words in M990D:0. The Japanese
layout reused parts of names (including the shared 太郎 in Momotaro/Kintaro) and ordinal suffixes;
painting English over those fragments would break another result. The English layout instead assembles:

| M990D ANM entry 3 items | English |
| --- | --- |
| 21-30 | Round 1! through Round 10! |
| 31-34 | Momotaro, Kintaro, Urashima or Yashahime wins! |
| 35-37, 51 | Momotaro and Urashima / Kintaro and Yashahime / Momotaro and Red Oni / Kintaro and Blue Oni win! |
| 38-39 | Win! / Lose! |
| 41-50 | Try 1! through Try 10! (the original 本目 attempt counter) |
| 61-70 | Question 1! through Question 10! |

- `gfx_layout.py` applies **743 checked u16 geometry edits**, in addition to the earlier 26 announcement
  edits. The original ANM SHA-1 must equal `f68f9b95c19678d6caaeefd5c3d34e36ccb8616c`.
- Changes are limited to UVs, dimensions and positions. Record counts, animation tables, flags, CLUTs,
  texture pages, scales and all unrelated items are preserved. Surplus records sample a transparent texel.
- Ordinals put the label before the number. Paired winners use plural `win`; individual winners use `wins`.
  Full glossary names fit without abbreviations. The longest line is 224 pixels, within the 320-pixel screen.
- Atlas allocation reuses only the old large-letter regions. Tests scan **every other archive's ANM tables**
  for references to those page-27 pixels, and find none. They also guard non-result sprites in M990D, word
  overlap, permitted pixel ranges, counts, English word order and unrelated animation fields.
- The original palette indices and committed OFL Fredoka font provide the lettering. No palette, engine
  code, disc loading behaviour or shared skill file changed.
- `python -X utf8 tools/gfx_results.py` regenerates this unique atlas alone; `gen_gfx.py` regenerates it as
  part of the normal complete graphics pipeline. The complete duplicate scan found only M990D:0.

## Cold-boot evidence

The existing `announcements.lua` fixture enters Janken from a cold boot, pauses with the controller and
redirects the pause item's RAM selector to each real result item. It does not inject pixels or replace
the rendering code. Each item's own geometry and palette pass through the game renderer. These shots
prove assembly and legibility; they do not prove the player earned every outcome in its original minigame.

```powershell
python -X utf8 tools/gfx_results.py
python -X utf8 tools/build.py
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/results8_fixture --script tools/debug/warp.lua --script tools/debug/announcements.lua --script tools/lua/textlog.lua --var "SCENE='game_m11_0d'" --var ANNOUNCEMENTS=true --var 'ANNOUNCEMENT_SOURCE={file=350,entry=3,items={21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,41,42,43,44,45,46,47,48,49,50,51,61,62,63,64,65,66,67,68,69,70}}' --var HOLD=-1 --frames 900 --timeout 180
python -X utf8 tools/debug/announcements_qa.py work/qa/results8_fixture --out work/qa/results8_coverage --items 21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,41,42,43,44,45,46,47,48,49,50,51,61,62,63,64,65,66,67,68,69,70
```

The oracle found **40/40 complete items**, comparing every opaque glyph/outline pixel to the built
ANM/TIMs. Original reference: the same fixture on the original CUE in `work/qa/results8_original`.
The paired-winner reference confirms names and singular/plural meaning. Full-frame checks include
the scoreboard, pause question and choices; the new banners do not obscure those controls.

An extra natural route (`game_m51_2f`, CLICK=60, HOLD=6000) reached the History Quiz Oni's one-question
encounter, chose the first answer, lost and returned to the story. It **did not exercise the question-counter
banners** (the image oracle found 0/10) and is not counted as their coverage. Its text log contains no Japanese. Natural round/attempt/
question progression in the minigames that use these banners remains part of the wider phase-8 tour.

## Fresh read-only review (D10)

After the final redraw and cold build, all four enlarged fixture sheets and the full-frame context sheet
were read without editing art or implementation. Round/attempt/question numbering, full names, paired
grammar, legibility, palette, clipping and surrounding UI pass. Original paired-winner shots were compared
separately. Scope is only the 40 listed banners, not every Japanese element elsewhere in the game.

Manifest: `work/qa/results8_review/manifest.tsv`; verdicts: `verdicts/review.tsv` beside it.

Regenerate the scoped sheets after creating the output directory:

```powershell
New-Item -ItemType Directory -Force work/qa/results8_review | Out-Null
python -X utf8 "$(python tools/skill.py)/scripts/sheet.py" 'work/qa/results8_fixture/announcement_*.png' --crop 32,80,256,88 --zoom 2 --max 12 --cols 3 --out work/qa/results8_review/fixture_sheet.png
python -X utf8 "$(python tools/skill.py)/scripts/sheet.py" work/qa/results8_fixture/announcement_21.png work/qa/results8_fixture/announcement_35.png work/qa/results8_fixture/announcement_70.png --zoom 2 --cols 3 --out work/qa/results8_review/context_sheet.png
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" init work/qa/results8_review/manifest.tsv work/qa/results8_review
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/results8_review/manifest.tsv work/qa/results8_review/verdicts
```

| Sheet | SHA-1 | Verdict |
| --- | --- | --- |
| fixture_sheet | 99287257fadd8bd1ae6fa80924b062ba3a4dc3dc | ok |
| fixture_sheet_2 | 458a725fb8c77c02afdd83b9c8954a34feecc0c1 | ok |
| fixture_sheet_3 | 0e5775d2139abe631ebc8cbebf07d1e6ed53e826 | ok |
| fixture_sheet_4 | 6ddbd176fba22f44b6f453038e04d7f3cc2e7bca | ok |
| context_sheet | 433e066e62aabac4a31366fd6d587df21eb29333 | ok |

## Validation and remaining work

- `tools/check.py`: 54 tests passed; lint 0 errors.
- `tools/verify_build.py`: 363 changed files, 0 errors.
- Cold smoke: `work/qa/results8_smoke`, passed.
- Fixture textlog: 0 Japanese lines; graphics are outside the logger's detection.
- Disc: `build/momotarou-matsuri_en.bin`, **182,496,384 bytes**, **2026-11-01 03:39:19 UTC**,
  SHA-1 **2423760e259876a8dfce16a26db5ca994aa7557b**.

Still open: M990D small HUD words/counters, M03/M14/M56/M59 outcome coverage, card illustration lettering,
town signs, remaining graphics/menu variants, full visual manifest, captions and nine hanging-map routes.
No owner decision blocks these tasks; phase 8 cannot advance to release on this scoped gate.

The red Card Album notice was investigated but not changed: no duplicate of its distinctive glyph rows
was found by `gfxfind.py HOUGEN0D.BIN:0 232 160 256 184`, and the album's two ANMs do not reference its
fragments. Its actual runtime draw path remains unproven; no unused-asset exemption is inferred.

Skill gotcha for `references/graphics.md`: when repacking a shared atlas, scan ANM users in **all archives**,
not only the atlas's own file; shared kanji fragments need dedicated English word storage and layout edits.
