# Card063 final margin repair, 2026-11-02

Card063's remaining margin finding is fixed. The cold full-album gate is now
**20/20 accepted sheets**, with the enlarged card063 comparison also accepted.
This closes the card-background artwork findings, not phase 8 or the separate
red new-card notice investigation.

## Correction

`gen_card_words.repair_card63` clears reviewed sky windows without overwriting
their pale blue pixels. It removes the isolated grey/yellow antialias remnants
which survived the warm-ink mask. A two-tone, original-palette lower contour
reconstructs the top falling leaf where the Japanese first kana covered it.
Its upper and left edges remain original. The caption wording, position,
prefecture strip, other illustrations and 99 other cards are unchanged.

The first static candidate still retained a curved fringe to the right of
the second leaf. The final source removes it before drawing the English.
`work/qa/card063_candidate*` are diagnostic renders, not runtime approval.

## Cold proof and fresh D10 review

Main disc SHA-1: **30553cd86663b6a9af287ff00e626d2771e25c85**;
**182,449,344 bytes**, built **2026-11-01 17:25:34 UTC**.

- `tools/check.py`: **129 tests passed; lint 0 errors**.
- `tools/verify_build.py`: **399 changed files; 0 errors**.
- Cold smoke `work/qa/card063_smoke`: passed.
- Cold navigation `work/qa/card063_cold`: **100/100 complete card captures**.
- `textlog.py`: **0 Japanese lines in 1 log**; this excludes graphics.
- Full gate `work/qa/card063_review/manifest.tsv`: **20/20 accepted**, no
  missing/stale verdicts or changed hashes.
- Detail gate `work/qa/card063_detail_review/manifest.tsv`: **1/1 accepted**.

The fresh read-only pass inspected the complete changed sheet (cards061-065)
and the enlarged original/English margin comparison. The top leaf is closed,
the upper/right pale remnants are gone, and “All together!” remains complete.
The other four cards retain their accepted lettering and artwork. All nineteen
other complete sheet hashes exactly match the accepted full-scope rows in
`card-background-verdicts.tsv`; those verdicts are carried forward explicitly.
Historical issue verdicts remain unchanged.

| Current sheet | SHA-1 | Verdict |
|---|---|---|
| `card063_audit/compare_sheet_13.png` | `061477766d95a2e32ce82cba7dc901ae9c7f286e` | fixed |
| `card063_details/card063_sheet.png` | `21f74b15a7fe1958ef1a8fcc11761f56d496464b` | fixed |

## Reproduction

`<skill>` means the directory printed by `python tools/skill.py`.

```powershell
python -X utf8 tools/gen_card_words.py
python -X utf8 tools/build.py
python -X utf8 tools/check.py
python -X utf8 tools/verify_build.py
python -X utf8 <skill>/scripts/emu.py build/momotarou-matsuri_en.cue --out work/qa/card063_smoke --route tools/routes/boot.txt --smoke
python -X utf8 <skill>/scripts/emu.py build/momotarou-matsuri_en.cue --out work/qa/card063_cold --script tools/debug/warp.lua --script tools/debug/cards.lua --script tools/lua/textlog.lua --var "SCENE='card_album'" --var HOLD=-1 --frames 900 --timeout 300
python -X utf8 tools/debug/cards_qa.py work/qa/card063_cold --out work/qa/card063_coverage
python -X utf8 tools/debug/card_art_review.py --run work/qa/card063_cold --out work/qa/card063_audit --cards (1..100)
python -X utf8 <skill>/scripts/sheet.py work/qa/card063_cold/card_063.png --compare work/qa/cards8_jp_all3/card_063.png --crop 224,56,40,128 --zoom 6 --out work/qa/card063_details/card063_sheet.png
```

Create the detail directory before calling `sheet.py`. The album route seeds
collection flags, then uses native controller navigation and loading. It does
not establish natural card-acquisition or story-progress coverage. No shared
skill files changed, and no release was built or published.
