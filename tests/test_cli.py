import pytest
from typer.testing import CliRunner

from dfplayer_card_manager.cli.cli import app, content_checker, fat_sorter
from dfplayer_card_manager.fat import fat_checker

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="cli_runner")
def get_cli_runner(monkeypatch) -> CliRunner:
    monkeypatch.setattr(fat_checker, "check_is_fat32", lambda _filesystem_path: True)
    monkeypatch.setattr(
        fat_checker,
        "check_has_correct_allocation_unit_size",
        lambda _filesystem_path: True,
    )
    monkeypatch.setattr(fat_sorter, "is_fat_root_sorted", lambda _filesystem_path: True)
    monkeypatch.setattr(
        content_checker,
        "get_root_dir_numbering_gaps",
        lambda _dirs: [],
    )
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
        assert "is not a path within a FAT32" in fat32_check_output.stdout

    def test_fat_check_returns_true(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(fat_checker).check_is_fat32(...).thenReturn(True)
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        assert fat32_check_output.exit_code == 0
        assert "is a path within a FAT32" in fat32_check_output.stdout

    def test_fat_check_returns_false_allocation_unit_size(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(fat_checker).check_has_correct_allocation_unit_size(...).thenReturn(False)
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        assert fat32_check_output.exit_code == 0  # Since the check is not fatal
        assert (
            "does not have the correct allocation unit size"
            in fat32_check_output.stdout
        )

    def test_fat_check_returns_true_allocation_unit_size(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(fat_checker).check_has_correct_allocation_unit_size(...).thenReturn(True)
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        assert fat32_check_output.exit_code == 0
        assert "has the correct allocation unit size" in fat32_check_output.stdout

    def test_fat_check_returns_false_sorted(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(fat_sorter).is_fat_root_sorted(...).thenReturn(False)
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        assert fat32_check_output.exit_code == 0
        assert "is not sorted" in fat32_check_output.stdout

    def test_fat_check_returns_true_sorted(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(fat_sorter).is_fat_root_sorted(...).thenReturn(True)
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        assert fat32_check_output.exit_code == 0
        assert "is sorted" in fat32_check_output.stdout

    def test_fat_check_returns_gaps(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(content_checker).get_root_dir_numbering_gaps(...).thenReturn(["01", "03"])
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        assert fat32_check_output.exit_code == 0
        assert "misses some dirs/has gaps" in fat32_check_output.stdout
        assert "01" in fat32_check_output.stdout
        assert "03" in fat32_check_output.stdout
