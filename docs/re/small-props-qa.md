# Small signs and winning flag (phase 8)

This is a scoped graphics checkpoint. It does not complete phase 8's full
visual, graphics, caption or story-interaction gates.

## Changes and bugs found during cold review

`tools/gfx_props.py` translates the Moat Swimming Meet winning flag (M170D:20),
the sushi menu (M440D:0/1), and the bath counter's private-booking placard
(GV16090D:1 plus its byte-identical GV36110D:1 and GV36120D:1 copies).
The generator retains palettes, sprite geometry, silhouettes and surrounding
art. All source PNGs regenerate through `gen_gfx.py --only` with those four keys.

- The flag's 一番 reads **First**, inside its original white flag.
- The sushi prices are **Fatty Tuna 400**, **Sea Urchin 300**, **Salmon Roe
  200**, **Shrimp 200**, **Egg 100**. The Japanese board shares one 200 label
  between salmon roe and shrimp. Repeating 200 keeps the horizontal pairs clear.
- The bath's 予約 / 本日 / 貸切 becomes **Private Today**.

The inherited first draft failed cold review in several ways. Its sushi eraser
removed grey ink but retained dark brown antialiasing, leaving Japanese strokes
under the English. It also kept the old vertical layout, whose lower portions
are covered by the cats and other actors. The final eraser borrows light wood
from the same scanline, and complete English names/prices sit above the actors
at y=48..63. The price font uses five new hand-drawn digits in the existing MIT
`fonts/credits7.txt`; no tiny scaled TrueType numerals remain.

The first horizontal layout clipped Egg at the texture seam. M440D:0 has a
256-pixel canvas, but its opaque background ends at x=240; M440D:1 starts at
screen x=240. The complete Egg/100 pair now occupies atlas 1. Both the old
Japanese tail across the seam and the original vertical prices are erased.

The first victory-flag draft had wrong bounds: (224,8)..(240,56) added English
beside the Japanese instead of removing it. The read-only full-screen and zoom
review rejected both sheets even though that small rectangle matched. The final
bounds (206,24)..(238,80) cover both characters while excluding the pole and
wavy flag edges. A doubled pixel word fills the flag vertically; three separate
original-stroke locations are regression-tested as cleared paper. The updated
pixel oracle now checks the whole lettering region, not the old corner.

The placard uses **CLUT 2**, where CLUT 0's purple indices 1/2/3 are dark ink,
and 4/5 are pale paper. Erasing by CLUT 0 brightness inverted the lower English
line in game. The final code identifies paper/ink by those indices and letters
both lines with index 3, which is (32,32,32) in the actual palette. Tests cover
both lines in all three copies, brown edge removal, intact alpha and frames,
binary pixel-font numerals, and the space above the sushi actors.

## Reproduction

Build first, with no emulator holding the output file:

```powershell
python -X utf8 tools/check.py
python -X utf8 tools/build.py --out build/props_final9.bin
python -X utf8 tools/verify_build.py build/props_final9.cue
python -X utf8 tools/debug/warp_all.py build/props_final9.cue --out work/qa/props8_sushi_final --only game_m44_2c --hold 3500 --click 45 --every 120 --probe tools/lua/textlog.lua --jobs 1
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/props_final9.cue --out work/qa/props8_flag_retry --script tools/debug/warp.lua --script tools/lua/textlog.lua --var "SCENE='game_m17_13'" --var HOLD=75000 --var CLICK=45 --frames 1 --shot-every 300 --timeout 600
python -X utf8 tools/debug/signs_tour.py --cue build/props_final9.cue --out work/qa/props8_baths_final --jobs 1
```

The race and sushi runs use only Circle after the standard cold minigame warp.
They substitute no sprites, textures, dice results, victory flags or record
values. The bath routes use the correct map initializers and controller walking.
Original references use the same commands without the positional English CUE,
or `signs_tour.py --original`, in `remaining_props_jp`, `remaining_flag_long_jp`
and `remaining_baths_jp` respectively. The long race plays multiple rounds;
300-frame captures are searched for the winning illustration. A 30,000-frame
attempt did not prove it and is not an accepted route.
The first final-disc rerun (`props8_flag_recheck`, HOLD=80000) did capture the
correct victory, but the emulator returned exit -1 at shutdown. It is not the
accepted successful route; the shorter cold retry above stops after the first
victory sequence. An earlier phase-7 parallel tour also recorded intermittent
PCSX exit -1; this run's cause is unconfirmed, and its failure is not waived.

`tools/debug/props_qa.py RUN --key FILE.BIN:ENTRY --out DIR` requires every
complete English label rectangle to match a real screenshot. Add `--original`
for reference pixels, or `--glob 'walk_*.png'` for the bath captures. It records
frame, screen position and palette. The original sushi comparison uses the
English layout's rectangles; it is not a claim that the original vertical
Japanese is fully unobscured. Sprite-assembly and surrounding-art checks still
require the visual pass.

## Coverage and limits

The final sushi run matches all **five full name/price pairs** at f003960:
screen (72,48), (116,48), (160,48), (204,48), and (240,48), palette 0.
All **three private-bath placards** match at `walk_0060.png`, screen (145,21),
palette 2. The original race's complete flag matches at f057000, (206,24),
palette 0. The final English flag matches at **f074100, (206,24), palette 0**
in `work/qa/props8_flag_retry`; that cold run exits **0**, with 264 captures.
The combined gate covers **9/9 labels**: five food/price pairs, three placards,
and the complete victory flag. The six accepted English textlogs (sushi, race,
contest and three baths) have **0 Japanese lines**; the logger excludes graphics.

Original title logos in CI0D/TITLE0D, YUGI0D:1, HOUGEN0D:2 and FILESL0D:1
were also inspected and classified under the existing **D5** exception. They
contain the original product title/subtitle/furigana; this ruling does not
exempt other graphics lettering. See `graphics.md` and the updated survey.

The existing phase-wide gaps remain: town signs, card illustration lettering,
ending art, remaining HUD/outcome contexts, Rank Details, caption scenes and
the corrected map interaction tour. No release artifact was generated.

## Final build validation

`tools/check.py` passes **97 tests**, with **0 lint errors**.
`verify_build.py build/props_final9.cue` reports **369 changed files, 0 errors**.
The default main disc is byte-identical to that QA disc: **182,482,272 bytes**,
SHA-1 **81f569029bc195b8ea7e8bdb725b1de469099a43**, built **2026-11-01 09:45:58 UTC**.
Its final cold smoke at `work/qa/smallprops8_main_smoke` passes.

## Fresh read-only visual verdicts (D10)

All eight sheets were inspected after the assets were frozen. The first flag
review rejected the old rectangle; its two issue verdicts are retained in
`01_review.tsv`, with newer fixed verdicts in `02_flag_fixed.tsv`. The accepted
retry's flag sheets are byte-identical to the reviewed corrected previews.
The final sushi/bath reruns also leave all six previously accepted hashes
unchanged. Comparison sheets use English on the left, original on the right;
flag fireworks differ by ordinary animation timing.

`qa_gate.py check work/qa/smallprops8_review/manifest.tsv work/qa/smallprops8_review/verdicts`
accepts **8/8**, with no missing, stale or issue verdicts. These approvals cover
the named props and preserved surrounding art, not the entire phase-wide tour.

| Sheet | SHA-1 | Verdict |
|---|---|---|
| bath189_sheet | 7f9ed3244fbeebb53368bf81559c962cec0b0156 | ok, complete private-booking sign |
| bath332_sheet | dd0ac16ddcf73b9f7c91f3c4f7186a0f0b187937 | ok, second cold context |
| bath333_sheet | dd0ac16ddcf73b9f7c91f3c4f7186a0f0b187937 | ok, third cold context |
| bath_zoom_sheet | c579ee8408ad0f396f5d6d7168ad4044e707bb1c | ok, both words dark and legible |
| sushi_sheet | b4a8c276bab5bd6d94f53c7e50a3f6e2d9c48efe | ok, complete labels above the actors |
| sushi_zoom_sheet | 0d81a126006929b3342c4bebe108b307a333ef04 | ok, five full names and correct prices |
| flag_sheet | a92b97e77f66c10272086886229e143b7872e539 | fixed, both kanji replaced |
| flag_zoom_sheet | b50393b8add167b483e92c31fe8d2501ade9be26 | fixed, full First with intact flag edges |

Skill gotchas for `references/graphics.md`: source-palette brightness may be
opposite to the sprite's actual CLUT; dark brown text antialiasing is not grey;
and a texture's visible seam can precede its canvas edge. Match complete words
in cold screenshots and preserve transparent atlas padding. No shared skill
files were changed.
