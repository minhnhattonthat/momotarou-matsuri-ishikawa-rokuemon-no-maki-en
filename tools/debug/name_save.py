"""Enter a name, save over a disposable existing file, cold-reload, verify all bytes.

Requires the game-written fixture from save_fixture.py. Neither the seed card
nor any record/name bytes are written by the probe. --original compares the
same native character IDs, which have different spellings on the two discs.
"""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from skill import SKILL  # noqa: E402


def run(cue, out, card, scripts, extra):
    out.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
               '--out', str(out), '--sav', str(card), '--timeout', '360']
    for script in scripts + ['tools/debug/name_save.lua', 'tools/lua/textlog.lua']:
        command += ['--script', str(ROOT / script)]
    result = subprocess.run(command + extra, capture_output=True, text=True, encoding='utf-8')
    (out / 'harness.log').write_text(result.stdout + result.stderr, encoding='utf-8')
    if result.returncode:
        print(result.stdout + result.stderr)
        raise RuntimeError(f'emulator failed in {out}: {result.returncode}')
    return (out / 'log.txt').read_text(encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--original', action='store_true')
    ap.add_argument('--short', action='store_true')
    ap.add_argument('--save', type=Path, default=ROOT / 'work/qa/save_fixture_checked/memcard1.mcd')
    args = ap.parse_args()
    before = args.save.read_bytes()
    cue = ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue' if args.original
                  else 'build/momotarou-matsuri_en.cue')
    variables = ['--var', f'NAME_SHORT={str(args.short).lower()}']
    written = args.out / 'write'
    try:
        log = run(cue, written, args.save,
                  ['tools/debug/warp.lua', 'tools/debug/name_entry.lua'],
                  ['--var', "SCENE='name_entry'", '--var', 'HOLD=-1', '--var', 'NAME_QUICK=true',
                   '--var', 'NAME_CONTINUE=true', '--frames', '900'] + variables)
        for marker in ('NAME_OVERWRITE', 'NAME_SAVE_COMPLETE', 'NAME_SAVED_RETURN'):
            assert marker in log, f'missing save evidence: {marker}'
        if not args.original:
            assert 'Is that okay?' in log, 'overwrite question lost letters in the native scanner'
        for name in ('record_name', 'save_prompt', 'use_file', 'overwrite', 'save_complete', 'saved_return'):
            assert (written / f'{name}.png').exists(), f'missing save screenshot: {name}'
        saved = written / 'memcard1.mcd'
        assert saved.read_bytes() != before, 'game did not change its copied memory card'
        log = run(cue, args.out / 'reload', saved, [],
                  ['--route', str(ROOT / 'tools/routes/status_saved.txt'), '--var', 'NAME_RELOAD=true']
                  + variables)
        assert 'NAME_PERSISTENCE_OK' in log, 'name did not survive a cold load'
        assert (args.out / 'reload/reloaded_name.png').exists(), 'missing loaded-name screenshot'
        print('Name entered, overwritten in game, cold-loaded, all eight bytes verified')
        return 0
    finally:
        assert args.save.read_bytes() == before, 'source memory card changed'


if __name__ == '__main__':
    raise SystemExit(main())
