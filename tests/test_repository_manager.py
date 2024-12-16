import os

import pytest

from src.repository.repository_manager import get_source_repository_tree

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


class TestRepositoryTreeCreation:
    def test_get_repository_tree_creates_correct_tree_wo_overrides(
        self,
        when,
    ):
        # GIVEN
        root_dir = "/root"
        when(os).listdir(root_dir).thenReturn(
            [
                "01",
                "02",
                "03",
            ],
        )
        when(os).listdir(os.path.join(root_dir, "01")).thenReturn(
            [
                "001.mp3",
                "002.mp3",
            ],
        )
        when(os).listdir(os.path.join(root_dir, "02")).thenReturn(
            [],  # empty dir
        )
        when(os).listdir(os.path.join(root_dir, "03")).thenReturn(
            [
                "001.mp3",
                "002.mp3",
                "003.mp3",
            ],  # extra file
        )
        when(os.path).isdir(...).thenReturn(True)
        when(os.path).isfile(...).thenReturn(True)

        # WHEN
        repository_tree = get_source_repository_tree(
            root_dir,
            r"^\d{2}$",
            r"\d{3}\.mp3",
        )
        # THEN
        assert len(repository_tree) == 5
        assert repository_tree[0] == os.path.join("01", "001.mp3")
        assert repository_tree[1] == os.path.join("01", "002.mp3")
        assert repository_tree[2] == os.path.join("03", "001.mp3")
        assert repository_tree[3] == os.path.join("03", "002.mp3")
        assert repository_tree[4] == os.path.join("03", "003.mp3")

    def test_get_repository_tree_creates_correct_tree_with_overrides(
        self,
        when,
    ):
        # GIVEN
        root_dir = "/root"
        when(os).listdir(root_dir).thenReturn(
            [
                "01",
                "02",
                "03",
            ],
        )
        when(os).listdir(os.path.join(root_dir, "01")).thenReturn(
            [
                "001.mp3",
                "002.mp3",
            ],
        )
        when(os).listdir(os.path.join(root_dir, "02")).thenReturn(
            [],  # empty dir
        )
        when(os).listdir(os.path.join(root_dir, "03")).thenReturn(
            [
                "001.mp3",
                "02.mp3",
                "003.mp3",
            ],  # extra file
        )
        when(os.path).isdir(...).thenReturn(True)
        when(os.path).isfile(...).thenReturn(True)

        # WHEN
        repository_tree = get_source_repository_tree(
            root_dir,
            r"^\d{2}$",
            r"\d{3}\.mp3",
            {"03": r"^\d{2}\.mp3$"},
        )
        # THEN
        assert len(repository_tree) == 3
        assert repository_tree[0] == os.path.join("01", "001.mp3")
        assert repository_tree[1] == os.path.join("01", "002.mp3")
        assert repository_tree[2] == os.path.join("03", "02.mp3")
