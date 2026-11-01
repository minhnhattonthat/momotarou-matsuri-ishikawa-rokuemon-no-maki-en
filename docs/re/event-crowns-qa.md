# Enma's event crowns, 2026-11-02

Four event-art crown initials now read **E**, matching the project's treatment
of character emblems. All four textures have complete native crown matches
on both discs across **five cold event routes**. A fresh D10 read-only
self-review accepts **10/10** context/detail comparison sheets. This closes
the Enma-initial findings in the historical event tour; **phase 8 remains
incomplete** and phase 9 has not started.

## Source and preservation

`tools/gfx_event_crowns.py` redraws explicit row spans inside each white
triangle, then adds a hand-drawn 4x7 E (4x5 in the smallest crown). The font
is project MIT and listed in `docs/fonts.md`. A rectangular erase would
damage the sloping outline where the cursive ink approaches the edge.
The first atlas preview revealed a pale old-ink pixel at EVT180D:1 (131,14);
the accepted mask includes it. That intermediate PNG was never built.

| Source | Changed bounds, right/bottom exclusive | Native event |
|---|---|---|
| EVT030D:1 | 167,157–180,166 | 03 |
| EVT170D:0 | 201,81–212,91 | 11 |
| EVT180D:1 | 129,7–138,15 | 12, 23 |
| EVT190D:1 | 143,98–152,108 | 13 |

The four omitted images are now survey rows #82/#123/#128/#132 (210 rows
total). Whole-TIM duplicate expansion found no additional images. The
archive-wide `gfxfind_rect.py` scans of the four rectangles found only their
listed sources. The EVT180 scan includes its pale tail, ending at y=15.
This does not classify differently drawn crowns elsewhere in the game.

Tests preserve every pixel outside the declared spans, the full alpha
silhouette and bottom crown rim, and check the regenerated PNGs against the
committed assets. The usual all-redraws test also constrains changed palette
indices. No palette, ANM, engine or script changes are made. The blue outer
fringe in EVT180/190 is present in the original cold captures and is retained.

## Cold reproduction and oracle

```powershell
python -X utf8 tools/gen_gfx.py --only EVT030D.BIN:1 EVT170D.BIN:0 EVT180D.BIN:1 EVT190D.BIN:1
python -X utf8 tools/build.py
python -X utf8 tools/debug/event_crowns_qa.py --original --out work/qa/crowns8_jp
python -X utf8 tools/debug/event_crowns_qa.py --out work/qa/crowns8_en --compare work/qa/crowns8_jp
```

The helper cold-boots via `emu.py`/`warp.lua`, selects the event, then lets
the original animation run for 1,800 frames without automatic clicks. It
captures every 60 frames and compares all opaque pixels of each complete
crown region, including its border, with the **named disc**. It stamps the
disc SHA-1 before/after capture and rejects changed discs on `--check-only`.
The source regions are wider than the edited lettering. No pose, palette,
sprite, animation or story-state substitution occurs after event selection.

| Event | Frame on both discs | English crown-region top-left | Original top-left |
|---|---|---|---|
| 03 | f003480 | 110,84 | 110,84 |
| 11 | f003540 | 185,70 | 185,70 |
| 12 | f003540 | 139,70 | 139,69 |
| 13 | f003660 | 146,52 | 146,52 |
| 23 | f003540 | 139,70 | 139,69 |

The initial exploratory route mapped events 10/11/12 to the wrong archives;
its oracle correctly failed on the original. Event10 instead shows the
large seated demon with an unlettered gold crown. Correcting the case table
and adding event13 yields **5/5 matches on each disc**. Historical sheet003's
event10/11/12 crown note is therefore imprecise; actual Enma consumers are
11/12/13. Event13 was an additional original cold run in `crowns8_jp`; all
five accepted captures are from the same original SHA-1.

## Fresh read-only verdicts and validation

All five full-scene comparisons at 2x and five complete-crown crops at 10x
were inspected after the final build, with English left/original right.
The E is legible, no old stroke remains, and the crown outlines and visible
surrounding artwork match. Event12/23 naturally differ by one pixel of actor
animation; their source-matched detail crops align correctly. The two events
produce identical sheets but are separate cold routes, not distinct artwork.
Durable hashes and observations are in `event-crowns-verdicts.tsv`.

```powershell
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/crowns8_en/review/manifest.tsv work/qa/crowns8_en/review/verdicts
python -X utf8 tools/textlog.py work/qa/crowns8_en
```

Validation: **137 tests passed / lint 0**, verifier **403 changed files /
0 errors**, cold `crowns8_smoke` passed, **0 Japanese lines in five logs**
(graphics excluded). Main disc: **182,451,696 bytes**, built
**2026-11-01 19:53:46 UTC**, SHA-1
`cf1016cd768c209df01f5f5ff5cf87e18d8c3a0d`. Original SHA-1:
`5d4768ed47341760d287ec08b37f5b62c5b8dc60`.

## Remaining work and exploratory evidence

The initial 21-route original-only sweep is `work/qa/event_marks8_jp`, with
all arrivals passing. It is navigation evidence, not a final English visual
gate. Event06's three-dot flags depict dumpling skewers; its tiny foreground
lantern mark was not confidently classified. The bonfire contains 大 plus
separate torii/peach shapes (the old tentative 開 transcription is wrong).
The script calls it the Daimonji Bonfire. Bonfire art remains unchanged and
unapproved; its alternate versions and old historical sheets remain open.
The Tanabata strips, snow placards and ending gold-prop mark also remain open.

Other graphics, natural outcome/record contexts, intermediate dialogue,
NPC interactions and later story-state coverage still prevent phase 8 from
advancing. These ten accepted sheets do not make the full manifest green.
No owner decision or scope exception is inferred, and no release was made.

Gotcha for `references/emulator-qa.md`: a historical review's event number
can be off by one; verify the actual cold shot and named-disc region before
mapping an artwork fix to a route. No shared skill files were changed.
