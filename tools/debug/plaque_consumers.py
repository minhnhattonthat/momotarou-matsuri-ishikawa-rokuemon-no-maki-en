"""Print static map consumers of engraved roof plaques; navigation leads only.

    python tools/debug/plaque_consumers.py tea

Unreferenced tiles and background layers are not runtime visibility verdicts.
"""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gfx_signs
from field_consumers import inspect


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('label', choices=('inn', 'tea', 'bank'))
    args = parser.parse_args()
    atlases = {'inn': gfx_signs.INN_ATLASES, 'tea': gfx_signs.TEA_ATLASES,
              'bank': gfx_signs.BANK_ATLASES}[args.label]
    for stem, positions in atlases.items():
        for x, y in positions:
            owners, rows = inspect(stem + '.BIN:0', (x, y, x + 13, y + 13))
            print(stem, owners, [(r[0], r[4], r[-1]) for r in rows if r[-1]])


if __name__ == '__main__':
    main()
