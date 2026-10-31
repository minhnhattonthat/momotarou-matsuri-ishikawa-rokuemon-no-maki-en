# Translation reviewer brief - Momotarou Matsuri: Ishikawa Rokuemon no Maki

You review a group of batches of a JP->English fan translation. Read-only: no edits, no git, no subagents.
Mechanical validity (ids, control codes, encodable characters, width, byte caps) is already enforced by the check
tool - judge translation quality. Return the report as your final message.

## Inputs (paths in your dispatch)
- Pairs file: every translated entry as `>> id | JP` / `EN` with +-2 context lines. Read ALL of it, in passes if large.
- `glossary.md` (rulings at the top), `docs/style-reference.md`, `docs/synopsis.md`.
- Codes: `{KP}` new page, `{KN}` wait/end, `{bb}..{ww}` blue highlight, `{rr}` red, `{MM}` / `{R0}`.. inserted
  name or number. Code strings (ids `FILE@ADDR`) have byte caps, so short forms there are expected; flag only a
  short form that is wrong or unreadable.
- Quizzes (M510D/M530D/M580D): the `.0` choice is the correct answer; kanji questions are glossed in English
  ("Live+Start"). Check the right answer stays right and the decoys stay wrong.

## Judge
- Accuracy: mistranslation, omission, addition, wrong speaker or addressee, reversed meaning. Quote the JP and say
  what it means.
- Consistency: glossary names/terms exactly; honorifics kept per the rulings.
- Things players caught that reviewers missed: jokes/wordplay losing their punch; ordinal suffix after a variable
  ("1th"); stock phrases that read awkwardly in English ("... GET!").
- Voice: each speaker against the style reference. Speech quirks (ぞい, ニャ, ござる, drawn-out endings), register
  (old-man じゃ/のう/わし, rough ぜ/ねぇ, feminine かしら/わよ) and emotional intensity must come through.
- Naturalness: would a fan-translation reader stumble?

## Report
### Issues
#### Critical (meaning reversed, broken placeholder grammar, wrong speaker, wrong quiz answer)
#### Important (clear mistranslation, glossary inconsistency, a character's voice flattened, joke dead)
#### Minor (style - deferred to one polish pass)
Each: `id - JP gist - problem - suggested EN`.
### Assessment
Approved | Needs fixes - one sentence why.
