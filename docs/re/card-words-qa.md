# Marginal dialect-caption QA, 2026-11-01

Phase 8 remains incomplete. This checkpoint localizes the brown marginal phrases on all 100 dialect cards.
It does **not** approve the black illustration sound effects, signs, clothing emblems or the whole card artwork
as fully English. Those still need individual redraws. The fragmented red Card Album notice also remains open.

## Implementation

- `gfx/card_words.tsv` holds all 100 English phrases and their declared rectangles in the original 208x128
  illustration. `tools/gen_card_words.py` regenerates them from original TIMs, preserving the translated
  prefecture strips. `tools/gen_gfx.py` invokes it after the existing redraws; standalone regeneration works too.
- English runs clockwise down the same margins, using the committed OFL Fredoka font and the card's own
  brown palette colour. A one-pixel white keyline separates it from adjacent illustration strokes. No palette,
  ANM, code, caption-number or image-dimension changes are required.
- Plain-paper caption regions are cleared to their original white. On illustrated backgrounds, a bounded
  brown-ink mask plus a two-pixel antialias fringe is filled from nearby unmasked pixels. Card 39's leaves and
  card 69's diagonal three-column caption require multiple erase rectangles; one large rectangle damaged
  surrounding art and was rejected. Card 38's margin was narrowed to preserve the adjacent character, and
  card 59's to preserve the small figure's staff.
- The full-card comparison then caught broad clears clipping card 10's bottle, card 49's tail, card 80's
  club and card 100's hair. Narrower erase/draw regions restore those props; a dedicated regression test
  requires those original pixel rectangles to remain byte-identical. Card 20's grass was checked as well.
- Regression checks cover both TIM indices and decoded pixels outside the declared regions. All 100 card
  numbers stay byte-identical. The screenshot oracle rejects an old Japanese illustration even when its
  prefecture caption is English. Existing whole-card coverage still checks every opaque illustration pixel.
- The 100 card TIMs are unique in the archive duplicate sweep used by `gen_gfx.py`; there is no second copy
  of these illustrations to patch. No shared skill file was changed.

## Translation review

The game's own 100 gloss pointers, exposed by `cards_qa.py` in `coverage.tsv`, provide the meanings. Phrases
use concise conversational equivalents: “Two peas in a pod!”, “Knock one back!”, “All thumbs!” and “Noggin!”.
They do not assign specific English regional accents to Japanese prefectures. Prefecture spellings remain
unchanged from the previous caption checkpoint.

Card 001 is an original inconsistency: its art says `なまら あっつぃべゃぁ` and depicts heat/fanning, while its
gloss says `すごくムカツク`. The art is now “It's scorchin'!”; the previously translated runtime gloss remains
“Really ticks me off”. This pass does not silently rewrite the source-game gloss. Reconcile this documented
source mismatch in polish if desired; it is not a new pointer-order or screenshot-ID error.

## Reproduce

```powershell
python -X utf8 tools/gen_gfx.py
python -X utf8 tools/build.py
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/words8_final4 --script tools/debug/warp.lua --script tools/debug/cards.lua --script tools/lua/textlog.lua --var "SCENE='card_album'" --var HOLD=-1 --frames 900 --timeout 300
python -X utf8 tools/debug/cards_qa.py work/qa/words8_final4 --out work/qa/words8_coverage4
python -X utf8 tools/debug/card_words_review.py work/qa/words8_final4 --out work/qa/words8_review
python -X utf8 tools/textlog.py work/qa/words8_final4
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" init work/qa/words8_review/manifest.tsv work/qa/words8_review
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/words8_review/manifest.tsv work/qa/words8_review/verdicts
```

`card_words_review.py` uses the skill's `sheet.py` for cropping, rotation and zoom. Its five sheets show only
the marginal phrases, turned horizontal for reading. Their scoped verdicts must never be treated as whole-card
approval. Original cold-boot reference remains `work/qa/cards8_jp_all3`; prior runtime details are in
[cards-qa.md](cards-qa.md). Full-card comparison sheets from final3 are retained under
`work/qa/words8_full_review`; the five corrected final4 cards are in `work/qa/words8_props_final_compare.png`.

## Fresh read-only review (D10)

The initial read-only pass found background strokes blending into captions 007, 026, 075 and 093. The first
verdict file records these issues. A white keyline was added, and the disc and cold tour were regenerated.
All 100 captions were read again after the keyline change. A separate whole-card comparison caught the
four clipped props described above. Final4 was rebuilt and cold-booted after those corrections; all changed
caption sheets and corrected full cards were rechecked. All five scoped sheets pass, with final verdicts in
`work/qa/words8_review/verdicts/final.tsv`. Japanese illustration SFX are explicitly outside that approval.

| Scoped sheet | Cards | Final SHA-1 |
| --- | --- | --- |
| phrases_sheet | 001-020 | d0010bf671f5655017c26a63d885c6cf684eff2b |
| phrases_sheet_2 | 021-040 | 41e5fd14a2ee49758c8c960ff594d5ab61ebb5b8 |
| phrases_sheet_3 | 041-060 | 182efad448ea803a07f7199b7c29bd3dd14c2381 |
| phrases_sheet_4 | 061-080 | b27af1bef32764a88832c798d27dc389d97be17b |
| phrases_sheet_5 | 081-100 | 977dfa38dbcd0c3a9cd9e8cc75f47b792a77222e |

Final validation: `tools/check.py` **52 tests passed**, lint **0 errors**; `verify_build.py` **363 changed files,
0 errors**. Cold smoke `work/qa/words8_smoke4` passed. The complete final4 card oracle found **100/100** captures,
no missing cards; textlog found **0 Japanese lines** (graphics are not detected by that log).

Verified disc: `build/momotarou-matsuri_en.bin`, **182,503,440 bytes**, **2026-11-01 03:25:16 UTC**,
SHA-1 **f7b8c56da2e6026b7d154cb3a8496b0806e3f60b**. Phase 8 is still incomplete.

## Remaining phase 8 work

- Card illustration SFX and signs, including the embedded shop banners; clothing insignia need explicit
  classification under D5. No exemption for them is inferred from the title-logo exception.
- Locate the runtime drawing of the red Card Album notice. Its fragments are visible in HOUGEN0D:0,
  but HOUGEN0D ANM entries 5/6 do not reference them; the simple ANM selector is insufficient evidence.
- The existing minigame outcome/HUD gaps, menu/record categories, remaining graphics survey, captions,
  nine hanging-map routes and complete visual tour remain open. Do not advance to phase 9.

Skill gotcha for `references/graphics.md`: a colour-based text mask can select a nearby character outline or
prop in the same brown; use explicit narrow regions and compare the surrounding art, then test legibility
on actual cold-boot screenshots. A clean image-import test cannot detect visual merging with background art.
