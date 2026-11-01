# Credits graphics QA, 2026-11-01

The credit lettering is English across **101 logical lines / 22 ANM items**, with complete cold-boot
screenshots for every item. This is a scoped phase-8 checkpoint, not phase-wide approval. Ending-art
signs and 祭 emblems are separate survey rows, and unconfirmed staff-name readings still need polish.

## Source, layout and implementation

- `gfx/credits.tsv` transcribes the disc images and gives each English line by ANM item and screen x/y.
  The source is EVT600D entries 2-4, assembled by ANM entry 37. All 22 assembled originals were inspected
  (`work/gfx/credits_jp/`, `work/gfx/credits_jp_sheet*.png`).
- `tools/gen_credits.py` joins adjacent fragments at the same screen y, letters the complete line, then
  scatters pixels back into the original source rectangles. It refuses missing/extra translations,
  reused source pixels and overflow. It changes no ANM, CLUT, code, sprite anchor or scrolling timing.
- `fonts/credits7.txt` is a new MIT hand-drawn 7-pixel font. Full names fit at native resolution without
  downscaling. Chief Director, Tsuyoshi Nakagawa and Created by use intentional two-line layouts.
- The 160-pixel T's Music line uses three fragments from three atlas rows. The final Special Thanks
  page draws from two different texture pages. Whole-row atlas replacement would break both.
- Every one of the three TIMs has **six byte-identical copies**, in EVT600D/610D/620D/630D/640D/650D.
  The generator uses `gen_gfx.copies()` over every archive, and emits all **18 PNGs**. The main
  `gen_gfx.py` command runs it too and shares its already-computed copy map.
- The first exploratory build changed only EVT600D and showed English for the first three items,
  then reloaded Japanese. `work/qa/credits8_en` is rejected evidence. The regression test for every
  reload failed on missing `EVT610D_2.png` before the fix and passes with all six archives redrawn.

## Reproduce

```powershell
python -X utf8 tools/gen_credits.py --preview work/gfx/credits_en
python -X utf8 tools/build.py
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/credits8_final --script tools/debug/warp.lua --script tools/lua/textlog.lua --var "SCENE='event20'" --var HOLD=11500 --frames 900 --shot-every 60 --timeout 300
python -X utf8 tools/debug/credits_qa.py work/qa/credits8_final --out work/qa/credits8_review
python -X utf8 "$(python tools/skill.py)/scripts/sheet.py" "work/qa/credits8_review/credit_*.png" --zoom 2 --cols 2 --max 6 --out work/qa/credits8_review/credits_sheet.png
python -X utf8 tools/textlog.py work/qa/credits8_final --all
```

Original cold reference: `work/qa/credits8_jp`, same warp on the original disc with HOLD=22000.
It reaches the final Hudson screen, which stays displayed. No controller input or save is needed.

`credits_qa.py` checks actual screenshots against all glyph and outline pixels of each complete ANM item,
at its original x anchor and any scroll y. It copies a matching frame per item and writes `coverage.tsv`.
It returns nonzero for missing items. It found **3/22** on the rejected partial build and **22/22** on
the final build. This checks presence/assembly, not translation quality; visual review remains required.

## Fresh read-only visual verdicts

D10 pass: read all four 2x cold-boot sheets after building and generating the manifest, then write only
the verdict file. All credit roles and names are legible, with no damaged background, clipped letter,
stray stroke, Japanese credit glyph or overlapping column. Outgoing credits crossing the screen edge
are original scrolling behavior, not a fit defect. Japanese background art remains separately tracked.

| Sheet in work/qa/credits8_review | Items | SHA-1 | Verdict |
|---|---|---|---|
| credits_sheet.png | 0-5 | 71a20f5b0f15b34baae6195a65f8747c8b054632 | ok |
| credits_sheet_2.png | 6-11 | 290c8bbfc4b42c797061ed285a18153528f0c788 | ok |
| credits_sheet_3.png | 12-17 | 93227d3f898e7de7863b5b3afd14f1447145d988 | ok |
| credits_sheet_4.png | 18-21 | 73b95ecc0c7009963b6728d9f993ab91a5e52b44 | ok |

Gate: `qa_gate.py check work/qa/credits8_review/manifest.tsv work/qa/credits8_review/verdicts` → **4/4 ok**.
The manifest must not substitute for the phase-wide manifest.

## Name readings and remaining polish

The on-disc credits are the primary source for names, roles and order. They have no kana for many names.
Western order and macron-free spellings follow D1/D2. Public credits were used to cross-check readings:

- [PS1 transcription](https://raido.moe/staff/ps1/ps1_momotaro_matsuri.html): useful as a second transcription,
  but it omits Product Managers/井上佳典 and attaches 梶野竜太郎 to the preceding role; the actual ANM item 19
  unambiguously contains both Product Managers. The disc takes precedence.
- [Music credits](https://vgmdb.net/release/20754): Kazuyuki Sekiguchi, Takeshi Ike, Kazuaki Miyaji,
  Yoshiyuki Kadooka, Pop'n T and Keisuke Mitsui.
- [Super Robot Taisen A credits](https://www.mobygames.com/game/141676/super-robot-taisen-a/credits/gameboy-advance/):
  Norio Okubo, Norihisa Takahata, Naoki Hirasawa, Takashi Fujii, Hidetoshi Goto, Tetsuma Yoshida,
  Masami Yasuraoka, Hiroyuki Kaneda, Minoru Sato, Katsutoshi Sato and Hiroyuki Arai.
- [Mario Party 2 credits](https://www.mobygames.com/game/6521/mario-party-2/credits/n64/):
  Hideyuki Kubota, Akira Katagi, Hiroyo Yokozawa and Tadayuki Kawada.
- [Akira Katagi's own profile](https://www.wantedly.com/id/akira_katagi) and
  [Hirotaka Hoshi's site](https://hoshihirotaka.github.io/PlayMakerLabLP/about.html) support those readings.
- [Yasuhiko Kubota](https://www.mobygames.com/game/211566/dx-nippon-tokkyu-ryoko-game/),
  [Takahide Otoizumi](https://www.mobygames.com/person/471548/takahide-otoizumi/credits/),
  [Tsuyoshi Nakagawa](https://www.mobygames.com/person/60355/tsuyoshi-nakagawa/), and
  [Yoshihide Ishizaki / Kazue Maeda](https://www.mobygames.com/game/28463/hudson-selection-vol-2-star-soldier/credits/gamecube/)
  were also cross-checked against credited names.

**Not a full linguistic approval:** the remaining kanji-name readings are conventional provisional
readings, not independently confirmed romanizations. In particular, check Takahiro Nishiyama, Hiromi
Nagashima, Koji Shioya, Akimitsu Takagi, Shoji Matsubara, Yasuto Kitai, Shigeaki Komiyaji, Kunihisa Uno,
Tomohiro Seguchi and the pen name 夢眠 (currently Mumin), plus the other uncited kanji names in the TSV.
Record the evidence or an explicit editorial ruling before closing the credits polish item. No owner
decision currently blocks other phase-8 work. The Exa search backend hit its free rate limit during
research; subsequent lookups used web search. GameFAQs' credits page was blocked by its host.

## Validation

- `tools/check.py`: **45 tests passed**, lint 0.
- `tools/verify_build.py`: **352 changed files, 0 errors**.
- `tools/textlog.py work/qa/credits8_final --all`: **0 Japanese lines, 0 markers**.
- Cold smoke: `work/qa/credits8_final_smoke`, exit 0 and smoke ok.
- `build/momotarou-matsuri_en.bin`: 182,571,648 bytes, **2026-11-01 02:06:24 UTC**.
- SHA-1: **4031eba32228dbfe896eb6222fa86c63a4a943d1**.

Skill gotcha for `references/graphics.md`: each ending background can reload a complete copy of the
credit atlas, even if that background displays only a few of its rows. Scan all archives, then verify
the whole roll cold; a first-screen shot or clean textlog misses the reload. The skill was not edited.
