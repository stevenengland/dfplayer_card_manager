from faker import Faker
from multipledispatch import dispatch

from dfplayer_card_manager.config.config_merger import merge_configs
from dfplayer_card_manager.config.configuration import (
    Configuration,
    ProcessingConfig,
    RepositoryConfig,
)
from dfplayer_card_manager.repository.detection_source import DetectionSource
from dfplayer_card_manager.repository.diff_modes import DiffMode

faker = Faker()


@dispatch()
def create_source_repo_config() -> RepositoryConfig:
    return RepositoryConfig(
        root_dir=faker.file_path(),
        valid_subdir_pattern=faker.word(),
        valid_subdir_files_pattern=faker.word(),
    )


@dispatch(RepositoryConfig)  # type: ignore[no-redef]
def create_source_repo_config(config) -> RepositoryConfig:  # noqa: WPS440, F811
    base_config = create_source_repo_config()

    # merge the base config with the provided config in a generic manner
    for config_key, config_value in config.__dict__.items():
        if config_value is not None:
            base_config.__dict__[config_key] = config_value
    return base_config


def create_source_repo_config_all_sources_tag(
    config: RepositoryConfig,
) -> RepositoryConfig:
    base_config = create_source_repo_config(config)
    base_config.album_source = DetectionSource.tag
    base_config.artist_source = DetectionSource.tag
    base_config.dir_number_source = DetectionSource.dirname
    base_config.title_source = DetectionSource.tag
    base_config.track_number_source = DetectionSource.tag
    return merge_configs(base_config, config)


def create_target_repo_config() -> RepositoryConfig:
    return RepositoryConfig(
        root_dir=faker.file_path(),
        valid_subdir_pattern=faker.word(),
        valid_subdir_files_pattern=faker.word(),
    )


@dispatch()
def create_processing_config() -> ProcessingConfig:
    return ProcessingConfig(
        diff_method=faker.enum(DiffMode),
        overrides_file_name=faker.word(),
    )


@dispatch(ProcessingConfig)  # type: ignore[no-redef]
def create_processing_config(config) -> ProcessingConfig:  # noqa: WPS440, F811
    base_config = create_processing_config()

    # merge the base config with the provided config in a generic manner
    for config_key, config_value in config.__dict__.items():
        if config_value is not None:
            base_config.__dict__[config_key] = config_value
    return base_config


def create_config() -> Configuration:
    return Configuration(
        repository_source=create_source_repo_config(),
        repository_target=create_target_repo_config(),
        repository_processing=create_processing_config(),
    )
