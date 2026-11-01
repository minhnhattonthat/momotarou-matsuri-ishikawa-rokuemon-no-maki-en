# Snow badge and ending fans, 2026-11-02

Three Festival fans in EVT620D and Kintaro's snow-statue initial in EVT110D
are translated. The fans use the full word split FEST / IVAL, as on the
previously approved attract-mode fans. The statue uses K for the original
hiragana initial き, matching the translated card badges; this is an emblem,
not an abbreviated character name. The two tiny snow placards remain
unclassified, and a black mark on the ending's gold prop near screen (164,53)
needs a separate enlarged classification. **Phase 8 remains incomplete.**

## Sources and preservation

`tools/gfx_event_props.py` regenerates four PNGs through `gen_gfx.py`.
The two snow TIMs form a 320-pixel illustration with a seam at x=240, not
x=256. The original initial has two disconnected ink components, 288 and
125 pixels. The generator asserts those component bounds and sizes, erases
only them, then scatters the outlined ice-blue K back to the two TIMs.
The separate oval border, characters, placards and all other artwork survive.

The top and right fan inscriptions are isolated non-background components
of 300 and 661 pixels. The small left fan's cream outline touches its ribs,
so explicit row spans stop at the inscription. Clean orange samples come
from each fan's untouched face. The first fresh cold review rejected six
cream fringe pixels at (24,67), (25,68), (25,70), (24,71), (25,72), (26,73);
the spans now remove them and a regression checks each one. Rejected sheet:
`work/qa/event_props8_rejected/fan_left_detail_sheet.png`, SHA-1
`f79b7e5cb136002e57c3383588b67a679a437920`.

The new tests preserve the snow oval, all pixels outside the old/new initial,
the illustration alpha, fan ribs and handles, and generated-PNG consistency.
The existing all-redraws test still limits changed indices to declared bounds.
No ANM, palette, layout, script, or engine bytes are changed by this work.

An archive-wide exact indexed-rectangle sweep finds only the five edited
source rectangles listed below; whole-TIM duplicate expansion also finds no
additional images. This does not classify differently drawn costume marks.

| Source | Rectangle (exclusive right/bottom) |
|---|---|
| EVT620D:0 top fan | 107,0–139,15 |
| EVT620D:0 small fan | 7,62–27,79 |
| EVT620D:1 right fan | 43,127–76,157 |
| EVT110D:0 initial, left fragment | 228,105–240,136 |
| EVT110D:1 initial, right fragment | 0,105–15,136 |

Reproduce each sweep with `tools/gfxfind_rect.py FILE.BIN:ENTRY x0 y0 x1 y1`.
The one-pass results are saved in `work/gfx/event_prop_copies.tsv`.

## Cold routes and oracle

The actual snow illustration is **event07**. Event01 remains the bath scene,
as corrected in `symbol-classification-qa.md`. The snow route cold-boots,
selects event07 through the existing warp, and lets the event renderer run.
The ending route selects event20 and runs for another 11,500 frames, without
replacing sprites, artwork, palettes or animation records. It reaches the
festival illustration during the credits sequence.

```text
python -X utf8 tools/gen_gfx.py --only EVT620D.BIN:0 EVT620D.BIN:1 EVT110D.BIN:0 EVT110D.BIN:1
python -X utf8 tools/build.py
python -X utf8 tools/debug/warp_all.py build/momotarou-matsuri_en.cue --out work/qa/event_props8_final_snow --only '^event07$' --hold 900 --click 45 --every 120 --probe tools/lua/textlog.lua --jobs 1
python -X utf8 <skill>/scripts/emu.py build/momotarou-matsuri_en.cue --out work/qa/event_props8_final_ending --script tools/debug/warp.lua --script tools/lua/textlog.lua --var "SCENE='event20'" --var HOLD=11500 --frames 900 --shot-every 120 --timeout 300
python -X utf8 tools/debug/event_props_qa.py build/momotarou-matsuri_en.bin --snow work/qa/event_props8_final_snow/event07 --ending work/qa/event_props8_final_ending --out work/qa/event_props8_final
```

Replace `<skill>` with `python tools/skill.py`'s output. Original-disc controls
use the original BIN/CUE, `work/qa/snow8_jp/event07` and
`work/qa/ending_props8_jp`; the oracle's copied captures and coverage table are
in `work/qa/event_props8_original`.

`event_props_qa.py` reads its expected pixels from the **named disc image**,
not the generator's PNGs. It requires both complete original-initial regions
(upper and lower, together covering all changed snow pixels) and three
complete fans with their borders. The snow oval's lower right is naturally
covered by Yashahime; requiring that entire oval wrongly failed the original
disc too. No translated stroke is excluded for this occlusion.

EVT620D:0 and :1 both upload their CLUT at (0,480). The later TIM's palette
wins for both halves. Decoding :0 with its own stored palette wrongly fails
the screenshot check, despite the matching shape. The oracle models that
shared-CLUT overwrite using the actual palette bytes from the named disc.
This is specific to the two-image event artwork; it is not a general emulator
palette inference. Snow uses separate CLUT rows 480/481.

## Review and validation

Final cold evidence and the fresh D10 verdict hashes are recorded in
`event-props-verdicts.tsv`. The full-scene views remain explicitly separate
from approval of the four changed props: snow placards and the ending's gold
mark remain open. No historical tour verdict is rewritten by this pass.

After the final fringe correction, a fresh read-only self-review inspected
all six regenerated comparison sheets (English left, original right), under
D10. **Four detail sheets pass; two context sheets retain issues**, with zero
missing/stale verdicts. `qa_gate.py check work/qa/event_props8_review/manifest.tsv
work/qa/event_props8_review/verdicts` correctly exits **1**. The full manifest
has not been made green by narrowing those context verdicts.

Both original and final English discs pass **5/5 complete prop regions**.
All three fans occur in the same frame, f008160; both snow-initial regions
occur together in f003480. Four original/English props are therefore covered,
not five separate signs. The two final English text logs contain **0 Japanese
lines**, which excludes graphic text. This does not translate/classify the
remaining placards or gold mark.

Final main disc: `build/momotarou-matsuri_en.bin`, **182,454,048 bytes**,
**2026-11-01 15:32:34 UTC**, SHA-1
**d20bb64a57a110da58795477de0bf197effcc0de**. Validation: **125 tests passed**,
lint **0 errors**, verifier **399 changed files / 0 errors**, cold smoke
`work/qa/event_props8_main_smoke` passed. The older `build/event_props8.bin`
(79acc97a...) retains the rejected six fringe pixels and is not the final build.

Phase-wide graphics, intermediate dialogue, NPC interactions, later story
states and natural minigame outcomes remain open. These targeted routes do
not authorize phase 9 or a release.

No shared skill files changed. Gotcha for `references/platform-ps1.md`:
consecutive TIMs can overwrite one CLUT address; compare screenshots using
the last uploaded palette, rather than each TIM's independently stored CLUT.
