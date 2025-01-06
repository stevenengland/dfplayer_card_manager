import os
import traceback
from typing import Callable

import typer
from typing_extensions import Annotated

from dfplayer_card_manager.cli import cli_setup
from dfplayer_card_manager.cli.printing import (
    print_action,
    print_error,
    print_neutral,
    print_ok,
    print_task,
    print_warning,
)
from dfplayer_card_manager.dfplayer.dfplayer_card_manager_error import (
    DfPlayerCardManagerError,
)
from dfplayer_card_manager.fat import fat_checker
from dfplayer_card_manager.fat.fat_error import FatError
from dfplayer_card_manager.os import path_sanitizer

# SETUP

# ToDo: Switch to ctx: Context .obj = CliContextObj for more flexibility
cli_context = cli_setup.setup_cli_context()
app = typer.Typer()


# ToDo: Help text
@app.command()
def check(
    sd_card_path: Annotated[  # noqa: WPS320
        str,
        typer.Argument(help="The path to the SD card. Like /media/SDCARD or D:\\"),
    ],
):
    # ToDo: switch to callback for parameter evaluation
    sd_card_path = _sd_card_path_pre_processing(sd_card_path)
    print_task(f"Checking {sd_card_path}")
    _try(_check, sd_card_path, error_prepend="Checking failed.")


@app.command()
def sort(
    sd_card_path: Annotated[  # noqa: WPS320
        str,
        typer.Argument(help="The path to the SD card. Like /media/SDCARD or D:\\"),
    ],
):
    sd_card_path = _sd_card_path_pre_processing(sd_card_path)

    print_task(f"Sorting {sd_card_path}")
    _try(_sort, sd_card_path, error_prepend="Sorting failed.")


@app.command()
def clean(
    sd_card_path: Annotated[  # noqa: WPS320
        str,
        typer.Argument(help="The path to the SD card. Like /media/SDCARD or D:\\"),
    ],
    dry_run: bool = False,
):
    sd_card_path = _sd_card_path_pre_processing(sd_card_path)
    print_task(f"Cleaning {sd_card_path}")
    if dry_run:
        _print_unwanted_entries_dry_run(sd_card_path)
    else:
        _try(_remove_unwanted_entries, sd_card_path, error_prepend="Cleaning failed.")


@app.command()
def sync(
    sd_card_path: Annotated[  # noqa: WPS320
        str,
        typer.Argument(help="The path to the SD card. Like /media/SDCARD or D:\\"),
    ],
    repository_path: Annotated[  # noqa: WPS320
        str,
        typer.Argument(
            help=r"The path to the repository. Like /home/user/music or C:\\Users\\me\\Music",
        ),
    ],
    dry_run: bool = False,
):
    sd_card_path = _sd_card_path_pre_processing(sd_card_path)
    repository_path = _sd_card_path_pre_processing(repository_path)

    cli_context.card_manager.target_repo_root_dir = sd_card_path
    cli_context.card_manager.source_repo_root_dir = repository_path

    print_task("Creating repositories")
    _try(
        cli_context.card_manager.create_repositories,
        None,
        error_prepend="Creating repositories failed.",
    )

    repo_comparison_result = cli_context.card_manager.get_repositories_comparison()
    if not repo_comparison_result:
        print_ok("Nothing to do.")
        exit(0)
    for compared_item in repo_comparison_result:
        print_action(compared_item)
        if not dry_run:
            pass


def _print_unwanted_entries_dry_run(sd_card_path: str):
    unwanted_entries: list[str] = []
    unwanted_entries.extend(
        os.path.join(sd_card_path, unwanted_root_entry)
        for unwanted_root_entry in cli_context.content_checker.get_unwanted_root_dir_entries(
            sd_card_path,
        )
    )
    unwanted_entries.extend(
        os.path.join(sd_card_path, unwanted_subdir, unwanted_file)
        for unwanted_subdir, unwanted_file in cli_context.content_checker.get_unwanted_subdir_entries(
            sd_card_path,
        )
    )
    if unwanted_entries:
        print_neutral("Would remove:")
    else:
        print_ok("Nothing to remove.")
    for unwanted_entry_dry in unwanted_entries:
        print_warning(unwanted_entry_dry, is_bullet=True)


def _remove_unwanted_entries(sd_card_path: str):
    unwanted_entries = cli_context.content_checker.delete_unwanted_root_dir_entries(
        sd_card_path,
    )
    unwanted_entries.extend(
        cli_context.content_checker.delete_unwanted_subdir_entries(sd_card_path),
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
    if cli_context.fat_sorter.is_fat_volume_sorted(sd_card_path):
        print_ok(f"{sd_card_path} is sorted, nothing to do.")
        exit(0)
    cli_context.fat_sorter.sort_fat_volume(sd_card_path)
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

    if cli_context.fat_sorter.is_fat_volume_sorted(sd_card_path):
        print_ok(f"{sd_card_path} is sorted.")
    else:
        print_warning(f"{sd_card_path} is not sorted.")

    unwanted_root_dir_entries = (
        cli_context.content_checker.get_unwanted_root_dir_entries(
            sd_card_path,
        )
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

    unwanted_subdir_entries = cli_context.content_checker.get_unwanted_subdir_entries(
        sd_card_path,
    )
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

    root_gaps = cli_context.content_checker.get_root_dir_numbering_gaps(sd_card_path)
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

    subdir_gaps = cli_context.content_checker.get_subdir_numbering_gaps(sd_card_path)
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


def _try(func: Callable[..., None], *args: object, error_prepend: str = "") -> None:  # type: ignore[misc]
    try:
        if args[0] is not None:
            func(*args)
        else:
            func()
    except (DfPlayerCardManagerError, FatError) as check_exc:
        if error_prepend:
            print_error(f"{error_prepend}")
        print_error(f"Error: {check_exc.message}")
        _abort(check_exc)
    except Exception as exc:
        print_error(f"An unexpected exception occurred: {exc}")
        traceback.print_exc()
        _abort(exc)


def _abort(*args: object) -> None:
    raise typer.Abort(*args)


if __name__ == "__main__":
    app()
