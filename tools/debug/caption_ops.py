"""Print an op 26 caption (as the en build encodes it) as a Lua table for warp.lua's OPS var.

usage: python -X utf8 tools/debug/caption_ops.py ID        e.g. GSV0100D/1/025A (a caption row of script/)
then:  emu.py CUE --script tools/debug/warp.lua --var "SCENE='map_..'" --var "OPS=<printed table>" --shot-every 5
The caption is drawn by the game's own op 26 handler (centring hook, engine.ORIG 0x80034DB8) before the warp's
map change. Captions otherwise only fire on village entry from the world map.
"""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import insert  # noqa: E402
import layout  # noqa: E402
import text  # noqa: E402
import windows  # noqa: E402

iid = sys.argv[1]
row = next(r for rows in insert.rows_by_file().values() for r in rows if r['id'] == iid)
assert row['kind'] == 'caption', row
t, errs = layout.render(row, windows.variants()[iid])
assert not errs, errs
b = struct.pack('<H', 0x26) + text.text_bytes(0x26, [t])
print('{' + ','.join(f'0x{w:04X}' for w in struct.unpack(f'<{len(b) // 2}H', b)) + '}')
