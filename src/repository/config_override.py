import os

from src.config.configuration import RepositorySourceConfig


def get_config_overrides(
    root_dir: str,
    subdirs: list[str],
    overrides_file_name: str,
) -> dict[str, RepositorySourceConfig]:
    config_overrides = {}
    for subdir in subdirs:
        override_file_name = os.path.join(root_dir, subdir, overrides_file_name)
        if os.path.isdir(os.path.join(root_dir, subdir)):
            if os.path.isfile(override_file_name):
                config = RepositorySourceConfig().from_yaml(  # type: ignore [no-untyped-call]
                    override_file_name,
                )
            config_overrides[subdir] = config
    return config_overrides
