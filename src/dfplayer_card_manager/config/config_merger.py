from multipledispatch import dispatch

from dfplayer_card_manager.config.configuration import (
    ProcessingConfig,
    RepositoryConfig,
)


@dispatch(RepositoryConfig, RepositoryConfig)
def merge_configs(
    config: RepositoryConfig,
    overrides: RepositoryConfig,
) -> RepositoryConfig:
    return _merge_common(config, overrides, RepositoryConfig())


@dispatch(ProcessingConfig, ProcessingConfig)  # type: ignore[no-redef]
def merge_configs(  # noqa: WPS440, F811
    config: ProcessingConfig,
    overrides: ProcessingConfig,
) -> ProcessingConfig:
    return _merge_common(config, overrides, ProcessingConfig())


def _merge_common(config, overrides, merged):
    for config_key in config.__annotations__:
        if getattr(config, config_key) is not None:
            setattr(merged, config_key, getattr(config, config_key))
    for overrides_key in overrides.__annotations__:
        if getattr(overrides, overrides_key) is not None:
            setattr(merged, overrides_key, getattr(overrides, overrides_key))
    return merged
