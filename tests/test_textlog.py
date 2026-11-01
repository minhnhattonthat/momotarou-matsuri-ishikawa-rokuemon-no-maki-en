"""Japanese detection must retain logs with repeated nested run names."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import textlog  # noqa: E402


def test_nested_names_cannot_hide_japanese(tmp_path, capsys):
    for case, line in (('a', '{93FA}{967B}'), ('b', 'English')):
        run = tmp_path / case / 'attempt_00'
        run.mkdir(parents=True)
        (run / 'log.txt').write_text(f'TEXT f123 48,170 {line}\n', encoding='utf-8')
    (tmp_path / 'log.txt').write_text('TEXT f124 48,170 Root log\n', encoding='utf-8')
    assert textlog.main(tmp_path) == 1
    output = capsys.readouterr().out
    assert 'a/attempt_00: 1 Japanese lines' in output
    assert '1 Japanese lines in 3 logs' in output


def test_single_level_names_and_empty_logs(tmp_path):
    for scene, line in (('scene1', 'TEXT f123 48,170 English\n'), ('scene2', 'ARRIVED scene2\n')):
        run = tmp_path / scene
        run.mkdir()
        (run / 'log.txt').write_text(line, encoding='utf-8')
    assert textlog.scan(tmp_path) == {'scene1': [(123, 48, 170, 'English')]}
