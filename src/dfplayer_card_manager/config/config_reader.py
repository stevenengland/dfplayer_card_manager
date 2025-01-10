import os

from dfplayer_card_manager.config import config_checker, yaml_config
from dfplayer_card_manager.config.configuration import OverrideConfig


def read_override_config(config_file_path: str) -> OverrideConfig:
    if not os.path.isfile(config_file_path):
        raise FileNotFoundError("Configuration file not found")

    config = yaml_config.create_yaml_object(config_file_path, OverrideConfig)
    config_checker.check_override_config(config)

    return config
