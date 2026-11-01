# Destination-specific map initialization

## Defect and evidence

The old `warp.lua` changed to every map with `1D map x y dir FFFE; 1E 0063`.
Script 0x63 is **GSF0000D entry 60**, the world-map initializer, not a generic
return-to-field routine. It creates world-map actors and triggers on unrelated
town maps. Backgrounds could render while the correct town actors were absent;
some coordinates hung. The old 452-scene text tour therefore cannot establish
map NPC/dialogue or animated-sign coverage.

The script-call table at OVLGMAIN **0x800E480C** uses **8-byte** records
`{u32 data_file_id, u32 entry}`. EXE 0x80034A88 multiplies the 1E operand by 8;
0x80034A94/98 load those two words, and 0x80034A9C..AC load/find that script.
Examples:

| Map | Call | Target |
|---|---|---|
| 59 | 0x0A5 | GSV0200D:10 |
| 163 | 0x1C4 | GSV1300D:1 |
| 189 | 0x20C | GSV1609D:1 |
| 332 | 0x39B | GSV3611D:1 |
| 333 | 0x39D | GSV3612D:1 |

The bath initializer unconditionally creates the curtain actors with op 1F.
Original-disc controller route, old initializer: no curtains, **0/2** pixel
matches. Same route with 0x20C and the input correction: attendant and both
curtains visible, **2/2** matches. See `field-signs-qa.md` for commands and paths.
The corrected contest warp also restores its NPCs and completes at (40,33),
where the previous initializer timed out on the English disc.

## Fix and safeguards

`gen_scenes.initializers()` scans parsed original script operations. It uses a
unique immediately-following 1E when available (337 maps); otherwise it requires
a unique following call before another map change/end. This identifies 360 map
initializers, including every map with a usable destination in the scene list.
For maps 35 and 140, adjacent calls avoid misleading conditional fallthroughs
into another map's initializer. No arbitrary default is accepted.

Every generated `map MAP X Y DIR INIT [PREOPS POSTOPS]` row carries its initializer. `warp.lua`
rejects old map rows without it; `MAP_INIT` is an explicit diagnostic override.
`find_arrivals.py` writes the initializer into its temporary scene list too.
Existing save/mask/event/minigame paths retain their own entry mechanisms.

A second bug was the warp's every-30-frame Circle tap while the loader yielded.
In the bath trace, a tap at frame 3866 remained active until initialization ended
at 3873, immediately opening the "search at your feet" dialogue. Circle taps now
stop while VM op 1D or 1E is active. This restores the unattended walking route.

## Coverage and remaining work

The scene list now has **464 entries**, including the nine maps previously
commented out. Cold English tests in `work/qa/mapinit8_recovered` first recovered eight:
**9, 29, 30, 31, 34, 187, 201, 204**. Each has an arrival screenshot and a clean
text log. Map **294** additionally needs its normal entry's setup operations:
`59 2; 56 14` before the map change, and `57 0 0 1` afterward (hex words).
These come directly from GSF0000D:25 at offsets 0x10 and 0x24. All alternative
coordinates still failed without this setup. With the full sequence it passes
on the original (`work/qa/mapinit8_294_original`) and English
(`work/qa/mapinit8_294_final`) discs at the original (17,20), direction 2.
**All nine previously excluded maps are therefore recovered.** The scene row
holds these extra words explicitly; `find_arrivals.py` preserves them too.
This checks the sequence's effect, not an inferred meaning of every setup op.

The replacement cold sweep passes **358/358 maps** with **0 Japanese lines in
358 logs** (graphics excluded):

```
python -X utf8 tools/debug/warp_all.py build/signs8.cue --out work/qa/mapinit8_all --jobs 3 --only '^map_' --hold 300 --probe tools/lua/textlog.lua
python -X utf8 tools/textlog.py work/qa/mapinit8_all
```

`build/signs8.bin` and the main built disc have SHA-1
`4493a392249171d9e12b467c1cfba74522e49a30`. Every result row is `ok`; no failed
map was silently removed. Six map-table entries without usable destinations
remain outside the generated scene list, as before.

This is cold load/initialization coverage, **not** a full visual approval or
interaction tour. Map 9's arrival shot precedes its initializer's scripted
walk; its `final.png` shows the correct ice room and translated dialogue.
Initializer execution is not a story-state model: chapters, flags, alternate
populations and all NPC conversations still require dedicated routes. The map
captures have not been given a phase-wide visual verdict.

Static checks: `tests/test_map_initializers.py` requires every script destination
to have an initializer, checks actual table targets for the bath, contest and
previously failing map families, and verifies the generated list has no implicit
world-map fallback.
