# Equipment shop plaques and narrow-plaque investigation

Map45's three equipment plaques now read **Weapons**, **Armor** and **Shoes**.
Cold original/English captures show all three completely, and a fresh read-only
D10 pass accepts all six context/detail sheets. This resolves the equipment
finding in the older shop-board review; that historical verdict is unchanged.
Phase 8 remains incomplete and cannot advance to release.

## Sources and preservation

`tools/gfx_signs.py` declares three 32x16 source strips in GV01000D:0 at
(0,80), (32,80) and (64,80). GV01001D:2 records 70-75 draw them as paired
16x16 tiles at grid positions (30,31)/(31,31), (38,31)/(39,31), and
(30,24)/(31,24), respectively. No tile records or map grids were changed.

The complete engraved stroke/highlight masks occur only once each in the
original archive sweep:

```
python -X utf8 tools/gfxfind_rect.py GV01000D.BIN:0 9 81 22 94 --indices 12 13
python -X utf8 tools/gfxfind_rect.py GV01000D.BIN:0 41 81 54 94 --indices 12 13
python -X utf8 tools/gfxfind_rect.py GV01000D.BIN:0 73 81 86 94 --indices 12 13
```

These are exact glyph-family sweeps, not coverage of differently drawn sprite
strips or other equipment signage. Whole-image duplicate expansion also runs
in `gen_gfx.py`; this atlas has no additional identical image copy.

The existing MIT credits7 font retains the full words. Weapons is 30 pixels
wide, so rows 3-11 of the plaque interior receive wood behind the outer
letters. The original tile pair, top/bottom edge and mounting posts stay in
place. Armor and Shoes only replace the original engraved stroke/highlight
pixels plus their English letters. Every pixel outside the declared rectangles
is protected by the existing preservation test. The inserted-index test now
also checks every English stroke and absence of old highlighting in all three
equipment labels. Existing plaque rendering is unchanged.

## Cold evidence and validation

```
python -X utf8 tools/gen_gfx.py --only GV01000D.BIN:0
python -X utf8 tools/build.py --out build/equipment8.bin
python -X utf8 tools/debug/signs_tour.py --cue build/equipment8.cue --out work/qa/equipment8_en --only equipment45
python -X utf8 tools/debug/signs_tour.py --original --out work/qa/equipment8_jp --only equipment45
python -X utf8 tools/debug/field_signs_review.py work/qa/equipment8_en work/qa/equipment8_jp --out work/qa/equipment8_review
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/equipment8_review/manifest.tsv work/qa/equipment8_review/verdicts
```

The route uses map45's native initializer at (34,29), with no story-flag
override. The complete source rectangles match at (89,157), (217,157), and
(89,45) under native palette 1 on both discs. The full context and each
enlarged detail were inspected after implementation. The scoped gate is
**6/6 ok**, with no missing or stale verdicts; hashes and verdicts are in
[equipment-signs-verdicts.tsv](equipment-signs-verdicts.tsv). The three
context sheets deliberately show the same screenshot; this is one scene,
not three independent gameplay routes.

Validation: **111 tests / lint 0**, **394 changed disc files / 0 verifier
errors**, **0 Japanese lines in one English log**, and a passing cold smoke
at `work/qa/equipment8_smoke`. Text logs exclude graphical lettering and
dialogue not reached by this route. The verified image is copied byte-for-byte
to `build/momotarou-matsuri_en.bin` and cold-smoked there too.

Build: **182,451,696 bytes**, **2026-11-01 14:08:30 UTC**, SHA-1
`49e632d7417e4901ca0bfb0bc872b18eb65ab6bd` (same as `build/equipment8.bin`).
No release was created and no shared skill files changed.

## Narrow plaques: next implementation seam

Superseded for the six named Flowers/Items placements by
[narrow-plaques-qa.md](narrow-plaques-qa.md): isolated tile slots and checked
front-grid changes now have cold original/English proof. The investigation
below remains useful for the original layout and unknown story consumers.

The adjacent flower and item signs are not equivalent to map45's tile pairs.
The atlas's apparent board width does not establish its runtime width.
`tools/debug/field_label_plan.py` prints page/CLUT-qualified native tile
neighborhoods and conservative, unreferenced transparent 48x16 allocation
candidates. It reads only; these are navigation leads, not runtime verdicts.

```
python -X utf8 tools/debug/field_label_plan.py GV06000D.BIN:0 200 80
python -X utf8 tools/debug/field_label_plan.py GV22000D.BIN:0 80 80
python -X utf8 tools/debug/field_label_plan.py GV12000D.BIN:0 16 80
```

- Maps99/100: GV06001D tables 2 and 3 record 200 draws only (200,80,16,16)
  from the flower board; grid 0 cell (20,39), neighbors 197 and 199. The full
  board's records 102/103 are unplaced. All three visible tiles use CLUT 30784,
  page 5. No completely unreferenced transparent 48x16 slot was found in this
  atlas under the helper's conservative all-record check.
- Maps237/238: GV22001D table 4 record 75 is the flower tile at (80,80).
  It occurs at (70,26) in grids 0-3. The front neighbors 742/744 use CLUT
  31616; the rear neighbors 288/289 use a different page and CLUT 30977.
  Merely painting a wider word across adjacent atlas columns would overwrite
  other labels and still fail to draw the complete word. Unreferenced 48x16
  transparent candidates exist at (176,240), (192,240) and (208,240); these
  overlap, and do not establish freedom from unknown native consumers.
- Map143: GV12001D table 2 record 71 is the item tile at (16,80), grid cell
  (24,20) in grids 0/1. Front neighbors 99/101 share CLUT 31488 and page 5;
  rear neighbors 289/260 are on another page. No conservative free 48x16
  slot was found. Map144's snow counterpart still needs separate inspection.

The exact flower mask at GV06000D:0 (201,81)-(214,94) also occurs at
GV22000D:0 (81,81); the tested medicine mask at GV01000D:0
(137,81)-(150,95) occurs only there. Neither family was edited this session.
Their full English labels need a verified wider tile assembly or a renderer
change, preserving neighboring tiles and palette behavior. Do not abbreviate
or stretch the current 16-pixel source rectangle and call that complete.

For `references/graphics.md`: a field atlas may contain a 32-pixel plaque
while its map draws only the middle 16 pixels; inspect actual tile-grid
consumers before choosing an English label width. Other open phase-8 work
remains in `docs/status.md`, including the full visual manifest, story/NPC
routes, HUD outcomes and unresolved graphics. This checkpoint is not a
phase-wide QA approval.
