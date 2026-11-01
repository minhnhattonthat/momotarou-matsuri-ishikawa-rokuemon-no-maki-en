# Map 284: missing native transition setup, 2026-11-01

The corrected warp now passes **two cold runs on each of three discs**: original,
frozen card-prop and current English. It preserves the normal entrance's setup
around op1D, just as map294 already does. No game executable, disc layout,
arrival test or arbitrary delay was changed to obtain these results.

## Failure and diagnosis

The bare warp repeatedly fails on the frozen disc SHA-1
`1ff27c30c241edca355a724a9fce8e56d94f36cf`. A permanent negative fixture,
`tools/debug/map284_bare.txt`, retains the old scene row. Runs
`work/qa/map284_dispatch_baseline`, `map284_dispatch_stack`,
`map284_dispatch_exception` and `map284_negative_final` preserve the evidence.

`map_watch.lua` now reads CPU/CP0 registers and nearby stack words in addition
to the script VM. It can dump RAM at frame 4200 with `MAPWATCH_DUMP=true`.
In the failed run the VM stays on op001D, but the CPU is **not waiting for a
map-load completion flag**: it is in the BIOS exception path at BFC0D8E0,
with Cause **00000024** and EPC **8006D494**. Original EXE disassembly shows:

```
8006D488  div   zero,t0,v0
8006D48C  bnez  v0,8006D498
8006D490  nop
8006D494  break 7
```

The routine at 8006D410 divides 60,000,000 by a three-byte sequence tempo;
the divisor is zero in this failure. This identifies an audio-sequence
exception, not a heap exhaustion or untranslated-text fault. The exact
upstream source/lifetime of the zero tempo remains untraced; do not claim an
audio-library or general CD-loader fix.

Diagnostic interventions on the frozen disc:

| Extra ops before op1D | Result |
| --- | --- |
| None | repeated failure, same exception |
| `01 0078` (120-frame script wait) | passed; diagnostic only, not retained |
| `56 001D` (pending music selection) | failed, same exception |
| `59 0002` (volume-step state) | passed |
| `59 0002 56 001D` | passed |

An exploratory `3E 0078` was a wrong opcode, stopped explicitly and excluded
from these comparisons; the verified wait handler is op01 at 800342F4.

## Native sequence retained

GSF0000D entry 23 contains, at hexadecimal byte offsets 14 through 30:

```
59 0002
56 001D
1D 011C 0013 000B 0000 FFFF
57 0000 0000 0001
1E 0314
```

The warp retains its existing exit sentinel FFFE but now preserves both
surrounding setup groups. `gen_scenes.MAP_OPS[284]` and `scenes.txt` contain
them; `test_map_284_setup_matches_its_normal_entry_script` compares their exact
bytes with the original entry and checks the generated scene row. The test
failed before the fix (missing map284 setup), then passed. The final full
check is **105 tests / lint0**.

Op59 calls 8002372C to store the volume-step state at gp+2D4. Op56 records a
pending selection through 8003398C; op57 uses 800339B0 for the native post-load
music path. These are state changes from the original entrance, not an
assumed timing delay. The effect of op59 alone does not prove why the old
sequence reader reached zero tempo. Keep the negative fixture and frozen disc
for future audio investigation if a natural route exhibits the same failure.

## Reproduction and scope

```
python -X utf8 tools/debug/warp_all.py build/tour8_corrected/momotarou-matsuri_en.cue --out work/qa/map284_native_frozen1 --jobs 1 --only '^map_gv2500_284$' --hold 1500 --click 45 --every 60 --probe tools/debug/map_watch.lua --probe tools/lua/textlog.lua
```

Repeat with the main CUE and with the original CUE (omit the positional CUE
for original). The `map284_native_{original,frozen,current}{1,2}` directories
contain all six cold results. Every result is `1/1 scenes ok`; the first
original/frozen/current arrivals are frames 3926/3923/3922. Both English discs
have zero Japanese lines in their text logs. The initializer returns, the VM
resumes normal interaction and ground-search dialogue runs.

To reproduce the negative fixture in PowerShell (expected nonzero exit):

```
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/tour8_corrected/momotarou-matsuri_en.cue --out work/qa/map284_negative_final --script tools/debug/warp.lua --script tools/debug/map_watch.lua --var "SCENE='map284_bare'" --var "SCENES=[[$((Resolve-Path tools/debug/map284_bare.txt).Path)]]" --var HOLD=300 --frames 1 --timeout 100
```

Current disc: **182454048 bytes**, **2026-11-01 12:10:14 UTC**, SHA-1
`a55a142561d6bb35cd67b479a08e9692f57434c3`.

Fresh read-only D10 review accepts `work/qa/map284_native_review/map284_sheet.png`
(SHA-1 `63506ffa671c03bf76f87750feb07d946a9f41e2`) for arrival and continued
field rendering. English is left, original right; the final dialogue timing
differs because the text lengths differ. This is **not** a full story playtest
or a replacement for the outstanding 25 corrected-tour visual findings.
