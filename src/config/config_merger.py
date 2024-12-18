from src.config.configuration import RepositorySourceConfig


def merge_configs(
    config: RepositorySourceConfig,
    overrides: RepositorySourceConfig,
) -> RepositorySourceConfig:
    merged = config
    for key in overrides.__annotations__:
        if getattr(overrides, key) is not None:
            setattr(merged, key, getattr(overrides, key))
    return merged
