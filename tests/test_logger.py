import pytest
from mockito import contains, verify

from dfplayer_card_manager.logging.logger import Logger
from dfplayer_card_manager.logging.verbosity_level import VerbosityLevel

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def get_logger(when) -> Logger:
    sut = Logger()
    return sut  # noqa: WPS331


def test_debug(sut: Logger, when):
    # GIVEN
    sut.verbosity = VerbosityLevel.debug
    when(sut.console).print(...).thenReturn(None)
    # WHEN
    sut.debug("This is a debug message")
    # THEN
    verify(sut.console, times=1).print(contains("D: "))


def test_debug_does_not_print_when_verbosity_is_info(sut: Logger, when):
    # GIVEN
    sut.verbosity = VerbosityLevel.info
    when(sut.console).print(...).thenReturn(None)
    # WHEN
    sut.debug("This is a debug message")
    # THEN
    verify(sut.console, times=0).print(contains("D: "))


def test_info(sut: Logger, when):
    # GIVEN
    sut.verbosity = VerbosityLevel.info
    when(sut.console).print(...).thenReturn(None)
    # WHEN
    sut.info("This is an info message")
    # THEN
    verify(sut.console, times=1).print(contains("I: "))


def test_warn(sut: Logger, when):
    # GIVEN
    sut.verbosity = VerbosityLevel.warn
    when(sut.console).print(...).thenReturn(None)
    # WHEN
    sut.warn("This is a warning message")
    # THEN
    verify(sut.console, times=1).print(contains("W: "))


def test_error(sut: Logger, when):
    # GIVEN
    sut.verbosity = VerbosityLevel.error
    when(sut.console).print(...).thenReturn(None)
    # WHEN
    sut.error("This is an error message")
    # THEN
    verify(sut.console, times=1).print(contains("E: "))
