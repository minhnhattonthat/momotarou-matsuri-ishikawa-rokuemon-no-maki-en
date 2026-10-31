# Momotarou Matsuri: Ishikawa Rokuemon no Maki (PS1) English translation

Skill: translate-retro-game (Claude Code: plugin, enabled in .claude/settings.json; other agents: its SKILL.md). `python tools/skill.py` prints its folder; `"$(python tools/skill.py)"` works in bash and PowerShell; never paste a `plugins/cache/<hash>` path. Read SKILL.md before ROM, text or QA work.

## Commands (run from repo root)
- Build:    `python -X utf8 tools/build.py` -> `build/momotarou-matsuri_en.cue/.bin` (phase 3+; checks the dump against `rom.sha1` first)
- Check:    `python -X utf8 tools/check.py` (tests + lint; the pre-commit hook runs it; `git config core.hooksPath tools/hooks` once per clone)
- Smoke:    `python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/smoke --route tools/routes/boot.txt --smoke` (boot.txt ends on the New/Continue menu)
- Warp:     `python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/warp --script tools/debug/warp.lua --var "SCENE='<name>'" --frames 900 --sheet` (scenes: `tools/debug/scenes.txt`, RE in `docs/re/debug.md`; all scenes: `python -X utf8 tools/debug/warp_all.py [CUE]`; never ask the user to play to a scene)
- Release:  `python -X utf8 tools/release.py` (phase 9; xdelta against the .bin; patch + verify; never publish without the user)
- Clean:    `python -X utf8 tools/clean.py` (published projects: lists rebuildable/downloadable files; `--yes` deletes)

## Paths
- Original disc: `rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).bin/.cue` (gitignored; one MODE2/2352 track; SHA-1 of the .bin in `rom.sha1`, checked by `tools/check_rom.py`).
- Emulator: PCSX-Redux nightly 29999.20261030.11 x64 in `tools/pcsx/` (`fetch_emu.py pcsx`, distrib.app dev-win-x64 channel; gitignored; settings copy in `tools/emu-config/pcsx.json`). BIOS `tools/bios/scph5500.bin` (`fetch_emu.py psx-bios`, used automatically). Savestates: `work/states/`.
- Disc tools: `tools/mkpsxiso-2.30-win64/` (dumpsxiso/mkpsxiso 2.30), `tools/armips/`; xdelta3 on PATH (scoop). All gitignored: re-download from the URLs in `references/setup.md` of the skill.
- Text: `script/<FILE>.json` (one per disc file; fields id/kind/jp/en[/max]; format and codes in `tools/text.py`
  docstring; `text.py dump` never overwrites). JP table: built in `tools/text.py` (cp932 + codes). Glossary: `glossary.md`. RE notes index: `docs/re/README.md`. Fonts and their licences: `docs/fonts.md`.

## Rulings
- Edit source files (.py .lua .asm .tbl .json) only with the file-edit tool; scripts here read and analyse, never `.replace()` and write back.
- Subagents: dispatch the `.claude/agents/` types (translator, reviewer, visual-qa, playtester), never general-purpose: their short tool list cuts each agent's start-up context from ~43k to ~9k tokens.
- The user's decisions, with the options and reasons: `docs/decisions.md`. Read it before asking the user anything; add each new ruling there the same session.
- Player bug reports: GitHub issues (`gh issue list --label bug`). Copy the attached save into `work/states/`, reproduce in the emulator, fix, commit with `Fixes #N`, and update `docs/status.md`.
- Emulator runs headless through `emu.py` only. Japanese games confirm with circle (`--mash-key circle`). The title takes Start only from ~frame 2400 after a cold boot (intro length varies by a few hundred frames).
- Sibling repo `../momotarou-densetsu-en` (PS1, same series) has names and terms to reuse in `glossary.md`.

## Status
`docs/status.md`: done, next, open bugs. Update it at the end of every session.
