from faker import Faker
from multipledispatch import dispatch

from src.repository.repository_element import RepositoryElement

faker = Faker()


@dispatch()
def create_repository_element() -> RepositoryElement:
    return RepositoryElement(
        track_number=faker.random_int(min=1, max=255),
        dir_number=faker.random_int(min=1, max=99),
        repo_root_dir=faker.file_path(),
        dir=faker.word(),
        file_name=faker.file_name(),
        title=faker.word(),
        artist=faker.word(),
        album=faker.word(),
        hash=faker.md5(),
        tree_id=faker.uuid4(),
    )


@dispatch(RepositoryElement)  # type: ignore[no-redef]
def create_repository_element(config) -> RepositoryElement:  # noqa: WPS440, F811
    base_element = create_repository_element()

    # merge the base config with the provided config in a generic manner
    for config_key, config_value in config.__dict__.items():
        if config_value is not None:
            base_element.__dict__[config_key] = config_value
    return base_element
