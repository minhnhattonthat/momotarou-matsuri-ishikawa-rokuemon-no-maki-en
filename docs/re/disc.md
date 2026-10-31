# Disc, file table, archives, compression

## Disc (verified: `tools/iso.py` lists it; dumpsxiso 2.30 extracts it into `work/disc/tree`)
- One MODE2/2352 data track, ISO9660, volume SLPM_86888, Hudson, 2001-06-29. Boot `SLPM_868.88` (PS-X EXE,
  load 0x80010000, size 0x7C800, entry 0x80048D50, stack 0x801FFF00).
- `OUTBIN/` holds 1,607 files; `ZZZZMIN3.PAD` (38,000,000 bytes of ASCII '0') sits twice, in the root (LBA 24)
  and at the end of `OUTBIN/`: outer-ring filler, can shrink if the disc ever needs room.
- Unpack: `tools/mkpsxiso-2.30-win64/dumpsxiso.exe -x tree -s layout.xml <cue>` from `work/disc/`.
  File LBAs: `python tools/iso.py <bin>` (copy in `work/disc/lba.txt`).

## File table in the EXE (verified statically: all 1,606 pairs match the ISO directory)
- **The game finds files by an LBA table, not ISO9660** (no file names in the EXE). EXE file offset 0x6F1B0
  (RAM 0x8007E9B0), 1,606 x `{u32 start LBA, u32 end LBA}` with `end - start = ceil(size / 2048)`, in the game's
  own file-id order (entry 0 OVLSYS.BIN, 1 OVLTEST, 2 OVLGMAIN, 3 OVLXTTL, 4 OVLEVT, 5 OVLM00 ...), ends at 0x723E0.
  Every file but SYSTEM.CNF, the EXE and root ZZZZMIN3.PAD is in it.
- A rebuild that moves or grows any file must rewrite this table from the new layout: `tools/build.py` does it
  every build (mkpsxiso `-noisogen -lba` gives the new LBAs; entries matched to files by original start LBA).
  Verified: unchanged repack is byte-identical; a build with OUTBIN/CHR0D.BIN grown by 5,000 bytes (every OUTBIN
  file shifted) boots and plays the story opening (tests/test_build.py checks the table against the ISO directory).

## Load addresses (verified from RAM dumps with `tools/ramfind.py`)
- EXE 0x80010000-0x8008C800. Every `OVL*.BIN` overlay loads at **0x800CB338** (OVLXTTL on the title,
  OVLM00 in the first minigame; tools/re.py uses this base). OVLGMAIN would end at 0x800F82B4.
- Data files load whole into heap buffers, e.g. PREM0D.BIN at 0x8010D150, NAME0D 0x80117EE0, YUGI0D 0x80118230,
  M000D 0x8011ACE0 (minigame 0), GDEF0D 0x801D1020, SYS1D 0x801D6830.
- **Heap** (phase 7): malloc 0x80023EDC (heap A, free list at gp+0x2F8; gp = 0x8008C0B8) / 0x8002400C (heap B,
  gp+0x2FC), init 0x8002413C(start, size). Bounds per game mode via 0x8001ED4C / 0x8001ED7C: story/field heap A
  0x80100000 + 0xD0000 (to 0x801D0000), heap B 0x801D0000 + 0x20000. malloc returns 0 when full and the file
  loader 0x8001F3B0 does not check it (the file would load to address 0). `tools/lua/heapwatch.lua` logs use/peak:
  map 284 (215 KB GCV0250D) peaks at 400,816 bytes in both builds, 451 KB free. Whole en tour (`tools/heaplog.py`):
  least free 156,128 bytes (minigames m25, m70-72 peak at 695,840).

## Archives (verified: `tools/arc.py` parses all 1,543 `*D.BIN` files; the 64 others are OVL code + the pad)
- Header: u32 LE offsets; the first equals the header size, zero words pad it. Entry i runs from offs[i] to the
  next offset (or EOF). Entries are 16-byte aligned. Most archives end on a 16-byte `end\x1a` entry.
- Entry kinds by magic: `pQES` SEQ music (5,736), `ANM\0` animation (5,277), `ECD\x01` compressed TIM (2,313),
  `pBAV` VAB sound (483), the rest data or scripts (4,826; text lives here, see text.md).
- Code reads an entry by indexing this table (verified for PREM0D: a dialogue entry is entry 13, offset 0x100D0,
  read at RAM 0x8011D220 by the message window, docs/re/text.md). So entries can grow if the table is rewritten.

## ECD compression (verified: `tools/ecd.py`; all 2,313 entries decode to exactly their stated size;
the encoder roundtrips 40/40 sampled entries, sizes within a few % of the originals)
- Decoder EXE 0x80024834. Header 16 bytes: `ECD\x01`, big-endian u32 raw-prefix length (8 = the TIM header,
  copied without touching the ring), u32 stream length (raw prefix included), u32 decompressed size.
- LZSS: flag byte LSB-first, 1 = literal; 0 = 2-byte reference, ring position `b0 | (b1 & 0xC0) << 2`,
  length `(b1 & 0x3F) + 3`. Ring 1,024 bytes zero-filled, first write at 0x3BE. No magic check in code.
- Every ECD entry is a TIM: 1,396 4bpp, 569 8bpp, 348 CLUT-only (magic 0x11, flags 0x0A). The build should
  recompress only entries it changed (the encoder is not byte-identical to Hudson's).

## Free space (candidates only, none trap-tested)
- Disc: mkpsxiso rebuilds every file, so text files can grow once the LBA table is rewritten.
- EXE zero runs: 0x800840CD (4,203 bytes), 0x8008B7C8 (1,057), 0x8008C362 (1,182). OVLGMAIN zero run
  0x800F4B38 (14,204 bytes). Overlay-region runs may be BSS; trap-fill and tour before use.
