# Native dice outcomes and nested text-log coverage, 2026-11-02

Gussurin (M56), the first Oni Mask Gang opponent (M59 selector 0), and
Ishikawa Rokuemon (M59 selector 5) now have **9/9 native Win/Lose/Draw
placements on both discs**. Their result banners are checked against the actual dice values
and complete ANM/TIM pixels from the named disc. This replaces the earlier
actor-substitution fixtures for the captured outcomes; it does not approve
normal story entry/return or the other four Oni encounters.

## Entry and native state evidence

`tools/debug/dice_outcomes.lua` runs after the existing cold game warp.
For M59 it sets only **0x8008C540**, once, before the overlay initializer;
OVLM59 **0x800CCC14..1C** copies that encounter selector to **0x800CE508**
in entry context 1. The helper requires the native copy to match. The
script starts controller input after the warp's 600-frame arrival delay;
it never changes RNG, dice values, outcomes, object pointers or artwork.

| Encounter | State / result state | Two u16 dice | Result descriptor | ANM / TIM |
|---|---|---|---|---|
| Gussurin | 800CCFE8 / 6 | 800CCFCC | 800CCE68 | 4 / 1 |
| Oni Mask Gang | 800CE514 / 7 | 800CE4F4 | 800CE390 | 9 / 0 |
| Ishikawa Rokuemon | 800CE514 / 7 | 800CE4F4 | 800CE390 | 16 / 6 |

Descriptor +0x10 is the item and +0x14 is its ANM bank. Items 0/1/2
mean player Win/Lose/Draw. OVLM56 **0x800CBBA0..CBCCC** and OVLM59
**0x800CC9F4..CCB20** choose those items from the dice comparison and
display the result for approximately 30 native updates. Screenshots at
result-state age 12 require the native item/bank to agree with the dice.
The Python oracle then checks every opaque banner pixel, including its
outline. Draw also leads through the native replay dialogue and another roll.

OVLM59 **0x800CCCBC..CCD18** loads TIMs 0..4 for selectors below 5,
but TIMs 5/6 for selector 5. **0x800CCE40..60** selects ANM9 versus
ANM16. Thus the previously unapproved M590D TIM6 is Rokuemon's alternate
encounter atlas, not the first Oni opponent's palette.

Original script leads independently confirm the encounter selector:
GSF0100D entry 4 at 0x14E contains `2D 003B 0001 0005 0005`;
GSV0200D entry 31 at 0xC4 contains `2D 003B 0001 0000 0017`.
GDEF0D entry 8 at 0x152 calls M56 with `2D 0038 0001 0000 0000`.
These are navigation leads only: this route still redirects Quick Match,
and its native exit to mode 0x61 is not a verified return to those scripts.

## Reproduce

```powershell
python -X utf8 tools/debug/dice_outcomes_qa.py --out work/qa/dice8_en --attempts 40
python -X utf8 tools/debug/dice_outcomes_qa.py --original --out work/qa/dice8_jp
python -X utf8 tools/debug/dice_outcomes_qa.py --original --out work/qa/dice8_jp --check-only
python -X utf8 tools/debug/dice_outcomes_qa.py --out work/qa/dice8_en --check-only --compare work/qa/dice8_jp
python -X utf8 tools/textlog.py work/qa/dice8_en
```

Each attempt is a fresh `emu.py` cold boot. Attempt i uses Circle period
`90 + 7*i` and offset `17*i`; only controller timing varies. The search
stops after all three outcomes match, and fails if the attempt limit leaves
one missing. `--resume` retains only completed attempts with the same disc
hash when extending a search. The initial 16-attempt English Rokuemon
search lacked Draw and correctly exited 1; it was extended, not accepted.
Final English coverage took **3/13/19 attempts** for Gussurin/Oni/Rokuemon;
the original took **4/2/2**. All **39 English result captures and 11 original
captures** match their complete sprites and native dice comparisons.

Both capture and `--check-only` use the named disc's SHA-1. Expected pixels
come from that disc, not mutable `gfx/en` sources. The English disc is
unchanged by this session: **182,446,992 bytes**, SHA-1
`1b0e790cf5bbc1142a2adc1d6f68dd1476a49e75`; original SHA-1
`5d4768ed47341760d287ec08b37f5b62c5b8dc60`.
An intentional negative `--original --check-only --out work/qa/dice8_en`
exits 1 with `stale disc captures` before generating coverage artifacts.

## Text scanner defect

The nested dice runs exposed a real QA false negative: `textlog.scan` keyed
each log by `log.parent.name`, so e.g. `gussurin/attempt_00` was overwritten
by `rokuemon/attempt_00`. A Japanese line in the former could disappear
from the final gate. The regression in `tests/test_textlog.py` first failed
with **0 Japanese lines in 2 logs** for three logs containing one Japanese
line. The fix keys by the path relative to the scan root, preserving flat
scene names and every nested case; the same regression now detects the
line and counts all three logs. Empty non-text logs remain excluded.

A read-only collision audit over every top-level `work/qa` directory found
only this session's `dice8_en` and `dice8_jp` affected. No older local
top-level QA collection had duplicate log-directory leaf names. This is
not a claim about deleted or external evidence.

## Review and remaining scope

Comparison sheets pair the first complete matching occurrence of each
outcome, with English left and original right. Different dice values and
actor poses are expected between builds. Whole-context sheets use 2x;
banner details use `(104,96,112,48)` at 6x.

A fresh read-only D10 pass inspected all **18 sheets** after implementation
and capture. **15 ok / 3 issue**, with **0 missing/stale verdicts**:
all nine banner details and the six Gussurin/Oni whole-context sheets pass.
The three Rokuemon whole-context sheets retain the coat-mark finding below;
the combined gate correctly exits 1. Durable hashes and notes are in
`dice-outcomes-verdicts.tsv`; live gate:

```powershell
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/dice8_en/review/manifest.tsv work/qa/dice8_en/review/verdicts
```

Rokuemon's tiny pale coat badges in M590D TIM5 need separate classification;
the enlarged atlas and native result views do not establish a reliable
reading. Their resemblance to his larger, already translated 六 badges is
a lead, not permission to call them decoration or approve all costume art.
The static inventory now includes **#895, M590D:5@12e80** (206 rows total).
Native mark near `(174,83)`; inspect the actor at `(108,36,104,120)` at 5x
and the original atlas at `(12,92,64,48)` at 10x with `sheet.py`.

Final validation: **136 tests passed / lint 0**, verifier **400 changed
files / 0 errors**, cold `work/qa/dice8_smoke` passed, and the corrected
text scanner reports **0 Japanese lines in all 35 English logs** (graphics
excluded). No disc sources or graphics were changed, and no rebuild was
necessary; the named main image retains the previous build's hash above.

Phase 8 remains incomplete: remaining graphics/classifications, natural
outcome and record contexts, the full corrected visual manifest and
story/NPC coverage still prevent phase 9. No owner decision is required.

Gotcha for the emulator-QA workflow: give recursively collected logs a
relative-path identity; repeated leaf names must not silently collapse
separate runs. No shared skill files were changed.
