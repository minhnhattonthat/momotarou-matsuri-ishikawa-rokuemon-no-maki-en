"""Mask-preview sprites must not obscure code instructions or wrapped messages."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import engine  # noqa: E402
import layout  # noqa: E402
import text  # noqa: E402


def test_mask_code_instructions_clear_preview_and_fit_original_slots():
    rows = json.loads((ROOT / 'script/OVLM70.json').read_text(encoding='utf-8'))
    instructions = [r for r in rows if r['jp'].startswith('　')]
    assert len(instructions) == 6
    for row in instructions:
        indent = row['en'][:len(row['en']) - len(row['en'].lstrip())]
        assert 48 + engine.width_px(indent) >= 96  # preview ends at x=88
        assert 48 + engine.width_px(row['en']) <= 276
        assert len(text.encode_text(row['en'])) <= row['max']


def test_mask_dialogue_reserves_preview_space_on_every_wrapped_line():
    rows = json.loads((ROOT / 'script/M250D.json').read_text(encoding='utf-8'))
    rows = [r for r in rows if r['id'].startswith(('M250D/34/', 'M250D/35/'))]
    assert len(rows) == 4
    # The name control must remain intact and count towards the available width.
    for row in rows:
        rendered, errors = layout.render(row, 'msg_mask')
        assert not errors
        for line in rendered.splitlines():
            if layout.CODE.sub('', line).strip():
                assert line.startswith('　' * 4)
                assert layout.width(line) <= 228
                assert layout.units(line) <= 32
        assert rendered.count('{MM}') == row['en'].count('{MM}')
    stress = 'Choose the mask you would like to wear. Please check every part carefully.'
    rendered, errors = layout.render_msg(stress, 'a\nb\nc', 228, indent='　' * 4)
    assert not errors
    assert len(rendered.splitlines()) == 3
    visible = [line for line in rendered.splitlines() if line.strip()]
    assert len(visible) >= 2
    assert all(line.startswith('　' * 4) and layout.width(line) <= 228 for line in visible)
