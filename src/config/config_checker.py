from src.config.configuration import RepositoryConfig
from src.repository.detection_source import DetectionSource


def check_repository_config(  # noqa: C901, WPS238, WPS231
    config: RepositoryConfig,
) -> None:
    # detection constellations that are not supported
    if config.track_number_source == DetectionSource.dirname:
        raise ValueError("Track number source cannot be read from dir name")

    # detection completeness checks
    if config.album_source in {DetectionSource.filename, DetectionSource.dirname}:
        if config.album_match is None or config.album_match < 1:
            raise ValueError("Album match number must be set and greater than 0")

    if config.artist_source in {DetectionSource.filename, DetectionSource.dirname}:
        if config.artist_match is None or config.artist_match < 1:
            raise ValueError("Artist match number must be set and greater than 0")

    if config.title_source in {DetectionSource.filename, DetectionSource.dirname}:
        if config.title_match is None or config.title_match < 1:
            raise ValueError("Title match number must be set and greater than 0")
