# Native timing game and Poverty God emblem, 2026-11-02

M50's Start cue now has native countdown proof, and all four costume cells
replace Poverty God's び with **P**, matching the established card emblem.
Two controller-only routes produce a successful timing result and an early
failure on both discs. All six actor poses and both Start placements pass
complete pixel checks. **Phase 8 remains incomplete.**

## Artwork and preservation

`gen_gfx.py` changes only four 13x8 cloth interiors in M500D TIM0:
`(26,60)`, `(90,61)`, `(154,60)`, `(26,133)`. The full original kana rectangle
occurs exactly at those four coordinates in the archive-wide indexed sweep:

```text
python -X utf8 tools/gfxfind_rect.py M500D.BIN:0 26 60 39 68
```

The P uses the existing MIT `hud7.txt`, tight seven-pixel mask and original
grey ink. Cloth borders, skin, jewellery, headband, alpha, palettes and ANM
geometry remain intact. Only `gfx/en/M500D_0.png` changes. The earlier Start
lettering is unchanged. ANM1 poses 0-3 use those four bodies; angry poses 4/5
assemble upper bodies with the first two poses' cloth strips. The six natural
body matches therefore cover every changed cell and both reused-strip states.
Other drawings remain separate scope. Correction from the M49 follow-up:
M49 depicts **God of Fortune**, with a ふ badge, not Poverty God; its F redraw
and native reward route are now documented in `fortune-qa.md`.

## Reproduction and native state evidence

```powershell
python -X utf8 tools/gen_gfx.py --only M500D.BIN:0
python -X utf8 tools/build.py
python -X utf8 tools/debug/timing_qa.py --out work/qa/timing8_en_final
python -X utf8 tools/debug/timing_qa.py --original --out work/qa/timing8_jp_retry
python -X utf8 tools/debug/timing_qa.py --check-only --out work/qa/timing8_en_final
python -X utf8 tools/debug/timing_review.py work/qa/timing8_en_final --original work/qa/timing8_jp_retry --out work/qa/timing8_review
```

The helper selects `game_m50_2e` through the existing cold warp. Thereafter
`timing_start.lua` only reads RAM and queues controller input. It advances
instruction dialogue in native states 1/4 and waits during the countdown.
The success route presses Circle at the requested seconds times 60; the early
route presses halfway through that time, after the cue has disappeared.
Neither route changes the timer, result, RNG, sprite selection or coordinates.

Original OVL M50 load address is `0x800CB338`. Relevant state:

| Address | Meaning / native code |
|---|---|
| `800CC77C` | Main state; switch at `800CBC0C`, 1 instructions, 2 countdown, 5 timing, 6 result |
| `800CC638` | Countdown state; `800CB5D0..800CB710` advances each step after 61 frames |
| `800CC640` / `800CC644` | Bound countdown item / ANM entry; cue 4 selects ANM2 item3 |
| `800CC784` | Requested seconds; loaded at `800CB4E8`, multiplied by 60 |
| `800CC760` | Elapsed frames; `800CBD5C` increments the live timer |
| `800CC774` | Native result; `800CB74C..7E8` accepts +/-6 frames for result1; early result2 |
| `8008C410` / `8008C420` | Held / newly pressed pad bits, logged around the test response |

The oracle reads M500D ANM/TIM data from the **named disc**, stamps each
capture with its SHA-1, and rejects stale evidence. It requires all four
countdown logs and the actual native result code. The Start search and full
actor searches are bounded to the central actor area. Actor matching excludes
only the separate translucent ground shadow, while retaining every opaque
body and anger-puff pixel. Background animation and requested time can vary;
the English runs requested four seconds, and the original runs five seconds.
The wrong-disc `--check-only` negative control rejects the capture before
writing templates or coverage. Fresh reruns clear the previous coverage table
so an emulator failure cannot leave an apparently current passing summary.

## Rejected controls and input gotcha

The first bib generator candidate failed its fit check: the default pixel
mask includes two margin rows, so it cannot fit an eight-pixel interior.
Enabling the existing tight mask produces a seven-pixel P without scaling.

Original early-response runs in `timing8_jp` and `timing8_jp_final` are
rejected. Six-frame presses did not reach the game's pad copy, and its native
1000-frame cutoff produced a late result. The accepted original run logs
zero held/new bits for 17 frames after the queued early response, then
`0020/0020` at age18; state6 follows at age19 with result2. Holding the early
response for 30 frames accommodates that observed polling gap. The strict
result assertion stays in place. The precise success response retains six
frames and reaches result1 on both discs. This is input-harness evidence,
not a game bug or permission to accept the timeout.

The preliminary `timing8_en` also passes coverage, but the final repeat uses
the finished input logger and route. The final comparison sheets were all
re-inspected after regeneration; earlier hashes are not silently reused.

## Fresh read-only review and validation

Under D10, the final separate read-only pass inspected all **12** paired
sheets: six enlarged actor poses, two enlarged cues and four whole contexts.
All are **ok**. P is legible without kana remnants, cloth borders and reused
strip seams are intact, Start is complete and centred, and both result
messages fit. The original also overlays Start across the actor's mouth.
Exact final hashes and scoped verdicts are in `timing-verdicts.tsv`.

```powershell
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/timing8_review/manifest.tsv work/qa/timing8_review/verdicts
python -X utf8 tools/textlog.py work/qa/timing8_en_final
```

Both discs pass **10/10** requested label/pose checks (six distinct actor
poses, with the two idle poses checked in both routes). Final validation:
**131 tests passed / lint 0**, verifier **400 changed files / 0 errors**, cold
`work/qa/timing8_smoke` passed, **0 Japanese text lines in two English logs**
(graphics excluded). Main disc: **182,446,992 bytes**, **2026-11-01 18:24:12 UTC**,
SHA-1 **92c95b24ef934bdc5ed86e66d2a0bac3be149016**.

This does not cover every timing judgement, payout, later story transition,
or the full game. The red card notice, Rank Details title consumer, unresolved
signs/emblems, and phase-wide visual/story/NPC gates remain open. No release
was created and no shared skill files changed. Gotcha for
`references/emulator-qa.md`: a short queued press can miss the native pad
copy even while frame counters advance; log held/new bits and assert the
actual result instead of accepting an emulator exit or fixed-frame press.
