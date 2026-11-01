# Momotarou Matsuri: Ishikawa Rokuemon no Maki English translation

Unofficial English fan translation of **Momotarou Matsuri: Ishikawa Rokuemon no Maki** (PlayStation, Hudson Soft, 2001): the source text and tools
that build the patch.

**Just want to play?** Download the patch from [Releases](../../releases) and follow its README. This repository holds
no game data you can play; you need your own dump of the Japanese game.

**Found a bug?** [Report it](../../issues/new/choose): untranslated text, typos, overflow, crashes. Attaching a savestate
helps most.

## Translation status

| Part | Status |
|---|---|
| Dialogue / story | Translated |
| Menus, items, quizzes, minigames, system messages | Translated |
| Title, menus, banners, Dialect Cards, readable shop and place signs | Translated |
| Marks on character clothes, emblems, tiny placards, wall scrolls | Left as art |
| Credits roll | Translated |
| Music and sound | Unchanged |

Known issues: see [Issues](../../issues).

## What's here

| Path | What it is |
|---|---|
| `script/` | Every text block: original Japanese and English. Translation fixes go here. |
| `glossary.md` | Binding names, terms and style rules. |
| `tools/` | Python build chain: extract, insert, lint, release. |
| `tests/` | pytest suite (ROM-dependent tests skip when the ROM is absent). |
| `docs/re/` | Reverse-engineering notes. |
| `docs/decisions.md`, `docs/status.md` | Rulings with their reasons; current progress and open bugs. |
| `docs/fonts.md` | Fonts used and their licences. |
| `AGENTS.md` | Instructions for coding agents (`CLAUDE.md` points to it). |
| `.claude/agents/` | Subagent types (translator, reviewer, visual QA, playtester) with only the tools each needs. |

## Build your own patched ROM

Needs Python 3.12+ and your own dump of the Japanese game.

```sh
git clone https://github.com/minhnhattonthat/momotarou-matsuri-ishikawa-rokuemon-no-maki-en
cd momotarou-matsuri-ishikawa-rokuemon-no-maki-en
# copy your dump to: rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).bin (+ its .cue)
#   (182816256 bytes, SHA-1 5d4768ed47341760d287ec08b37f5b62c5b8dc60; the build refuses any other dump, see rom.sha1)
python -X utf8 tools/build.py                          # -> build/momotarou-matsuri_en.cue/.bin
python -X utf8 tools/check.py                          # tests + text lint
```

## Support

If you enjoy this translation, you can support my work on Ko-fi:

[![Support me on Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/minhnhattonthat)

## Licence

Tools and English translation: MIT. The original Japanese text in `script/` is Hudson Soft's and is included only so
the translation can be checked against it. Momotarou Matsuri is (c) 2001 Hudson Soft (now Konami); this project is not affiliated with them.
Do not share patched ROMs.

The translation was made with extensive AI assistance (Claude by Anthropic). Corrections are very welcome.
