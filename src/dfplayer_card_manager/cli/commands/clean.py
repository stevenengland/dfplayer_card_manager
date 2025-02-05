import os

from dfplayer_card_manager.cli.cli_context import CliContext
from dfplayer_card_manager.cli.printing import (
    print_error,
    print_neutral,
    print_ok,
    print_warning,
)
from dfplayer_card_manager.fat import fat_device_mount


def clean(cli_context: CliContext, sd_card_path: str, dry_run: bool) -> None:
    _device_path, mount_point_path = fat_device_mount.detect_device_path_and_mount_path(
        sd_card_path=sd_card_path,
    )

    if not mount_point_path or not os.path.isdir(mount_point_path):
        print_error(
            "You provided a device path that has no corresponding mount point. Aborting.",
        )
        exit(1)

    if not os.access(mount_point_path, os.W_OK):
        print_error(
            f"You don't have write permissions to {mount_point_path}. Aborting.",
        )
        exit(1)

    if dry_run:
        _print_unwanted_entries_dry_run(cli_context, mount_point_path)
    else:
        _remove_unwanted_entries(cli_context, mount_point_path)


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
