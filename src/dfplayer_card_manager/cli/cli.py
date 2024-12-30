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

from dfplayer_card_manager.dfplayer.dfplayer_card_manager_error import (
    DfPlayerCardManagerError,
)
from dfplayer_card_manager.fat import fat_checker

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
    except DfPlayerCardManagerError as check_exc:
        print(f"[red]Checking failed: {check_exc.message}[/red]")
        raise typer.Abort(check_exc)
    except Exception as check_exc:
        print(f"[red]An unexpected exception occurred: {check_exc}[/red]")
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
        print(f"[green]{sd_card_path} is a path within a FAT32 filesystem[/green]")
    else:
        raise DfPlayerCardManagerError(
            f"{sd_card_path} is not a path within a FAT32 filesystem.",
        )
    if fat_checker.check_has_correct_allocation_unit_size(sd_card_path):
        print(
            f"[green]{sd_card_path} has the correct allocation unit size of 32 kilobytes[/green]",
        )
    else:
        print(
            f"[yellow]{sd_card_path} does not have the correct allocation unit size of 32 kilobytes.[/yellow]",
        )


if __name__ == "__main__":
    app()
