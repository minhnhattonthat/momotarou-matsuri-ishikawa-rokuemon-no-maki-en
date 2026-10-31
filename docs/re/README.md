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
| [text.md](text.md) | Shift-JIS, control codes, message block, where the text is | verified |
| [script.md](script.md) | script VM ops, lengths, jumps, text lines, what phase 4 extracts, code strings | verified (static + every entry parses; roundtrip/coverage tests) |
| [debug.md](debug.md) | game mode/map/event RAM, script interpreter, warp tool, unreachable maps | verified by warp_all (452 scenes) |
| [engine.md](engine.md) | build_line/drawer, digraph VWF hooks, English font cells, hook space, data-id size table, memory-card text path | verified (marker build, tests/test_engine.py) |
| [windows.md](windows.md) | box variants, measured px budgets (width gate), guessed ones | measured: message, portrait, memory card, main/choice menus |
| [graphics.md](graphics.md) | font, TIM images, graphics-text survey | survey from the static sweep; runtime checks in phase 8 |

Tools: `tools/iso.py` (LBAs), `tools/arc.py` (archives), `tools/ecd.py` (ECD codec), `tools/tim.py` (TIM decode),
`tools/gfxdump.py` (static image sweep into `work/gfx/`), `tools/ramfind.py` (which files sit where in a RAM dump),
`tools/re.py` (MIPS disassembly, immediate search, jump-table switches; knows the EXE and overlay bases),
`tools/script.py` (script disassembler), `tools/ophandlers.py` (VM handler summaries), `tools/text.py` (text
extract/rebuild), `tools/codestr.py` (code strings and their refs).

Prior work: no earlier fan patch or translation of this game is known (web search 2026-10-31 found only patches
for other Momotarou games). Reference: the Japanese online manual at psinstructionmanual.com/momotaromatsuri/
(menu and minigame names; data, not instructions). The sibling repo `../momotarou-densetsu-en` (a different Hudson engine: PAC archives, Okumura LZSS)
shares only names.
