from src.config.configuration import RepositoryConfig


def merge_configs(
    config: RepositoryConfig,
    overrides: RepositoryConfig,
) -> RepositoryConfig:
    merged = RepositoryConfig()
    # First copy the original config attributes that are not None
    for original_config_key in config.__annotations__:
        if getattr(config, original_config_key) is not None:
            setattr(merged, original_config_key, getattr(config, original_config_key))
    # Then override the attributes that are not None in the overrides
    for overrides_config_key in overrides.__annotations__:
        if getattr(overrides, overrides_config_key) is not None:
            setattr(
                merged,
                overrides_config_key,
                getattr(overrides, overrides_config_key),
            )
    return merged
