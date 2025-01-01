# - Create Delta List
# What would be done?
# also identify gaps, unwanted files and foldersks

# - Write to SD Card
# Check if unwanted files exist on the SD card and warn the user
# Check if Gaps exist in the root directory and subdirs and warn the user
# Check if file needs to be written to SD card
# Check if file exists on SD card (function needs foldernumber / file number)
# Check if file is the same (hash of content) on the SD card
# check tags (function needs tags, foldernumber / file number)
# 1. Write a file to the SD card with
# if anything was written, call sort_fat_root


# - check root for unwanted files
# check if file is in the root
# check if file is in a subdirectory

# create a cli interface that first reads command line arguments handles defaults and mandatory arguments.
# It also prints a help text explaining the cli parameters. Two arguments are: source-folder (default = .)
# and target-folder (mandatory).

import typer
from rich import print
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
    try:
        _check(sd_card_path)
    except (DfPlayerCardManagerError, FatError) as check_exc:
        print_error(f"Checking failed: {check_exc.message}")
        raise typer.Abort(check_exc)
    except Exception as check_exc:
        print_error(f"An unexpected exception occurred: {check_exc}")
        raise typer.Abort(check_exc)


@app.command()
def clean(sd_card_path: str, dry_run: bool = False):
    # Check if the SD card path exists and is fat32
    check(sd_card_path)

    if dry_run:
        typer.echo("Dry run")
    else:
        typer.echo("Clean")


def _check(sd_card_path: str):
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
    if fat_sorter.is_fat_root_sorted(sd_card_path):
        print_ok(f"{sd_card_path} is sorted.")
    else:
        print_warning(f"{sd_card_path} is not sorted.")

    root_gaps = content_checker.get_root_dir_numbering_gaps(sd_card_path)
    if root_gaps:
        print_warning(f"{sd_card_path} misses some dirs/has gaps:")
        for gap in root_gaps:
            print(f"[yellow]-> {str(gap).zfill(2)}[/yellow]")
    else:
        print(
            f"[green]{sd_card_path} has no missing dirs/gaps in the root dir.[/green]",
        )


if __name__ == "__main__":
    app()
