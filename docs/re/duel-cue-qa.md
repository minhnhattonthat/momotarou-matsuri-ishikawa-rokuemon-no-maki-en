# Paper Fan Chop Duel cue, 2026-11-02

The native five-second countdown now ends with **Duel**, matching both
instruction pages (`M160D/15/000A` and `M160D/16/000A`). The previous shared
HUD graphic said Match. Cold solo and versus runs on both discs show the
complete cue through the game's own timer logic, with no sprite substitution,
timer writes or outcome edits. **Phase 8 remains incomplete.**

## Change and preservation

`gfx_hud.WORDS[73]` changes Match to Duel in M990D TIM 0's already allocated
English region. Item 73's ANM rectangle becomes 15x8. Its horizontal offset
now centres that width within the original 32-pixel cue; other HUD units keep
their left edges. The existing preservation test checks the cue's centre to
within one pixel and preserves every other item's position. Original shared
Japanese fragments remain untouched for their separate, unresolved consumers.

The first enlarged review rejected the new word's inherited left alignment:
`work/qa/duel8_review/solo_detail_sheet.png`, SHA-1
`7dc644c15f15bba53a8577bce29925b2b9df0d59`. That build
(`b3ce2debb5903b2af655d3ef24f7ae3076856bc4`) is superseded. The final
screens place English at (152,64), compared with Japanese at (144,60).
The original 32x16 cue and its panel retain the same centre.

## Native routes and rejection checks

`tools/debug/duel_qa.py` cold-boots both cases, waits without Circle presses,
and requires a complete ANM/TIM match inside the timer panel. It reads its
template from the **named disc**, stamps each capture run with that disc's
SHA-1, and rejects stale captures. `duel.lua` verifies the native selector at
**0x8008C580** and M16's copied selector at **0x800D1104** after initialization.
EXE **0x800428F0** returns that selector (0 solo, 1 versus).

Mashing Circle attacks early and repeatedly skips the cue. The old exploratory
solo click route did not display it. Waiting instead reaches complete solo
and versus cues at **f004440** and **f004710**, respectively, on both discs.
The original control is `work/qa/duel8_final_jp`; final English is
`work/qa/duel8_centered_en`. All four cases pass the whole-cue check.
The original reference SHA-1 is `5d4768ed47341760d287ec08b37f5b62c5b8dc60`.

The old Match screenshot at `work/qa/duel8_wait_en/f004440.png` is rejected
by the new Duel template (0/1 items), providing a negative content control.
The initial fixed-time 2P experiment is also rejected: it selected the wrong
branch on one disc and encountered a disconnected second controller on the
other. Those exploratory screenshots are not accepted versus evidence.

`two_player.lua` now supplies controller input using Quick Match's native
state at **0x800E2ABC**: state 1 selects the game, state 2 chooses 2P, and
state 4 confirms. It waits for message typing, checks controller presence at
**0x800A3DD4**, and asserts selector 1 at game entry. `warp.lua` permits this
probe to own those menu presses via `WARP_GAME_INPUT=false`; its default
behaviour is unchanged. The emulator configuration snapshot and local copy
now connect controller port 2. The probe neither spoofs presence in game RAM
nor writes the player count. Both characters appear in the final versus shot.

The menu still previews Daruma Drop before the established warp redirects its
mode to M16. This verifies native player selection plus M16's own loader and
renderer, not full menu selection of M16 or story progression. No second-player
attack is needed to display the countdown-expiry cue.

```powershell
python -X utf8 tools/gen_gfx.py --only M990D.BIN:0
python -X utf8 tools/build.py
python -X utf8 tools/debug/duel_qa.py --out work/qa/duel8_centered_en
python -X utf8 tools/debug/duel_qa.py --original --out work/qa/duel8_final_jp
python -X utf8 tools/debug/duel_qa.py --check-only --out work/qa/duel8_centered_en
python -X utf8 tools/textlog.py work/qa/duel8_centered_en
```

For each case, compare `cue.png` against the same case on the original using
`sheet.py --zoom 2`; detail crops use `--crop 128,48,64,40 --zoom 6`.
Also compare `versus/two_player_menu.png` at 2x. The final five sheets live in
`work/qa/duel8_centered_review`. Fresh D10 read-only review inspected all five
after the centering change: **5/5 ok**, hashes in `duel-cue-verdicts.tsv`.
This is scoped to the cue, surrounding HUD and player-selection menu; it does
not approve every sign, natural result, later story state or NPC interaction.

## Validation and remaining work

Final disc: **182,449,344 bytes**, built **2026-11-01 18:09:17 UTC**, SHA-1
**cbadc82590fd4cfb81d78ddca889a293d47faebe**. Disc verification reports
**400 changed files / 0 errors**. The final cold smoke at
`work/qa/duel8_centered_smoke` passes. Both English textlogs contain **0
Japanese lines** (graphics excluded). Repository checks: **131 tests / lint 0**.

Natural Win/Loss/min/sec/later/small-Bonus coverage and the preserved M990D
fragments remain open. So do the unresolved field/event artwork and phase-wide
visual/story/NPC gates listed in `docs/status.md`; phase 9 has not started.
The separate red card-notice investigation gained static leads only, recorded
in `card-full-art-qa.md`. `call_contexts.py` preserves the reusable direct-call
scan; it explicitly does not prove register dataflow or unused code.

No shared skill files changed. Gotchas for `references/emulator-qa.md`:
controller mashing can skip the very result cue being tested, and a native
two-player route must verify both controller presence and the game's selected
player count rather than trusting a timed Down press.
