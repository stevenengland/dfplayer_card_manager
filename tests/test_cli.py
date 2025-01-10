import os

import pytest
from factories.repository_element_factory import create_repository_element
from file_system_helper import FakeFileSystemHelper
from typer.testing import CliRunner

from dfplayer_card_manager.cli.cli import app, cli_context
from dfplayer_card_manager.fat import fat_checker
from dfplayer_card_manager.repository.compare_result import CompareResult
from dfplayer_card_manager.repository.compare_result_actions import (
    CompareResultAction,
)

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
    monkeypatch.setattr(
        cli_context.fat_sorter,
        "is_fat_volume_sorted",
        lambda _filesystem_path: True,
    )
    monkeypatch.setattr(
        cli_context.content_checker,
        "get_root_dir_numbering_gaps",
        lambda _dirs: [],
    )
    monkeypatch.setattr(
        cli_context.content_checker,
        "get_subdir_numbering_gaps",
        lambda _dirs: [],
    )
    monkeypatch.setattr(
        cli_context.content_checker,
        "get_unwanted_root_dir_entries",
        lambda _entries: [],
    )
    monkeypatch.setattr(
        cli_context.content_checker,
        "get_unwanted_subdir_entries",
        lambda _entries: [],
    )
    return CliRunner()


@pytest.fixture(scope="function", name="cli_runner_e2e")
def get_cli_runner_e2e() -> CliRunner:
    return CliRunner()


class TestChecks:  # noqa: WPS214
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
        if fat32_check_output.exit_code != 0:
            print(fat32_check_output.stdout)
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
        if fat32_check_output.exit_code != 0:
            print(fat32_check_output.stdout)
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
        if fat32_check_output.exit_code != 0:
            print(fat32_check_output.stdout)
        assert fat32_check_output.exit_code == 0
        assert "has the correct allocation unit size" in fat32_check_output.stdout

    def test_fat_check_returns_false_sorted(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(cli_context.fat_sorter).is_fat_volume_sorted(...).thenReturn(False)
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        if fat32_check_output.exit_code != 0:
            print(fat32_check_output.stdout)
        assert fat32_check_output.exit_code == 0
        assert "is not sorted" in fat32_check_output.stdout

    def test_fat_check_returns_true_sorted(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(cli_context.fat_sorter).is_fat_volume_sorted(...).thenReturn(True)
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        if fat32_check_output.exit_code != 0:
            print(fat32_check_output.stdout)
        assert fat32_check_output.exit_code == 0
        assert "is sorted" in fat32_check_output.stdout

    def test_sd_root_dir_numbering_returns_gaps(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(cli_context.content_checker).get_root_dir_numbering_gaps(...).thenReturn(
            ["01", "03"],
        )
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        if fat32_check_output.exit_code != 0:
            print(fat32_check_output.stdout)
        assert fat32_check_output.exit_code == 0
        assert "Missing dirs:" in fat32_check_output.stdout
        assert "01" in fat32_check_output.stdout
        assert "03" in fat32_check_output.stdout

    def test_sd_root_dir_numbering_returns_no_gaps(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(cli_context.content_checker).get_root_dir_numbering_gaps(...).thenReturn(
            [],
        )
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        if fat32_check_output.exit_code != 0:
            print(fat32_check_output.stdout)
        assert fat32_check_output.exit_code == 0
        assert "has no missing dirs/gaps" in fat32_check_output.stdout

    def test_sd_subdir_numbering_returns_gaps(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(cli_context.content_checker).get_subdir_numbering_gaps(...).thenReturn(
            [("01", "001")],
        )
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        if fat32_check_output.exit_code != 0:
            print(fat32_check_output.stdout)
        assert fat32_check_output.exit_code == 0
        assert "Missing files:" in fat32_check_output.stdout
        assert f"01{os.sep}001" in fat32_check_output.stdout

    def test_sd_subdir_numbering_returns_no_gaps(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(cli_context.content_checker).get_subdir_numbering_gaps(...).thenReturn([])
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        if fat32_check_output.exit_code != 0:
            print(fat32_check_output.stdout)
        assert fat32_check_output.exit_code == 0
        assert "has no missing files/gaps" in fat32_check_output.stdout

    def test_unwanted_root_dir_entries(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(cli_context.content_checker).get_unwanted_root_dir_entries(...).thenReturn(
            ["01", "03"],
        )
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        if fat32_check_output.exit_code != 0:
            print(fat32_check_output.stdout)
        assert fat32_check_output.exit_code == 0
        assert "has unwanted entries in the root dir" in fat32_check_output.stdout
        assert "01" in fat32_check_output.stdout
        assert "03" in fat32_check_output.stdout

    def test_no_unwanted_root_dir_entries(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(cli_context.content_checker).get_unwanted_root_dir_entries(...).thenReturn(
            [],
        )
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        if fat32_check_output.exit_code != 0:
            print(fat32_check_output.stdout)
        assert fat32_check_output.exit_code == 0
        assert "has no unwanted entries in the root dir" in fat32_check_output.stdout

    def test_unwanted_subdir_entries(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(cli_context.content_checker).get_unwanted_subdir_entries(...).thenReturn(
            [("01", "001"), ("03", "003")],
        )
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["check", "tests/test_assets"])
        # THEN
        if fat32_check_output.exit_code != 0:
            print(fat32_check_output.stdout)
        assert fat32_check_output.exit_code == 0
        assert "has unwanted entries in its subdirs" in fat32_check_output.stdout
        assert f"01{os.sep}001" in fat32_check_output.stdout
        assert f"03{os.sep}003" in fat32_check_output.stdout


class TestSort:
    def test_sort_returns_if_is_already_sorted(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(cli_context.fat_sorter).is_fat_volume_sorted(...).thenReturn(True)
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["sort", "tests/test_assets"])
        # THEN
        assert fat32_check_output.exit_code == 0
        assert "is sorted" in fat32_check_output.stdout

    def test_sort_is_applied_if_is_not_sorted_yet(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(cli_context.fat_sorter).is_fat_volume_sorted(...).thenReturn(False)
        when(cli_context.fat_sorter).sort_fat_volume(...).thenReturn(None)
        # WHEN
        fat32_check_output = cli_runner.invoke(app, ["sort", "tests/test_assets"])
        # THEN
        if fat32_check_output.exit_code != 0:
            print(fat32_check_output.stdout)
        assert fat32_check_output.exit_code == 0
        assert "has been sorted" in fat32_check_output.stdout


class TestCleanDryRun:
    def test_clean_dry_run(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(cli_context.content_checker).get_unwanted_root_dir_entries(...).thenReturn(
            ["01", "03"],
        )
        when(cli_context.content_checker).get_unwanted_subdir_entries(...).thenReturn(
            [("01", "001"), ("03", "003")],
        )
        # WHEN
        fat32_check_output = cli_runner.invoke(
            app,
            ["clean", "tests/test_assets", "--dry-run"],
        )
        # THEN
        if fat32_check_output.exit_code != 0:
            print(fat32_check_output.stdout)
        assert fat32_check_output.exit_code == 0
        assert "Would remove" in fat32_check_output.stdout
        assert "01" in fat32_check_output.stdout
        assert "03" in fat32_check_output.stdout
        assert f"01{os.sep}001" in fat32_check_output.stdout
        assert f"03{os.sep}003" in fat32_check_output.stdout


class TestSyncing:
    def test_syncing_dry_run(
        self,
        cli_runner,
        when,
    ):
        # GIVEN
        when(cli_context.card_manager).create_repositories().thenReturn(None)
        when(cli_context.card_manager).get_repositories_comparison(...).thenReturn(
            [
                CompareResult(
                    dir_num=1,
                    track_num=1,
                    action=CompareResultAction.copy_to_target,
                    source_element=create_repository_element(),
                ),
                CompareResult(
                    dir_num=2,
                    track_num=2,
                    action=CompareResultAction.delete_from_target,
                    target_element=create_repository_element(),
                ),
            ],
        )

        # WHEN
        sync_output = cli_runner.invoke(
            app,
            [
                "sync",
                "tests/test_assets/repositories/target",
                "tests/test_assets/repositories/source",
                "--dry-run",
            ],
        )

        # THEN
        if sync_output.exit_code != 0:
            print(sync_output.stdout)
        assert sync_output.exit_code == 0
        assert f"+++ |01{os.sep}001| <--" in sync_output.stdout
        assert f"--- |02{os.sep}002| <-- X" in sync_output.stdout

    @e2e
    def test_syncing_dry_run_e2e(
        self,
        cli_runner,
        test_assets_fs: FakeFileSystemHelper,
    ):
        # GIVEN
        expected_results = [
            CompareResult(
                dir_num=1,
                track_num=1,
                action=CompareResultAction.copy_to_target,
            ),
            CompareResult(
                dir_num=1,
                track_num=2,
                action=CompareResultAction.copy_to_target,
            ),
            CompareResult(
                dir_num=2,
                track_num=1,
                action=CompareResultAction.copy_to_target,
            ),
            CompareResult(
                dir_num=2,
                track_num=2,
                action=CompareResultAction.no_change,
            ),
            CompareResult(
                dir_num=2,
                track_num=3,
                action=CompareResultAction.no_change,
            ),
            CompareResult(
                dir_num=2,
                track_num=4,
                action=CompareResultAction.copy_to_target,
            ),
            CompareResult(
                dir_num=2,
                track_num=5,
                action=CompareResultAction.copy_to_target,
            ),
            CompareResult(
                dir_num=2,
                track_num=6,
                action=CompareResultAction.copy_to_target,
            ),
            CompareResult(
                dir_num=2,
                track_num=7,
                action=CompareResultAction.unstuff,
            ),
            CompareResult(
                dir_num=2,
                track_num=8,
                action=CompareResultAction.delete_from_target,
            ),
        ]

        # WHEN
        sync_output = cli_runner.invoke(
            app,
            [
                "-vvv",
                "sync",
                os.path.join(test_assets_fs.test_assets_path, "repositories", "target"),
                os.path.join(test_assets_fs.test_assets_path, "repositories", "source"),
                "--dry-run",
            ],
        )

        # THEN
        if sync_output.exit_code != 0:
            print(sync_output.stdout)
        assert sync_output.exit_code == 0
        for comparison_result in expected_results:
            assert (
                f"{comparison_result.dir_num}/{comparison_result.track_num}/{comparison_result.action}"
                in sync_output.stdout
            )

    @e2e
    def test_syncing_e2e(
        self,
        cli_runner_e2e,
        test_assets_fs_w: FakeFileSystemHelper,
    ):
        # GIVEN
        source_dir = os.path.join(
            test_assets_fs_w.test_assets_path,
            "repositories",
            "source",
        )
        target_dir = os.path.join(
            test_assets_fs_w.test_assets_path,
            "repositories",
            "target",
        )

        mtime_before_02_002 = os.path.getmtime(
            os.path.join(target_dir, "02", "002.mp3"),
        )
        mtime_before_02_003 = os.path.getmtime(
            os.path.join(target_dir, "02", "003.mp3"),
        )
        mtime_before_02_004 = os.path.getmtime(
            os.path.join(target_dir, "02", "004.mp3"),
        )
        mtime_before_02_005 = os.path.getmtime(
            os.path.join(target_dir, "02", "005.mp3"),
        )
        mtime_before_02_006 = os.path.getmtime(
            os.path.join(target_dir, "02", "006.mp3"),
        )

        # WHEN
        sync_output = cli_runner_e2e.invoke(
            app,
            [
                "-vvv",
                "sync",
                target_dir,
                source_dir,
            ],
        )

        # THEN
        if sync_output.exit_code != 0:
            print(sync_output.stdout)
        assert sync_output.exit_code == 0
        files01 = os.listdir(os.path.join(target_dir, "01"))
        files02 = os.listdir(os.path.join(target_dir, "02"))
        assert len(files01) == 3
        assert len(files02) == 6
        assert "001.mp3" in files01
        assert "002.mp3" in files01
        assert "001.mp3" in files02
        assert "002.mp3" in files02
        assert mtime_before_02_002 == os.path.getmtime(
            os.path.join(target_dir, "02", "002.mp3"),
        )
        assert "003.mp3" in files02
        assert mtime_before_02_003 == os.path.getmtime(
            os.path.join(target_dir, "02", "003.mp3"),
        )
        assert "004.mp3" in files02
        assert mtime_before_02_004 != os.path.getmtime(
            os.path.join(target_dir, "02", "004.mp3"),
        )
        assert "005.mp3" in files02
        assert mtime_before_02_005 != os.path.getmtime(
            os.path.join(target_dir, "02", "005.mp3"),
        )
        assert "006.mp3" in files02
        assert mtime_before_02_006 != os.path.getmtime(
            os.path.join(target_dir, "02", "006.mp3"),
        )
        assert "007.mp3" not in files02
        assert "008.mp3" not in files02

    @e2e
    def test_syncing_idempotency_e2e(
        self,
        cli_runner_e2e,
        test_assets_fs_w: FakeFileSystemHelper,
    ):
        # GIVEN
        source_dir = os.path.join(
            test_assets_fs_w.test_assets_path,
            "repositories",
            "source",
        )
        target_dir = os.path.join(
            test_assets_fs_w.test_assets_path,
            "repositories",
            "target",
        )

        # WHEN
        cli_runner_e2e.invoke(
            app,
            [
                "-vvv",
                "sync",
                target_dir,
                source_dir,
            ],
        )

        sync_output = cli_runner_e2e.invoke(
            app,
            [
                "-vvv",
                "sync",
                target_dir,
                source_dir,
            ],
        )
        # THEN
        if sync_output.exit_code != 0:
            print(sync_output.stdout)
        assert sync_output.exit_code == 0
        assert str(CompareResultAction.copy_to_target) not in sync_output.stdout
        assert str(CompareResultAction.delete_from_target) not in sync_output.stdout
