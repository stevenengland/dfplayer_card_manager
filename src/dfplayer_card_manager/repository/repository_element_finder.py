import os

from dfplayer_card_manager.repository.repository_element import (
    RepositoryElement,
)


def find_repository_element(
    repository_elements: list[RepositoryElement],
    dir_number: int,
    track_number: int,
) -> RepositoryElement:
    for element in repository_elements:
        if element.dir_number == dir_number and element.track_number == track_number:
            return element
    return RepositoryElement()


def find_repository_element_path(
    repository_elements: list[RepositoryElement],
    dir_number: int,
    track_number: int,
) -> str | None:
    for element in repository_elements:
        if element.dir_number == dir_number and element.track_number == track_number:
            return os.path.join(element.repo_root_dir, element.dir, element.file_name)
    return None
