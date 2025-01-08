import os

from dfplayer_card_manager.cli.cli_context import CliContext
from dfplayer_card_manager.cli.printing import (
    print_action,
    print_error,
    print_neutral,
    print_ok,
)
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

    cli_context.card_manager.create_repositories()

    repo_comparison_result = cli_context.card_manager.get_repositories_comparison()
    if not repo_comparison_result:
        print_ok("Nothing to do.")
        exit(0)
    for compared_item in repo_comparison_result:
        print_action(compared_item)
        if not dry_run:
            pass


def _set_config_override(cli_context: CliContext, repository_path: str) -> None:
    try:
        config_override = config_reader.read_override_config(
            os.path.join(
                repository_path,
                cli_context.configuration.repository_processing.overrides_file_name,
            ),
        )
    except FileNotFoundError:
        print_neutral("No configuration found, using default configuration.")
    except DfPlayerCardManagerError as config_exc:
        print_error(f"Error reading configuration: {config_exc.message}")
        print_neutral("Using default configuration.")
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
