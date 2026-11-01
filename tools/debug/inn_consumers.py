"""Print static map consumers for every translated Inn plaque.

    python tools/debug/inn_consumers.py

Coordinates are navigation leads, never visibility verdicts. Several original
atlases retain unreferenced plaques or a second Inn hidden by the front layer.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gfx_signs
from field_consumers import inspect


def main():
    for stem, positions in gfx_signs.INN_ATLASES.items():
        for i, (x, y) in enumerate(positions):
            owners, rows = inspect(stem + '.BIN:0', (x, y, x + 13, y + 13))
            print(stem, i + 1, owners, [(r[0], r[4], r[-1]) for r in rows if r[-1]])


if __name__ == '__main__':
    main()
