# Saved-record and Status QA, 2026-11-01

Phase 8 remains open. This pass fixes a saved-record extraction gap and supplies the missing game-written
save fixture; it does not certify the full graphics survey or scene tour.

**Superseded Status layout/coverage:** [status-ranks-qa.md](status-ranks-qa.md)
adds all six rank pictures and counter stress cases, fixes money/card overlap,
restores panel borders missed by this early review, and translates the Hermit
staff badge. The two-sheet verdict below is historical, not approval of those
subsequently discovered defects.

## Reproduce

From the repo root, with the skill path resolved by `python tools/skill.py`:

```powershell
python -X utf8 tools/debug/save_fixture.py --out work/qa/save_fixture_checked
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/status8_final_cold --route tools/routes/status_saved.txt --sav work/qa/save_fixture_checked/memcard1.mcd --shot-every 300 --sheet --script tools/lua/textlog.lua
python -X utf8 tools/textlog.py work/qa/status8_final_cold --all
```

The default seed is the empty formatted card at `tools/pcsx/memcard1.mcd`. If that card has become populated,
pass an empty card with `--seed`; the tool refuses populated seeds. The output fixture is written by the
game's own save routine, has allocated directory entry `BISLPM-86888-A`, and the seed is checked unchanged.
The route loads slot 1, confirms Yes, dismisses completion and selects Status again.

The first save attempt appeared stuck because confirmation defaults to No. The warp's message-closing
circle presses must stop outside field mode 1. The save scene is now explicit, and failed fixture creation
returns a nonzero exit code instead of treating a visible menu as proof of a saved card.

## Findings and changes

- `codestr.py` omitted digit-slot templates unless their unit was 両. Every code file was swept for the same
  form: eleven additional OVLXTTL rows, including both record-screen copies, are now extracted and translated.
  These include rank, hours, minutes, points, counts and a time separator. Their `[20]` digit slots stay intact.
- STATUS0D entry 0 has English title, rank/mastery labels, panel labels and four rank plates. The generator
  removes neutral lettering from coloured rank artwork instead of clearing the whole plate. Redraw tests
  reject changed pixels outside the declared label rectangles.
- The narrow money-unit sprite could not display “ryo” legibly, so the label is “Money (ryo)”. Redundant card,
  step, rank and mastery-count suffixes are removed. Steps uses an 11-pixel font to clear the game's hidden
  counter; the other panel labels use 14 pixels.
- `work/qa/status8_original/final.png`, reached cold on the original with the same save and route, also shows
  question marks for steps. This is expected for the initial fixture without a pedometer.
- `tools/debug/records.lua --var RECORDS=true` enables one played-record flag in RAM (EXE 0x800435F4 scans
  70 entries at 0x800BDBF0, stride 0x1C). It reaches the album without requiring a completed minigame, but
  does not create genuine scores/ranks. `work/qa/album8_*` are exploratory evidence only, not final cold-boot
  verdicts for mode labels, name entry, or record categories.

## Fresh read-only visual verdicts

After the final redraw, reviewed the enlarged images directly under the owner's D10 allowance. An earlier
review found Steps crowding the question marks; the final image below has a smaller label and was rechecked.

| Sheet | SHA-1 | Verdict and scope |
|---|---|---|
| work/qa/status8_review/status_sheet.png | 2185332431673d4a2f17c74c3c047a6508455210 | ok: current Status labels and base Momotaro plate; no clipping/overlap; hidden steps match original |
| work/qa/status8_review/save_sheet.png | 05725e61d2eb5f62393bb60faee02973b131468c | ok: translated save-selector counters/completion; original title-logo art retained under D5 |

Manifest: `work/qa/status8_review/manifest.tsv`; verdicts: `work/qa/status8_review/verdicts/review.tsv`.
This two-sheet manifest must not substitute for the phase-wide manifest. The three higher rank plates,
nonzero/maximal counters, record categories, cards, banners, credits and the full scene tour remain unverified.

## Validation and build

- `tools/check.py`: 40 tests passed, lint 0 errors.
- `tools/verify_build.py`: 345 changed disc files, 0 errors.
- `tools/textlog.py work/qa/status8_final_cold --all`: 0 Japanese lines.
- Cold-boot smoke: `work/qa/smoke8_final`, exit 0 and `smoke ok`.
- Built disc: `build/momotarou-matsuri_en.bin`, 182,844,480 bytes, built 2026-11-01 01:29:27 UTC.
- Disc SHA-1: `a3db1fb15d377b7933560c661b1fdf4b3344896e`.

Skill gotchas for `references/emulator-qa.md`: confirmation can default to No; stop warp message-mashing
when entering another mode. For `references/pipeline.md` Extract: a kana/length filter misses numeric
templates with spaces plus a single kanji; sweep every referenced occurrence when one is found. The skill
itself was not modified.
