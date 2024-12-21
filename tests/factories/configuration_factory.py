from faker import Faker
from multipledispatch import dispatch

from src.config.configuration import RepositoryConfig

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


def create_target_repo_config() -> RepositoryConfig:
    return RepositoryConfig(
        root_dir=faker.file_path(),
        valid_subdir_pattern=faker.word(),
        valid_subdir_files_pattern=faker.word(),
    )
