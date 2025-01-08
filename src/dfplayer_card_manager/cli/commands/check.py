import os

from dfplayer_card_manager.cli.cli_context import CliContext
from dfplayer_card_manager.cli.printing import print_ok, print_warning
from dfplayer_card_manager.dfplayer.dfplayer_card_manager_error import (
    DfPlayerCardManagerError,
)
from dfplayer_card_manager.fat import fat_checker


def check(cli_context: CliContext, sd_card_path: str):  # noqa: C901, WPS213, WPS231
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
