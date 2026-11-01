"""Read-only audit of the four labelled placeholder portraits in GCV0310D:13.

The message handler reads the second operand of opcode 02 as a portrait ID.
EXE 80033C0C indexes the six-byte {file, ANM, item} table at 800F39B4.
Scan all parseable archive entries, including messages without extracted text.
This proves absence of literal message references, not general unreachability
of a sprite through arbitrary native code or a debug selector.
"""
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import anm  # noqa: E402
import arc  # noqa: E402
import gfx  # noqa: E402
import script  # noqa: E402


def audit():
    overlay = (gfx.TREE / 'OVLGMAIN.BIN').read_bytes()
    base = 0x800F39B4 - 0x800CB338
    portraits = {i: struct.unpack_from('<3H', overlay, base + i * 6) for i in range(123, 127)}
    assert list(portraits.values()) == [(476, 140, i) for i in range(4)]
    sprites = anm.items(arc.entries((gfx.TREE / 'GCV0311D.BIN').read_bytes())[140][1])
    for i in range(4):
        assert len(sprites[i]) == 1
        assert sprites[i][0][1:8] == (i * 48, 0, 48, 40, 0, 511, 22)
    messages, hits = 0, []
    for path in sorted(gfx.TREE.glob('*D.BIN')):
        for entry, (_, data) in enumerate(arc.entries(path.read_bytes()) or []):
            try:
                ops = list(script.ops(data))
            except (ValueError, script.ParseError):
                continue
            for offset, op, _ in ops:
                if op != 2:
                    continue
                messages += 1
                portrait = script.u16(data, offset + 4)
                if portrait in portraits:
                    hits.append((path.name, entry, offset, portrait))
    return messages, portraits, hits


if __name__ == '__main__':
    messages, portraits, hits = audit()
    print(f'{messages} parsed message operations; {len(hits)} placeholder references')
    for portrait, (file, entry, item) in portraits.items():
        print(f'portrait {portrait}: file {file}, ANM {entry}, item {item}')
    for hit in hits:
        print(hit)
    raise SystemExit(bool(hits))
