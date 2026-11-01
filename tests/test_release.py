import glob
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
import release  # noqa: E402
import story  # noqa: E402


def test_polish_check_needs_every_line_ticked():
    release.polish_check('- [x] a\n- [x] b\n')
    with pytest.raises(SystemExit):
        release.polish_check('- [x] a\n- [ ] b\n')
    with pytest.raises(SystemExit):
        release.polish_check('nothing here\n')


def test_story_chapters_cover_every_story_file_once():
    every = [f for fs in story.files().values() for f in fs]
    assert len(every) == len(set(every))
    wanted = set(glob.glob(os.path.join(story.ROOT, 'script', 'GS[VFS]*.json')))
    wanted |= set(glob.glob(os.path.join(story.ROOT, 'script', 'EVT*.json')))
    wanted.add(os.path.join(story.ROOT, 'script', 'OVLEVT.json'))
    assert set(every) == wanted
