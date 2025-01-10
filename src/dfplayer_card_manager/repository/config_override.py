import os

from dfplayer_card_manager.config import yaml_config
from dfplayer_card_manager.config.configuration import RepositoryConfig


def get_config_overrides(
    root_dir: str,
    subdirs: list[str],
    overrides_file_name: str,
) -> dict[str, RepositoryConfig]:
    config_overrides = {}
    for subdir in subdirs:
        override_file_name = os.path.join(root_dir, subdir, overrides_file_name)
        if os.path.isdir(os.path.join(root_dir, subdir)):
            if os.path.isfile(override_file_name):
                config: RepositoryConfig = yaml_config.create_yaml_object(
                    override_file_name,
                    RepositoryConfig,
                )

                config_overrides[subdir] = config
    return config_overrides
