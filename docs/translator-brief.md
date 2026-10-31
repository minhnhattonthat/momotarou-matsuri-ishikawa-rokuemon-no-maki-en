# Translator brief - Momotarou Matsuri: Ishikawa Rokuemon no Maki (PS1, Hudson 2001)

You translate part of the Japanese script of Momotarou Matsuri into English for a fan patch. It is a comic,
all-ages Hudson party game set in the Momotaro Densetsu world: Momotaro travels from village to village to play
festival games (minigames, quizzes, races), earns levels and trophies, and along the way foils Ishikawa Rokuemon
and his Oni Mask Gang, who steal four bells to revive the God of Destruction. Work only on the batches named in
your dispatch, one at a time in the order given, each to a passing check before the next. Do all translation
yourself; do not dispatch subagents.

## Read first
1. `docs/style-reference.md` - voices, tics and approved example pairs. Match this voice.
2. `build/terms_<batch>.txt` - binding glossary rows for this batch (`glossary.md` has the rulings and full tables).
3. `docs/synopsis.md` - who is who and the plot. Don't give a reveal away early.

## Input: `work/tl/<batch>.tsv`
`id<TAB>speaker<TAB>form<TAB>limit<TAB>Japanese` (speaker is blank: the script has none; infer it from context).
- form: `msg` (dialogue/narration box, 228 px a line), `msg_portrait` (box with a face, 192 px a line), `choice`
  (one answer/choice line, 72 px, about 13 characters), `choice_top` (200 px), `caption` (place name, 116 px),
  `code` (menu/label/UI string from the program), `memcard` (memory-card message).
- limit: `<px>px x3/page` for messages; `<px>px <n>B` for code strings: n bytes is a HARD cap (1 byte per English
  character); a px value with `~` is only the Japanese width (a soft guide: stay close).
- In the Japanese, ` / ` is a line break inside a page and `{KP}` a page break (button press). Entries are in game
  order: neighbours give context. Ids that share a prefix (`M510D/37/0000.0` .. `.3`) are one menu.
- Code strings (`OVLGMAIN@...`, `SLPM_868@...`): menu labels, shop names, and 2-3 line descriptions of places, arts
  and items stored one line per entry, often **bottom line first** (`島です` then `えんま大王が　暮らす` = "an island
  where Great King Enma lives"). Translate the description as a whole and split the English across its entries so
  it reads top to bottom in the game's order (the entry listed second is drawn first), each within its byte cap.

## Output: `work/tl/<batch>.out.tsv`, written with your file-write tool (never a shell heredoc)
`id<TAB>English`, every input id exactly once, same order. Plain printable ASCII only: straight quotes, `...`;
no tabs inside the English, no Japanese or full-width characters, no `\uXXXX`, no `\n`.
- **Messages: do not write line breaks.** The build word-wraps each page to the box (3 lines a page). Write each
  page as one run of text and separate pages with `{KP}` where the JP has one. You may add a `{KP}` when a page runs
  past 3 lines (about 120 characters in `msg`, 100 in `msg_portrait`); never remove one. A message whose JP ends
  with `{KN}` ends with `{KN}` too.
- Copy every other code exactly, same count: `{MM}` (an inserted name: item, card...), `{R0}`-`{R3}` (a number),
  `{bb}...{ww}` (blue highlight around a name or key word: keep it around the English of the same words; `{rr}`
  `{oo}` `{dd}` are other colours), `[XX]` raw bytes, `{KK}`/`{KE}` (memory-card line break / end).
- Forced break `{n}`: only where a break must fall (a quote followed by narration on its own line, a list); never to
  fit text.
- Dry run any line: `python -X utf8 tools/layout.py "English" --jp <id>` prints the wrapped lines with widths.
- Choices and code strings are one line: no `{n}`/`{KP}`. Quiz answers must stay distinguishable and fit 72 px
  (capitals ~6 px, lower case ~5 px, i/l 2 px, space 4 px).

## Validate
Run `python -X utf8 tools/batches.py check <batch>` from the repo root and fix every ERROR until it prints OK.
A glossary term from the JP missing in your English, or an honorific dropped (桃太郎さん without "Momotaro-san"),
is an ERROR. When the JP word is not the glossary sense (a pun, a common noun), keep your English and report
`GLOSSARY: id term reason`; the controller lists it in `script/glossary_ok.txt`.

## Style
- Faithful: keep the information and order of ideas; adapt idiom, not meaning. Don't add or skip content. Adapt
  wordplay, puns, proverbs and parodies so the joke still lands (no translator notes).
- Names and terms exactly as in the glossary and terms file. Never abbreviate to fit; rephrase, and report
  `LONG: id` if meaning had to give.
- Honorifics kept and hyphenated (Momotaro-san, -sama, -kun, -chan, -dono); Western name order. 「」 -> "...",
  『』 -> '...', … -> `...`, ！？ -> `?!`.
- Placeholders: no suffix glued to a variable ("No. {R0}", never "{R0}th"); no a/an right before {MM}; numbers with
  a counter: "{R0} ryo", "{R0} points".
- Quizzes (M510D etc.): translate question and answers so the correct answer stays correct in English. Japanese
  language quizzes (kanji readings, opposite words, proverbs, dialects): keep the Japanese word in romaji where the
  question is about it ("What is the opposite of 'takai' (high)?") so the answer still works; keep answers short.
  History/geography answers: standard English names (Toyotomi Hideyoshi, Hokkaido, Saitama Prefecture).
- Menu labels and UI: short title-case English that says what it does (Quit, Sell, Buy, Items, Status).
- Stock phrases: "Momotaro got X!", "Momotaro used X!", "X appeared!", "X left!"; no "GET!" calques.

## Consistency
Never edit `glossary.md`. For a recurring name or term not in it, pick a form, use it consistently, and report it.

## Report (reply with only this)
Files written and entry count; then any lines: `NEW TERM: jp -> en`, `GLOSSARY: id term reason`,
`UNSURE: id - note`, `LONG: id - note`.
