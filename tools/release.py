"""Build and verify a local patch-only release (xdelta + README in a zip); never publishes.

usage: python -X utf8 tools/release.py [--version 1.0] [--force] [--xdelta PATH]

Stops at the first failure: build -> check.py -> verify_build.py -> cold smoke -> jp_left.py (Japanese runs
unchanged from the original, minus docs/re/jp_known.txt) -> story chapters regenerated -> qa_gate.py check on every
work/qa/**/manifest.tsv -> docs/polish.md fully ticked -> xdelta3 patch -> re-apply to the original and compare ->
zip. The debug tool is external Lua (tools/debug/), never built into the image. Output: release/v<version>/.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from skill import SKILL  # noqa: E402
import story  # noqa: E402

PY = [sys.executable, '-X', 'utf8']
IMAGE = ROOT / 'build/momotarou-matsuri_en.bin'
CUE = IMAGE.with_suffix('.cue')
ORIGINAL = ROOT / 'rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).bin'
QA = ROOT / 'work/qa/release'


def run(*args):
    subprocess.run([str(a) for a in args], cwd=ROOT, check=True)


def py(*args):
    run(*PY, *args)


def hashes(path):
    h = {'md5': hashlib.md5(), 'sha1': hashlib.sha1()}
    crc, size = 0, 0
    with open(path, 'rb') as f:
        while chunk := f.read(1 << 22):
            crc = zlib.crc32(chunk, crc)
            size += len(chunk)
            for x in h.values():
                x.update(chunk)
    return {'size': size, 'crc32': f'{crc:08X}', **{k: v.hexdigest() for k, v in h.items()}}


def polish_check(text):
    if re.search(r'^\s*- \[ \]', text, re.M) or not re.search(r'^\s*- \[x\]', text, re.M):
        raise SystemExit('docs/polish.md is empty or has unticked lines')


def gates():
    qa_gate = Path(SKILL) / 'scripts/qa_gate.py'
    story.generate(str(ROOT / 'work/qa/story/chapters'))
    py(qa_gate, 'init', ROOT / 'work/qa/story/manifest.tsv', ROOT / 'work/qa/story/chapters', '--glob', '*.txt')
    manifests = sorted((ROOT / 'work/qa').glob('**/manifest.tsv'))
    assert any(m.parent.name == 'story' for m in manifests), 'no story manifest'
    for m in manifests:
        py(qa_gate, 'check', m, m.parent / 'verdicts')  # same rule as the publish guard
    polish_check((ROOT / 'docs/polish.md').read_text(encoding='utf-8'))


def package(version, xdelta, force):
    folder = ROOT / 'release' / f'v{version}'
    stem = f'Momotarou_Matsuri_EN_v{version}'
    patch, readme, archive, proof = (folder / f'{stem}.xdelta', folder / 'README.txt', folder / f'{stem}.zip',
                                     folder / 'verification.json')
    if not force and any(p.exists() for p in (patch, readme, archive, proof)):
        raise SystemExit(f'{folder}: version exists; use --force to replace it')
    folder.mkdir(parents=True, exist_ok=True)
    proof.unlink(missing_ok=True)
    run(xdelta, '-f', '-e', '-9', '-s', ORIGINAL, IMAGE, patch)
    again = ROOT / 'build/momotarou-matsuri_reapplied.bin'
    run(xdelta, '-f', '-d', '-s', ORIGINAL, patch, again)
    wanted = hashes(IMAGE)
    if hashes(again) != wanted:
        raise SystemExit('re-applied patch differs from the built image')
    again.unlink()
    base = hashes(ORIGINAL)
    text = (ROOT / 'docs/release-readme.txt').read_text(encoding='utf-8')
    values = {'VERSION': version, 'PATCH': patch.name, **{f'BASE_{k.upper()}': str(v) for k, v in base.items()},
              **{f'PATCHED_{k.upper()}': str(v) for k, v in wanted.items()}}
    for k, v in values.items():
        text = text.replace(f'@{k}@', v)
    if re.search(r'@[A-Z_]+@', text):
        raise SystemExit('unresolved README placeholder')
    readme.write_text(text, encoding='utf-8', newline='\r\n')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_STORED) as z:
        z.write(patch, patch.name)
        z.write(readme, readme.name)
    with zipfile.ZipFile(archive) as z:
        assert sorted(z.namelist()) == sorted([patch.name, readme.name]) and z.testzip() is None
    proof.write_text(json.dumps({'version': version, 'base': base, 'patched': wanted,
                                 'patch_sha1': hashes(patch)['sha1'], 'zip_sha1': hashes(archive)['sha1'],
                                 'reapplied_identical': True, 'published': False}, indent=2) + '\n',
                     encoding='utf-8')
    print(f'Verified local release: {archive}\nPatched SHA-1: {wanted["sha1"]}')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--version', default='1.0')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--xdelta', default=shutil.which('xdelta3'))
    args = ap.parse_args(argv)
    if not re.fullmatch(r'\d+\.\d+(\.\d+)?', args.version):
        ap.error('version must be X.Y or X.Y.Z')
    if not args.xdelta:
        ap.error('xdelta3 not on PATH; pass --xdelta')
    folder = ROOT / 'release' / f'v{args.version}'
    if folder.is_dir() and any(folder.iterdir()) and not args.force:
        ap.error(f'{folder} already has files; use --force')
    py(ROOT / 'tools/build.py')
    py(ROOT / 'tools/check.py')
    py(ROOT / 'tools/verify_build.py', CUE)
    py(Path(SKILL) / 'scripts/emu.py', CUE, '--out', QA / 'smoke', '--route', ROOT / 'tools/routes/boot.txt', '--smoke')
    py(Path(SKILL) / 'scripts/jp_left.py', IMAGE, '--orig', ORIGINAL, '--sjis', '--min', '4',
       '--known', ROOT / 'docs/re/jp_known.txt')
    gates()
    package(args.version, args.xdelta, args.force)


if __name__ == '__main__':
    main()
