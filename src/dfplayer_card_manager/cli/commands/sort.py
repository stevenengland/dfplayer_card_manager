import os

from dfplayer_card_manager.cli.cli_context import CliContext
from dfplayer_card_manager.cli.printing import print_error, print_ok
from dfplayer_card_manager.fat import fat_device_mount


def sort(cli_context: CliContext, sd_card_path: str) -> None:
    # Needs the device path
    device_path, _ = fat_device_mount.detect_device_path_and_mount_path(
        sd_card_path=sd_card_path,
    )

    if not device_path or not os.path.exists(device_path):
        print_error(
            "You provided a (mount) path that has no corresponding device path. Aborting.",
        )
        exit(1)

    if not os.access(device_path, os.W_OK):
        print_error(
            "You don't have write permissions to the device path. Aborting.",
        )
        exit(1)

    if cli_context.fat_sorter.is_fat_volume_sorted(device_path):
        print_ok(f"{device_path} is sorted, nothing to do.")
        exit(0)
    cli_context.fat_sorter.sort_fat_volume(device_path)
    print_ok(f"{device_path} has been sorted.")
