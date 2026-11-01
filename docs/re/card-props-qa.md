# Card signs and costume emblems, 2026-11-01

Phase 8 remains incomplete. This pass translates **20 placements on 18
cards** and removes additional marginal-caption fragments on **five cards**.
All 100 cards again have complete cold screenshot coverage. The red Card
Album notice, older marginal-caption polish elsewhere, and the phase-wide
visual/story tour remain open.

## Content and boundaries

`tools/gfx_card_props.py` records each source reading, polygon, background/ink
colour, English text, drawing rectangle and orientation. It runs after the
existing caption and sound-effect stages in `gen_card_words.py`, from the
original TIM each time; committed PNG consistency tests cover all 100 cards.

| Cards | Original | Replacement |
| --- | --- | --- |
| 035 | 酒, on the helper's shirt | Sake |
| 062 | 千両, on the sword's price tag | 1000 ryo, aligned with the tilted tag |
| 068 | だんご, on the shop banner | Dumplings |
| 073 | ふぐ, across two curtain panels | Puffer / fish |
| 018, 048, 061, 097 | き, Kintaro's costume initial | K |
| 022, 042, 068, 072, 086 | び, Poverty God's costume initial | P |
| 006, 019, 025, 047, 077, 085 | 閻, Enma's crown mark | E |

The emblem initials retain the original single-character device; full names
in dialogue and captions are unchanged. K/P glyphs were added to the existing
MIT `hud7.txt` so they remain distinct in tiny badges. The full sign words use
the existing MIT condensed seven-pixel capitals. No palette, sprite, archive
membership, engine, save-format or image-dimension changes are made.

Only the explicit polygons and drawing rectangles may change. Crown erasure
also selects the red antialias fringe within two pixels; gold borders remain.
The curtain mask preserves every blue wave pixel even inside its erase
polygon. A new regression guards those pixels and the adjacent shirt collar,
price-tag edge, banner post, Kintaro's hand and badge outline. Existing tests
still check decoded pixels and packed TIM indices against allowed regions.

Enlarged review rejected early dark Sake/cloth fills, incomplete kana erasure
and indistinct narrow K lettering. The final masks use suitable original
palette backgrounds and complete stroke bounds. Marginal-caption erase
regions were widened on 028, 036, 045, 046, 081 and 099; only **028, 036, 046,
081 and 099** produce different pixels. The 045 expansion is a no-op, so this
pass makes no new claim of correcting that card. Some older caption fringes
on other cards (including 022, 085 and 086) still need polish; the new prop
verdicts do not approve them.

## Reproduce

```powershell
python -X utf8 tools/gen_card_words.py
python -X utf8 tools/build.py
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/card_props8_cold6 --script tools/debug/warp.lua --script tools/debug/cards.lua --script tools/lua/textlog.lua --var "SCENE='card_album'" --var HOLD=-1 --frames 900 --timeout 300
python -X utf8 tools/debug/cards_qa.py work/qa/card_props8_cold6 --out work/qa/card_props8_coverage6
python -X utf8 tools/debug/card_art_review.py --run work/qa/card_props8_cold6 --out work/qa/card_props8_review6/details --props
python -X utf8 tools/debug/card_art_review.py --run work/qa/card_props8_cold6 --out work/qa/card_props8_review6/cards --cards 6 18 19 22 25 28 35 36 42 45 46 47 48 61 62 68 72 73 77 81 85 86 97 99
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" init work/qa/card_props8_review6/manifest.tsv work/qa/card_props8_review6
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/card_props8_review6/manifest.tsv work/qa/card_props8_review6/verdicts
```

`--props` enlarges each original/cold-English prop pair with surrounding
borders. `--cards` selects complete-card comparisons; neither changes the
game. Cold album navigation still uses the native controller-driven loader,
with collectible bits seeded in RAM, and checks all 100 whole illustrations
and prefecture strips. Original cold evidence remains `cards8_jp_all3`.

## Validation and fresh read-only review

- `tools/check.py`: **102 passed**, lint **0 errors**.
- `tools/verify_build.py`: **369 changed files, 0 errors**.
- Cold smoke `work/qa/card_props8_smoke`: exit 0, smoke passed.
- Cold album `work/qa/card_props8_cold6`: exit 0; **100/100 complete cards**.
- `textlog.py`: **0 Japanese lines in 1 log**, excluding graphics.
- Fresh read-only D10 review: **9/9 scoped sheets accepted**, comprising five
  whole-card comparisons and four enlarged prop comparisons. Verdicts are
  `work/qa/card_props8_review6/verdicts/01_readonly.tsv`.

Main disc: **182,458,752 bytes**, built **2026-11-01 11:03:30 UTC**,
SHA-1 **1ff27c30c241edca355a724a9fce8e56d94f36cf**.

| Sheet | SHA-1 |
| --- | --- |
| cards/compare_sheet | `0c32b73acb3262ac3eae066414705f3166d701ad` |
| cards/compare_sheet_2 | `d354f33edc6275fe44fdc53e1c577be5d181a2ac` |
| cards/compare_sheet_3 | `d4eb5b04f795141a58bd2dd2785d7467d0599187` |
| cards/compare_sheet_4 | `565f0ea16112aeb4b89b558b1cd9d8e0cac150d4` |
| cards/compare_sheet_5 | `0ce9b4e86d69329ea41798bca7afbb740be4f49d` |
| details/compare_sheet | `257f97e8b7c84e2fd42b98a3c4a4e129615d3619` |
| details/compare_sheet_2 | `953127899eb8c69703db53c438b92541a5f4d36d` |
| details/compare_sheet_3 | `dcfcede324b19bce2a89498b17ac28f937ec6c7d` |
| details/compare_sheet_4 | `946018e908af4bdecc1c5ad8e2aba3e9f7c8ba89` |
