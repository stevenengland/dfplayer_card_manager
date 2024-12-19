from src.config.configuration import RepositoryConfig


def merge_configs(
    config: RepositoryConfig,
    overrides: RepositoryConfig,
) -> RepositoryConfig:
    merged = config
    for key in overrides.__annotations__:
        if getattr(overrides, key) is not None:
            setattr(merged, key, getattr(overrides, key))
    return merged
