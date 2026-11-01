# Even Tanuki scrolls and History Quiz helmet, 2026-11-02

Even Tanuki's two wall-scroll drawings now say **MATCH** for 勝負. Cold
controller-only play shows both complete sprites and the previously
fixture-only **Streak** label on both discs. Eight sheets pass a fresh D10
read-only review. **Phase 8 remains incomplete.**

## Source, preservation and copies

The scrolls are M140D TIM0, ANM11 items 0/1: `(160,128,24,32)` and
`(160,168,24,40)`, page5, CLUT `(0,480)`. `gfx_tanuki.py` replaces only
their paper interiors, using the existing MIT seven-pixel `credits7.txt`
font. MATCH runs down the narrow scroll, with a row-wise offset following
the tilted drawing. The green binding, shaded edges, brown mounts and red
seals remain unchanged, as do the palette, transparency and ANM records.

Tests check every pixel outside the paper spans, both red seals, the
unchanged alpha channel, and that the only ANM users of the edited spans
are items 0/1. Existing Win/Lose/Streak edits in the same atlas are retained.
The generator's whole-TIM duplicate search found no other copies. An
indexed rectangle search for the upright lettering also found only this
atlas: `gfxfind_rect.py M140D.BIN:0 166 134 178 153`. The separately drawn
tilted lettering is explicitly included rather than inferred from that scan.

## Reproduce the accepted cold evidence

```powershell
python -X utf8 tools/gen_gfx.py --only M140D.BIN:0
python -X utf8 tools/build.py
python -X utf8 tools/debug/tanuki_qa.py --out work/qa/tanuki8_en
python -X utf8 tools/debug/tanuki_qa.py --original --out work/qa/tanuki8_jp
```

The helper uses `warp.lua`'s `game_m14_10` cold entry, then Circle every 90
frames for 6500 frames. After the established warp, all progression comes
from controller input; no outcomes, RNG, animation selections, coordinates
or story state are injected. Native rolls differ between builds. The helper
reads ANM/TIM data from the named disc, stamps its SHA-1, verifies arrival,
and requires every opaque pixel of each complete sprite. `--check-only`
rejects a different disc hash before regenerating coverage artifacts.

| Item | English capture | Original capture | Complete placement |
|---|---|---|---|
| Upright scroll, ANM11 item 0 | f004308 | f004308 | (148,56), 24x32 |
| Tilted scroll, ANM11 item 1 | f005280 | f006360 | (152,56), 24x40 |
| Streak, ANM11 item 2 | f007284 | f005664 | (152,104), 32x16 |

English source SHA-1: `191e61ff4305eb4e21c0a596edefe71fbe4feb8e`;
original: `5d4768ed47341760d287ec08b37f5b62c5b8dc60`.
These are **3/3 complete native matches on each disc**. The earlier
`tanuki8_jp_probe` is exploratory; accepted hash-stamped runs are named above.

The original hanging scroll is absent from the two-player stage, which
places Even Tanuki in the centre. `tanuki.lua` adds native controller port 2
input to `two_player.lua`, with a 45-frame offset from player 1. Reproduce
the exploratory versus route with:

```powershell
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/tanuki_versus8_offset_en_probe --script tools/debug/warp.lua --script tools/debug/two_player.lua --script tools/debug/tanuki.lua --script tools/lua/textlog.lua --var "SCENE='game_m14_10'" --var HOLD=6000 --frames 900 --shot-every 12 --timeout 180
```

The earlier synchronous-pad runs `tanuki_versus8_en_probe` and
`tanuki_versus8_jp_probe` reached native three-round play; the English first
match tied 120–120. Both synchronous and offset English runs still have
**0/2 matches for M14 Win/Lose** in a full-width y 40–160 scan. This is not
evidence of disuse: natural Win/Lose remains unproved. The versus artwork
also exposes **Kintaro's untranslated 金 bib in M140D TIM2**; those broader
screens are not accepted. Its normal story return remains outside this route.

## History Quiz helmet: corrected classification

`corrected-tour-verdicts.tsv` sheet 015 called the History Quiz Oni helmet
Japanese. Enlarged original M510D TIM0 and fresh cold captures show a red
**question mark**, its separate square dot, and tiger stripes. No kanji or
kana appears on that helmet. This corrects that finding without changing
the artwork or granting an exception for other costume lettering.

Both discs were cold-booted with `warp.lua`, `SCENE='game_m51_2f'`,
`HOLD=180`, `--frames 900`, into `work/qa/quiz_helmet8_en` and
`work/qa/quiz_helmet8_jp`. Their `final.png` shows the helmet and intro text.
The final detail crop is `(140,84,40,22)` at 10x. The old verdict file remains
historical; this finding supersedes only its helmet concern. The other two
costume findings in that sheet have separate Fortune/Poverty God reports.

## Review and validation

After implementation and captures, a fresh read-only D10 pass inspected
all eight original/English sheets: two scroll contexts, two scroll details,
Streak context/detail, and Quiz context/helmet. **8/8 ok**, with hashes and
observations in `tanuki-verdicts.tsv`. The scrolls retain their outlines,
seals and paper edges. MATCH and STREAK are complete and readable, and
all shown English dialogue/counters fit.

For scroll sheets, use `sheet.py EN --compare JP --zoom 2` for context and
`--crop 144,52,40,48 --zoom 8` for detail. Streak detail uses
`--crop 148,96,60,32 --zoom 6`. Review artifacts and gate:

```powershell
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/tanuki8_review/manifest.tsv work/qa/tanuki8_review/verdicts
python -X utf8 tools/textlog.py work/qa/tanuki8_en
```

Validation: **133 tests passed / lint 0**, verifier **400 changed files /
0 errors**, cold `tanuki8_smoke` passed, **0 Japanese lines in one English
textlog** (graphics excluded). Main disc: **182,446,992 bytes**, built
**2026-11-01 18:55:20 UTC**, SHA-1
**191e61ff4305eb4e21c0a596edefe71fbe4feb8e**.

Remaining event/field marks, costume art, native banner/record routes, the
full visual manifest and story/NPC coverage still block phase 8. No shared
skill files changed. Gotcha for `references/emulator-qa.md`: `L.press`
queues controller 1 only; a real two-player gameplay route must drive
`PCSX.SIO0.slots[2].pads[1]` as well as selecting 2P in the native menu.
