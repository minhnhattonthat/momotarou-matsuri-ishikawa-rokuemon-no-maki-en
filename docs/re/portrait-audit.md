# GCV0310 dialogue-portrait audit

Survey row #265 is a set of **placeholder dialogue portraits**, rather than
ordinary character name tags. Four copies of the same faded Momotaro picture
have red labels 桃太郎, 柿太郎, 栗太郎 and 月姫. The last label is not a name used
in the extracted game script. These assets remain unchanged.

## Static evidence

`GCV0310D.BIN` data ID 475, entry 13, is an 8bpp TIM at VRAM (384,256),
256x256 pixels, CLUT (0,511). `GCV0311D.BIN` data ID 476, ANM entry 140,
items 0-3 each use one complete 48x40 sprite at U=0/48/96/144, V=0.
Items 4-9 reference blank parts of the same atlas.

The EXE message handler at **0x8002BD88** reads the second operand of opcode
02 as a portrait ID (0x8002BEB4), with FFFF meaning no portrait. It calls
**0x80033C0C**, which indexes the overlay's six-byte `{file, ANM entry, item}`
table at **0x800F39B4** and calls the static sprite binder **0x8001E224**.
Table IDs **123-126** map exactly to `(476,140,0..3)`.

`python -X utf8 tools/debug/portrait_audit.py` scans every fully parseable
archive entry, including entries that have no extracted text. Result:
**4,894 message operations, zero references to IDs 123-126**. It also asserts
the four table records and their actual sprite bounds. This corrects the older
`script.md` description of the second message operand as a voice field.

## Runtime evidence and limits

```
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" "rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue" --out work/qa/tags8_trace_final --script tools/debug/warp.lua --script tools/debug/portrait_trace.lua --var "SCENE='map_gv3100_294'" --var HOLD=600 --frames 1 --debugger --timeout 180
```

The cold Moon-map trace uploads GCV0310D entries 4-9, 12 and **13**, but both
sprite-binding probes (animated **0x8001E160**, static **0x8001E224**) see only
GCV0311D entry **64**, the field character. They do not see entry 140. The final
shot contains no labelled portrait. Merely uploading a TIM is not evidence that
its lettering is visible.

The absence of literal message references and absence in this one cold route
support classifying these as dormant dialogue placeholders. They do **not**
prove that arbitrary native code, a developer selector or every possible story
state can never draw the assets. If a future route displays them, reopen the
survey row and translate the names in that context; do not count this audit as
a translated graphics verdict or a phase-wide reachability proof.

No shared skill files changed. For `references/emulator-qa.md`: trace both
static and animated sprite binders, since dialogue portraits can use a
different API from field actors; PCSX-Redux numeric registers are `GPR.r[n]`.
