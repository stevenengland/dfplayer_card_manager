import os

import pytest

from src.repository.repository_tree import RepositoryTree

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def repository_tree() -> RepositoryTree:
    sut = RepositoryTree()
    return sut  # noqa: WPS331


class TestValidSubdirDetection:
    def test_get_valid_subdirs_returns_valid_subdirs(self, sut: RepositoryTree, when):
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
        valid_subdirs = sut.get_valid_subdirs(root_dir)
        # THEN
        assert valid_subdirs == [
            "02",
            "40",
        ]
