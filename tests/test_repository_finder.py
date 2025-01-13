import os

import pytest

from dfplayer_card_manager.repository.repository_finder import (
    get_repository_tree,
    get_valid_root_dirs,
    get_valid_subdir_files,
)

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


class TestValidSubdirDetection:
    def test_get_valid_subdirs_returns_valid_subdirs(
        self,
        when,
    ):
        # GIVEN
        root_dir = "/root"
        when(os).listdir(root_dir).thenReturn(
            [
                "01",
                "mp3",
                "advert",
                "02",
                "003",
                "3",
                "40",
                ".6dir",
                ".git",
            ],
        )
        when(os.path).isdir(...).thenReturn(True)
        file_not_dir_path = os.path.join(root_dir, "01")
        when(os.path).isdir(file_not_dir_path).thenReturn(False)
        # WHEN
        valid_subdirs = get_valid_root_dirs(root_dir, r"^\d{2}$")
        # THEN
        assert valid_subdirs == [
            "02",
            "40",
        ]


class TestValidFileDetectionInSubdirs:
    def test_get_valid_subdir_files_returns_valid_files(
        self,
        when,
    ):
        # GIVEN
        subdir = "/subdir"
        when(os).listdir(subdir).thenReturn(
            [
                "01.file",
                "002.mp3",
                "advert",
                "006.mp3",
                "003",
                "001.mp3",
                "04.mp3",
                ".git",
            ],
        )
        when(os.path).isfile(...).thenReturn(True)
        dir_not_file_path = os.path.join(subdir, "002.mp3")
        when(os.path).isfile(dir_not_file_path).thenReturn(False)
        # WHEN
        valid_files = get_valid_subdir_files(subdir, r"^\d{3}\.mp3$")
        # THEN
        assert valid_files == [
            "001.mp3",
            "006.mp3",
        ]


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
        repository_tree = get_repository_tree(
            root_dir,
            r"^\d{2}$",
            r"\d{3}\.mp3",
        )
        # THEN
        assert len(repository_tree) == 5
        assert repository_tree[0] == ("01", "001.mp3")
        assert repository_tree[1] == ("01", "002.mp3")
        assert repository_tree[2] == ("03", "001.mp3")
        assert repository_tree[3] == ("03", "002.mp3")
        assert repository_tree[4] == ("03", "003.mp3")

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
        repository_tree = get_repository_tree(
            root_dir,
            r"^\d{2}$",
            r"\d{3}\.mp3",
            {"03": r"^\d{2}\.mp3$"},
        )
        # THEN
        assert len(repository_tree) == 3
        assert repository_tree[0] == ("01", "001.mp3")
        assert repository_tree[1] == ("01", "002.mp3")
        assert repository_tree[2] == ("03", "02.mp3")
