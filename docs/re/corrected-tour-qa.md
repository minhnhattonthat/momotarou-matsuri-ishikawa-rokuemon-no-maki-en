# Corrected-initializer tour, 2026-11-01

The complete 465-scene sweep now uses each map's native initializer. **464/465
scenes passed on the frozen card-prop build; map 284 failed.** A separate retry
on the current Games-sign build supplies its arrival/final pair for visual
review. This is a mixed-build review, not a 465/465 passing run of either disc.
Phase 8 remains incomplete.

**Later follow-up:** [map284-regression.md](map284-regression.md) identifies the
bare-warp failure as a SEQ tempo exception and records six cold passes after
restoring native transition setup. The historical mixed-build audit below
retains its original counts and verdicts; it has not been silently replaced.

## Builds and reproduction

| Use | Disc SHA-1 | Size | Build time UTC |
| --- | --- | --- | --- |
| Frozen tour, commit 39e9d50 | 1ff27c30c241edca355a724a9fce8e56d94f36cf | 182458752 | 2026-11-01 11:03:30 |
| Map284 retry and final Games signs | 606ce85331274eff4e3e495021c391f1f2e29112 | 182454048 | 2026-11-01 11:40:47 |

```
python -X utf8 tools/debug/warp_all.py build/tour8_corrected/momotarou-matsuri_en.cue --out work/qa/tour8_corrected --jobs 3 --hold 1500 --click 45 --every 60 --probe tools/lua/textlog.lua
python -X utf8 tools/debug/warp_all.py build/momotarou-matsuri_en.cue --out work/qa/tour8_main284 --jobs 1 --only '^map_gv2500_284$' --hold 1500 --click 45 --every 60 --probe tools/lua/textlog.lua
python -X utf8 tools/debug/tour_review.py work/qa/tour8_corrected --fallback work/qa/tour8_main284 --out work/qa/tour8_corrected_review
python -X utf8 tools/textlog.py work/qa/tour8_corrected
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" init work/qa/tour8_corrected_review/manifest.tsv work/qa/tour8_corrected_review --glob '*sheet*.png'
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/tour8_corrected_review/manifest.tsv work/qa/tour8_corrected_review/verdicts
```

The text log reports **0 Japanese lines in 464 logs**, markers 0. It cannot
detect lettering drawn as graphics or lines never reached. The main retry has
English ground-search dialogue. All runs are cold through `emu.py`; source
disc and memory-card data are unchanged.

## Fresh read-only review (D10)

All **78 sheets / 465 arrival-final pairs** were inspected. Each row contains
arrival at left and final at right, six scenes per sheet except the last three.
The only fallback is `map_gv2500_284`, sheet 064 row 3. The helper records each
pair's source directory in `work/qa/tour8_corrected_review/scenes.tsv`.

The gate reports **0 missing verdicts, 25 not ok, 0 changed since init** and
correctly exits 1. [corrected-tour-verdicts.tsv](corrected-tour-verdicts.tsv)
preserves every sheet SHA-1, scene order and latest human-authored verdict;
it is a durable audit copy, not a substitute for the live manifest gate.

Remaining findings include event crowns, Kintaro/Poverty God clothing marks,
hill bonfire kanji, event flags/statue signs, ending art, M14's hanging plaque,
History Quiz's helmet and town roof signs. The snow-event placard, shrine
paper charms and round back-wall banner emblem still need close classification.
Five Games atlases are fixed and separately accepted in [games-signs-qa.md](games-signs-qa.md),
but that does not approve the Japanese pixels in these older tour sheets.

Two suspected issues were classified against additional evidence:

- `game_m99_3d` also shows its HUD over black on a cold original-disc route
  (`work/qa/tour8_m99_original`). This helper context is not a translation fault.
- The common inn wall scroll is a landscape pattern. An enlarged map61 crop
  and matching map116/146/155/240/265 crops establish this; map83's enlarged
  crop shows the same drawing. It does not need lettering replacement.

Only the four product-logo families listed under D5 in `graphics.md` have a
general Japanese-logo exception. The visual brief no longer exempts arbitrary
Japanese graphics. An `ok` here covers only the two shown moments. Numbered
intermediate frames, NPC conversations, minigame outcomes and later story flags
still need their own review; these sheets cannot establish those gates.

## Map 284 regression: historical failure (follow-up above)

The exact scene is `map_gv2500_284 map 284 19 11 0 0x314`. The frozen tour and
two isolated frozen retries all report `map 284 never loaded`. The original
disc passes (`tour8_jp284`), and the current Games-sign build passes twice
(`tour8_main284`, `tour8_main284_repeat`) with identical scene parameters.

The read-only `tools/debug/map_watch.lua` probe logs map number, VM script,
program counter and current opcode every 300 frames. On the failing frozen
probe, frames 3900-6600 retain map 284, script 80140310, PC 80140314 and opcode
001D. The current-build repeat restores the injected script at frame 3831,
reaches the scene at 3922 and returns to idle before ground-search dialogue.
Thus the frozen failure stalls within map loading, before the initializer
returns; simply checking the map-number variable would falsely report success.

Prior evidence in `debug.md` linked this map's failure to disc-sector shifts.
The new result is consistent with a layout/timing dependency, but does not
identify the underlying race or prove that Games graphics fixed it. In
particular, direction 0 is **not** a universally reliable workaround as the
older note claimed. Keep both builds and failure logs until the loader/warp
precondition is understood; then rerun the same original/frozen/current cases.
Do not weaken the arrival check, silently substitute a retry, or mark this
reliable solely because the latest image happens to pass.

## Next work

Use the durable verdict rows to locate the remaining graphics and classify
the three uncertain families with enlarged cold original/English captures.
Resolve the map284 warp regression, then rerun affected routes on the final
build and review intermediate dialogue and natural outcome frames. Continue
the existing targeted gaps in `status.md`; no release gate is satisfied by
this arrival/final audit alone.
