import os

from dfplayer_card_manager.config import config_checker, yaml_config
from dfplayer_card_manager.config.configuration import (
    OverrideConfig,
    ProcessingConfig,
    RepositoryConfig,
)


def read_override_config(config_file_path: str) -> OverrideConfig:
    if not os.path.isfile(config_file_path):
        raise FileNotFoundError("Configuration file not found")

    read_config: OverrideConfig = yaml_config.create_yaml_object(
        config_file_path,
        OverrideConfig,
    )

    return_config = OverrideConfig(
        repository_source=read_config.repository_source or RepositoryConfig(),
        repository_processing=read_config.repository_processing or ProcessingConfig(),
    )

    config_checker.check_override_config(return_config)

    return return_config
