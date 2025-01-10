import os

from dfplayer_card_manager.cli.cli_context import CliContext
from dfplayer_card_manager.cli.printing import print_action, print_ok
from dfplayer_card_manager.config import config_merger, config_reader
from dfplayer_card_manager.dfplayer.dfplayer_card_manager_error import (
    DfPlayerCardManagerError,
)


def sync(
    cli_context: CliContext,
    sd_card_path: str,
    repository_path: str,
    dry_run: bool,
) -> None:
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
