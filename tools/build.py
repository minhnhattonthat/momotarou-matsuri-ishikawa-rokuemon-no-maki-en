"""build.py: original disc -> build/momotarou-matsuri_en.cue/.bin.

    python -X utf8 tools/build.py [--out build/NAME.bin]

Steps: check the dump (rom.sha1); unpack it once with dumpsxiso into work/disc/ (pristine, never edited);
collect changed files (patched_files(), empty until phase 4); rewrite the EXE LBA table from the layout mkpsxiso
will build (docs/re/disc.md: the game finds files by that table, not ISO9660); repack with mkpsxiso.
Changed files go to build/files/ and the generated build/layout.xml points those entries there; every other file
is read straight from work/disc/tree. With no changes the output is byte-identical to the original (tests/test_build.py).
"""
import argparse
import re
import shutil
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import check_rom  # noqa: E402

TOOLS = ROOT / "tools" / "mkpsxiso-2.30-win64"
DISC = ROOT / "work" / "disc"
TREE = DISC / "tree"
CUE = ROOT / "rom" / "Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue"
EXE = "SLPM_868.88"
TABLE, COUNT = 0x6F1B0, 1606  # EXE file offset, {u32 start LBA, u32 end LBA} pairs (disc.md)
SIZES, DATA = 0x6C9D8, 63  # EXE file offset (RAM 0x8007C1D8): u32 byte size per data id d = table index - 63;
# the loader 0x8001F3B0 allocates from it, so a grown file must update it (else it overruns the next buffer)


def unpack():
    """dumpsxiso the original into work/disc once (idempotent)."""
    if (DISC / "layout.xml").is_file() and (TREE / EXE).is_file():
        return
    DISC.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(TOOLS / "dumpsxiso.exe"), "-x", "tree", "-s", "layout.xml", str(CUE)], cwd=DISC, check=True,
                   stdout=subprocess.DEVNULL)


def patched_files(mode="en", overrides=None):
    """{disc path: new bytes} for every file the translation changes (tools/insert.py)."""
    import insert
    return insert.files(mode, overrides)


def write_layout(changed, files_dir, out_xml):
    """Copy work/disc/layout.xml with absolute sources; entries in `changed` read from files_dir instead."""
    tree = ET.parse(DISC / "layout.xml")
    root = tree.getroot()
    root.find("track/license").set("file", str(DISC / root.find("track/license").get("file")))
    dt = root.find("track/directory_tree")
    dt.set("source", str(TREE))

    def walk(node, path):
        for child in node:
            if child.tag == "dir":
                walk(child, path + child.get("name") + "/")
            elif child.tag == "file":
                p = path + child.get("name")
                if p in changed:
                    child.set("source", str(files_dir / p))
    walk(dt, "")
    tree.write(out_xml, encoding="utf-8", xml_declaration=True)


def lbas(layout):
    """{disc path: (lba, size)} that mkpsxiso will assign for this layout (-noisogen -lba)."""
    log = layout.with_suffix(".lba.txt")
    subprocess.run([str(TOOLS / "mkpsxiso.exe"), "-q", "-noisogen", "-lba", str(log), str(layout)], check=True,
                   stdout=subprocess.DEVNULL)
    out, dirs = {}, []
    for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^( +)(File|Dir) *\|([^|]*)\|([^|]*)\|([^|]*)\|[^|]*\|([^|]*)\|", line)
        if not m:
            continue
        depth = len(m.group(1)) - 5  # root rows are indented 5 spaces, one more per directory level
        dirs = dirs[:depth]
        name = m.group(3).strip()
        if m.group(2) == "Dir":
            dirs.append(name)
        else:
            out["/".join(dirs + [name])] = (int(m.group(5)), int(m.group(6)))
    return out


def rewrite_lba_table(exe, orig_lbas, new_lbas):
    """Point each EXE table entry at its file's new location and size. Entries are matched to files by original
    start LBA. Also rewrites the per-data-id byte size table (SIZES)."""
    by_lba = {lba: path for path, (lba, _) in orig_lbas.items() if not path.startswith("ZZZZ")}  # root pad: not in table
    exe = bytearray(exe)
    for i in range(COUNT):
        start, end = struct.unpack_from("<II", exe, TABLE + 8 * i)
        lba, size = new_lbas[by_lba[start]]
        struct.pack_into("<II", exe, TABLE + 8 * i, lba, lba + (size + 2047) // 2048)
        if i >= DATA:
            if struct.unpack_from("<I", exe, SIZES + 4 * (i - DATA))[0] != orig_lbas[by_lba[start]][1]:
                raise ValueError(f"size table entry {i - DATA} does not match {by_lba[start]}")
            struct.pack_into("<I", exe, SIZES + 4 * (i - DATA), size)
    return bytes(exe)


def build(out_bin, changed=None):
    check_rom.check()
    unpack()
    work = out_bin.parent / "files"
    shutil.rmtree(work, ignore_errors=True)
    changed = dict(patched_files() if changed is None else changed)
    exe = changed.get(EXE, (TREE / EXE).read_bytes())
    changed[EXE] = exe  # always rewritten: its LBA table follows the new layout
    layout = out_bin.parent / "layout.xml"
    write_layout({}, work, layout)
    orig_lbas = lbas(layout)
    for p, data in changed.items():
        (work / p).parent.mkdir(parents=True, exist_ok=True)
        (work / p).write_bytes(data)
    write_layout(changed, work, layout)
    new_lbas = lbas(layout)
    (work / EXE).write_bytes(rewrite_lba_table(exe, orig_lbas, new_lbas))  # same size, so no LBA moves
    subprocess.run([str(TOOLS / "mkpsxiso.exe"), "-q", "-y", "-o", str(out_bin), "-c", str(out_bin.with_suffix(".cue")),
                    str(layout)], check=True)
    return out_bin


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--marker", action="store_true", help="every text item as [n] marker (work/markers.tsv)")
    ap.add_argument("--qa", action="append", default=[], metavar="ID=TEXT", help="override one item (stress lines)")
    a = ap.parse_args()
    out = a.out or ROOT / "build" / ("momotarou-matsuri_marker.bin" if a.marker else "momotarou-matsuri_en.bin")
    out.parent.mkdir(parents=True, exist_ok=True)
    ov = dict(q.split("=", 1) for q in a.qa)
    ov = {k: v.replace("\\n", "\n") for k, v in ov.items()}
    print(build(out.resolve(), patched_files("marker" if a.marker else "en", ov)))
