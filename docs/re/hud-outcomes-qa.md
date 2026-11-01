# Shared HUD and minigame outcome checks, 2026-11-01

**Phase 8 remains incomplete.** This checkpoint translates six additional labels, fixes M59's mixed
Japanese/English Lose banner, and establishes scoped cold-render evidence for previously unverified
sprites. It does not approve natural outcome progression, the alternate M59 atlas, or the full graphics tour.

## Changes and defects found

- M990D:0: Weather, Forecast, Race Result, Entry and Slow. Original cold shots corrected an early mistaken
  split of `レースけっか` / `遅い`; they are **Race Result** / **Slow**, not Race / Result.
  All five rectangles have only whole-sprite users, including a scan of other archives' ANMs.
- M030D:1: `どっち?` becomes **Which?** in its actual 32x8 sprite. Condensed seven-pixel capitals fit
  without scaling or clipping. M14 Streak now uses the same font with a dark outline; its old tiny rounded
  lettering blended into the bright railing.
- M590D:0 / ANM 9 item 1: the former Lose tail sampled `(64,120,16,32)`, containing part of Japanese `け!`
  **and shared actor art**. The old redraw therefore displayed `Loseけ!`. The complete English **Lose!**
  now occupies unused `(0,208,56,32)`; its second sprite samples a transparent texel. Only UV, size and
  position fields change, against pinned ANM SHA-1 `dffaf96bb9ef64da697e51f35b7dbdc80c8adc34`.
  Tests preserve the shared actor pixels, all flags/palettes/scales, and the Win/Draw records.
- `gen_gfx.py` can borrow a source rectangle's colours for a relocated label, and trim only blank margins
  of a pixel-font mask. The existing MIT `credits7.txt` font supplies the condensed labels.
  The duplicate-atlas scan found no additional identical copies of the changed atlases.
- `announcements_qa.py` previously matched short white words against a solid white panel because it checked
  ink only. Monochrome templates now require contrast around most transparent edges. Multicolour banners
  retain exact ink/outline matching; their dark outline may legitimately meet a black background.
- M590D reuses the same VRAM page/palette for different textures. `anm.render` now rejects ambiguous
  page assignments instead of silently taking the last TIM. `announcements_qa.py --textures 0` selects
  the story-mode texture explicitly. Without that selection, it compared the banner to unrelated actor art.

## Evidence and its limits

| Sprites | Cold capture | Complete pixel matches |
|---|---|---|
| M990D:2 items 15,16,17,18,19,35,44,45,46,47,72 | `work/qa/hud8_final` | 11/11 |
| M990D:3 Bonus items 17,52 (two palettes) | `work/qa/hud8_bonus` | 2/2 |
| M030D:6 Perfect, item 15 | `work/qa/outcomes8_m03_sprite` | 1/1 |
| M030D:7 Which?, item 3 | `work/qa/which8_fixture` | 1/1 |
| M140D:11 Streak, item 2 | `work/qa/outcomes8_m14_final` | 1/1 |
| M140D:11 Win/Lose, items 3/4 | `work/qa/outcomes8_m14_3`, `outcomes8_m14_4` | 2/2 |
| M560D:4 Win/Lose/Draw | `work/qa/outcomes8_m56_sprite` | 3/3 |
| M590D:9 story Win/Lose/Draw, texture 0 | `work/qa/outcomes8_m59_final` | 3/3 |

All matches use the current committed graphics/layout inputs. Earlier captures for unchanged sprites
remain valid at that limited scope; every newly changed sprite was recaptured after its final build.
Original comparisons: `hud8_original`, `outcomes8_m03_original`, `outcomes8_m14_original`,
`outcomes8_m56_original`, `outcomes8_m59_original`. The first M59 English capture failed visual review;
only `outcomes8_m59_final` contains the fixed Lose banner.

The shared HUD fixture redirects Pause's RAM item pointer, as in the earlier announcement checkpoint.
M14 instead replaces the natural Game Start item, because its Pause attempts did not show the banner.
`sprite_fixture.lua` redirects existing loaded ANM item pointers to another entry in the **same archive**,
then restores them. M03 replaces its backdrop; M56/M59 replace the speaking actor. Geometry, textures,
palettes and code are not injected. These are assembly/palette/legibility checks, **not** proof of normal
result timing or placement. The absent M03 background and absent speaking actors are intentional fixtures.

The circle-only M03 gameplay route (`which8_natural`, original `which8_original`) did not produce a complete
Which? match. Do not count it as natural Which? coverage. M59's other result sprites (TIM 6 / ANM 16) reuse
pages loaded with different images in the story fixture and remain unapproved. M14's Japanese wall scroll
also remains an open survey item; the banner verdict does not approve that background.

## Reproduce

Regenerate each changed atlas with `python -X utf8 tools/gen_gfx.py --only M990D.BIN:0 M030D.BIN:1 M140D.BIN:0 M590D.BIN:0`.
Check its exit code, then run `tools/build.py`. Every command below cold-boots the built disc:

```powershell
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/hud8_final --script tools/debug/warp.lua --script tools/debug/announcements.lua --script tools/lua/textlog.lua --var "SCENE='game_m11_0d'" --var ANNOUNCEMENTS=true --var 'ANNOUNCEMENT_SOURCE={file=350,entry=2,items={15,16,17,18,19,35,44,45,46,47,72}}' --var HOLD=-1 --frames 900 --timeout 180
python -X utf8 tools/debug/announcements_qa.py work/qa/hud8_final --out work/qa/hud8_coverage --entry 2 --items 15,16,17,18,19,35,44,45,46,47,72
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/outcomes8_m59_final --script tools/debug/warp.lua --script tools/debug/sprite_fixture.lua --script tools/lua/textlog.lua --var "SCENE='game_m59_37'" --var 'SPRITE_FIXTURE={mode=55,file=348,target=7,source=9,items={0,1,2}}' --var HOLD=-1 --frames 900 --timeout 180
python -X utf8 tools/debug/announcements_qa.py work/qa/outcomes8_m59_final --out work/qa/outcomes8_m59_final_coverage --file M590D.BIN --entry 9 --items 0,1,2 --textures 0
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/outcomes8_m14_final --script tools/debug/warp.lua --script tools/debug/announcements.lua --var "SCENE='game_m14_10'" --var ANNOUNCEMENTS=true --var ANNOUNCEMENT_MODE=16 --var ANNOUNCEMENT_TRIGGER=13 --var 'ANNOUNCEMENT_SOURCE={file=307,entry=11,items={2}}' --var HOLD=1000 --frames 900 --shot-every 15 --timeout 180
python -X utf8 tools/debug/announcements_qa.py work/qa/outcomes8_m14_final --out work/qa/outcomes8_m14_final_coverage --file M140D.BIN --entry 11 --items 2 --scan --glob 'f003[89]*.png'
```

Other fixture parameters (use a separate output directory per row):

| Scene | `SPRITE_FIXTURE` |
|---|---|
| game_m03_05, Perfect | `{mode=5,file=296,target=4,source=6,items={15}}` |
| game_m03_05, Which? | `{mode=5,file=296,target=4,source=7,items={3}}` |
| game_m56_34 | `{mode=52,file=345,target=2,source=4,items={0,1,2}}` |

For M14 Win/Lose, replace source item 2 with 3 or 4 and use the same scan gate. For Bonus, the shared
fixture uses `{file=350,entry=3,items={17,52}}` and the oracle uses `--items 17,52` (default entry 3).
Original comparisons use the original CUE with identical parameters and the oracle's `--original` flag.

## Fresh read-only visual review (D10)

After the final corrections, all six enlarged sheets were read without modifying implementation or art.
Scope: the listed glyphs, palette, complete assembly and legibility. The original comparisons confirmed
meanings and identified the shared Japanese Lose tail. Final verdicts are **6/6 scoped ok**:

| Manifest | Sheet | SHA-1 |
|---|---|---|
| `work/qa/hud8_review/manifest.tsv` | hud_sheet | 9083842599d25bdfead7c9bb8ab7f8441d5e7df6 |
| same | context_sheet | 7197b52de86b54463b8573d7be4a5650a6827d0f |
| same | bonus_sheet | 0e18a082f56547e0e195519c6283666ea605302f |
| `work/qa/outcomes8_review/manifest.tsv` | perfect_streak_sheet | e207dc0335b1bad4f1946bc2b5697693f83f37f6 |
| same | masks_sheet | 9ce59efa3a68691a9b3bfce07a91f8b32296c393 |
| same | which_sheet | 28d099bdc44ea72cb78f81fbcd1cab21dc838a03 |

Each manifest has `verdicts/review.tsv` beside it. Run the skill's `qa_gate.py check` on each manifest and
its sibling verdict directory. The HUD sheet crops `(152,124,80,28)` at 4x; other sheets retain full frames
at 2x (Which? at 3x). Hashes and scoped verdicts are preserved here because `work/` is ignored by git.

## Validation and outstanding phase work

- `tools/check.py`: 60 tests, lint 0 errors. Regression coverage includes white-panel false matches,
  black outlines on black backgrounds, ambiguous VRAM pages, missing pixel-font glyphs, partial sprite
  users across archives, and the protected M59 actor pixels.
- Disc verifier: 363 changed files, 0 errors.
- Cold smoke: `work/qa/outcomes8_final_smoke`, passed.
- Eight targeted textlogs (HUD, Bonus, M03/M14/M56/M59 fixtures, Which? fixture and gameplay) contain
  0 Japanese lines and 0 markers. Graphics are outside the text logger's detection.
- Main disc: 182,491,680 bytes; **2026-11-01 04:37:10 UTC**;
  SHA-1 **86480010b723c6376450b9181d30cd6b85c544ae**.
- Remaining: M59 TIM 6 / ANM 16 variant, natural outcome/Which? routes, other small HUD counters and the
  smaller Bonus with overlapping users, signs/cards/ending art, menu/record/rank states, captions, nine
  hanging-map routes and the full visual manifest. **The phase cannot advance to release.**

No owner-only decision blocks the remaining work. No shared skill files were changed.
Skill gotchas for `references/graphics.md`: ANM trailing fragments can include Japanese letters and actor
pixels, and one archive can reuse the same VRAM page for different TIMs. For `references/emulator-qa.md`:
exact opaque-pixel matching alone can falsely approve monochrome text on a solid panel.
