from dfplayer_card_manager.config.configuration import RepositoryConfig
from dfplayer_card_manager.repository.detection_source import DetectionSource


def check_repository_config(  # noqa: C901, WPS238, WPS231
    config: RepositoryConfig,
    check_mandatory_values: bool = True,
) -> None:
    # check mandatory config values
    if check_mandatory_values:
        if (
            config.album_source == DetectionSource.filename
            or config.artist_source == DetectionSource.filename
            or config.title_source == DetectionSource.filename
            or config.track_number_source == DetectionSource.filename
        ):
            if config.valid_subdir_files_pattern is None:
                raise ValueError("Valid subdir files pattern must be set")
        if (
            config.album_source == DetectionSource.dirname
            or config.artist_source == DetectionSource.dirname
            or config.title_source == DetectionSource.dirname
            or config.track_number_source == DetectionSource.dirname
        ):
            if config.valid_subdir_pattern is None:
                raise ValueError("Valid subdir pattern must be set")

    # detection constellations that are not supported
    if config.track_number_source == DetectionSource.dirname:
        raise ValueError("Track number cannot be read from dir name")

    if config.dir_number_source == DetectionSource.tag:
        raise ValueError("Directory number cannot be read from tags")

    # detection completeness checks
    if config.album_source in {DetectionSource.filename, DetectionSource.dirname}:
        if config.album_match is None or config.album_match < 1:
            raise ValueError("Album match number must be set and greater than 0")

    if config.artist_source in {DetectionSource.filename, DetectionSource.dirname}:
        if config.artist_match is None or config.artist_match < 1:
            raise ValueError("Artist match number must be set and greater than 0")

    if config.dir_number_source in {DetectionSource.filename, DetectionSource.dirname}:
        if config.dir_number_match is None or config.dir_number_match < 1:
            raise ValueError(
                "Directory number match number must be set and greater than 0",
            )

    if config.title_source in {DetectionSource.filename, DetectionSource.dirname}:
        if config.title_match is None or config.title_match < 1:
            raise ValueError("Title match number must be set and greater than 0")

    if config.track_number_source == DetectionSource.filename:
        if config.track_number_match is None or config.track_number_match < 1:
            raise ValueError("Track number match number must be set and greater than 0")
