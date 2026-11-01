# Decisions

The user's rulings on scope, style and trade-offs, newest last. Read before asking the user anything; if a later
decision replaces one, mark the old one "replaced by D<n>" instead of deleting it. Binding term spellings live in
`glossary.md`; this file holds the why.

| # | Date | Question | Options offered | Decision and reason |
|---|---|---|---|---|
| D1 | 2026-10-31 | Honorifics and name order | keep (-san), drop; JP or Western order | Keep honorifics; Western order (given name first). Owner's standing answer for one-shot runs. |
| D2 | 2026-10-31 | Romanization source for names | official art, earlier patch, Hepburn | Official English names where they exist, else an earlier fan patch, else Hepburn without macrons (Momotaro, not Momotarou). Owner's standing answer; matches `../momotarou-densetsu-en`. |
| D3 | 2026-10-31 | Credits | stay Japanese, translate | English. Owner's standing answer. |
| D4 | 2026-10-31 | Abbreviations | engine work first (default), abbreviate | Default: full names and terms; engine work before shortening; abbreviate only as a flagged last resort. |
| D5 | 2026-10-31 | Graphics text left in Japanese | none (default), list | Translate all graphics text (titles, menus, banners, cards); leave the Japanese logo only if it has no official English version (none known: this game was Japan-only). |
| D6 | 2026-10-31 | Specs and plans | need approval, pre-approved | Pre-approved: keep going through checkpoints, report at the end. Never `gh release create`, never change repo visibility; the run ends at a built and verified release zip. |
| D7 | 2026-10-31 | Existing saves / memory cards / savestates | user's files, none | None provided; build the debug tool (phase 2) as usual. |
| D8 | 2026-10-31 | Git identity | ask, preset | Already set by new-game.ps1; do not change it. |
| D9 | 2026-11-01 | Who does the independent reviews (phase 6 reviewer, phase 8 visual QA, phase 9 story pass) in one-shot runs | repo's read-only `reviewer`/`visual-qa` agents in-session, `codex exec`, wait | Run brief: no Orca worker will start a reviewer; do it in a fresh read-only pass. In-session `.claude/agents` read-only agents count as that pass (codex is out of quota until 2026-11-05). |
| D10 | 2026-11-01 | Review ownership for the resumed Orca dispatch | fresh read-only self-review, `codex exec` | Current owner brief explicitly permits the worker's own fresh read-only pass and says nested Orca workers are unavailable. Record concrete verdicts and their limited scope; this does not waive any phase-wide QA gate. |
| D11 | 2026-11-02 | Phase 8 graphics QA was too strict (redrawing marks on character clothes) | keep strict, lenient | Lenient, then move to phase 9. Narrows D5: translate legible UI, menus, titles, banners, cards and readable shop/place signs. Leave as art: marks on character clothes/costumes (bibs, badges, crowns, coat marks), emblems, tiny or illegible placards, wall scrolls, landscape kanji, and copies with no proven on-screen use. Fixture/cold proof is enough; natural-route proof is not required. Work already done stays. |
| D12 | 2026-11-02 | Publish v1.0; make the private repo public (D6 forbade visibility changes) | make public, keep private | Owner asked to publish and chose public. Replaces D6's visibility clause for this repo. |
