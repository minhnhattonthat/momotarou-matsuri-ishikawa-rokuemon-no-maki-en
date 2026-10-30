# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** Step 0 (setup) done; next is phase 1 (research and recon). No build yet.
- **Done (2026-10-31, Step 0):**
  - Dump pinned: `rom.sha1` (the .bin; `tools/check_rom.py` passes). Single MODE2/2352 data track, 182,816,256 bytes.
  - PCSX-Redux nightly 29999.20261030.11 in `tools/pcsx/`, SCPH-5500 BIOS in `tools/bios/`. Original boots headless:
    `emu.py rom/...cue --route tools/routes/boot.txt --smoke` exits 0 and ends on the New/Continue menu
    (初めて / 続き), proving scripted pad input; a `--script` probe's `L.log` lands in `log.txt`.
  - Title accepts Start only from ~frame 2400 (Hudson logo, festival intro, title); earlier presses are ignored.
  - Disc tools copied in: `tools/mkpsxiso-2.30-win64/` (dumpsxiso, mkpsxiso), `tools/armips/`; xdelta3 on PATH.
  - `tools/check.py` (pytest on `tests/`) gates commits through `tools/hooks/pre-commit`
    (`git config core.hooksPath tools/hooks`); a failing canary test was rejected. Guard hook (plugin) blocks
    `sed -i` (canary checked). `tools/tbl.py`, `tools/romdiff.py`, `tools/skill.py` copied from the skill.
- **Next:** phase 1 recon: `dumpsxiso` the disc into `work/disc/`, list files, find the main EXE, text encoding
  (Shift-JIS likely), archives/compression, pointer tables, font; survey graphics text (title logo, menus, banners).
  Write findings to `docs/re/`. Check for any earlier fan patch (none known).
- **Open bugs:** none.
- **Waiting on the user:** GUI keyboard input in `tools/pcsx/` not proven by hand (headless-only runs; default
  keyboard bindings copied to `tools/pcsx/pcsx.json` from `tools/emu-config/pcsx.json`). Non-blocking; check when
  playtesting.
