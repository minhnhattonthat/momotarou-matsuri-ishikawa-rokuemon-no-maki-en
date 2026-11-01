# Minigame graphics QA, 2026-11-01

Phase 8 is **incomplete**. This checkpoint translates eight atlases and verifies Janken's five prompts/results
and its Score/Record HUD in a cold boot. It does not certify the other outcome graphics, the full tour, or
the 200-row graphics survey; do not advance to release on its scoped manifest.

## Changes and constraints

| Atlas | Redraw | Runtime review |
|---|---|---|
| M110D:0 | Ready..., Go!, Win!, Lose!, Draw! | all five seen in Janken 7 |
| M990D:0 | Score, Record, Time, Course, Stage, ryo, Bonus (large small-font variant) | Score/Record seen; other labels need their screens |
| M010D:4 | Perfect!, Hit Award!, Bonus Award!, Sharp Eye!, Survivor! | not yet accepted |
| M030D:3 | Perfect! | not yet accepted |
| M140D:0 | Win!, Lose!, Streak | not yet accepted |
| M560D:1 | Win!, Lose!, Draw! | story-mode dice route did not show these outcome sprites |
| M590D:0/6 | Win!, Lose!, Draw! | not yet accepted |

`tools/gen_gfx.py` regenerates every edited PNG. The generator's byte-identical-copy sweep found no additional
whole-image copies of these eight atlases. Source-row searches also found result words at different positions
in M110D/M140D/M560D/M590D; all those surveyed copies now have redraws. Partial matches are not proof of identity.

The first Janken review rejected a tiny rounded-font Record label: its gradient looked like a strike through
the word. The final small HUD words use uniform white, hand-drawn 7-pixel capitals in `fonts/hud7.txt`, under
the repository's MIT licence. Banner lettering continues to use Fredoka and the original colours.

## ANM rectangle evidence

`tools/anm.py` reads the sprite tables instead of inferring the drawn rectangle from visible image bounds:

```powershell
python -X utf8 tools/anm.py M990D.BIN 2 --render work/gfx/anm_m990_2
python -X utf8 tools/anm.py M990D.BIN 3 --render work/gfx/anm_m990_3
python -X utf8 tools/anm.py M010D.BIN 4 --labels
```

Verified statically against EXE sprite data consumers and the Janken shots:

- ANM header: count at +4, **table location at +8**, relative item offsets. Static tables commonly use +20;
  animated files such as M110D entries 8-10 put a sequence section before the table.
- Each item has a u32 sprite count, then 28-byte records. Record +2/+4: u/v; +6/+8: width/height;
  +10/+12: CLUT x/y; +14: texture page; +16/+18: signed screen offsets; +20/+22: 12-bit scales.
- M990D:2 reads the seven changed HUD regions as whole words; a regression test rejects any partial user
  in either M990D ANM table. The other Bonus at (136,16,40,16) is **unchanged**: M990D:3 items 19/20 overlap
  it with an 8x24 fragment and an external CLUT at y=512. Resolve those users before redrawing that region.
- Award source widths are 152/152/144/144/144, not 160. The Bonus award's last 24-pixel sprite is also used
  independently; it gets a separate exclamation mark. M030D's Perfect starts at y=216, not y=224.
- M590D:0's Lose word is only 40 pixels wide; its exclamation mark is a separate sprite. Janken has a full
  56-pixel Lose! rectangle. Sharing one guessed rectangle between these atlases clips the English.

`--labels` reports candidate references sharing a texture page, including other textures loaded on that page
in different modes; it does not prove all candidates use the same image. The preview renderer currently supports
unscaled 4bpp records and explicitly reports external page/palette skips. It is not a full animation emulator.

## Reproduce Janken and review

The old circle-only tour stops at the seven undecided hand panels. `tools/debug/janken.lua` waits for the
game to accept input, selects seven rocks with up/right, then confirms OK using ordinary controller input.
Starting the sequence 900 frames after mode entry lost an early input; the checked route waits 1500 frames.

```powershell
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/banners8_final2_janken --script tools/debug/warp.lua --script tools/debug/janken.lua --script tools/lua/textlog.lua --var "SCENE='game_m11_0d'" --var HOLD=6500 --frames 900 --shot-every 60
python -X utf8 tools/textlog.py work/qa/banners8_final2_janken --all
```

Original cold reference: `work/qa/janken_route_jp_final`, same inputs on the original disc. The results vary
slightly in timing between disc layouts. The accepted five frames are 6000, 6120, 6180, 6420 and 6660 from
`banners8_final2_janken`, enlarged 2x in `work/qa/banners8_review/janken_sheet.png`.

Fresh read-only pass under D10: read the whole enlarged sheet after the final build; check each prompt/result,
the scoreboard and surrounding artwork. Verdicts live at `work/qa/banners8_review/verdicts/review.tsv`;
manifest at `work/qa/banners8_review/manifest.tsv`. Other Japanese HUD/result graphics elsewhere in the run
remain tracked in the survey; this sheet deliberately certifies only the listed seven labels.

Accepted sheet SHA-1: `e86c4f8f2f52ce44cce9e2b552160780e92958cf`; gate: **1/1 ok**.

## Validation

- `tools/check.py`: 42 tests passed; lint 0 errors.
- `tools/verify_build.py`: 346 changed files, 0 errors.
- `tools/textlog.py work/qa/banners8_final2_janken --all`: 0 Japanese lines, 0 markers.
- Cold smoke: `work/qa/banners8_final2_smoke`, exit 0, smoke ok.
- Final disc: `build/momotarou-matsuri_en.bin`, 182,839,776 bytes; 2026-11-01 01:50:59 UTC.
- Disc SHA-1: `e4ccf3f32f96fcc03e2834d2716a0a97e4261ce3`.

## Remaining phase work

The M010D circle-mash route reaches repeated zero-score attempts without an award; the M140D and M560D
single-player routes do not establish all result-sprite states. Add score/versus fixtures and capture each
outcome. These exploratory directories (`banners_en_m01`, `banners_en_m14`, `banners_en_m56`) predate the final
HUD font and cannot supply final-build verdicts. Retake them cold after adding suitable inputs/fixtures.

Also still open: shared M990D big announcement glyphs, the remaining small HUD words, credits, cards, signs,
menu/rank variants, all caption shots, nine hanging-map routes, and the complete phase-wide visual manifest.
No owner decision is blocking; the outstanding implementation and evidence prevent phase advancement.

Skill gotcha for `references/graphics.md`: inspect animation source rectangles as well as atlas pixels;
whole-word redraws can corrupt a second animation that samples a glyph fragment. The skill itself was not edited.
