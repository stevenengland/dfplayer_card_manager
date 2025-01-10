from pathlib import PurePath

import pytest
from file_system_helper import FakeFileSystemHelper
from mockito import unstub

BASE_DIR = PurePath(__file__).parent.parent
TEST_ASSETS_DIR = BASE_DIR.joinpath("tests", "test_assets")


@pytest.fixture
def unstub_all():
    yield
    unstub()


@pytest.fixture(scope="function")
def test_assets_fs(fs):
    fsh = FakeFileSystemHelper(TEST_ASSETS_DIR, fs)
    yield fsh


@pytest.fixture(scope="function")
def test_assets_fs_w(fs):
    fsh = FakeFileSystemHelper(TEST_ASSETS_DIR, fs, read_only=False)
    yield fsh


def pytest_addoption(parser):
    parser.addoption(
        "--e2e",
        action="store_true",
        dest="e2e",
        default=False,
        help="enable e2e tests",
    )
