# Card Album and card-caption QA, 2026-11-01

Phase 8 remains incomplete. This checkpoint translates the album overview and all 100 prefecture captions,
and reaches all 100 card illustrations from a cold boot. The handwritten dialect words and sound effects
inside those illustrations remain Japanese and are **not** approved by the caption-only visual manifest.

## Reproduce

```powershell
python -X utf8 tools/gen_gfx.py
python -X utf8 tools/build.py
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/cards8_captions3 --script tools/debug/warp.lua --script tools/debug/cards.lua --script tools/lua/textlog.lua --var "SCENE='card_album'" --var HOLD=-1 --frames 900 --timeout 300
python -X utf8 tools/debug/cards_qa.py work/qa/cards8_captions3 --out work/qa/cards8_review
python -X utf8 tools/textlog.py work/qa/cards8_captions3
python -X utf8 "$(python tools/skill.py)/scripts/sheet.py" "work/qa/cards8_captions3/card_[0-9]*.png" --crop 88,32,120,16 --zoom 3 --cols 5 --max 25 --out work/qa/cards8_review/captions_sheet.png
python -X utf8 "$(python tools/skill.py)/scripts/sheet.py" work/qa/cards8_captions3/album.png --zoom 3 --out work/qa/cards8_review/album_sheet.png
```

The run recorded here used `build/cards8.cue`, then rebuilt the identical default disc. Its SHA-1 is below.
Original reference: the same route on `rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue`,
output `work/qa/cards8_jp_all3`; run `cards_qa.py ... --original` for its expected Japanese captions.
`CARD_COUNT=3` is an optional short probe; it cannot pass the 100-card coverage gate.

## Runtime findings (verified)

- Card Album is top-level mode **0x4C**, entry **OVLXTTL 0x800D7FA8**, initialization **0x800D78E0**.
  The mode-switch table at EXE 0x80018158 is indexed by **mode minus one**.
- `card_album cards 0` in the scene list follows New Game -> Story and changes the first mode-0x4D frame
  to 0x4C. It sets only collectible flags 0-99 at **0x800BD9F8**, preserving the upper nibble of byte 12.
  EXE **0x800428D0 -> 0x80033234** reads these bits. No save, ROM code or player file is edited.
- OVLXTTL **0x800E0414** maps display indices to collectible bit indices (100 u32s); display order is not
  acquisition-bit order. **0x800E05DC** is the 100-pointer table of card meanings already in the script.
  `cards_qa.py` emits the exact script IDs, Japanese meanings and English meanings in `coverage.tsv`.
- Card index is u32 **0x800E2324**, card-view state is u16 **0x800E232C** (7 = ready), held-repeat counter is
  u32 **0x800E2328**. The controller drives the game's normal loader, including all ten HCARD archive banks.
- A timed tap can be lost or retained while loading from CD. Initial runs failed explicitly after card 004,
  and the next attempt skipped 021-023 at a bank boundary, on **both original and translated discs**.
  `cards.lua` now retries only the unchanged previous page, and clears Right in the RAM pad snapshots
  (**0x8008C410** held, **0x8008C420** newly pressed) plus the repeat counter as soon as the target index
  arrives. An unexpected index/state still fails. It neither supplies textures nor bypasses card loading.
- Final runs capture **100/100** complete cards on both discs. The image gate checks all nontransparent
  pixels of the **208x128** illustration at screen **(56,56)** and the **120x16** caption at **(88,32)**,
  against each card's own TIM. Palette conversion allows at most 8 units of RGB difference. Tests reject
  both an old Japanese caption and the wrong card illustration.
- Card 001's English meaning “Really ticks me off” matches the original's `すごくムカツク`; do not change it
  based on a literal reading of the hand-lettered dialect phrase. The source game supplies the meaning.

## Redraws and limits

- `HOUGEN0D:0`: green Card Album title, seven region names, and redundant Japanese count suffixes removed.
  Region labels stop before the dynamic counters. Chugoku-Shikoku and Kyushu-Okinawa use the existing MIT
  condensed seven-pixel capitals to keep both full names. An initial faint rendition was rejected; final
  lettering uses the original solid dark palette colour.
- `HCARD00D` through `HCARD90D`, entries 0-9: all 100 prefecture names, in the name strip **(48,128)-(120,144)**.
  Original `NO.###`, illustrations, palettes and ANM records stay unchanged. The whole-archive duplicate
  sweep is still used. The six prefectures with three cards are Tokyo, Osaka, Nara, Wakayama, Tokushima and
  Ehime; every other prefecture has two. Names fit the actual 120-pixel caption sprite.
- Still open: every card's handwritten dialect/SFX graphics; the red fragmented new-card tag in the album
  atlas (not displayed by this overview route); the retained Japanese title-logo panel. The existing D5 logo
  exception does not exempt dialect/SFX or new-card tags. None of these rows is declared fully translated.
- Future artwork edits must update the intentional art-preservation assertion in `tests/test_cards.py` with
  the newly reviewed edit regions; they must not silently drop this protection.

## Fresh read-only verdicts (D10)

After the final build, opened and read all five enlarged sheets. These are restricted to the overview and
the caption strips; they are not verdicts for the full card illustrations or the phase-wide scene tour.

| Sheet under `work/qa/cards8_review` | SHA-1 | Verdict |
|---|---|---|
| album_sheet.png | 92c9a8078ef1165e2d91d26eed5480ef02e716d6 | ok: full region names, title and all counters readable, no overlap |
| captions_sheet.png | 57cf44c2f66a4628ce0668ae86c46e80fb69e6aa | ok: cards 001-025, names and numbers complete |
| captions_sheet_2.png | 264083d1496079722797ff0cf25a4538442a225a | ok: cards 026-050, names and numbers complete |
| captions_sheet_3.png | d7008a41bf31a223ade0c4c86b6fa04c11a937e4 | ok: cards 051-075, names and numbers complete |
| captions_sheet_4.png | f470e9252cc95c21fb6637ee0a4975b7b46a56eb | ok: cards 076-100, names and numbers complete |

`qa_gate.py check work/qa/cards8_review/manifest.tsv work/qa/cards8_review/verdicts`: **5/5 ok**.

## Validation

- `tools/check.py`: **50 tests passed**, lint **0 errors**.
- `tools/verify_build.py`: **363 changed files, 0 errors**.
- `cards_qa.py`: **100/100** complete card captures on each disc.
- `tools/textlog.py work/qa/cards8_captions3`: **0 Japanese lines**, no markers. This logger does not inspect
  handwritten graphics, so this is not evidence that the full cards are translated.
- Cold smoke: `work/qa/cards8_final_smoke`, **smoke ok**.
- Default disc: **182,543,424 bytes**, built **2026-11-01 02:52:33 UTC**,
  SHA-1 **dcd7600ce28f778f642cd81b7908ae947d753591**.

Skill gotcha for `references/emulator-qa.md`: a short controller tap can be retained across a PS1 CD-load
stall; check the selected page and actual texture, and release the game's cached pad bits in a RAM-only
fixture if necessary. The skill itself was not modified.
