import os

from dfplayer_card_manager.cli.cli_context import CliContext
from dfplayer_card_manager.cli.printing import (
    print_neutral,
    print_ok,
    print_warning,
)


def clean(cli_context: CliContext, sd_card_path: str, dry_run: bool) -> None:
    if dry_run:
        _print_unwanted_entries_dry_run(cli_context, sd_card_path)
    else:
        _remove_unwanted_entries(cli_context, sd_card_path)


def _print_unwanted_entries_dry_run(cli_context: CliContext, sd_card_path: str):
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


def _remove_unwanted_entries(cli_context: CliContext, sd_card_path: str):
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
