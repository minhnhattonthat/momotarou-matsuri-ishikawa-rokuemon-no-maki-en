# Text

## Encoding (verified)
- **Shift-JIS** (cp932), full-width only in dialogue. Verified: the trial-match prompt on screen
  (`work/qa/explore1/f003600.png`, "ダルマおとし を / 始めますか？") is PREM0D.BIN entry 13 decoded with cp932
  (`MM　をKG` / `始めますか？KG` / `　KN`), and a read watch on its RAM copy (0x8011D220..) fires from the message
  window code during that frame window (`work/qa/watch1/log.txt`).
- Each line is NUL-terminated and padded to an even length (lines are u16-aligned: `...KG 00 00`).
- No custom table needed: `tbl/` will hold a cp932-equivalent table only if phase 4 wants one for the codec.

## Control codes (ASCII pairs inside lines; counts over all script files)
| Code | Count | Meaning (guess unless marked) |
|---|---|---|
| `KG` | 11,674 | end of line (newline); verified: renderer EXE 0x8002C024 compares glyph code 0x474B |
| `KP` | 3,742 | page break / wait for button (renderer compares 0x504B) |
| `KN` | 1,084 | end of message, keep window (choice follows); renderer compares 0x4E4B |
| `bb` .. `ww` | 1,352 | colour on (blue?) .. colour back to white |
| `rr`, `oo` | few | other colours (red, orange?) closed by `ww` |
| `MM` | 88 | insert a name (minigame or player); e.g. `bbMMwwを　すてた！` |
| `R0`..`R3` | 16 | insert a number (money 両, seconds 秒) |
- Continuation lines start with a full-width space `　` (U+3000, 0x8140); a page/message ends on a line holding
  `　` + `KP`/`KN`, or a bare `　` line. The English layout plan (indent or not) is phase 5's.
- The renderer turns text into 8-byte glyph records (first u16 = SJIS code or control pair) before drawing;
  window state block at 0x800BF7B8 (`message_open` below).

## Message block (verified by the read watch above)
`u16 a, u16 2, u16 1, u16 voice (0xFFFF = none), lines...`. `a` is stored at window+0x44 (meaning unknown:
0x16 in most stand-alone messages; other values inside scripts). The window code reads +0, +2, +4, +6, then text.
- `message_open(file_id, entry)` = EXE 0x8002B864 (31 callers in the EXE). It gets the pointer from
  `file_entry(file_id, entry)` = EXE 0x8001F2CC: 32 loaded-file slots at 0x800A3DE0 `{u32 base, u16 id}`,
  returns `base + offs[entry]` (archive table, disc.md). So stand-alone messages are whole archive entries
  (PREM0D, YUGI0D, NAME0D, many EVT entries) and can grow once the archive is repacked.

## Where the text is (SJIS run scan, `kana >= 1/3` filter; duplicates included)
| Files | JP chars | Form |
|---|---|---|
| GSV????D.BIN (299, board-game event scripts by map/area) | ~100,800 | script bytecode entries with inline message blocks (entries 0-11) |
| M???D.BIN (58, one per minigame) | ~51,700 | rules/explanations + minigame dialogue, message blocks in entries 2-13 |
| GSF????D.BIN (37) | ~20,800 | script bytecode with inline messages (entries 1-24) |
| EVT???D.BIN (37, story events) | ~5,700 | stand-alone message entries (`16 00 02 00 01 00 ff ff ...`) |
| GDEF0D/1D.BIN | ~4,100 | shared board messages; entry 0 = table `{u16 a, u16 0x0D, u32 n}` then scripts |
| GSS????D.BIN (11) | ~3,600 | scripts with inline messages |
| PREM0D, YUGI0D, NAME0D | ~400 | stand-alone message entries (menus of minigame trial, name entry) |
| OVLGMAIN.BIN | ~3,300 | strings in code overlay (board UI: items, cards, menus) |
| OVLXTTL.BIN | ~1,400 | title/mode menus (`初めて　　　　続き`, `おためし対戦！`, minigame titles and ranks) |
| OVLM??.BIN (58), OVLEVT.BIN, SLPM_868.88 | ~900 + EXE 213 runs | strings in code (minigame HUD, system messages) |

## Resolved in phase 4 (script.md)
- The "message block" above is two ops: `16` (open window) then `02 mode voice` + text lines; `a` is the opcode.
  Scripts are VM bytecode with byte-offset jumps (05-0A if-blocks, 0D-13 branches): script.md lists every op's
  length; `tools/text.py rebuild` moves the jumps when text grows.
- Code strings: reached by pointer words and `lui`/`addiu` pairs, both found by `tools/codestr.py`.
