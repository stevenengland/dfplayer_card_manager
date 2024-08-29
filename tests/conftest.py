import pytest
from mockito import unstub


@pytest.fixture
def unstub_all():
    yield
    unstub()


def pytest_addoption(parser):
    parser.addoption(
        "--e2e",
        action="store_true",
        dest="e2e",
        default=False,
        help="enable e2e tests",
    )
