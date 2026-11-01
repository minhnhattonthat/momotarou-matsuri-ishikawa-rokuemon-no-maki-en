# Script VM bytecode and the text it carries

Code: `tools/script.py` (op lengths, jumps, disassembler), `tools/text.py` (text items, codec, rebuild, dump),
`tools/codestr.py` (C strings in code), `tools/ophandlers.py` (per-handler summary used to read the handlers).
Tests: `tests/test_text.py`.

## Interpreter (verified: static read + every script entry parses, see below)
- Loop EXE 0x8003698C: `handler = table[0x800830D0 + 4 * op]`, called with a pointer to the pc; a handler returns
  0 to run the next op this frame, non-zero to yield. Before the loop, `wait[0x80082F2C + 4 * VM[+0x44]]` runs for
  the op that yielded (it may move VM+4, the saved pc). VM state at 0x800BF7B8: +0 script base, +4 pc, +8 op start
  of the last if-op, +0x44 current op. 0x69 ops (0x00-0x68).
- An op is u16 words: opcode then operands. Lengths in `script.LEN` (from the handlers), variable ones:
  | Op | Form | Length |
  |---|---|---|
  | 02 | message: `02 mode voice` + text lines (below) | 6 + text |
  | 26 | caption: one text line | 2 + line |
  | 41 | menu: `41 n` + n text lines (choice items; 04 then picks) | 4 + lines |
  | 15 | `15 n` + n x 3 words | 4 + 6n |
  | 33 | `33 n` + n x 6 words | 4 + 12n |
  | 3F | `3F n` + n x 5 words | 4 + 10n |
  | 36 | `36 n` + n records `{type, a, ...}`: 8 words if type 3, else 4 | 4 + sum |
- No fall-through after 00 (end), 1E N (run script N of the table at GMAIN 0x800E480C: `{file id, entry}`),
  30/32/43 (switch to another script via a callee), 3B (restart the current script).
- **Jumps hold byte offsets from the op's own start** (forward only, `& 0xFFFE`):
  - 0D-13 `op var val off`: test var against val (==, !=, <, >, ...), if true go to `op + off` (0x8002D2C0).
  - 05-0A `op var val else end`: if-block. The handler yields; the next frame 0x8002CFD8 tests, and on false
    goes to `op + else + 2` (else != 0xFFFF) or `op + end + 2`. `else`/`end` point at the 2-byte marker ops
    0B (else: jump to the enclosing if's `end + 2`, via VM+8) and 0C (end: falls through).
  - No other op adds an operand to the pc (operand-vs-boundary scan of every op/operand position, plus reads of
    the 41, 42, 55, 66 handlers). One GSS0200 entry-2 branch has offset 0xFFFF (target past the entry: never
    taken, or a game bug); `text.rebuild` leaves such raw offsets alone.
- Scripts are reached by `(file id, entry)` (message_open, the 1E table), never by an offset into an entry, so an
  entry can grow if its archive header is rewritten (disc.md).

## Text lines (verified: renderer 0x8002BB50 / wait handler 0x8002BFD8, and the roundtrip test)
- A line is u16 units ended by a unit whose low byte is 0 (always 0x0000 in the data). The message line walker
  advances by `chars * 2 + 2` (0x80029DF4 counts them).
- After each line the last unit decides: KG next line, KP wait for a button then next line (page), KN end and
  keep the window (a choice or another op follows), anything else (an empty line, a bare `　`) end and close.
- Units: Shift-JIS, and ASCII-pair codes KG KP KN, bb rr oo dd ... ww (colour on .. white), MM (name), R0-R3
  (number). The EXE memory-card messages use KK (line) and KE (end) instead (a different renderer).
- GSV0300 entry 19 is a debug message `#MCLRALLCLR` (left as is).

## What `tools/text.py` extracts (verified by tests/test_text.py)
- Script entries = archive entries that parse to their exact end and hold a text op: 1,975 entries in GSV (795),
  M???D (≈700), GSF (123), EVT (96), GDEF (96), GSS (11), PREM, YUGI, NAME. 5,329 text ops: 4,894 messages,
  408 menus (1,601 items), 27 captions. Every one rebuilds byte-identical; grown text moves every jump with its op.
- Code strings: 1,156 NUL-terminated strings reached by a pointer word or a `lui`+`addiu/ori/load` pair, in the
  EXE (259), OVLGMAIN (503), OVLXTTL (276), OVLEVT (17) and 13 OVLM overlays. `max` = bytes up to the next string
  (in-place room). Longer English (OVLGMAIN, OVLXTTL only) moves at build into slack that shorter English
  leaves inside other strings' original Japanese bytes; every ref is repointed and the old place keeps a cut copy
  (`insert.patch_code`, test `test_long_overlay_string_moves_into_slack_and_every_ref_follows`). EXE and OVLM
  strings must fit `max`: slack is short there, and tools/deadcode.py "dead" EXE functions can run (0x80058A98
  ran in event00 under an exec watch, tools/lua/deadwatch.lua), so no code cave for strings.
- Coverage: every Shift-JIS run with >= 4 chars and >= 1/3 kana on the disc lies inside an extracted item, except
  8 runs checked as binary noise (listed in the test). A looser kanji-only scan (6+ chars, NUL- or code-ended,
  even offset) found only noise too (1,258 hits, all in graphics/sound data).
- Not covered: text drawn as graphics (graphics.md survey); strings built in code from glyph codes (the marker
  build will show any as leftover Japanese); single-character code strings (a lone kanji like 両 is rejected as
  instruction noise, also left to the marker build).

Phase 8 saved-record coverage correction: `codestr.is_jp` used to accept digit-slot templates only for 両.
The save selector exposed `      段`, `      時間`, and `    分`, which the kana/length filter rejected.
A sweep of every referenced code string also found paired 点/個/： templates in the two record screens:
11 newly extracted rows in OVLXTTL, now translated. Templates are recognised by an even, nonempty ASCII-space
prefix and a full-width suffix; unprefixed single-kanji instruction noise stays excluded. Preserve every
`[20]` slot so `put_number` still inserts digits correctly. Cold saved-Status route textlog now reports zero JP.
