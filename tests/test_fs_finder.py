import os

import pytest

from src.repository.fs_finder import get_valid_root_dirs, get_valid_subdir_files

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
        valid_files = get_valid_subdir_files(subdir, r"^\d{3}\.mp3$")
        # THEN
        assert valid_files == [
            "001.mp3",
            "006.mp3",
        ]
