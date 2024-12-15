import os

import pytest

from src.repository.target_repository_tree import TargetRepositoryTree

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def target_repository_tree() -> TargetRepositoryTree:
    sut = TargetRepositoryTree()
    return sut  # noqa: WPS331


class TestValidSubdirDetection:
    def test_get_valid_subdirs_returns_valid_subdirs(
        self,
        sut: TargetRepositoryTree,
        when,
    ):
        # GIVEN
        root_dir = "/root"
        when(os).listdir(root_dir).thenReturn(
            [
                "01",
                "mp3",
                "advertisment",
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
        valid_subdirs = sut.get_valid_root_dirs(root_dir, r"^\d{2}$")
        # THEN
        assert valid_subdirs == [
            "02",
            "40",
        ]


class TestValidFileDetectionInSubdirs:
    def test_get_valid_subdir_files_returns_valid_files(
        self,
        sut: TargetRepositoryTree,
        when,
    ):
        # GIVEN
        subdir = "/subdir"
        when(os).listdir(subdir).thenReturn(
            [
                "01.file",
                "002.mp3",
                "advertisment",
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
        valid_files = sut.get_valid_subdir_files(subdir, r"^\d{3}\.mp3$")
        # THEN
        assert valid_files == [
            "001.mp3",
            "006.mp3",
        ]


class TestRepositoryTreeCreation:
    def test_get_repository_tree_creates_correct_tree(
        self,
        sut: TargetRepositoryTree,
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
        repository_tree = sut.get_repository_tree(root_dir)
        # THEN
        assert len(repository_tree) == 5
        assert repository_tree[0].tree_id == "01_001.mp3"
        assert repository_tree[0].dir == "01"
        assert repository_tree[0].file_name == "001.mp3"

        assert repository_tree[1].tree_id == "01_002.mp3"
        assert repository_tree[1].dir == "01"
        assert repository_tree[1].file_name == "002.mp3"

        assert repository_tree[2].tree_id == "03_001.mp3"
        assert repository_tree[2].dir == "03"
        assert repository_tree[2].file_name == "001.mp3"

        assert repository_tree[3].tree_id == "03_002.mp3"
        assert repository_tree[3].dir == "03"
        assert repository_tree[3].file_name == "002.mp3"

        assert repository_tree[4].tree_id == "03_003.mp3"
        assert repository_tree[4].dir == "03"
        assert repository_tree[4].file_name == "003.mp3"
