# Full-card artwork audit, 2026-11-02

All 100 cards received a fresh read-only whole-illustration comparison. Eight
cards have corrected caption masks: **034, 038, 049, 059, 076, 077, 078, 084**.
Fourteen other cards still have caption-fill or preservation defects. This is
an incomplete phase-8 checkpoint, not album-wide visual approval.

## Repairs and rejected candidates

| Card | Repair |
|---|---|
| 034 | Restore the small monkey's head edge; stepped paper clears remove the adjacent brown stroke |
| 038 | Restore the rightmost oni's outline while clearing the separate Japanese strokes beside it |
| 049 | Remove the brown stroke below the caption; stop before the hand at y90 |
| 059 | Restore the curled staff edge; remove brown and pale caption remnants around it |
| 076 | Clear the old first-stroke pixels above the English |
| 077 | Clear the old bottom stroke below the English |
| 078 | Clear the left-hand stroke beside the English |
| 084 | Clear the bottom stroke below the English |

Wording, font, position and colour are unchanged. Only eight generated PNGs
change. The generator now distinguishes blank paper from illustration edges
inside caption rectangles. Existing outer-bound checks cannot detect damage
inside those rectangles, so regressions compare protected original monkey,
oni and staff crops and check the formerly retained strokes independently of
the generator's mask constants. The existing hand-preservation regression
rejected an over-wide card049 candidate; the clear now ends at y90 exclusive.

Cold detail review rejected further remnants on 034/038/059, then three pale
pixels at card059 x189, y6/20/21. The latter are cleared only in the upper
blank-paper region, leaving the staff bounds narrow. Intermediate runs
`cards_full8_cold` and `cards_full8_accepted_cold` are rejected candidates;
despite the latter's directory name, **use `cards_full8_final_cold`**.
Their disc SHA-1 values were respectively
`a264a9930957deb46891976e0a54ad1a3aeaf946` and
`fb0fb7654b06d4e21d91e5ce713e6021c60b84ac`.

## Reproduction and evidence

`<skill>` below means the folder printed by `python tools/skill.py`.

```powershell
python -X utf8 tools/gen_card_words.py
python -X utf8 tools/build.py
python -X utf8 <skill>/scripts/emu.py build/momotarou-matsuri_en.cue --out work/qa/cards_full8_final_cold --script tools/debug/warp.lua --script tools/debug/cards.lua --script tools/lua/textlog.lua --var "SCENE='card_album'" --var HOLD=-1 --frames 900 --timeout 300
python -X utf8 tools/debug/cards_qa.py work/qa/cards_full8_final_cold --out work/qa/cards_full8_final_coverage
python -X utf8 tools/debug/card_art_review.py --run work/qa/cards_full8_final_cold --out work/qa/cards_full8_final_audit --cards (1..100)
python -X utf8 tools/textlog.py work/qa/cards_full8_final_cold
```

As in the earlier card tour, collectible bits are seeded in RAM and native
controller navigation loads all cards; this does not prove story acquisition.
The complete-card oracle checks both illustrations and prefecture strips.
Whole-card sheets show original TIM left and cold English right at 3x.
Enlarged details show cold English left and cold original right at 6x,
using `work/qa/cards8_jp_all3/card_NNN.png` as the original control.

Generate each detail with `<skill>/scripts/sheet.py`, the matching two PNGs,
`--compare`, `--crop` from the table, `--zoom 6`, and output
`work/qa/cards_full8_final_details/cardNNN_sheet.png`:

| Card | Screen crop x,y,width,height |
|---|---|
| 034 | 230,56,34,105 |
| 038 | 238,56,26,110 |
| 049 | 56,56,38,128 |
| 059 | 231,56,33,128 |
| 076 | 230,60,34,70 |
| 077 | 234,62,30,74 |
| 078 | 60,108,32,48 |
| 084 | 232,60,32,90 |

The first fresh D10 pass reviewed all 20 sheets at
`work/qa/cards_full8_review`: 5 ok, 15 with issues. After repairs, changed
whole-card sheets and all eight enlarged details are reviewed separately;
unchanged whole-card hashes retain their initial read-only observations.
Final verdicts and hashes are in `card-full-art-verdicts.tsv`.

## Remaining card findings

| Card | Outstanding issue |
|---|---|
| 007 | Grey horizontal donor streaks through/below Nighty-night |
| 026 | Caption fill breaks/doubles fine horizontal background lines |
| 033 | Grey fill artifacts below the caption |
| 039 | Square grey streak at the bottom of the caption margin |
| 044 | Grey tree-edge smear across the caption margin |
| 054 | Stepped grey bands and damaged house linework |
| 063 | Blocky pale/grey fill through the sky and leaves |
| 075 | Grey horizontal streak across the end of There it is |
| 079 | Brown remnants above the caption; check rose-background preservation |
| 082 | Grey donor artifacts below the caption |
| 087 | Brown top-of-caption pixels and blocky grey sky fill |
| 093 | Caption clear cuts the top falling leaf |
| 094 | Angular grey donor streaks among the left foliage |
| 098 | Stepped grey artifact below Welcome |

These defects keep the whole-album gate red. Other phase-8 requirements in
`docs/status.md`, including natural story/NPC routes and unresolved graphics,
also remain open. No owner decision is needed; no release was made.

## Red new-card notice investigation

`tools/debug/atlas_refs.py` is a reusable read-only cross-archive ANM scan for
a source TIM rectangle, matching texture page, depth and source CLUT rows.
VRAM reuse makes every result a lead, not proof of runtime use or disuse;
native-code sprite construction and runtime UV changes are outside its scope.

```powershell
python -X utf8 tools/debug/atlas_refs.py HOUGEN0D.BIN:0 196 160 256 184 --contained
python -X utf8 tools/debug/atlas_refs.py HOUGEN0D.BIN:0 168 184 256 208 --contained
python -X utf8 tools/debug/atlas_refs.py HOUGEN0D.BIN:0 168 216 232 240 --contained
python -X utf8 tools/debug/atlas_refs.py HOUGEN0D.BIN:0 0 56 160 80 --contained
```

Across 1543 archives and 5277 ANM tables, the three notice fragments produce
69, 20 and 11 candidates, mostly unrelated shared-VRAM sprites. The control
region produces seven candidates including the real HOUGEN0D entry5 item0
(u0,v56,w160,h24, CLUT0/480, flags0x3100). HOUGEN0D's own ANM5/6 still do
not assemble the red fragments. The notice is unchanged and unclassified;
this scan grants no unused-art exemption.

### Native-code follow-up, 2026-11-02

Read-only inspection of original OVLXTTL narrows two album paths:

- `0x800D6DFC` calls EXE `0x800428D0` to test the current card's collectible
  bit. `0x800D6E0C` reduces that result to a boolean and `0x800D6E24` adds
  three: the static binder at `0x800D6E48` selects HOUGEN0D ANM6 item **3 or
  4**, not a new-card notice. Both items are in the previously audited table.
- Initialization at `0x800D78E0` loads HOUGEN0D data ID **8**, TIM entries
  **0/1/2** at `0x800D7958..7978`. It binds the background tile table/map
  **3/4** at `0x800D7A14`. Entry point `0x800D7FA8` calls this same initializer
  on both sides of its context comparison (`0x800D8050` and `0x800D8060`).

These checks explain why toggling collected/missing status or changing only
that entry context is not evidence of a separate red-notice path. They do
not exclude another native consumer, dynamic UV changes or a card-acquisition
path outside this menu. No notice pixels, code or classifications change;
the runtime path remains open. Reproduce by disassembling the original
`work/disc/tree/OUTBIN/OVLXTTL.BIN` as little-endian MIPS32 with load address
`0x800CB338`, and comparing the cited calls to `tools/anm.py HOUGEN0D.BIN 6`.

### Further static leads, 2026-11-02

`tools/debug/call_contexts.py 8001f3ac --contains '$a0, $zero, 8'` also
finds a second HOUGEN loader at **0x800D8350** (load call **0x800D8360**).
It uploads the same three TIMs, then HCARD00D entry 0. There are **zero
direct JAL calls** to 0x800D8350 across the original EXE and overlays;
indirect calls and other ways of entering code remain outside that result.
The context filter also returns nearby loads of data ID 9: the earlier
`a0=8` has been overwritten before those calls. Inspect the actual last
assignment and delay slot; the helper deliberately does not infer dataflow.

HOUGEN0D's background tile table (entry 3) contains sixteen records, all at
u=0/16/32/48/64 and v=0/16, on page 5/CLUT 30720. Its entry-4 background
grid therefore cannot display the notice fragments at y=160 and below.
Together with the ANM audit this excludes the static album layout as the
notice's consumer, not every possible native-code path. The notice remains
open; these findings do not authorize an unused-art exemption.

## Final validation

Final main disc: **182,454,048 bytes**, built **2026-11-01 16:39:00 UTC**,
SHA-1 **5b1f3ee68331bd006fc9c1c7e0e49010a4a16816**.
`tools/check.py`: **127 tests passed, lint 0 errors**. Disc verifier:
**399 changed files, 0 errors**. Cold smoke at `work/qa/cards_full8_final_smoke`
passed. The final album tour has **100/100 complete captures** and **0 Japanese
lines in one textlog** (graphics excluded).

Fresh D10 review accepts **8/8 detail sheets**. The full-card gate has **7 ok /
13 issue sheets**, with no missing/stale verdicts and no changed hashes after
manifest initialization. It intentionally exits 1. Six whole-card sheets
changed since the initial pass (7, 8, 10, 12, 16, 17); all were re-inspected.
After the last pale-pixel correction only sheet12 and detail059 changed,
and both were re-inspected. The other fourteen whole-card hashes and seven
detail hashes match their reviewed predecessors. **Phase 8 cannot advance.**
