# Menu title coverage, 2026-11-02

Four cold original/English routes prove the complete Game Album, Quick Match!
and Name Entry graphics at their native positions. The saved-Status record
viewer also says Game Album on the original; it is not evidence for the
separate Rank Details artwork. **Phase 8 remains incomplete.**

## Reproduction and limits

```powershell
python -X utf8 tools/debug/menu_titles.py --out work/qa/menu_titles8_en
python -X utf8 tools/debug/menu_titles.py --out work/qa/menu_titles8_jp --original
python -X utf8 tools/debug/menu_titles.py --out work/qa/menu_titles8_en --check-only
```

The default disc is the main English image. `--cue` selects another CUE with
a same-named BIN; `--only` limits the named cases. `--check-only` checks the
recorded disc SHA-1 before using retained captures. Fresh runs remove custom
shots/logs first, reject emulator failures, and require the case, ready state,
mode and a complete title match. The oracle decodes ANM and TIM entries from
the **named disc**, not the current redraw PNGs. It searches only the top
48 screen pixels and checks every opaque pixel including the outline.

| Case | Cold route | Archive / ANM / item | Context | Sprite origin |
|---|---|---|---|---|
| album | Saved Status, Cross, Left, Circle | YUGI0D / 4 / 1 | 2 | 80,20 |
| saved_details | Saved Status, first icon, Circle | YUGI0D / 4 / 1 | 4 | 80,20 |
| quick | Existing trial_menu controller route | PREM0D / 10 / 7 | 2 | 80,20 |
| name | Existing name_entry cold warp | NAME0D / 4 / 8 | 3 | 70,20 |

Album and saved-Status cases load a copy of
`work/qa/save_fixture_checked/memcard1.mcd` and assert that the source card's
bytes stay unchanged. They seed only record 0's played word to enable access;
rank and score remain untouched. Name Entry uses the established mode/context
warp. No case changes a texture, palette, ANM selector or display coordinate.
This is header coverage, not natural record-setting or a complete menu tour.

## Rank Details investigation

The original OVLXTTL display table at `0x800E0C08` has four records
`(x, y, depth, ANM item)`:

```text
(160,120,15,0), (160,120,15,1), (295,105,17,3), (25,105,17,4)
```

Constructor `0x800DB144` walks that table unconditionally; the header uses
item 1, which is Game Album. Item 2 is the separate 96x24 Rank Details
graphic. These facts explain the two observed Album contexts; they do not
prove item 2 is globally unused. Do not substitute that title merely to make
the survey green. Its native consumer remains open.

## Read-only D10 review

After both tours and their pixel checks, inspected all eight comparison sheets
in `work/qa/menu_titles8_review` in a separate read-only pass: four complete
contexts and four enlarged headers, English left and original right.
All eight are **ok**, with hashes and scoped notes in
`menu-titles-verdicts.tsv`. Game Album, Quick Match! and Name Entry are complete,
with no clipping or old Japanese strokes. Name Entry's initially empty
selection matches the original; the earlier glyph/editing tour covers input.

```powershell
python -X utf8 <skill>/scripts/qa_gate.py check work/qa/menu_titles8_review/manifest.tsv work/qa/menu_titles8_review/verdicts
python -X utf8 tools/textlog.py work/qa/menu_titles8_en
```

Gate: **8/8 ok**, no missing/stale verdicts. English textlog: **0 Japanese
lines in four logs**, excluding graphics. `<skill>` is `python tools/skill.py`.
An explicit negative check against the later rebuilt disc rejects these older
captures with `captures belong to a different disc`, before writing coverage.
The first English tour used `d20bb64a57a110da58795477de0bf197effcc0de`;
the repeated tour at `work/qa/menu_titles8_final_en` passed all four cases on
`cad7ca64fac7c7a73f443f083f5ed4735be739f1` after the first four card fixes.
The final six-card build is recorded in `card-margin-polish-qa.md`; these menu
assets were not changed by that work.

No shared skill files changed. Gotcha for `references/emulator-qa.md`: a
menu's entry context does not necessarily select its similarly named atlas
header; check the native display table and original capture before claiming
coverage or changing the title.
