# Mask Maker and Mask Album QA

Verified from cold boots on 2026-11-01. This is a scoped phase-8 checkpoint, not approval of the full game.

## Graphics and text

`M250D.BIN:21` now says **Mask Album**. Entry 22 redraws **Done**, **Redo**, **L1** and **R1**, including
the bright and dim atlas variants. Only button interiors change; original beveled borders, TIM palette,
sprite geometry and face illustrations remain intact. `tools/gen_gfx.py --only M250D.BIN:21 M250D.BIN:22`
regenerates these images and still scans every archive for byte-identical copies.

The cold route exposed a separate English layout bug: the face preview covers the start of six OVLM70
instruction strings and four `M250D/34/` / `M250D/35/` dialogue rows. Seven ASCII spaces supplied only
28 pixels of padding. Four ideographic spaces provide 48 pixels and fit the original code-string slots.
The new `msg_mask` layout reserves the same 48 pixels on every wrapped dialogue line, within the existing
228-pixel budget. No wording is shortened. `tests/test_mask_layout.py` checks actual rows, code slot sizes,
pixel budgets, continuation-line padding and the `{MM}` substitution.

## Route and evidence

`SCENE='mask_editor'` follows New Game / Story and injects the game's Mask Maker shop call from
`GSV1306D:2` at byte 0x134: `2D 46 2 1 0 2E 3 0 0` (u16 operands). This avoids the invalid return context
of entering minigame mode 0x3A directly. The scene list now has 455 entries.

Pair `tools/debug/warp.lua` with `tools/debug/masks.lua`, `HOLD=-1`. The default controller route selects
all six parts, selects Done, and requires the confirmation state before succeeding. `MASK_ACCEPT=true`
also accepts the mask and requires a return to Story mode. It reads part slots
at 0x800CE7D0, interaction state at 0x800CE858, command-panel flag at 0x800CE7C8, and the cursor object
pointer at 0x800CE180. The Done cursor has y=0x82000 at object+0x1C. These reads synchronize controller
input; the probe does not manufacture selected parts. Optional `MASK_ACTIONS` supports error/cancel routes.

```powershell
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/mask8_adaptive3 --script tools/debug/warp.lua --script tools/debug/masks.lua --script tools/lua/textlog.lua --var "SCENE='mask_editor'" --var HOLD=-1 --frames 16000
python -X utf8 tools/debug/announcements_qa.py work/qa/mask8_final --out work/qa/mask8_coverage --file M250D.BIN --entry 25 --items 2,3,4,5,6,7 --scan --glob 'mask_*.png'
python -X utf8 tools/debug/announcements_qa.py work/qa/mask8_album --out work/qa/mask8_title_coverage --file M250D.BIN --entry 27 --items 0 --scan
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/mask8_review/manifest.tsv work/qa/mask8_review/verdicts
```

- `work/qa/mask8_final`: **6/6 complete ANM items** match cold screenshots (bright/dim Done and Redo,
  displayed L1/R1 hints). Dim L1/R1 are redrawn in the atlas but are not separate runtime coverage claims.
- `work/qa/mask8_album`: **1/1 complete title** matches; reached via `game_m72_3c`, HOLD=900.
- `work/qa/mask8_missing`: empty-mask error, Redo and Keep making masks? choice.
- `work/qa/mask8_adaptive3`: all six parts selected and Is this mask all right? confirmation reached.
- Original comparisons: `work/qa/mask8_original` (fixed inputs) and `work/qa/mask8_adaptive_original`
  (all six parts plus confirmation). The same original layouts confirm the indentation bug is English-only.
- `work/qa/mask8_accept` and `work/qa/mask8_accept_original`: accept the completed mask and return to
  Story; paired screenshot shows the opening invitation resumes correctly on both discs.
- Fresh read-only D10 review: **3/3 sheets ok** in `work/qa/mask8_review`. Textlog: **0 Japanese lines**
  across the final mask runs (this excludes graphics).

Build: **182,491,680 bytes**, **2026-11-01 04:02:28 UTC**, SHA-1
`bd6ff6ca1786b31afe0695b328a3a05af2c741b2`. `tools/check.py`: **56 tests passed**, lint 0;
`verify_build.py`: **363 changed files, 0 errors**; cold smoke `work/qa/mask8_smoke` passed.

## Gotchas and limits

- `references/graphics.md`: these ANM items use **8bpp** pages and flag **0x100**, not the common 4bpp
  format. `tools/anm.py` now checks the flag against source depth and renders both; other flags/scales still
  fail closed. This lets the screenshot oracle compare complete sprites rather than atlas fragments.
- `references/emulator-qa.md`: fixed taps can be lost during mask menu transitions. Wait for actual part
  values and cursor coordinates; a selected category index is not the part slot's storage index.
- `references/emulator-qa.md`: an unchanged box can still have a portrait exclusion zone. Reserve it on
  every wrapped line; ordinary space counts are unsafe when replacing Japanese padding with VWF English.

The accepted-mask route proves return to Story; memory-card persistence and populated album navigation
still need broader menu coverage. Town signs, card illustration lettering, small HUDs and the full visual
tour remain open.
