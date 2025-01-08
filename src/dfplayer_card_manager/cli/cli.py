import os
import traceback
from typing import Callable

import typer
from typing_extensions import Annotated

from dfplayer_card_manager.cli import cli_setup, commands
from dfplayer_card_manager.cli.printing import print_error, print_task
from dfplayer_card_manager.dfplayer.dfplayer_card_manager_error import (
    DfPlayerCardManagerError,
)
from dfplayer_card_manager.fat.fat_error import FatError
from dfplayer_card_manager.mp3.tag_error import TagError
from dfplayer_card_manager.os import path_sanitizer

# SETUP

# ToDo: Switch to ctx: Context .obj = CliContextObj for more flexibility
cli_context = cli_setup.setup_cli_context()
app = typer.Typer()


@app.callback()
def main(verbose: Annotated[int, typer.Option("--verbose", "-v", count=True)] = 0):
    cli_context.logger.verbosity = verbose


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
    try_safe(
        commands.check,
        cli_context,
        sd_card_path,
        error_prepend="Checking failed.",
    )


@app.command()
def sort(
    sd_card_path: Annotated[  # noqa: WPS320
        str,
        typer.Argument(help="The path to the SD card. Like /media/SDCARD or D:\\"),
    ],
):
    sd_card_path = _sd_card_path_pre_processing(sd_card_path)

    print_task(f"Sorting {sd_card_path}")
    try_safe(commands.sort, cli_context, sd_card_path, error_prepend="Sorting failed.")


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
    try_safe(
        commands.clean,
        cli_context,
        sd_card_path,
        dry_run,
        error_prepend="Cleaning failed.",
    )


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

    print_task("Sync repositories")
    try_safe(
        commands.sync,
        cli_context,
        sd_card_path,
        repository_path,
        dry_run,
        error_prepend="Sync failed.",
    )


def _sd_card_path_pre_processing(sd_card_path: str) -> str:
    if os.name == "nt":
        sd_card_path = path_sanitizer.sanitize_windows_volume_path(sd_card_path)

    if not os.path.exists(sd_card_path):
        print_error(f"{sd_card_path} does not exist (yet?).")
        raise typer.Abort()
    return sd_card_path


def try_safe(func: Callable[..., None], *args: object, error_prepend: str = "") -> None:  # type: ignore[misc]
    try:
        if args[0] is not None:
            func(*args)
        else:
            func()
    except (DfPlayerCardManagerError, FatError, TagError) as check_exc:
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
