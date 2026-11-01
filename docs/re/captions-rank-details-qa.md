# Location captions and saved-Status record viewing

This is a phase-8 checkpoint, not a release approval. It covers all 27 extracted
location captions and the 43 record pages reached from Status's first icon.
The graphics survey, natural minigame outcomes, and full story interaction tour
remain separate gates.

## Reproduce

```powershell
python -X utf8 tools/debug/caption_tour.py --out work/qa/captions8_final --jobs 2
python -X utf8 tools/debug/caption_tour.py --out work/qa/captions8_original --original --jobs 2
python -X utf8 tools/debug/rank_details.py --out work/qa/details8_final2
python -X utf8 tools/debug/rank_details.py --out work/qa/details8_original2 --original
python -X utf8 tools/debug/rank_details.py --out work/qa/details8_empty --empty
```

The default English image is `build/momotarou-matsuri_en.cue`. Each harness
supports `--check-only` for retained artifacts. Use at most three concurrent
emulators. The record route uses the unchanged game-written source card at
`work/qa/save_fixture_checked/memcard1.mcd`; emu.py operates on a copy, and the
Python wrapper asserts that the source card's bytes are unchanged.

## Caption findings

`caption_tour.py` obtains all `kind=caption` rows from the insertion pipeline,
wraps/encodes their English with the same production functions, and invokes the
native op-26 renderer through warp.lua's existing `OPS` interface. Original
runs encode the row's Japanese. Each row starts from a separate cold boot.

The caption appears over the opening field before the final destination warp.
This deliberately tests text, width and centering; it does **not** establish
that every location is reachable in the correct story state, or show each
caption against its real destination's background.

The first probe failed: warp.lua queued Circle on the frame it installed the
op, dismissing the caption before a screenshot could prove it. The optional
`WARP_CLOSE_DELAY=60` now delays those closing presses without changing other
routes' default behavior. `caption_capture.lua` reads the VM's current op at
`0x800BF7FC` and its line-object pointer at `0x800BF7D8`, then captures after ten
visible frames. Object x/y/count are at +4/+6/+2. The fixture temporarily sets
`0x8008C510` to zero immediately before the caption and restores it afterward:
EXE `0x80034D50` permits captions for incoming-map values below 37, with one
special 126/139 case. Every accepted run's original value was already zero;
the input delay, not this field, resolved the missing capture.

The checker requires the screenshot and an exact decoded textlog line at the
captured coordinates. English x must equal `160 - floor(width / 2)`, y must be
60, and width must fit the 116-pixel measured interior. Japanese uses the
original 12-pixel advance. Negative tests reject a successful arrival with no
caption, a partial/wrong line, an incorrect x, and an over-wide line.

English and original coverage are each **27/27**, including both separate Ryugu Palace strings.
All full glossary names fit. Examples: Momotaro's Home x123, Kachi-Kachi
Village x120, Capital of the Moon x118, and Onigashima x137. Two enlarged
caption sheets contain every row in `coverage.tsv` order. Runtime textlog:
**0 Japanese lines in 27 English logs**.

## Rank Details findings

The native route is saved Status -> first icon -> Circle, then Right through
all 43 pages, then Cross back to Status. It does not use the Game Album's
ordinary play-selection context. The main-menu saved-Status route enters mode
`0x4F` with context **4**, stored at `0x800A3F8F`; the initial hypothesis of
context 3 was rejected by both discs. `OVLXTTL 0x800D8834` selects context 3
for a different Status entry and context 4 for this one. The harness asserts
context 4 on every accepted page and the restored Status cursor at return.

Page index is `0x8008C5C0`; UI-ready state is u16 `0x800E27FC == 1`.
The 43-entry table at `0x800E077C` supplies each real record ID at row +8.
The fixture seeds only the native record array (`0x800BDBF0`, stride 28):
played=1, rank=`record_id % 11`, score=9999. Empty-record mode uses rank 0 and
score `0xFFFFFFFF`. It never substitutes textures, ANM selectors, drawing
positions, getters or executable code. Ranks and scores are fixtures, not
achievements earned through gameplay.

Both populated cold tours pass **43/43**, with all **11 rank values (0-10)**,
and return to Status. The empty English tour also passes **43/43** and returns.
All source-card comparisons pass. Initial tours stopped
after page 16 on both discs when a short Right press was lost at a loading
boundary. The harness now retries only if the immediately preceding page
remains in its native ready state; it rejects a skipped page. Timeout checks
run before any early return, so a stall cannot silently become a successful
fixed-frame emulator exit. The final tours also needed bounded-condition
retries at later pages; these are input timing, not translated text failures.

**The actual native header is Game Album, on both discs.** Original comparison
confirms this even in Status's read-only viewing context. YUGI0D:4 item 2 contains
the separate Rank Details artwork, but this route binds the ordinary Game
Album title. Do not claim that the Rank Details atlas title was shown, or alter
the working header just to make a static survey match an assumption. Name
Entry/Quick Match header coverage and any remaining dormant title consumers
remain distinct from this record-view route.

The four panel sheets show all pages, including Rank: ----, Level 1-9 and
Full Mastery. Full names, record units, time fields and borders are intact.
The original comparison confirms the inherited art and layout; the existing
English numeric-position fixes keep text inside the frame. Runtime textlog:
**0 Japanese lines in the populated English tour**.

## Remaining Card Album notice investigation

HOUGEN0D:0's red notice fragments still have no runtime proof. Both local ANM
tables (entries 5/6) omit them; the background tile table (entry 3) and map
(entry 4) use only the top peach-pattern rows, not these fragments. A page-5
search in unrelated archives is not evidence: the same VRAM page is reused by
many other textures. This investigation does not establish native-code
unreachability, and the notice remains open and unchanged.

## Review and validation

Fresh read-only D10 review accepts **10/10 record sheets** and **3/3 caption
sheets**. The verdict files are each `verdicts/01_readonly.tsv` under
`work/qa/details8_review` and `work/qa/captions8_review`. Both `qa_gate.py check`
commands exit 0, with no missing, stale or issue verdicts. Every approval is
scoped to these captures; none replaces the phase-wide manifest.

| Record sheet | SHA-1 | Verdict |
|---|---|---|
| navigation_sheet | e3c2b1f7ca3244764ad27633dc37cb93c2a89862 | ok: Status entry/return and complete header |
| panels_sheet | d2c58bd4c956ce318398229dce15425278e5528b | ok: pages 00-11 |
| panels_sheet_2 | 7aaa726971fd49c8be37b25a73af98002f7276da | ok: pages 12-23 |
| panels_sheet_3 | 4dfeeda6bd2e79c236ecef3ae145c7923a1f9fed | ok: pages 24-35 |
| panels_sheet_4 | a34009b0fb96f1c22fa71238828ca81f7c607b56 | ok: pages 36-42 |
| original_compare_sheet | 90e5cea23df65fbff1f098fb61b1df7927f5f07b | ok: original title/art comparison |
| empty_sheet | ac32156305c88a23ffc24c049f86ebbcec9d43ff | ok: pages 00-11, empty records |
| empty_sheet_2 | b45e4d19af19d993f50a62767801ae943797114b | ok: pages 12-23, empty records |
| empty_sheet_3 | c0030a39ee6fef8cebd9b9a816dd4198873580a4 | ok: pages 24-35, empty records |
| empty_sheet_4 | e1ec6c39752b2b20cffb18637548bf004d2c308f | ok: pages 36-42, empty records |

| Caption sheet | SHA-1 | Verdict |
|---|---|---|
| captions_sheet | 243b1ef3b9212e97976214bfc1ab7b613d3a97e2 | ok: captions 01-15 |
| captions_sheet_2 | 78fdf3bb6fed577c64fba24558ec42fee41041ad | ok: captions 16-27 |
| original_compare_sheet | 9dcb4a27b152f51881017fe00f9b49609729e80f | ok: longest caption, original comparison |

`tools/check.py`: **99 tests passed**, **0 lint errors**. `verify_build.py`:
**369 changed files, 0 errors**. Cold smoke at
`work/qa/caption_details8_smoke`: **passed**. The 27 caption logs plus populated
and empty Rank Details logs contain **0 Japanese lines in 29 English logs**;
this logger does not inspect graphics text.

This checkpoint changes QA tools and documentation only. The existing main
disc remains **182,482,272 bytes**, built **2026-11-01 09:45:58 UTC**, SHA-1
**81f569029bc195b8ea7e8bdb725b1de469099a43**, reverified and cold-smoked here.
No release artifact was generated, and phase 8 cannot advance yet.

Skill gotcha for `references/emulator-qa.md`: a warp's own opening-frame
confirmation press can dismiss an injected caption before capture; delay that
press and assert the actual line object and text. Saved-Status record viewing
uses a different native context from playable Game Album despite sharing its
header. No shared skill files were changed.
