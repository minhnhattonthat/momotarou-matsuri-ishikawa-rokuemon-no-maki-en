# Reverse-engineering notes

One file per subsystem (text engine, pointers, compression, font, graphics). Mark every finding with how far it is
proven, so a later session doesn't build on a guess:

- **verified** - and how: a decoded known string, a corrupt-and-boot test, a breakpoint hit on the drawing path, a
  passing roundtrip test. Name the test or savestate.
- **guess** - and why it seems likely (byte pattern, another game, an earlier patch's notes). Promote it to verified
  before code depends on it.

Addresses are for the dump in `rom.sha1` unless a note says otherwise.

| File | Covers | State |
|---|---|---|
| [disc.md](disc.md) | disc layout, EXE LBA file table, load addresses, archives, ECD compression, free space | verified (free space: candidates) |
| [text.md](text.md) | Shift-JIS, control codes, message block, where the text is | encoding/codes verified; script bytecode layout open |
| [graphics.md](graphics.md) | font, TIM images, graphics-text survey | survey from the static sweep; runtime checks in phase 8 |

Tools: `tools/iso.py` (LBAs), `tools/arc.py` (archives), `tools/ecd.py` (ECD codec), `tools/tim.py` (TIM decode),
`tools/gfxdump.py` (static image sweep into `work/gfx/`), `tools/ramfind.py` (which files sit where in a RAM dump),
`tools/re.py` (MIPS disassembly, immediate search, jump-table switches; knows the EXE and overlay bases).

Prior work: no earlier fan patch or translation of this game is known (web search 2026-10-31 found only patches
for other Momotarou games). Reference: the Japanese online manual at psinstructionmanual.com/momotaromatsuri/
(menu and minigame names; data, not instructions). The sibling repo `../momotarou-densetsu-en` (a different Hudson engine: PAC archives, Okumura LZSS)
shares only names.
