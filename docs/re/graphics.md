# Graphics, font, graphics-text survey

## Images (verified: `tools/gfxdump.py` decodes every one)
- Every image on the disc is an ECD-compressed TIM archive entry (disc.md): 953 unique images after dedup
  (1,965 TIM entries + 348 CLUT-only). No uncompressed or embedded TIMs anywhere (scan of every file incl. EXE
  and overlays for TIM headers at non-entry offsets found none).
- Some GV??01D images carry 0xCDCD (uninitialised) width/height in the TIM image header; the real size is
  256 px wide (4bpp) by data length. `tim.parse` handles it; a TIM writer must keep those header bytes as they are.
- Sweep output: `work/gfx/sheet_NNN.png` (80 sheets, first CLUT only, so colours can be off) and
  `work/gfx/index.tsv` (id -> file:entry@offset, size, duplicate copies). Regenerate: `python -X utf8 tools/gfxdump.py`.

## Main text font (verified by rendering; draw path not yet hooked)
- FONT0D.BIN entries 0 and 1: two 4bpp 256x256 TIMs (VRAM 896,256 and 960,256, CLUT at 256,480). Each holds
  **two 2-bit glyph pages** in the nibble planes (bits 0-1 and bits 2-3; values seen 0,3,4,7,8,11,12,15), each
  page 16x16 cells of 16x16 px (glyphs ~12 px). Entry 0 page B: digits, hiragana, katakana, punctuation,
  ○×□△, arrows, L/R and ~60 kanji; the other three pages are kanji. About 1,000 glyphs; **no Latin letters**
  (English needs new glyphs and a SJIS -> cell mapping change: phase 5). The SJIS -> cell table is not found yet.
- Other fonts drawn as images (from the survey): M990D 0/1 (shared minigame HUD words and big outlined result
  words), M230D:3 (small kana+ASCII font, one minigame), NAME0D:1 (name-entry hiragana keyboard).

## Graphics-text survey (static sweep, phase 1)
Every Japanese-bearing image found by five read-only reviewers over all 80 sheets: **`docs/re/gfx_survey.tsv`**
(201 rows including the subsequently discovered Status staff badge: id, file:entry, kind, transcription, note). Summary of the original 200-row sweep:

| Kind | Rows | What |
|---|---|---|
| logo | 6 | title logo pieces + press-start prompt (CI0D:3), logo panels (YUGI0D:1, HOUGEN0D:2, FILESL0D:1), name tags (CHR0D:1) |
| menu | 5 | character name plates (CHR0D:2), mode menu labels ゆうぎアルバム/段位詳細/おためし対戦!/ネームエントリー (NAME0D:0), status screen (STATUS0D:0), card-album UI (HOUGEN0D:0), mask album buttons (M250D:22) |
| banner | 14 | minigame start/result banners (勝ち!/負け!/引き分け!, じゃんけん!ぽん!, で賞! awards, 大当たり, スタート), 天下一だじゃれ大会 festival banner (GV02000D:2, GV13000D:2), hill kanji (EVT090D:1/2) |
| card | 100 | the 100 dialect cards HCARD00-90: prefecture captions and marginal dialect phrases English (`cards-qa.md`, `card-words-qa.md`); illustration SFX/signs still Japanese |
| credits | 3 | staff roll EVT600D:2-4 plus five copies each: English, 22/22 cold-shot items, scoped 4/4 visual gate; readings polish remains (`credits-qa.md`) |
| sign | 57 | town tilesets (八百屋, 宿, 茶, 湯, ゆ?? boards, round plaques, 男湯/女湯 noren), sushi price board (M440D:0), flags; many tiny and unread |
| font | 6 | FONT0D (main text), M990D 0/1, M230D:3, NAME0D:1 |
| hud / other | 9 | 白/赤 team icons (DEF0D:9), speech bubbles (M060D:2, M080D:6), 祭 emblems in ending art (keep), どっち? |

Open for later phases:
- Status now has all six rank illustrations and a maximum-width counter fixture.
  `status-ranks-qa.md` records the overlap/border fixes and the new Hermit staff
  lettering omitted from the original survey. `album-records-qa.md` now covers all
  43 Game Album and six Quick Match record panels, including populated and empty
  score categories. Name Entry now uses 80 Latin/symbol sprites in both NAME0D
  and PREM0D, with complete cold glyph matches, four- and one-letter entry,
  editing and record return (`name-entry-qa.md`). Four- and one-letter names
  now have native save/overwrite and separate cold-load proof on both discs
  (`name-persistence-qa.md`). Rank Details and naturally earned records remain unverified.
- GCV0310's four labelled images are dormant dialogue placeholders, IDs 123-126,
  with no references among 4,894 parsed message operations. The Moon route uploads
  their texture but never binds the portraits (`portrait-audit.md`). This is not
  proof of universal native-code unreachability; reopen the row if displayed.
- Character-introduction names: all five full names are English with natural cold title-attract proof,
  5/5 complete character/name pairs on each disc and 5 scoped visual sheets (`character-intro-qa.md`).
  Yashahime is three fragments of one name, not two copies. Follow-up `character-props-qa.md` covers both
  Festival fans and all ten coat numerals with new natural 5/5 pair matches and 3/3 scoped comparison sheets.
  Separate ending/card marks and the four GCV0310 tags remain outside this portrait approval.
- Field signs: both Pun Contest atlases are English; only GV13000D:2 has a cold display proof. The men's/women's
  bath curtains have six cold matches across all three atlas copies. Four scoped visual sheets are accepted;
  the tiny restored bath-counter placard remains unclassified (`field-signs-qa.md`). The corrected map warps
  now load NPCs/decorations; older background-only map captures cannot establish their graphics coverage.
- Shared HUD counter progress: twelve further words and M34's wider counter panel have cold proof and
  scoped verdicts in `hud-counters-qa.md`. Natural uses of seven words and three preserved fragment items
  remain open; an English atlas or a clean text log does not close those runtime gaps.
- Rows marked `unsure`/`?` (mostly tiny town signs and flags) need a zoomed look with the right CLUT (phase 8
  decides translate vs. keep-as-art; D5 says translate all graphics text).
- Not seen in the sweep but on screen in the Daruma minigame: blue `ターン!` (likely an M990D/DEF0D sprite;
  confirm with a VRAM dump in phase 5/8). Runtime screens (chapter cards, game over, ending) get the tour pass
  once the debug tool exists (phase 2) and the marker build shows what stays Japanese (phase 5).
