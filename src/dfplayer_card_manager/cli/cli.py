import os
import traceback

import typer
from typing_extensions import Annotated

from dfplayer_card_manager.cli.printing import (
    print_error,
    print_ok,
    print_warning,
)
from dfplayer_card_manager.config.configuration import (
    Configuration,
    RepositoryConfig,
)
from dfplayer_card_manager.dfplayer.dfplayer_card_content_checker import (
    DfPlayerCardContentChecker,
)
from dfplayer_card_manager.dfplayer.dfplayer_card_manager_error import (
    DfPlayerCardManagerError,
)
from dfplayer_card_manager.fat import fat_checker
from dfplayer_card_manager.fat.fat_error import FatError
from dfplayer_card_manager.fat.fat_sorter import FatSorter
from dfplayer_card_manager.fat.fat_sorter_interface import FatSorterInterface
from dfplayer_card_manager.os import path_sanitizer
from dfplayer_card_manager.repository.detection_source import DetectionSource


# SETUP Functions
def setup_config() -> Configuration:
    tmp_config = Configuration()
    tmp_config.repository_target = RepositoryConfig(
        valid_root_dir_pattern=r"^\d{2}$",
        valid_subdir_files_pattern=r"^(\d{3})\.mp3$",
        track_number_source=DetectionSource.filename,
        track_number_match=1,
    )
    return tmp_config


def setup_fat_sorter() -> FatSorterInterface:
    return FatSorter()


def setup_content_checker() -> DfPlayerCardContentChecker:
    return DfPlayerCardContentChecker(
        valid_root_dir_pattern=r"^\d{2}$",
        valid_subdir_files_pattern=r"^(\d{3})\.mp3$",
        valid_subdir_files_track_number_match=1,
        root_dir_exceptions={"mp3", "advertisment"},
    )


# SETUP

config: Configuration = setup_config()
fat_sorter: FatSorterInterface = setup_fat_sorter()
content_checker: DfPlayerCardContentChecker = setup_content_checker()
app = typer.Typer()


# ToDo: Help text
@app.command()
def check(
    sd_card_path: Annotated[  # noqa: WPS320
        str,
        typer.Argument(help="The path to the SD card. Like /media/SDCARD or D:\\"),
    ],
):
    sd_card_path = _sd_card_path_pre_processing(sd_card_path)

    try:
        _check(sd_card_path)
    except (DfPlayerCardManagerError, FatError) as check_exc:
        print_error(f"Checking failed: {check_exc.message}")
        raise typer.Abort(check_exc)
    except Exception as check_exc:
        print_error(f"An unexpected exception occurred: {check_exc}")
        traceback.print_exc()
        raise typer.Abort(check_exc)


@app.command()
def sort(sd_card_path: str):
    sd_card_path = _sd_card_path_pre_processing(sd_card_path)

    try:
        _sort(sd_card_path)
    except (DfPlayerCardManagerError, FatError) as check_exc:
        print_error(f"Sorting failed: {check_exc.message}")
        raise typer.Abort(check_exc)
    except Exception as check_exc:
        print_error(f"An unexpected exception occurred: {check_exc}")
        traceback.print_exc()
        raise typer.Abort(check_exc)


@app.command()
def clean(sd_card_path: str, dry_run: bool = False):
    sd_card_path = _sd_card_path_pre_processing(sd_card_path)
    if dry_run:
        _print_unwanted_entries_dry_run(sd_card_path)
    else:
        _remove_unwanted_entries(sd_card_path)


def _print_unwanted_entries_dry_run(sd_card_path: str):
    unwanted_entries: list[str] = []
    unwanted_entries.extend(
        os.path.join(sd_card_path, unwanted_root_entry)
        for unwanted_root_entry in content_checker.get_unwanted_root_dir_entries(
            sd_card_path,
        )
    )
    unwanted_entries.extend(
        os.path.join(sd_card_path, unwanted_subdir, unwanted_file)
        for unwanted_subdir, unwanted_file in content_checker.get_unwanted_subdir_entries(
            sd_card_path,
        )
    )
    if unwanted_entries:
        print_warning("Would remove:")
    else:
        print_ok("Nothing to remove.")
    for unwanted_entry_dry in unwanted_entries:
        print_warning(unwanted_entry_dry, is_bullet=True)


def _remove_unwanted_entries(sd_card_path: str):
    unwanted_entries = content_checker.delete_unwanted_root_dir_entries(sd_card_path)
    unwanted_entries.extend(
        content_checker.delete_unwanted_subdir_entries(sd_card_path),
    )
    if unwanted_entries:
        print_warning("Removed:")
    else:
        print_ok("Nothing to remove.")
    for unwanted_entry in unwanted_entries:
        print_warning(unwanted_entry, is_bullet=True)


def _sd_card_path_pre_processing(sd_card_path: str) -> str:
    if os.name == "nt":
        sd_card_path = path_sanitizer.sanitize_windows_volume_path(sd_card_path)

    if not os.path.exists(sd_card_path):
        print_error(f"{sd_card_path} does not exist (yet?).")
        raise typer.Abort()
    return sd_card_path


def _sort(sd_card_path: str):
    if fat_sorter.is_fat_volume_sorted(sd_card_path):
        print_ok(f"{sd_card_path} is sorted, nothing to do.")
        exit(0)
    fat_sorter.sort_fat_volume(sd_card_path)
    print_ok(f"{sd_card_path} has been sorted.")


def _check(sd_card_path: str):  # noqa: C901, WPS213, WPS231
    # CHeck if the SD card path exists and is fat32
    if fat_checker.check_is_fat32(sd_card_path):
        print_ok(f"{sd_card_path} is a path within a FAT32 filesystem.")
    else:
        raise DfPlayerCardManagerError(
            f"{sd_card_path} is not a path within a FAT32 filesystem.",
        )
    if fat_checker.check_has_correct_allocation_unit_size(sd_card_path):
        print_ok(
            f"{sd_card_path} has the correct allocation unit size of 32 kilobytes.",
        )
    else:
        print_warning(
            f"{sd_card_path} does not have the correct allocation unit size of 32 kilobytes.",
        )

    if fat_sorter.is_fat_volume_sorted(sd_card_path):
        print_ok(f"{sd_card_path} is sorted.")
    else:
        print_warning(f"{sd_card_path} is not sorted.")

    unwanted_root_dir_entries = content_checker.get_unwanted_root_dir_entries(
        sd_card_path,
    )
    if unwanted_root_dir_entries:
        print_warning(
            f"{sd_card_path} has unwanted entries in the root dir:",
        )
        for unwanted_root_dir_entry in unwanted_root_dir_entries:
            print_warning(
                f"{unwanted_root_dir_entry}",
                is_bullet=True,
            )
    else:
        print_ok(f"{sd_card_path} has no unwanted entries in the root dir.")

    unwanted_subdir_entries = content_checker.get_unwanted_subdir_entries(sd_card_path)
    if unwanted_subdir_entries:
        print_warning(
            f"{sd_card_path} has unwanted entries in its subdirs:",
        )
        for unwanted_subdir_entry in unwanted_subdir_entries:
            print_warning(
                f"{unwanted_subdir_entry[0]}{os.sep}{unwanted_subdir_entry[1]}",
                is_bullet=True,
            )
    else:
        print_ok(f"{sd_card_path} has no unwanted entries in the subdirs.")

    root_gaps = content_checker.get_root_dir_numbering_gaps(sd_card_path)
    if root_gaps:
        print_warning(
            f"{sd_card_path} misses some root level dirs/has gaps. Missing dirs:",
        )
        for root_gap in root_gaps:
            print_warning(
                f"{str(root_gap).zfill(2)}",
                is_bullet=True,
            )
    else:
        print_ok(f"{sd_card_path} has no missing dirs/gaps in the root dir.")

    subdir_gaps = content_checker.get_subdir_numbering_gaps(sd_card_path)
    if subdir_gaps:
        print_warning(
            f"{sd_card_path} misses some files/has gaps in the subdirs. Missing files:",
        )
        for subdir_gap in subdir_gaps:

            print_warning(
                f"{str(subdir_gap[0]).zfill(2)}{os.sep}{str(subdir_gap[1]).zfill(3)}",  # noqa: WPS221
                is_bullet=True,
            )
    else:
        print_ok(f"{sd_card_path} has no missing files/gaps in the subdirs.")


if __name__ == "__main__":
    app()
