# Latin player names, 2026-11-01

Phase 8 checkpoint. This is Name Entry and its Quick Match record display,
not natural record-setting, memory-card persistence or the full graphics gate.
Follow-up: `name-persistence-qa.md` now verifies four- and one-character name
save/overwrite/cold-reload on both discs. Natural record-setting remains open.

## Encoding and implementation

Name Entry is mode `0x51`, initialized by `OVLXTTL:0x800DF8A4`. It does not
use the text codec or show a keyboard. Each of four positions selects one of
80 sprite IDs with the D-pad. Circle advances to the next position; Cross
returns to the preceding position; the fourth Circle opens confirmation.
Start finishes before the currently selected position. The native four-character
limit is unchanged; this is a player-entered record name, not a shortened
translation of a character's name.

`tools/name_entry.py` defines a stable 80-character alphabet: A-Z, a-z, 0-9,
space and 17 punctuation marks. Every existing 16x16 glyph cell is redrawn with
the project's MIT `fonts/en12.txt`, in the original yellow palette colour.
The source atlas is NAME0D:1; the whole-archive identical-image sweep finds
PREM0D:1 as its only duplicate. Both are generated and built. NAME0D ANM 6
and PREM0D ANM 12 contain the same 80 records, and remain byte-identical.
Panel artwork, arrows, palettes, sprite placement and executable instructions
are unchanged.

The 19x10 signed-word selection table at `0x800E0D6C` originally has irregular
kana columns. Its replacement has eight rows of ten sequential IDs, followed
by eleven all-`-1` sentinel rows. The native D-pad logic now navigates the
alphabet in order, with horizontal and vertical wrap. The original 760 bytes
are checked before patching; the disc verifier allows only that exact table.
Tests check all 80 glyph masks, both font copies and unchanged pixels outside
the cells, plus the complete table and revision guard.

Names are stored at `0x800BDBFC + record_id * 0x1C`: four one-byte IDs followed
by four FF bytes. Native getter `0x8004269C`, setter `0x80042740` and Quick Match
sprite renderer `OVLXTTL:0x800DC800` are unchanged. **Existing Japanese record
names are reinterpreted as Latin characters**, because the IDs retain their
numeric values. This is not a save-format conversion. The owner supplied no
existing saves (D7); do not claim preservation of Japanese name spelling when
documenting save compatibility.

## Cold route and evidence

```powershell
python -X utf8 tools/debug/name_entry.py --out work/qa/name8_final6
python -X utf8 tools/debug/name_entry.py --out work/qa/name8_original6 --original
python -X utf8 tools/debug/name_entry.py --out work/qa/name8_short_final --short
python -X utf8 tools/debug/name_entry.py --out work/qa/name8_short_original --original --short
```

`name_entry` is scene 465. The warp substitutes mode 0x51 at the existing
Quick Match transition, then lets the real loader construct the screen.
The optional context argument sets `0x800A3F40 + mode` to 3. This is the
mode-context array read by native `0x8001EE10`; Name Entry returns to Quick
Match unless its context is 1. Omitting this selects the special 0x61 return
path. Setting the mode while a menu is already idle only changes its RAM tag
and leaves the old menu visible; that discarded attempt is not QA evidence.

After loading, `name_entry.lua` only reads state and sends controller input.
It traverses every ID using the live selection table, records each complete
glyph, enters IDs 0/51/61/66 (**Az9!** in English), rejects confirmation,
returns to the third position with Cross, restores the fourth character,
accepts, and verifies all eight stored bytes on return to Quick Match.
No glyph, selector, character buffer, executable instruction or record byte is
written by this probe. The original comparison enters the same IDs, which
naturally display different letters. Scores remain empty; this is a loader
fixture, not an earned high score or a memory-card save/reload test.

State addresses: u16 editor state `0x800E2D78`; active position u32
`0x800E30D8`; four position objects `0x800E2E38 + 0x1C * slot`, with sprite ID
u16 at +6, column/row u16 at +16/+18, and blink counter u32 at +24. Record ID
is `0x8008C564`. Screenshots wait for a visible blink phase, while advancement
waits for the game's actual active position/state. Short fixed taps and
blindly advancing the fixture's own index produced incomplete original routes.
Confirmation defaults to Yes; an unconditional Up wraps it to No.

The Python check requires ordered IDs 0-79, all screenshots, reject/back/return
markers, and complete glyph-pixel matches inside the actual first-position
region. Only the known space ID may be blank. The matcher rejected an early
tour's two blink-off screenshots (78/80). Return-byte assertions run inside
the emulator. Visual review is still required for the complete UI and name.

## Review and validation

Both complete tours pass **80/80 image matches**, ordered glyph coverage,
rejection/back/edit/accept and the eight-byte name-buffer assertion. Both short
tours pass Start/accept/return with ID 25 (**Z** in English), followed by seven
FF bytes. Runtime record rendering is directly shown for these five IDs; the
other 75 have Name Entry image proof and share identical native ANM records
with the record font, but were not each entered as a saved record.

An initial read-only review found the project's `@` glyph is a heart icon.
ID 77 now uses the actual asterisk instead, and the final disc and cold tour
were regenerated. After that change, a fresh read-only pass opened all four
final sheets, checked every glyph and compared the full UI against the original.
English title/instructions/confirmation fit, all name letters are complete,
and panels, arrows and unrelated art match. `qa_gate.py check` accepts **4/4**.

| Sheet under `work/qa/name8_review/` | SHA-1 | Verdict |
|---|---|---|
| glyphs_sheet.png | 90382a8a69724184a642415a7ff4d82fc0213184 | ok, all 80 glyphs, space intentional |
| flow_sheet.png | db31450debffe1859750b4d5df549683dcbde154 | ok, full name, confirmation, rejection |
| flow_sheet_2.png | 29c9f678ed5fb59410c2f12aa4e05995b878b597 | ok, editing, acceptance, Quick Match name |
| short_sheet.png | fcd2bfe0141fb5fad22798cf5acd67e91cad5c35 | ok, Start shortcut and single-letter record |

Recreate the glyph sheet with `sheet.py 'work/qa/name8_final6/glyph_*.png'
--crop 88,94,20,20 --zoom 4 --cols 10 --max 80`. The flow sheets use the six
shots `slot_4`, `confirm`, `declined`, `back`, `accept`, `record_name`, in that
order, with `--compare work/qa/name8_original6 --zoom 2 --cols 1 --max 3`.
The short sheet uses `accept` and `record_name` from the short tours.

- `tools/check.py`: **84 tests passed**, lint **0 errors**.
- `tools/verify_build.py`: **369 changed files**, **0 errors**.
- Cold smoke: `work/qa/name8_final_smoke`, **smoke ok**.
- Both final English tours: **0 Japanese lines**, one nonempty log each.
- Main disc: **182,482,272 bytes**, **2026-11-01 08:20:36 UTC**, SHA-1
  **8781edd1b47f4a947cb90197dbb65e9ac6730b17**.

Rank Details, natural high-score-to-name progression and memory-card persistence
remain open, along with the wider phase 8 graphics and story gates. The release
README must mention reinterpretation of pre-existing Japanese record names.
**Do not advance to phase 9.**

Tooling gotcha for the skill's `references/emulator-qa.md`: PCSX screenshot
requests can already be logged while their converted PNGs are still absent;
wait for `emu.py` to exit before inspecting or judging missing screenshots.
This session did not modify the shared translation skill.
