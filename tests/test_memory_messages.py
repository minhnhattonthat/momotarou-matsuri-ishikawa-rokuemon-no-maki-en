"""Memory-card messages use a byte scanner before the ordinary text renderer."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import layout  # noqa: E402


@pytest.mark.parametrize('message', [
    'This will overwrite{KK}that file.{KK}Is that OK?{KE}',
    'Keep the card inserted.{KE}',
    'Check [4B][7F] here.{KE}',
])
def test_memory_message_rejects_literal_control_prefix(message):
    row = {'id': 'SLPM_868@80018480', 'jp': '確認{KE}', 'max': 255}
    _, errors = layout.render_line(message, row, 500)
    assert errors, 'native EXE scanner splits at every literal K byte'


def test_memory_message_preserves_delimiters_and_lowercase_k():
    row = {'id': 'SLPM_868@80018480', 'jp': '確認{KE}', 'max': 51}
    message = 'This will overwrite{KK}that file.{KK}Is that okay?{KE}'
    rendered, errors = layout.render_line(message, row, 500)
    assert rendered == message and errors == []


@pytest.mark.parametrize('message', ['Save{KK}Error{KE}', 'a' * 64 + '{KE}'])
def test_memory_message_rejects_scanner_end_and_buffer_overrun(message):
    row = {'id': 'SLPM_868@80018480', 'jp': '確認{KE}', 'max': 255}
    _, errors = layout.render_line(message, row, 500)
    assert errors


def test_memory_message_allows_first_line_e_and_terminated_full_buffer():
    row = {'id': 'SLPM_868@80018480', 'jp': '確認{KE}', 'max': 255}
    _, errors = layout.render_line('E' + 'a' * 61 + '{KE}', row, 500)
    assert errors == []
