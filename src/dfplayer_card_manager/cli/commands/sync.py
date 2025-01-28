import os

from dfplayer_card_manager.cli.cli_context import CliContext
from dfplayer_card_manager.cli.printing import (
    print_action,
    print_error,
    print_ok,
)
from dfplayer_card_manager.config import config_merger, config_reader
from dfplayer_card_manager.dfplayer.dfplayer_card_manager_error import (
    DfPlayerCardManagerError,
)
from dfplayer_card_manager.fat import fat_device_mount


def sync(  # noqa: WPS213
    cli_context: CliContext,
    sd_card_path: str,
    repository_path: str,
    dry_run: bool,
) -> None:

    _device_path, mount_point_path = fat_device_mount.detect_device_path_and_mount_path(
        sd_card_path=sd_card_path,
    )

    _check_permissions_and_paths(mount_point_path, repository_path)

    cli_context.card_manager.target_repo_root_dir = mount_point_path
    cli_context.card_manager.source_repo_root_dir = repository_path

    _set_config_override(cli_context, repository_path)

    cli_context.logger.debug("Creating repositories ...")
    cli_context.card_manager.create_repositories()

    cli_context.logger.debug("Comparing repositories ...")
    repo_comparison_result = cli_context.card_manager.get_repositories_comparison(True)
    if not repo_comparison_result:
        print_ok("Nothing to do.")
        exit(0)
    for compared_item in repo_comparison_result:
        cli_context.logger.debug(
            f"Processing {compared_item.dir_num}/{compared_item.track_num}/{str(compared_item.action)}",  # noqa: WPS221
        )
        print_action(compared_item)
        if not dry_run:
            cli_context.card_manager.write_change_to_target_repository(compared_item)


def _check_permissions_and_paths(mount_point_path: str, repository_path: str) -> None:
    if not os.access(mount_point_path, os.W_OK):
        print_error(
            f"You don't have write permissions to {mount_point_path}. Aborting.",
        )
        exit(1)
    if not os.access(repository_path, os.R_OK):
        print_error(
            f"You don't have read permissions to {repository_path}. Aborting.",
        )
        exit(1)

    if not mount_point_path or not os.path.isdir(mount_point_path):
        print_error(
            "You provided a device path that has no corresponding mount point. Aborting.",
        )
        exit(1)


def _set_config_override(cli_context: CliContext, repository_path: str) -> None:
    config_path = os.path.join(
        repository_path,
        cli_context.configuration.repository_processing.overrides_file_name,
    )
    cli_context.logger.debug(f"Reading configuration from {config_path}")
    try:
        config_override = config_reader.read_override_config(config_path)
    except FileNotFoundError:
        cli_context.logger.debug("No configuration found, using default configuration.")
    except DfPlayerCardManagerError as config_exc:
        cli_context.logger.error(f"Error reading configuration: {config_exc.message}")
        cli_context.logger.error("Using default configuration.")
    else:
        cli_context.card_manager.config.repository_source = config_merger.merge_configs(
            cli_context.configuration.repository_source,
            config_override.repository_source,
        )
        cli_context.card_manager.config.repository_processing = (
            config_merger.merge_configs(
                cli_context.configuration.repository_processing,
                config_override.repository_processing,
            )
        )
