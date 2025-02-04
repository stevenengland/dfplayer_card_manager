import os

from dfplayer_card_manager.cli.cli_context import CliContext
from dfplayer_card_manager.cli.printing import (
    print_neutral,
    print_ok,
    print_warning,
)
from dfplayer_card_manager.dfplayer.dfplayer_card_manager_error import (
    DfPlayerCardManagerError,
)
from dfplayer_card_manager.fat import fat_checker, fat_device_mount
from dfplayer_card_manager.os import file_access


def check(cli_context: CliContext, sd_card_path: str):  # noqa: C901, WPS213, WPS231

    # check the capabilities
    device_path, mountpoint_path = fat_device_mount.detect_device_path_and_mount_path(
        sd_card_path,
    )

    # Device path is always available
    device_path_readable = os.access(device_path, os.R_OK)
    device_path_writable = os.access(device_path, os.W_OK)
    device_path_busy = file_access.probe_is_busy(device_path)

    print_neutral(f"Device path: {device_path}")
    print_neutral(f"Mountpoint path: {mountpoint_path}")
    cli_context.logger.trace(f"Device path readable: {device_path_readable}")
    cli_context.logger.trace(f"Device path writable: {device_path_writable}")
    cli_context.logger.trace(f"Device path busy: {device_path_busy}")

    # Check if the SD card path exists and is FAT32
    _check_is_fat32(sd_card_path)

    # Check if the SD card path has the correct allocation unit size
    if mountpoint_path:
        _check_allocation_unit_size(mountpoint_path)
    elif device_path and device_path_readable:
        _check_allocation_unit_size(device_path)
    else:
        print_warning(
            f"{sd_card_path} has no corresponding device path or is not readable (maybe you need elevated priviliges). "
            + "Cannot check allocation unit size.",
        )

    # Check if the SD card path is sorted
    if device_path and device_path_readable and not device_path_busy:
        _check_fat_volume_is_sorted(device_path, cli_context)
    else:
        print_warning(
            f"{device_path} has no corresponding device path or is not readable. "
            + "Maybe you need elevated priviliges or you need to unmount the device first. "
            + "Cannot check if FAT is sorted.",
        )

    # Check the file system
    if mountpoint_path:
        _check_unwanted_root_dir_entries(mountpoint_path, cli_context)
        _check_unwanted_subdir_entries(mountpoint_path, cli_context)
        _check_root_dir_gaps(mountpoint_path, cli_context)
        _check_subdir_gaps(mountpoint_path, cli_context)
    else:
        print_warning(
            f"{mountpoint_path} has no corresponding mountpoint. Cannot check for unwanted entries and gaps.",
        )


def _check_is_fat32(sd_card_path: str) -> None:
    if fat_checker.check_is_fat32(sd_card_path):
        print_ok(f"{sd_card_path} is a path within a FAT32 filesystem.")
    else:
        raise DfPlayerCardManagerError(
            f"{sd_card_path} is not a path within a FAT32 filesystem.",
        )


def _check_allocation_unit_size(sd_card_path: str) -> None:
    if fat_checker.check_has_correct_allocation_unit_size(sd_card_path):
        print_ok(
            f"{sd_card_path} has the correct allocation unit size of 32 kilobytes.",
        )
    else:
        print_warning(
            f"{sd_card_path} does not have the correct allocation unit size of 32 kilobytes.",
        )


def _check_fat_volume_is_sorted(sd_card_path: str, cli_context: CliContext) -> None:
    if cli_context.fat_sorter.is_fat_volume_sorted(sd_card_path):
        print_ok(f"{sd_card_path} is sorted.")
    else:
        print_warning(f"{sd_card_path} is not sorted.")


def _check_unwanted_root_dir_entries(
    sd_card_path: str,
    cli_context: CliContext,
) -> None:
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


def _check_unwanted_subdir_entries(sd_card_path: str, cli_context: CliContext) -> None:
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


def _check_root_dir_gaps(sd_card_path: str, cli_context: CliContext) -> None:
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


def _check_subdir_gaps(sd_card_path: str, cli_context: CliContext) -> None:
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
