# God of Fortune badges and native reward route, 2026-11-02

M49's four costume initials now read **F**. The sprite depicts **God of
Fortune** (福の神), whose badge says ふ; the prior M50 report's identification
as Poverty God was incorrect. Eight native poses cover all four edited badge
cells, and eleven comparison sheets pass a fresh D10 read-only review.
**Phase 8 remains incomplete.**

## Artwork and source coverage

`gfx_fortune.py` defines row-by-row interior masks for all four badges in
M490D TIM0. Their bounding rectangles are `(35,46)-(50,54)`,
`(83,15)-(98,23)`, `(142,14)-(151,22)` and `(198,45)-(210,53)`.
The latter two account for hands and cloth folds crossing the badge.
The F uses the newly added four-pixel-wide, seven-pixel-high MIT HUD glyph,
native yellow `(232,232,0)` and dark brown `(48,32,0)`. Surrounding hands,
bag, clothes, badge borders, transparency, palette and ANM records stay intact.

Only `gfx/en/M490D_0.png` changes. `gen_gfx.py` also checks byte-identical
TIM copies across archives; this atlas has none. Full badge rectangle
`(33,45)-(52,54)` has exactly two indexed matches, at `(33,45)` and
`(81,14)` in M490D itself. The other two badges are partially occluded
drawings, explicitly included in the mask. The common inner kana scan
`(40,46)-(47,54)` likewise finds only `(40,46)` and `(88,15)`.

ANM1 has fourteen poses. Poses0/1 use the two complete badges, pose2 bows
and hides the badge, pose3 uses the hand-covered badge, and poses4-13 reuse
the fourth cell. The regression test checks unchanged pixels outside the
explicit mask, alpha/palette preservation, the adjacent hand/fold rectangles
and all thirteen ANM users of the changed pixels.

## Cold reproduction

```powershell
python -X utf8 tools/gen_gfx.py --only M490D.BIN:0
python -X utf8 tools/build.py
python -X utf8 tools/debug/fortune_qa.py --out work/qa/fortune8_en_final
python -X utf8 tools/debug/fortune_qa.py --original --out work/qa/fortune8_jp_accepted
python -X utf8 tools/debug/fortune_review.py work/qa/fortune8_en_final --original work/qa/fortune8_jp_accepted --out work/qa/fortune8_review
```

`fortune.lua` follows the established cold `game_m49_2d` warp. It only reads
RAM, queues Circle, captures frames and checks the native return; it never
edits outcome, reward, RNG, animation selection or coordinates. Circle advances
intro/reward dialogue and stops the scrolling number selector. The native
reward differs with timing/RNG: **377 ryo** on English and **305 ryo** on the
original. Both reach native mode61 after the reward, the trial return path.
This is not proof of the normal story return.

Original OVLM49 load base is `800CB338`. Main state is the halfword at
`800CD580`, with the animation substate at `800CD582`; the switch at
`800CC314..344` drives intro=1, selector=2, reward animation=3 and dialogue=4.
Reward amount is `800CD57C`. Native Circle handling at `800CBEB8..ED4`
reads the game's newly pressed bits at `8008C420` and stops the selector.
`800CC3D0` starts the reward message and `800CC430..43C` selects the trial
return. These addresses are read-only route evidence, not patched code.

The oracle reads ANM/TIM entries from the **named disc** and stamps the run
with its SHA-1. Every opaque actor and coin-effect pixel must match inside
the central stage region; only the separate translucent ground shadow is
excluded. Accepted coverage is **8/8 poses on each disc**, indices0-7,
including every changed badge cell. Check-only against the original disc
rejects the English capture as stale before changing any artifacts.

## Rejected probes and limits

- `fortune8_jp` timed out in state2 because the initial route advanced
  dialogue but never pressed Circle at the selector. It is rejected.
- `fortune8_en` / `fortune8_jp_final` are exploratory broad probes: poses0-7
  matched, but alternate coin-effect poses9-13 did not occur in their
  captured sequence. Pose8's body-only template also matches the body
  inside pose4; it cannot prove native pose8 and is excluded from acceptance.
- The accepted route deliberately tests poses0-7. ANM1's alternate sequence
  at offset108 contains poses9-13 and reuses the already translated fourth
  badge; its full effects still need native coverage. No claim of disuse or
  whole-minigame completion follows from a missing match.
- The initial generator failed because the HUD font had no F. Adding the
  glyph to the existing MIT font fixes this without importing a system font.

## Fresh read-only review and validation

After capture and sheet generation, a separate read-only D10 pass inspected
all eleven final English/original pairs: eight enlarged actor poses and
three whole contexts. **11/11 ok**. F is legible in both idle cells and the
throwing cell; the raised hand naturally covers part of its badge without
losing hand or fold pixels. The bow remains untouched. All visible coin
and star artwork is preserved, selector numbers/ryo are readable and the
instruction and reward dialogue fit. Final hashes and observations are in
`fortune-verdicts.tsv`.

```powershell
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/fortune8_review/manifest.tsv work/qa/fortune8_review/verdicts
python -X utf8 tools/textlog.py work/qa/fortune8_en_final
```

Validation: **132 tests passed / lint 0**, disc verifier **400 changed files /
0 errors**, cold `work/qa/fortune8_smoke` passed, **0 Japanese lines in one
English textlog** (graphics excluded). Main disc: **182,446,992 bytes**,
**2026-11-01 18:40:47 UTC**, SHA-1
**28f5035d4aea1d2b282adc8e546803261b8ad926**.

The red Card Album notice, Rank Details title consumer, unresolved field/event
marks, phase-wide visual manifest and story/NPC coverage still prevent phase8
completion. No owner decision is needed for this badge change and no release
was created. No shared skill files changed. Gotcha for
`references/emulator-qa.md`: a body-only sprite template can match inside a
larger effect-bearing pose; do not count that subset as proof of the selected
native animation item.
