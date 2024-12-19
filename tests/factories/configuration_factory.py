from faker import Faker

from src.config.configuration import RepositoryConfig

faker = Faker()


def create_source_repo_config() -> RepositoryConfig:
    return RepositoryConfig(
        root_dir=faker.file_path(),
        valid_subdir_pattern=faker.word(),
        valid_subdir_files_pattern=faker.word(),
    )


def create_target_repo_config() -> RepositoryConfig:
    return RepositoryConfig(
        root_dir=faker.file_path(),
        valid_subdir_pattern=faker.word(),
        valid_subdir_files_pattern=faker.word(),
    )
