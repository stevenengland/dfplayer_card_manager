import hashlib
import re

from dfplayer_card_manager.config.configuration import RepositoryConfig
from dfplayer_card_manager.mp3.tag_collection import TagCollection
from dfplayer_card_manager.repository.detection_source import DetectionSource
from dfplayer_card_manager.repository.repository_element import (
    RepositoryElement,
)
from dfplayer_card_manager.repository.valid_file_types import ValidFileType


def update_element_by_dir(  # noqa: C901, WPS231
    element: RepositoryElement,
    config: RepositoryConfig,
) -> None:
    if config.album_source and config.album_source == DetectionSource.dirname:
        if not config.valid_subdir_pattern or not config.album_match:
            element.album = None
            return
        update_element_album_by_dir(
            element,
            config.valid_subdir_pattern,
            config.album_match,
        )

    if config.artist_source and config.artist_source == DetectionSource.dirname:
        if not config.valid_subdir_pattern or not config.artist_match:
            element.artist = None
            return
        update_element_artist_by_dir(
            element,
            config.valid_subdir_pattern,
            config.artist_match,
        )

    if config.dir_number_source and config.dir_number_source == DetectionSource.dirname:
        if not config.valid_subdir_pattern or not config.dir_number_match:
            element.dir_number = None
            return
        update_element_dirnum_by_dir(
            element,
            config.valid_subdir_pattern,
            config.dir_number_match,
        )

    if config.title_source and config.title_source == DetectionSource.dirname:
        if not config.valid_subdir_pattern or not config.title_match:
            element.title = None
            return
        update_element_title_by_dir(
            element,
            config.valid_subdir_pattern,
            config.title_match,
        )


def update_element_by_filename(  # noqa: WPS231, C901
    element: RepositoryElement,
    config: RepositoryConfig,
) -> None:

    update_element_file_type_by_filename(element)

    if config.album_source and config.album_source == DetectionSource.filename:
        if (
            not config.valid_subdir_files_pattern  # noqa: WPS204
            or not config.album_match
        ):
            element.album = None
            return
        update_element_album_by_filename(
            element,
            config.valid_subdir_files_pattern,
            config.album_match,
        )

    if config.artist_source and config.artist_source == DetectionSource.filename:
        if not config.valid_subdir_files_pattern or not config.artist_match:
            element.artist = None
            return
        update_element_artist_by_filename(
            element,
            config.valid_subdir_files_pattern,
            config.artist_match,
        )

    if (
        config.dir_number_source
        and config.dir_number_source == DetectionSource.filename
    ):
        if not config.valid_subdir_files_pattern or not config.dir_number_match:
            element.dir_number = None
            return
        update_element_dirnum_by_filename(
            element,
            config.valid_subdir_files_pattern,
            config.dir_number_match,
        )

    if config.title_source and config.title_source == DetectionSource.filename:
        if not config.valid_subdir_files_pattern or not config.title_match:
            element.title = None
            return
        update_element_title_by_filename(
            element,
            config.valid_subdir_files_pattern,
            config.title_match,
        )

    if (  # noqa: WPS337
        config.track_number_source
        and config.track_number_source == DetectionSource.filename
    ):
        if not config.valid_subdir_files_pattern or not config.track_number_match:
            element.track_number = None
            return
        update_element_tracknum_by_filename(
            element,
            config.valid_subdir_files_pattern,
            config.track_number_match,
        )


def update_element_album_by_dir(
    element: RepositoryElement,
    fs_pattern: str,
    album_match: int,
) -> None:
    match_result = _get_match(element.dir, fs_pattern, album_match)

    element.album = match_result


def update_element_album_by_filename(
    element: RepositoryElement,
    fs_pattern: str,
    album_match: int,
) -> None:
    match_result = _get_match(element.file_name, fs_pattern, album_match)

    element.album = match_result


def update_element_artist_by_dir(
    element: RepositoryElement,
    fs_pattern: str,
    artist_match: int,
) -> None:

    match_result = _get_match(element.dir, fs_pattern, artist_match)

    element.artist = match_result


def update_element_artist_by_filename(
    element: RepositoryElement,
    fs_pattern: str,
    artist_match: int,
) -> None:

    match_result = _get_match(element.file_name, fs_pattern, artist_match)

    element.artist = match_result


def update_element_title_by_dir(
    element: RepositoryElement,
    fs_pattern: str,
    title_match: int,
) -> None:
    match_result = _get_match(element.dir, fs_pattern, title_match)

    element.title = match_result


def update_element_title_by_filename(
    element: RepositoryElement,
    fs_pattern: str,
    title_match: int,
) -> None:
    match_result = _get_match(element.file_name, fs_pattern, title_match)

    element.title = match_result


def update_element_tracknum_by_dir(
    element: RepositoryElement,
    fs_pattern: str,
    match_num: int,
) -> None:
    match_result = _get_match(element.dir, fs_pattern, match_num)
    if match_result is None:
        element.track_number = None
        return
    try:
        element.track_number = int(match_result)
    except ValueError:
        return


def update_element_tracknum_by_filename(
    element: RepositoryElement,
    fs_pattern: str,
    match_num: int,
) -> None:
    match_result = _get_match(element.file_name, fs_pattern, match_num)
    if match_result is None:
        element.track_number = None
        return
    try:
        element.track_number = int(match_result)
    except ValueError:
        return


def update_element_dirnum_by_dir(
    element: RepositoryElement,
    fs_pattern: str,
    match_num: int,
) -> None:
    match_result = _get_match(element.dir, fs_pattern, match_num)
    if match_result is None:
        element.dir_number = None
        return
    try:
        element.dir_number = int(match_result)
    except ValueError:
        return


def update_element_dirnum_by_filename(
    element: RepositoryElement,
    fs_pattern: str,
    match_num: int,
) -> None:
    match_result = _get_match(element.file_name, fs_pattern, match_num)
    if match_result is None:
        element.dir_number = None
        return
    try:
        element.dir_number = int(match_result)
    except ValueError:
        return


def update_element_file_type_by_filename(element: RepositoryElement) -> None:
    if element.file_name.endswith(".mp3"):
        element.file_type = ValidFileType.mp3
    else:
        element.file_type = None


def _get_match(
    fs_text: str,
    fs_pattern: str,
    field_match: int,
) -> str | None:
    if field_match < 1:
        return None
    field_matched_text = re.search(
        fs_pattern,
        fs_text,
    )
    if field_matched_text:
        if len(field_matched_text.groups()) < field_match:
            return None
        return field_matched_text.group(field_match)

    return None


def update_element_by_tags(
    element: RepositoryElement,
    config: RepositoryConfig,
    id3_tags: TagCollection,
) -> RepositoryElement:
    if config.title_source == DetectionSource.tag and id3_tags.title:
        element.title = id3_tags.title
    if config.artist_source == DetectionSource.tag and id3_tags.artist:
        element.artist = id3_tags.artist
    if config.album_source == DetectionSource.tag and id3_tags.album:
        element.album = id3_tags.album
    if config.track_number_source == DetectionSource.tag and id3_tags.track_number:
        element.track_number = id3_tags.track_number
    return element


def update_element_by_audio_content(
    element: RepositoryElement,
    audio_content: bytes,
) -> RepositoryElement:
    # create md5 hash from audio content
    md5_hash = hashlib.md5(audio_content, usedforsecurity=False).hexdigest()
    element.hash = md5_hash
    return element
