# Village memory banner, 2026-11-02

EVT220D's village banner now reads **Welcome!!** for ようこそ!!, closing
graphics-survey row #141. It has complete cold proof at three positions of
the natural event15 animation on both discs. A fresh D10 read-only pass
accepts six comparison sheets; this is one translated sign, not three
separate contexts. Phase 8 remains open.

## Source and preservation

`tools/gfx_welcome.py` assembles TIM 1 using ANM entry 3, item 1: source
rectangles `(0,0,184,128)`, `(0,128,80,72)` and `(80,128,80,56)` become a
264x128 picture. The first two rectangles join at picture x=184 through
the banner. The native sprites use page 7, 8bpp, CLUT (0,481) and unit scale.

An explicit paper-interior polygon removes the old lettering and its pale
fringe, preserving the shaded rim, all four tacks and posts. The complete
English uses the existing MIT `credits7.txt` font, with a one-pixel downward
step every 18 columns to follow the cloth's slope. It is scattered back
through the same native rectangles. No code, palette, geometry, layout or
script bytes change.

`tests/test_welcome.py` checks the assembly against the original ANM, alpha
preservation, every assembled pixel outside the paper interior, absence of
old colour fringes inside it, and consistency with the committed PNG.
The existing all-redraw test limits changes to the two source rectangles.
Whole-TIM duplicate expansion produces one PNG. Exact indexed-rectangle
searches across all archives find only EVT220D:1 for both affected regions:

```text
python -X utf8 tools/gfxfind_rect.py EVT220D.BIN:1 168 18 184 35
python -X utf8 tools/gfxfind_rect.py EVT220D.BIN:1 0 146 36 164
```

## Natural cold route and oracle

**Do not use `--click` on this route.** Circle skips event15 before the village
memory appears. The initial `welcome8_original` run did this and supplies no
banner approval. `welcome8_fixture_original` demonstrates assembly only and
is also excluded from the final evidence. The accepted route simply lets
the native animation run after the existing cold warp:

```text
python -X utf8 tools/gen_gfx.py --only EVT220D.BIN:1
python -X utf8 tools/build.py
python -X utf8 tools/debug/warp_all.py build/momotarou-matsuri_en.cue --out work/qa/welcome8_natural_en --only '^event15$' --hold 4800 --every 60 --probe tools/lua/textlog.lua --jobs 1
python -X utf8 tools/debug/warp_all.py --out work/qa/welcome8_natural_original --only '^event15$' --hold 4800 --every 60 --jobs 1
python -X utf8 tools/debug/welcome_qa.py build/momotarou-matsuri_en.bin work/qa/welcome8_natural_en/event15 --out work/qa/welcome8_en_oracle
python -X utf8 tools/debug/welcome_qa.py "rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).bin" work/qa/welcome8_natural_original/event15 --out work/qa/welcome8_original_oracle
```

The oracle reads the **named disc**, verifies its native geometry/page/CLUT,
and matches the complete 62x30 banner, including rim and tacks. It does not
use the generator's PNG as the expected output. The village moves diagonally
through the viewport, so requiring its entire 264x128 picture in a single
frame would reject the original too. No banner pixels are excluded.

| Frame | Original banner x,y | English banner x,y |
|---|---|---|
| 4380 | 171,30 | 172,29 |
| 4440 | 111,90 | 112,89 |
| 4500 | 51,150 | 52,149 |

Both runs pass with three complete matches. The one-pixel difference is the
native animation phase. Original BIN SHA-1:
`5d4768ed47341760d287ec08b37f5b62c5b8dc60`.
The negative check using the English BIN with original-run screenshots finds
zero complete matches (`work/qa/welcome8_rejected_stale`), rejecting stale
Japanese evidence rather than accepting any banner-shaped region.

## Fresh read-only review and validation

After final generation/build/cold runs, a fresh D10 self-review inspected
three full-screen comparisons at 2x and three corresponding 6x details,
English left and original right. All six are **ok**; the three details are
pixel-identical crops at different scroll positions. Verdicts and hashes
are in `welcome-banner-verdicts.tsv`; the scoped manifest is
`work/qa/welcome8_review/manifest.tsv` with `verdicts/fresh.tsv`.

Recreate the full sheets with the skill's `sheet.py EN --compare JP --zoom 2`.
For details use `--zoom 6` and crops `169,27,67,35`, `109,87,67,35` and
`49,147,67,35`, respectively. Then run `qa_gate.py init` and `qa_gate.py check`
on that manifest and verdict directory.

Main disc: `build/momotarou-matsuri_en.bin`, **182,449,344 bytes**,
**2026-11-01 17:44:05 UTC**, SHA-1
**c9b124f5f466d4e4473e081d68163e4385d72ea0**. Disc verification: **400 changed
files / 0 errors**. Cold `work/qa/welcome8_smoke` passed. English textlog:
**0 Japanese lines in 1 log**, excluding graphics. Full tests/lint and the
scoped visual gate are recorded in `docs/status.md`.

The snow placards, gold-prop mark and round game-hall emblem were inspected
again, with no confident reading gained and no pixels or verdicts changed.
Other graphics, full visual-manifest approval, NPC/story-state interactions
and natural minigame outcomes remain open. This route does not close phase 8
or authorize phase 9.

No shared skill files changed. Gotcha for `references/emulator-qa.md`:
automatic dialogue clicks can skip an event's unlabelled intermediate art;
run the event without input and inspect intermediate frames before assuming
that a static-survey graphic has no runtime consumer.
