# Illustrated card margins, 2026-11-02

Thirteen of the fourteen outstanding card-margin findings are now accepted:
**007/026/033/039/044/054/075/079/082/087/093/094/098**. Card **063** is improved
but still rejected. The full-album gate has **19 ok / 1 issue** sheets; the
enlarged margin gate has **13 ok / 1 issue**. This does not complete phase 8.

## Changes

The old breadth-first caption fill copied nearby grey drawing edges into
letter-shaped gaps. The revised path is limited to eleven reviewed illustrated
margins. It retains grey components connected to unmasked artwork, preserves
the relevant blue/pink/yellow colours, and takes fill donors only from clean
paper or the relevant pale sky. Explicit fringe bounds exclude old ink that
touches a drawing through antialias pixels. Card087's grey sky fade is
reconstructed between clean columns 183 and 207 in the original palette;
the moon and the rest of the sky are unchanged.

Cards033/039 use stepped blank-paper bounds which stop before the bottle,
branch and leaves. Card093's caption moves from `(5,7)-(28,91)` to
`(0,20)-(12,108)`, clearing its original lettering separately and preserving
both falling leaves. The wording and font family are unchanged. The remaining
cards retain their text placement. Fourteen PNGs change; card063's change is
partial progress, not an accepted repair.

Regression checks compare actual original drawing pixels in seven illustrated
margins, both card093 leaves, card033's bottle and card039's lower leaf.
Separate blank-paper checks catch the old donor blocks and the final isolated
caption fragments. The existing all-card checks continue to enforce palette,
declared outer bounds, untouched number strips and generated-asset freshness.

## Review and rejected candidates

`card_repair8_candidate` through `candidate9` are static development comparisons,
not emulator approval. Earlier candidates left grey/pink antialias dots, copied
pale donor colours into bands, or made a white notch in the night sky. These
were rejected before the final source was built.

The first cold pass, `work/qa/card_repair8_cold`, used disc SHA-1
`58cae4b79098778acfbbb8da34e0645056766428`. A fresh read-only D10 pass reviewed
all fourteen enlarged margins. It found a brown remnant just outside card075's
right bound, a pale top fragment on card079, and card094's bottom stroke below
the old bound. These three findings were fixed and re-captured. Card063 remained
an issue. Do not use that first cold pass as the current build evidence.

The final pass uses `work/qa/card_repair8_final_cold`. All **13 changed whole-card
sheets** were inspected, including their other four cards; seven unchanged
whole-card hashes retain the accepted observations from `card-full-art-verdicts.tsv`.
All fourteen detail sheets were inspected. After the final three corrections,
only whole-card sheets **15/16/19** and details **075/079/094** changed; all six
were re-inspected. The remaining hashes match the reviewed earlier pass.
Exact verdicts and hashes are committed in `card-background-verdicts.tsv`.

## Remaining card063 finding

The broad lower grey donor bands are gone, but the original first kana overlaps
the top falling leaf at roughly `(182,4)-(199,17)`. Removing the caption still
leaves an incomplete lower/right leaf outline. Faint grey/pale fringe remains
near the upper/right caption, roughly `(197,18)-(208,35)` and around the adjacent
leaf. An explicit reconstruction/mask review is needed; a matching generated
sprite does not prove this artwork is correct. The existing final detail sheet
is the reproduction and negative visual evidence. No owner decision is needed.

## Reproduction

`<skill>` is the directory printed by `python tools/skill.py`.

```powershell
python -X utf8 tools/gen_card_words.py
python -X utf8 tools/build.py
python -X utf8 tools/check.py
python -X utf8 tools/verify_build.py
python -X utf8 <skill>/scripts/emu.py build/momotarou-matsuri_en.cue --out work/qa/card_repair8_final_smoke --route tools/routes/boot.txt --smoke
python -X utf8 <skill>/scripts/emu.py build/momotarou-matsuri_en.cue --out work/qa/card_repair8_final_cold --script tools/debug/warp.lua --script tools/debug/cards.lua --script tools/lua/textlog.lua --var "SCENE='card_album'" --var HOLD=-1 --frames 900 --timeout 300
python -X utf8 tools/debug/cards_qa.py work/qa/card_repair8_final_cold --out work/qa/card_repair8_final_coverage
python -X utf8 tools/debug/card_art_review.py --run work/qa/card_repair8_final_cold --out work/qa/card_repair8_final_audit --cards (1..100)
python -X utf8 tools/textlog.py work/qa/card_repair8_final_cold
```

The warp seeds collectible bits in RAM; the native controller/loader navigates
all 100 cards. This is not natural story-acquisition coverage. Full sheets show
original TIM left, cold English right at 3x. Detail sheets show cold English
left and cold original right at 6x, using original controls from
`work/qa/cards8_jp_all3/card_NNN.png`.

For each of the fourteen card numbers above (including 063), use `sheet.py`
with the final cold card PNG, `--compare` the original control, `--zoom 6`, and
`--crop 56,56,40,128` for cards044/075/082/093/094/098 or
`--crop 224,56,40,128` for the others. Output
`work/qa/card_repair8_final_details/cardNNN_sheet.png`; create the directory first.

## Validation

Final main disc: **182,449,344 bytes**, built **2026-11-01 17:14:04 UTC**,
SHA-1 **7015ad07c73b0721d0ab3526f2d4a26075088df2**.

- `tools/check.py`: **129 passed; lint 0 errors**.
- `verify_build.py`: **399 changed files; 0 errors**.
- Final cold smoke: passed.
- Final album: **100/100 complete captures**; **0 Japanese lines in 1 textlog**
  (graphics excluded).
- `qa_gate.py check work/qa/card_repair8_final_review/manifest.tsv work/qa/card_repair8_final_review/verdicts`:
  **19 ok / 1 issue**, no missing/stale verdicts or changed hashes.
- `qa_gate.py check work/qa/card_repair8_final_detail_review/manifest.tsv work/qa/card_repair8_final_detail_review/verdicts`:
  **13 ok / 1 issue**, no missing/stale verdicts or changed hashes.

Both visual gates intentionally exit 1 for card063. The red new-card notice,
remaining field/event/HUD graphics, and phase-wide dialogue/story coverage in
`docs/status.md` also remain open. Phase 9 has not started; no release was made.
