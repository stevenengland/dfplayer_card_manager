import pytest
from typer.testing import CliRunner

from dfplayer_card_manager.cli.cli import app
from dfplayer_card_manager.repository import fat_checker


@pytest.fixture(scope="function", name="cli_runner")
def get_cli_runner() -> CliRunner:
    return CliRunner()


class TestChecks:
    def test_fat_check_returns_false(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(fat_checker).check_is_fat32(...).thenReturn(False)
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        assert fat32_check_output.exit_code != 0
        assert "fat32" in fat32_check_output.stdout
