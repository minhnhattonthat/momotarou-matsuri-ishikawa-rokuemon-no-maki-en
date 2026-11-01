# Minigame labels and Rabbit-Turtle Race graphics, 2026-11-01

**Phase 8 remains incomplete.** This checkpoint covers six minigames' small labels,
the shared Race distance suffix, and all text assembled from the Rabbit-Turtle
Race font through its two text-bearing ANMs. It does not approve the remaining
graphics survey, every natural minigame outcome, or the phase-wide visual tour.

## Changes

| Atlas | Japanese | English |
|---|---|---|
| M050D:2 | 大当たり | Jackpot! |
| M060D:2 | れべる / よいしょ! / ほい! / まだまだ! / がんばれ! | Level / Heave! / Ho! / Not yet! / Go for it! |
| M080D:6 | リーチ! | One away! (matching Tanuki Slots) |
| M180D:3 | スカ | Miss |
| M230D:0 | ウサカメレース | Rabbit-Turtle Race |
| M500D:0 | スタート | Start |
| M990D:0 | 走 (after distance in metres) | Race |
| M230D:3, ANM 20 | 位 / コース / じかん / 当リ / 両 | . / Lane / Time / Hit / ryo |
| M230D:3, ANM 21 | 30 runner names | Full romanizations in `gfx/racers.tsv` and `glossary.md` |

Level 1's sprite contains its number; levels 2 and 3 use a 40-pixel word fragment
and a separate digit. The redraw touches only the shared word interior. All
three digits, speech-bubble borders/tails, sign borders, actor art, palettes and
animation timings remain intact. The slot-game's leaf at `(144,32)` is separate
art and is not part of リーチ!. The atlas duplicate sweep found no additional
byte-identical copies of the eight changed images.

## Sprite-built race text: the text logger's blind spot

The first English natural-menu capture still showed Japanese runner names even
though the main text log was clean. These are **not encoded strings**. M230D ANM
21 has 30 items, each assembling 8x8 glyph sprites from TIM 3. ANM 20 additionally
contains the five Japanese labels above and four punctuation/numeric symbols.
The whole-archive font-page reference sweep found no other users of kana text.

`gfx_racers.py` transcribes the original names from glyph UVs, checks them against
the TSV, and renders full names with the existing MIT `credits7.txt` pixel font.
The destinations at y=136..215 were transparent and unreferenced. Each English
name uses at most 50 pixels; tests enforce the standings budget including its
column separator. The compound names Kamenonarita and Kamenosugata retain every
syllable as single words, with no abbreviation. The original
font remains intact for punctuation, numeric sprites and any unused glyphs.

Only UV, dimensions and offsets change in ANMs 20/21. Counts, item tables, flags,
CLUTs, texture pages, scales and timing remain identical. Names retain their left
anchors; unused records sample transparent `(255,255)`. Seven original items store
their glyphs out of left-to-right order. The first implementation incorrectly
used the first stored glyph as its anchor; the enlarged natural standings review
caught Yoku Kame reaching the Lane column. The final implementation uses the
minimum glyph x/y, and tests require x=-24 for every name. Original ANM hashes:

- ANM 20: `f68f1b0842ad7453a6861ebcc66a61e96eedc270`.
- ANM 21: `27810d3328f186e8ba9fa4b0baf1a29b60a7d16f`.

Rank suffix 位 becomes a baseline dot, giving numbered-list notation such as
`1.` and `2.` instead of a single ordinal suffix reused for every number. Other
small labels keep their original anchors; the multiplication, equality, dash and
colon records are untouched. The verifier accepts only these pinned edits.
The one-pixel rank dot initially matched an unrelated panel corner in the
whole-screen oracle. `announcements_qa.py --region` now confines these five tiny
label checks to the first runner row. A regression test rejects the corner;
the accepted dot capture is at `(106,104)` and agrees with the visible list.

## Reproduce

Run each step separately and check its exit code before continuing:

```powershell
python -X utf8 tools/gen_gfx.py --only M050D.BIN:2 M060D.BIN:2 M080D.BIN:6 M180D.BIN:3 M230D.BIN:0 M230D.BIN:3 M500D.BIN:0 M990D.BIN:0
python -X utf8 tools/build.py
python -X utf8 tools/debug/minigame_labels.py --original --out work/qa/labels8_jp
python -X utf8 tools/debug/minigame_labels.py --out work/qa/labels8_final4
python -X utf8 tools/debug/minigame_labels_review.py work/qa/labels8_final4 --out work/qa/labels8_review2
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" init work/qa/labels8_review2/manifest.tsv work/qa/labels8_review2
```

The runner checks every requested ANM item against its complete opaque pixels,
with explicit texture selection. Its case table is the reproducible fixture
specification. `--check-only` reruns the pixel gates without emulation. Review
sheets contain all matched items, never a sample; the review helper creates no
verdicts.

`sprite_fixture.lua` now allows source and target to be the same ANM. It caches
all original offsets before editing and restores them at completion. This lets
all 30 runner names cycle through the **real list positions** without changing
gameplay data, score, palettes or geometry. Several visible rows intentionally
show the same name during the fixture; normal menus retain distinct identities.

### Fixture limits and rejected attempts

- M05 substitutes the backdrop; its black background is intentional.
- M06 uses the paused renderer to keep natural speech from covering the test
  speech. The initial actor fixture matched only 4/7 original states and was
  rejected; the paused fixture covers all seven.
- M08 substitutes the Game Start item, using frame scanning. The initial actor
  substitution overlapped repeated labels, the backdrop substitution was hidden
  by the slot actors, and Start did not open a pause menu. All three attempts
  were rejected. The final start-cue substitution preserves the source sprite
  geometry but does not prove natural near-win timing or positioning.
- M18 and M50 substitute actors. Miss is legible at the gate edge in this fixture;
  natural miss positioning and the natural Start cue remain wider QA work.
- The race title and shared Race suffix are on the natural menu. Names cycle
  through normal list slots; small race labels borrow those slots for assembly
  proof. Fixtures alone do not establish the labels' normal result-screen fit.

### Natural race route

`tools/debug/race.lua` uses only controller input after the cold warp. It selects
distinct runners, confirms, watches the race and advances the result screens.
There are no score, movement, RNG or outcome edits.

```powershell
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/race8_english_final2 --script tools/debug/warp.lua --script tools/debug/race.lua --script tools/lua/textlog.lua --var "SCENE='game_m23_19'" --var HOLD=10000 --frames 900 --shot-every 120 --sheet --timeout 180
```

Run the same command on the original CUE into `work/qa/race8_original`. Random
runner lineups, distances and outcomes can differ between cold boots. Compare
the screen states and behavior, not identical results or frame numbers.
After the result/insufficient-money dialogue, **both discs return to mode 0x61's
original Play Station System Menu**. This is the direct game-warp return context,
not a translation defect or proof of a normal story-mode return.

## Validation and read-only review

Final build: `build/momotarou-matsuri_en.bin`, **182,496,384 bytes**,
**2026-11-01 05:21:18 UTC**, SHA-1
`4ca27d7a3651f537adcaf74d27d913cc7d7dd992`.

- `tools/check.py`: **64 tests passed, lint 0**.
- `tools/verify_build.py`: **363 changed files, 0 errors**.
- Cold smoke `work/qa/labels8_final4_smoke`: passed.
- Final English `work/qa/labels8_final4` and original `work/qa/labels8_jp`:
  **48/48 complete sprite states each**, all nine case gates passed.
- English fixture textlog: **0 Japanese lines / 0 markers in nine logs**.
  Natural race textlog: **0 Japanese lines / 0 markers in one log**.
  These counts exclude graphic lettering.
- Fresh read-only review under D10, after the final cold runs: **10/10 scoped
  sheets accepted**, including the fixed natural standings. `qa_gate.py check`
  uses `work/qa/labels8_review2/manifest.tsv` and its `verdicts` directory.

| Sheet | Verdict | Final SHA-1 |
|---|---|---|
| context_sheet | ok | `75a8ac7e52c2fed61a234d725dc32dd1991c7011` |
| context_sheet_2 | ok | `d34b86b18a57d62a9b1cc808d5939b4aa86d6d3b` |
| context_sheet_3 | ok | `f80046db81c77306d348fc865d52ef59386b8672` |
| labels_sheet | ok | `7d9a8dd998e7f015b7ff13f9f03b370f0981513d` |
| labels_sheet_2 | ok | `313e5c26e0f8f667de41bb09073451352d352959` |
| natural_sheet | fixed | `82ee0ec4f495a0ea502588abbf33a615fbf3959c` |
| natural_sheet_2 | ok | `0add1cb0ae4ba8b1967b234e25408571215767d1` |
| racers_sheet | ok | `809e63d0f51390305278f96253d18292fb085ed6` |
| racers_sheet_2 | ok | `34e20730a67d244954a7a6c0dc27ba3c1650498a` |
| racers_sheet_3 | ok | `7ea73e44c9163363c20775809fc797b0f33ccbbd` |

The original issue verdict is retained alongside the final fixed verdict.
The earlier six-case manifest is named `manifest.superseded.tsv` and is not a
current release gate. No shared skill files were modified.

Gotchas for `references/graphics.md`: a font atlas can contain whole strings
assembled by ANM glyph records, invisible to Shift-JIS scans and text hooks.
For `references/emulator-qa.md`: repeated actor substitutions can overlap test
labels; a successful emulator exit is not evidence that a complete sprite was
visible, and the same-game original fixture must pass its own coverage check.
