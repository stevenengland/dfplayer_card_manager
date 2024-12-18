from faker import Faker

from src.config.configuration import (
    RepositorySourceConfig,
    RepositoryTargetConfig,
)

faker = Faker()


def create_source_repo_config() -> RepositorySourceConfig:
    return RepositorySourceConfig(
        root_dir=faker.file_path(),
        valid_subdir_pattern=faker.word(),
        valid_subdir_files_pattern=faker.word(),
    )


def create_target_repo_config() -> RepositoryTargetConfig:
    return RepositoryTargetConfig(
        root_dir=faker.file_path(),
        valid_subdir_pattern=faker.word(),
        valid_subdir_files_pattern=faker.word(),
    )
