# Character introductions (phase 8)

The five attract-mode name labels are English, with natural cold-boot proof.
This closes the **name-label** part of survey rows #1 and #2, not phase 8 or the
Japanese emblems in the character illustrations.

## Layout and translation

`CHR0D.BIN:1` contains Momotaro's 88x32 name sprite at (120,208).
`CHR0D.BIN:2` contains Kintaro (0,192,88,32), Urashima (200,184,56,32), and
Ishikawa Rokuemon (88,216,168,32). Full names follow `glossary.md`. Urashima uses
the condensed rounded font to fit the original narrow sprite, without abbreviation.

Yashahime is **one name assembled from three pieces**, not two independent
copies of the word. ANM entry 8 item 1 places these in an 88x32 canvas:

| Atlas rectangle (x,y,w,h) | Canvas position |
|---|---|
| 0,224,88,16 | 0,0 |
| 88,200,80,16 | 8,16 |
| 0,240,8,16 | 0,16 |

`gen_gfx.py` letters the assembled name and scatters it back into those three
rectangles. The regression test reconstructs it and checks equality with the
unfragmented English draw. It also renders every complete character before and
after and requires identical pixels. All ANM data, palettes, character artwork,
timings and positions remain unchanged. The archive-wide duplicate scan finds
only these two affected TIMs.

## Reproduction and runtime oracle

```
python -X utf8 tools/gen_gfx.py --only CHR0D.BIN:1 CHR0D.BIN:2
python -X utf8 tools/build.py
python -X utf8 tools/debug/character_intro.py --out work/qa/names8_final
python -X utf8 tools/debug/character_intro.py --original --out work/qa/names8_original
```

`character_intro.py` lets the game run untouched for 9,600 frames and captures
every 60 frames. It uses `emu.py` only, with no save, controller input, RAM
fixture or renderer substitution. The title automatically enters the character
introductions at about frame 6,300. The complete name and complete character
must both match their own ANM item in the **same screenshot**.

Final English run: `work/qa/names8_final`, **5/5 pairs**. Original reference:
`work/qa/names8_attract_jp`, **5/5 pairs**, an exploratory 18,000-frame run with
180-frame captures; the same `--check-only --original` oracle verifies it. The
later minigame-demo frames from that original run are not approved by this pass.
Both cases use the original `CHR0D` ANM entries 5 through 9, item 0 for the
character and item 1 for the name.

The text probe emits no text log during these introductions. Thus “0 Japanese
lines in 0 logs” is **not** evidence of text coverage or absence of graphic text.
The pixel oracle and direct visual inspection provide the name-label evidence.

## Fresh read-only verdicts (D10)

Reviewed all five complete 2x comparison sheets after the final build. English
is on the left; an independent cold original capture is on the right. Full
names fit without overlap or clipping, retain their original colour and dark
outline, and remain clear of the characters. Yashahime has no seam or leftover
Japanese fragment. Urashima is smaller than the other labels but readable.

| Sheet | Frame | SHA-1 | Verdict |
|---|---|---|---|
| momotaro_sheet | 6660 | 684539dde6b67162f4b2400a19e4ad46831c01bc | ok, complete label and character |
| kintaro_sheet | 7200 | 9d7f602c6722b1c86a7e502c35fe14b8b2b8302f | ok, complete label and character |
| urashima_sheet | 7740 | 1e7cb3d7e45ac316909dc15d639d427cfdf8ceb1 | ok, full narrow label, legible |
| yashahime_sheet | 8280 | da5f4665f4e70f35a1b5585cff7e565d68f655c2 | ok, three pieces join cleanly |
| rokuemon_sheet | 8640 | d36933b0b3a1b06b84f57800b404056fca02b3c5 | ok, full Ishikawa Rokuemon fits |

`qa_gate.py check work/qa/names8_review/manifest.tsv work/qa/names8_review/verdicts`
passes **5/5 sheets**. Recreate comparisons with `sheet.py` using each English
`f<frame>.png`, `--compare` the same original frame, and `--zoom 2`; create the
output directory first. This is a scoped name-label verdict, not a whole-image
Japanese-text approval: Kintaro's and Urashima's festival fans remain Japanese,
and Rokuemon's costume marks still need classification under D5. The survey
previously failed to identify those marks explicitly.

## Build and remaining gates

Main disc and `build/names8.bin` are identical: **182,494,032 bytes**, built
**2026-11-01 06:57:03 UTC**, SHA-1
`3f33c5f80f72f7b7288ca70c74a417f49c46b85c`.
Disc verification: **369 changed files / 0 errors**. Cold boot smoke at
`work/qa/names8_smoke` passes. The complete test/lint result is in `docs/status.md`.

Phase 8 still lacks the full visual manifest and many graphics/story-state
routes. Name entry, the four small GCV0310 name tags, card illustration text,
remaining town signs and fan/costume marks are separate outstanding work.
Do not advance to release on these five verdicts.

Skill gotcha for `references/graphics.md`: apparent repeated lettering in an
atlas may be the top and bottom of **one** sprite; reconstruct all ANM records
before drawing. For `references/emulator-qa.md`, waiting through the untouched
title attracts can provide natural coverage without a RAM fixture. No shared
skill files were changed.
