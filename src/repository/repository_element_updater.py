import re

from src.config.configuration import RepositoryConfig
from src.repository.detection_source import DetectionSource
from src.repository.repository_element import RepositoryElement


def update_element_by_dir(
    element: RepositoryElement,
    config: RepositoryConfig,
) -> None:
    if config.album_source == DetectionSource.dirname:
        update_element_album_by_fs(
            element,
            config.valid_subdir_pattern or "",
            config.album_match or 0,
        )

    if config.artist_source == DetectionSource.dirname:
        update_element_artist_by_fs(
            element,
            config.valid_subdir_pattern or "",
            config.artist_match or 0,
        )

    if config.title_source == DetectionSource.dirname:
        update_element_title_by_fs(
            element,
            config.valid_subdir_pattern or "",
            config.title_match or 0,
        )


def update_element_by_filename(
    element: RepositoryElement,
    config: RepositoryConfig,
) -> None:
    if config.album_source == DetectionSource.filename:
        update_element_album_by_fs(
            element,
            config.valid_subdir_files_pattern or "",
            config.album_match or 0,
        )

    if config.artist_source == DetectionSource.filename:
        update_element_artist_by_fs(
            element,
            config.valid_subdir_files_pattern or "",
            config.artist_match or 0,
        )

    if config.title_source == DetectionSource.filename:
        update_element_title_by_fs(
            element,
            config.valid_subdir_files_pattern or "",
            config.title_match or 0,
        )

    if config.track_number_source == DetectionSource.filename:
        update_element_tracknum_by_fs(
            element,
            config.valid_subdir_files_pattern or "",
            config.track_number_match or 0,
        )


def update_element_album_by_fs(
    element: RepositoryElement,
    dir_pattern: str,
    album_match: int,
) -> None:
    match_result = _get_match(element, dir_pattern, album_match)

    element.album = match_result


def update_element_artist_by_fs(
    element: RepositoryElement,
    dir_pattern: str,
    artist_match: int,
) -> None:

    match_result = _get_match(element, dir_pattern, artist_match)

    element.artist = match_result


def update_element_title_by_fs(
    element: RepositoryElement,
    dir_pattern: str,
    title_match: int,
) -> None:
    match_result = _get_match(element, dir_pattern, title_match)

    element.title = match_result


def update_element_tracknum_by_fs(
    element: RepositoryElement,
    filename_pattern: str,
    match_num: int,
) -> None:
    match_result = _get_match(element, filename_pattern, match_num)
    try:
        element.track_number = int(match_result)
    except ValueError:
        element.track_number = element.track_number


def _get_match(element: RepositoryElement, dir_pattern: str, field_match: int):
    if field_match < 1:
        raise ValueError("Match number must be 1 or greater")
    field_matched_text = re.search(
        dir_pattern,
        element.dir,
    )
    if field_matched_text:
        if len(field_matched_text.groups()) < field_match:
            return None
        artist_result = field_matched_text.group(field_match)
    return artist_result
