# Medicine plaques, 2026-11-02

The two Medicine plaques now show the complete word in cold map143/144
captures. Both existing Items placements still pass. Fresh read-only D10
review accepts all eight context/detail sheets; this is scoped evidence,
and phase 8 still cannot advance to release.

## Source and allocation

Both maps use native front-grid cell (98,20), records 99/74/101 and source
tiles (208,48), (64,80), (144,48) from GV12000D:0 / GV12002D:0. Their native
page5 / CLUT31488, flags, trailing attributes and tile count are retained.
The full 30-pixel Medicine mask needs the existing 48x16 assembled layout.

There are only two free transparent 16x16 cells in the sunny atlas after
Items. Medicine uses (0,32), (64,48) and (160,240), with new records
1018-1020. The last cell contains the atlas's repeated diagnostic checker,
96 index-1 pixels and 160 index-0 pixels. Its exact original index SHA-1 is
`642b2cd0c1dd310cebbd714cbb7b19b356f12527` in both weather variants. The draw
refuses any other pattern or a destination already changed by another label.
All three cells have zero decoded tile/ANM references in their paired map
archives, including records without default grid placements. This is static
allocation evidence, not proof against unknown native-code consumers.

`gfx_field.py` now applies multiple named plaque plans to the same atlas and
companion archive. Hash validation always uses the original entry; each plan
writes its distinct cells/records into the shared output. Existing Items
records 1021-1023 and their atlas allocation remain intact. Rear grids,
source records, original Japanese source pixels and unrelated entries stay
unchanged. The verifier permits only the exact specified layout edits.

The tests cover every allocation's decoded consumers, disjoint destinations
and record IDs, exact grid edits, preserved attributes/entries, bad original
hash rejection, complete word pixels, surrounding roof pixels, and rejection
of an unrelated grid mutation. Both Medicine/Items plans are tested together.

## Reproduction

```text
python -X utf8 tools/gen_gfx.py --only GV12000D.BIN:0 GV12002D.BIN:0
python -X utf8 tools/build.py --out build/medicine8.bin
python -X utf8 tools/debug/signs_tour.py --cue build/medicine8.cue --out work/qa/medicine8_en --only medicine143 medicine144 items143 items144 --jobs 2
python -X utf8 tools/debug/signs_tour.py --original --out work/qa/medicine8_jp --only medicine143 medicine144 items143 items144 --jobs 2
python -X utf8 tools/debug/field_signs_review.py work/qa/medicine8_en work/qa/medicine8_jp --out work/qa/medicine8_review
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" init work/qa/medicine8_review/manifest.tsv work/qa/medicine8_review
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/medicine8_review/manifest.tsv work/qa/medicine8_review/verdicts
```

Both discs pass 4/4 complete 48x16 assemblies at (136,76). The routes run the
native map initializer, then frame the shop without story-flag overrides.
The screenshot oracle selects the correct named layout and original/English
tiles under their native palettes. Fresh review inspected all eight sheets:
complete Medicine/Items lettering, intact snow/roof edges and posts, and
preserved actors/buildings. Exact hashes are in `medicine-plaques-verdicts.tsv`.

Validation: **123 tests passed / lint 0**, verifier **398 changed files /
0 errors**, **0 Japanese lines in 4 logs** (graphics excluded), and cold
smoke passed for `medicine8`. Disc size **182,454,048 bytes**, build
**2026-11-01 15:00:39 UTC**, SHA-1
`d0552aced38bba6aed45e37620cf76e7ddff331d`.
The default main build is byte-identical, built **2026-11-01 15:08:17 UTC**;
its separate cold smoke at `work/qa/medicine8_main_smoke` also passes.

The original unplaced/rear-grid Medicine tiles and GV01000D:0 records102/103
remain runtime gaps. This does not approve other medicine sprite forms,
later story rewrites, the full visual tour or NPC dialogue. No shared skill
files changed. Gotcha for `references/graphics.md`: an atlas's unused region
can contain diagnostic checker pixels rather than transparency; require an
exact pattern check and a consumer audit before allocating it.
