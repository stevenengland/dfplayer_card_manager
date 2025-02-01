from pathlib import PurePath

import pytest
from file_system_helper import FakeFileSystemHelper

BASE_DIR = PurePath(__file__).parent.parent
TEST_ASSETS_DIR = BASE_DIR.joinpath("tests", "test_assets")


@pytest.fixture(name="unstub_wo_verify", scope="function")
def get_unstub_wo_verify():
    from mockito import unstub  # noqa: WPS433

    yield unstub
    unstub()


@pytest.fixture(name="unstub", scope="function")
def get_unstub(unstub_wo_verify):
    from mockito import verifyStubbedInvocationsAreUsed  # noqa: WPS433

    yield unstub_wo_verify

    verifyStubbedInvocationsAreUsed()


@pytest.fixture
def when(unstub):
    from mockito import when  # noqa: WPS442, WPS433

    yield when
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
