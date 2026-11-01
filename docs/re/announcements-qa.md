# Shared announcements and award QA, 2026-11-01

**Phase 8 remains incomplete.** This checkpoint covers M990D:1's shared announcements and the five
M010D:4 awards. It does not approve the full graphics survey, remaining minigame outcomes, or full tour.

## Changes

- `tools/gen_gfx.py` redraws New Record, Level Up, Full Mastery, Game Start, Good Work, Pause, Draw and
  Finish in M990D:1. Level 1 replaces 初; levels 2-9 keep their original numerals. The level suffix is
  redundant with the translated header. Existing palette variations are preserved.
- Good Work spans two atlas rectangles. Pause's top and bottom halves are stored side-by-side.
  `COMPOSITES` letters these in screen space, then scatters the pixels into the original rectangles.
- Game Start originally borrowed a dash from inside another word. A pixel-only attempt produced uneven,
  tiny lettering and was rejected. `tools/gfx_layout.py` checks and changes **26 u16 fields** in M990D:3:
  eight fields join/centre Game Start and replace the borrowed dash with a transparent texel; eighteen
  centre each level number and its exclamation. Counts, offsets, scales, palettes, timing and code remain.
  The verifier requires the exact approved ANM bytes, not a broad exemption for animation entries.
- M010D's Perfect had a duplicated exclamation: its ANM adds a separately stored `!` to the main banner.
  The original cold screenshot confirmed one exclamation. The main redraw now says `Perfect`.
- Tests protect other sprite fields, reject corruption of unrelated items/palettes, constrain redraws
  to declared rectangles, and reject screenshots with even one missing letter pixel.

## Runtime evidence and limits

`tools/debug/announcements.lua` cold-warps to Janken, presses Start, and changes only the RAM offset
for the pause label's ANM item. The game renders the selected original item with its own UVs, dimensions,
palette and anchors. There is no injected image or patched rendering code. This proves display/assembly,
not whether a player earned a particular score or rank. The Lua is not part of the built disc.

The same fixture can point to another **already loaded** archive's ANM item. M010's five awards all work.
M03/M14/M56/M59 attempts did not pause at the right time: they stayed in dialogue or changed mode.
Their exit-0 exploratory runs are **not** accepted evidence. In particular, `awards8_m03`, `awards8_m14`,
`awards8_m56`, `awards8_m56_early` and `awards8_m59` remain unapproved. Other loaded palettes are not
automatically interchangeable; inspect each item on its actual minigame background.

`tools/debug/announcements_qa.py` compares every opaque glyph/outline pixel with the built ANM/TIM data,
allowing 8 RGB levels for PS1 palette expansion. It rejects blank templates and missing/obscured lettering.
The paused object overrides ANM blend bits (EXE 0x8001B66C..0x8001B6A4); other unsupported flags/scales
remain errors. The oracle supplements visual review, not translation review.

- Shared pause fixture: **15/15** items. The sixteenth, Full Mastery, was partially covered by the pause
  choice window; the oracle correctly rejected it. The accepted fixture sheet excludes that shot.
- Full Mastery: **1/1** on `announcements8_mastery/f007980.png`, using the ordinary Janken input route
  with only its level-up draw selector redirected to item 10. This does not change the saved score/rank.
- M010 awards: **5/5** complete items on the final build. The oracle rejected the earlier duplicate-!
  screenshot after the redraw changed, then accepted the fresh run.
- Natural Janken completion: `announcements8_final_natural`, level-up, completion text and replay menu.
- Original comparisons: `announcements8_jp_fixture`, `awards8_m01_jp`; earlier natural Janken original
  route remains at `work/qa/janken_route_jp_final`.

## Reproduce

```powershell
python -X utf8 tools/gen_gfx.py
python -X utf8 tools/build.py
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/announcements8_final_fixture --script tools/debug/warp.lua --script tools/debug/announcements.lua --var "SCENE='game_m11_0d'" --var ANNOUNCEMENTS=true --var HOLD=5000 --frames 900 --shot-every 300
python -X utf8 tools/debug/announcements_qa.py work/qa/announcements8_final_fixture --out work/qa/announcements8_coverage --items 1,2,3,4,5,6,7,8,9,11,13,14,15,16,18
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/announcements8_mastery --script tools/debug/warp.lua --script tools/debug/janken.lua --script tools/debug/announcements.lua --script tools/lua/textlog.lua --var "SCENE='game_m11_0d'" --var ANNOUNCEMENTS=true --var 'ANNOUNCEMENT_REPLACE={from={1,2,3,4,5,6,7,8,9},to=10}' --var HOLD=7000 --frames 900 --shot-every 60
python -X utf8 tools/debug/announcements_qa.py work/qa/announcements8_mastery --out work/qa/announcements8_mastery_coverage --items 10 --scan
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/awards8_m01_final --script tools/debug/warp.lua --script tools/debug/announcements.lua --var "SCENE='game_m01_03'" --var ANNOUNCEMENTS=true --var ANNOUNCEMENT_MODE=3 --var ANNOUNCEMENT_PAUSE=2500 --var ANNOUNCEMENT_CLICKS=true --var 'ANNOUNCEMENT_SOURCE={file=294,entry=18,items={0,1,2,3,4}}' --var HOLD=5000 --frames 900 --shot-every 300
python -X utf8 tools/debug/announcements_qa.py work/qa/awards8_m01_final --out work/qa/awards8_m01_coverage --file M010D.BIN --entry 18 --items 0,1,2,3,4
```

For an unmodified natural completion, omit announcements.lua and its globals; keep janken.lua, textlog.lua,
the scene and HOLD=7000. Fixture runs finish themselves and can have no `final.png`; their named captures
and coverage gate are the evidence. They are not substitutes for the separate cold smoke.

## Fresh read-only verdicts (D10)

After the final fixes, all six enlarged sheets were read again without modifying source or art. Scope:
legibility, missing fragments, palettes, clipping, surrounding artwork and completion route progression.
Entering/exiting banners cross the screen edge in the original animation; complete in-bounds frames are
present as well. The first 15 shared fixture items are pixel-identical between the last two builds; the
last rebuild changed only M010's award pixels. Mastery and M010 were captured on the final disc.

Manifest: `work/qa/announcements8_review/manifest.tsv`; verdicts: `verdicts/review.tsv` beside it.

| Sheet | SHA-1 | Verdict |
|---|---|---|
| fixture_sheet | 226a9d2d77c3822e6b58c88fefee85a80c6391f4 | ok |
| fixture_sheet_2 | fcc38c17edbc9ccef6ea8ba8441926403dc2a493 | ok |
| awards_sheet | 0dd09f51770b1108d2194b3db3e636fca33d5fa1 | ok |
| natural_sheet | 1056d983383da6aa32b5f32e289296f6332ce04a | ok |
| natural_sheet_2 | e21a4d0245d07a7f2a5f8743d236561c33fe5289 | ok |
| mastery_sheet | 9ada95e603c2e824d9d960e6966230a97236c816 | ok |

## Validation and handoff

- `tools/check.py`: **48 passed**, text lint 0 errors.
- `tools/verify_build.py`: **352 changed files, 0 errors**.
- Shared/natural/mastery textlogs: 0 Japanese lines and 0 markers.
- Final cold smoke: `work/qa/announcements8_release_smoke`, exit 0, smoke ok.
- Disc: `build/momotarou-matsuri_en.bin`, **182,564,592 bytes**, **2026-11-01 02:34:07 UTC**.
- SHA-1: **c84d1a018c9649a1468efa45564c88475b4e4cb8**.

Next: remaining M990D:0 words and minigame outcomes, then the menu/cards/signs/ending-art survey, captions,
nine hanging-map routes and complete visual tour. Phase 8 cannot advance to release on this scoped gate.
No owner-only decision is blocking. The skill was not edited.

Skill gotchas for `references/graphics.md`: a word can borrow a glyph from another word's source rectangle;
inspect ANM before redrawing. For `references/emulator-qa.md`: Start may be ignored during dialogue, and
pause windows can cover the target banner; require complete-pixel coverage rather than emulator exit 0.
