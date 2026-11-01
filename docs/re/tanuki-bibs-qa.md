# Even Tanuki's Kintaro bibs, 2026-11-02

All eight 金 bib cells in M140D TIM2 now use **K**, matching Kintaro's
already translated costume initials. Cold native two-player play gives
**9/9 complete actor matches on each disc**; a fresh D10 read-only pass
accepts **10/10 comparison sheets**. This closes the bib finding in
`tanuki-qa.md`, but **phase 8 remains incomplete**.

## Source and preservation

`gfx_tanuki_bibs.py` draws only explicit row spans inside the gold badges.
The eight first-ink coordinates are (62,143), (110,144), (20,200), (56,194),
(92,193), (140,194), (180,193), (222,214). The side/eating masks exclude
hands and cloth folds. The gold rim, red cloth, skin, transparency, CLUT,
ANM data and other characters remain unchanged. A hand-drawn 4x5 K keeps
both diagonal arms distinct at native size; its project MIT licence is
recorded in `docs/fonts.md`.

Preservation tests compare every pixel outside the spans and the full alpha
channel, assert that only Kintaro ANM6 poses 0/1/5/6/7/8/9/10/11/12 use the
edited areas, and compare the regenerated image with the committed PNG.
The whole-TIM duplicate sweep finds no additional copies. The indexed scan
`gfxfind_rect.py M140D.BIN:2 60 143 68 150` finds the same upright lettering
at (60,143), (108,144), (18,200), all included. The five differently drawn
cells are explicitly included too; this is not a claim about other games'
Kintaro art. The survey now includes previously omitted image #746.

## Cold route and complete-actor oracle

```powershell
python -X utf8 tools/gen_gfx.py --only M140D.BIN:2
python -X utf8 tools/build.py
python -X utf8 tools/debug/tanuki_bibs_qa.py --out work/qa/bibs8_final_en
python -X utf8 tools/debug/tanuki_bibs_qa.py --original --out work/qa/bibs8_jp
```

The helper cold-boots through `emu.py`, uses `two_player.lua` to select 2P
in the native menu and `warp.lua` to select Even Tanuki, then drives both
controllers with Circle. `tanuki.lua` now accepts `TANUKI_OFFSET` (default
45 frames; exposed as `--offset`) for reproducible controller timing probes.
After entry there are no outcome, RNG, pose, location or story-state writes.
The route reaches normal dice rounds and the replay question.

The oracle reads the expected ANM/TIM pixels from the **named disc**, stamps
its SHA-1 before/after capture, and rejects stale captures on `--check-only`.
It checks every opaque pixel of each complete assembled actor, including
face overlays and sweat particles; only the separate translucent ground
shadow is excluded. ANM6 items 9 and 10 assemble identical actor pixels at
different vertical offsets, so they count as one cell proof, not two
distinct animation-timing proofs.

| ANM6 item | English frame | Original frame | English top-left |
|---|---|---|---|
| 0 | f004158 | f004248 | 256,128 |
| 1 | f004200 | f004266 | 256,128 |
| 5 | f004920 | f004920 | 252,128 |
| 6 | f004932 | f004932 | 258,128 |
| 7 | f005076 | f005796 | 258,128 |
| 8 | f005070 | f005790 | 258,128 |
| 9 (same pixels as 10) | f005094 | f005814 | 256,123 |
| 11 | f005880 | f005070 | 256,122 |
| 12 | f005898 | f005088 | 258,128 |

Original SHA-1: `5d4768ed47341760d287ec08b37f5b62c5b8dc60`.
English SHA-1: `1b0e790cf5bbc1142a2adc1d6f68dd1476a49e75`.
Scores and frame timing differ naturally between discs; matching source
actors does not require equivalent random dice values.

## Review and rejected candidates

The first candidate (`486a1e66...`, `bibs8_en`, `bibs8_review`) passed the
pixel oracle but failed fresh visual review: the condensed three-pixel K
looked like parallel bars. It is rejected. A 5x5 resampling candidate also
had disconnected diagonal arms in its atlas preview and was not accepted.
The final hand-drawn 4x5 form has a continuous stem and distinct diagonals.
An earlier atlas preview also exposed one pale leftover stroke at each
badge's right side; the masks include that fringe in the final build.

Fresh read-only D10 inspection of all ten final sheets accepts their K
legibility, preserved artwork and shown English HUD. Durable hashes and
observations: `tanuki-bibs-verdicts.tsv`. Reproduce each pose comparison with
`sheet.py EN_FRAME --compare JP_FRAME --crop 246,114,64,72 --zoom 6`.
The context sheet compares the two item-11 frames at 2x without cropping.

```powershell
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/bibs8_final_review/manifest.tsv work/qa/bibs8_final_review/verdicts
python -X utf8 tools/textlog.py work/qa/bibs8_final_en
```

Final checks: **134 tests passed / lint 0**, disc verifier **400 changed
files / 0 errors**, cold `bibs8_final_smoke` passed, **0 Japanese lines in
1 textlog** (graphics excluded). Main disc: **182,446,992 bytes**, built
**2026-11-01 19:18:23 UTC**, SHA-1 above.

## Remaining phase-8 work

Natural M14 Win/Lose still has no accepted capture. Read-only code follow-up
locates the ANM selector map at OVLM14 `0x800CFFAC` (entries 4..11), the
scroll descriptor at `0x800D00C8` (bank 7 = ANM11, current item at +0x10),
and Streak at `0x800D0548` (same bank, item 2). The scroll initializes as
item 0 at `0x800CB4E4..528`; `0x800CF7F0..864` switches it to item 1 for
solo result states 2/4 and skips the two-player case. These are static
navigation leads, not proof that Win/Lose items 3/4 are unused. Do not keep
changing two-pad timing and count an ordinary Good Work screen as those
banners. Normal story return also remains outside this route.

Event crowns/bibs/bonfire lettering, unresolved field and event marks,
remaining native outcome/record contexts, the full visual manifest and
story/NPC coverage still prevent phase 8 from advancing. No owner decision
or scope exception is inferred. No shared skill files changed.

Gotcha for `references/emulator-qa.md`: an exact source-to-screenshot match
can pass with an illegible glyph; the separate enlarged visual pass caught
the condensed K failure here.
