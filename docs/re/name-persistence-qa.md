# Player-name persistence and overwrite prompt, 2026-11-01

Phase 8 checkpoint: controller-entered names survive the game's save and a
separate cold load. This closes the name-persistence gap from
`name-entry-qa.md`, not natural high-score progression or the full phase.

## Reproduction and scope

```powershell
python -X utf8 tools/debug/name_save.py --out work/qa/np_en
python -X utf8 tools/debug/name_save.py --out work/qa/np_jp --original
python -X utf8 tools/debug/name_save.py --out work/qa/np_short --short --save work/qa/np_en/write/memcard1.mcd
python -X utf8 tools/debug/name_save.py --out work/qa/np_sjp --original --short --save work/qa/np_jp/write/memcard1.mcd
python -X utf8 tools/debug/name_save_review.py
```

The initial seed is the game-written shrine fixture from `save_fixture.py`,
default `work/qa/save_fixture_checked/memcard1.mcd`. Each run uses `emu.py`
with a copied card. The wrapper proves its source card remains unchanged.
No file-format edits, checksum edits, record/name-byte writes, UI selectors,
glyph substitutions or executable edits are used by these probes.

The existing `name_entry` loader warp starts Name Entry. Its controller-only
probe enters IDs **0,51,61,66** (`Az9!` in English), rejects, edits and accepts.
`NAME_CONTINUE=true` lets the new driver take over after the verified return to
Quick Match; the normal name-entry tour still exits at that point by default.
Cross opens the native save question. The driver chooses Yes, dismisses the
game's advice, selects slot 1, accepts Use this file and the overwrite warning,
waits for Save complete, and returns to the main menu. The wrapper then starts
a **new emulator process from a cold boot**, loads that card and checks all
eight name bytes both after loading and on the rendered Quick Match page.

The short tests overwrite the preceding four-letter fixture with **Z** (ID 25),
finished using Start, followed by **seven FF bytes**. The complete-name tests
require four FF bytes after the four glyph IDs. Original-disc comparisons enter
the same IDs, which naturally display kana rather than the English letters.
All **four save/reload cases pass**, including the eight-byte comparisons and
full name screenshots. Scores remain empty; none of these names was earned by
setting a high score. An exploratory controller-only Daruma run did not reach
Name Entry and timed out, so it provides no natural-record coverage.

This starts from a new Quick Match session, not an existing Story session.
Saving over the shrine fixture changes its location from Dragon God Marsh to
Momotaro's Home, and Album/Status are disabled after loading the resulting file,
on **both original and English**. Do not count this as preservation or merging
of existing Story progress. The shared `status_saved.txt` load route ends on
disabled Status for this fixture; the driver instead enters the enabled Quick
Match item directly with controller input.

## Native state fields

- Record 0's eight-byte name: `0x800BDBFC`; encoding and native setter/getter
  are documented in `name-entry-qa.md`.
- Quick Match: mode `0x50`, u16 state `0x800E2ABC`, u32 page `0x8008C5B8`.
- Save: mode `0x4B`, u32 state `0x800E1F30`: 2 file selection, 3 Use this file,
  4 native card operation/overwrite confirmation, 6 Save complete. State 7 is
  an exit animation, not the Save complete input state.
- Use-file choice: u32 `0x800E1F28`, 1 No / 0 Yes. The overwrite question also
  defaults to No; the driver changes it once before confirming.
- Native script's active op: u16 `0x800BF7FC`; wait for op 4 before answering
  Quick Match's save question, then dismiss its op-2 advice message.

An early driver waited for state 7 and stalled after a successful write. Other
exploratory runs exited with PCSX heap error `0xC0000374`; those are rejected
as QA runs. The four accepted directories above each have zero emulator exits
for both write and reload, and the successful cold reload is the persistence
proof. The cause of the intermittent emulator exit error is not established.

## Fixed overwrite-message bug

Before the fix, the overwrite warning displayed **`Is that ?`**, despite its
translation being `Is that OK?`. The native memory-card byte scanner at
EXE `0x80025884..0x80025910` branches on **every uppercase K byte** at
`0x800258D0`. It removes the K and advances the line even without a complete
KK/KE token, leaving the preceding O as an incomplete text unit. OVLXTTL has
the same scanner at `0x800D2C84..0x800D2D10`.

`SLPM_868@80018480` now says **`Is that okay?`**, preserving the complete meaning
inside the original 51-byte space. No native code or graphics changed.
`layout.render_line` rejects a literal K byte, including an explicit raw byte,
inside every `{KE}`-terminated message. A full sweep of **25 messages** found
only this one offending translation. The same scanner also treats uppercase
E immediately after KK as an end, and a full 64-byte line leaves no zero-filled
terminator; the lint now rejects those cases too. All current messages pass.

Seven regression cases in `tests/test_memory_messages.py` include the exact
broken overwrite string, K at the beginning and as a raw byte, the two further
scanner constraints, and valid delimiters/lowercase k/62-byte text. The relevant
cases failed against the old validation before the fix. The cold save wrapper
also requires the complete **`Is that okay?`** renderer log and screenshot.

## Fresh read-only visual pass (D10)

After freezing the final assets, the worker opened all six comparison sheets
at 2x zoom. The full and shortened names, prompts, cursor choices, file metadata
and menu returns are complete and fit their original panels. The original
comparisons confirm unchanged unrelated artwork and disabled-menu behavior.
These are **scoped text/name verdicts**: the Japanese lantern logos remain
outside this approval and retain the graphics survey's existing classification
work. No claim of whole-screen Japanese removal is made.

`qa_gate.py check work/qa/np_review/manifest.tsv work/qa/np_review/verdicts`
accepts **6/6**, with no stale or missing verdicts.

| Sheet under `work/qa/np_review/` | SHA-1 | Verdict |
|---|---|---|
| save_sheet.png | 2dbd10e3be0b3e10f5afd5af40d53eaef3009fb5 | ok, full name, save choice and advice |
| save_sheet_2.png | b1673f8179c68ff545ad82be3fa67c83969739e6 | ok, file selection and fixed overwrite text |
| save_sheet_3.png | f46bc7e8e17182b92b272e2e3915373cace82564 | ok, save completion and native menu return |
| reload_sheet.png | dc30262d063bdc7a057ab2d795b4e63258c1c8f5 | ok, cold-loaded full name |
| short_write_sheet.png | 038f5515e9287a6d68f64242b3e67372a44c612d | ok, short name and overwrite text |
| short_reload_sheet.png | 4f75050fc622e150a6317262caf33e151737f4ad | ok, cold-loaded Z with no trailing glyphs |

Validation: `tools/check.py` **91 tests, lint 0**; disc verifier **369 changed
files, 0 errors**; cold smoke `work/qa/persist8_smoke` **passed**. Both English
write/reload pairs contain **0 Japanese lines in four nonempty logs**; the
logger excludes graphics. Main disc: **182,482,272 bytes**, **2026-11-01
08:36:29 UTC**, SHA-1 **dca819a139f5c9ccba906a1e083f764e46077269**.

Rank Details, naturally earned record/name transitions, remaining graphics,
caption scenes and corrected map/story interaction coverage are still open.
**Phase 8 is incomplete; do not advance to phase 9.**
