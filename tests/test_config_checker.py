import pytest

from src.config import config_checker
from src.config.configuration import RepositoryConfig
from src.repository.detection_source import DetectionSource
from tests.factories.configuration_factory import create_source_repo_config

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.mark.parametrize(
    "config, expected_error",
    [
        (
            create_source_repo_config(
                RepositoryConfig(track_number_source=DetectionSource.dirname),
            ),
            "Track number source",
        ),
        (
            create_source_repo_config(
                RepositoryConfig(album_source=DetectionSource.dirname, album_match=0),
            ),
            "Album match",
        ),
        (
            create_source_repo_config(
                RepositoryConfig(artist_source=DetectionSource.dirname, artist_match=0),
            ),
            "Artist match",
        ),
        (
            create_source_repo_config(
                RepositoryConfig(title_source=DetectionSource.dirname, title_match=0),
            ),
            "Title match",
        ),
    ],
)
def test_config_check_raises2(config: RepositoryConfig, expected_error: str):
    with pytest.raises(ValueError, match=expected_error):
        config_checker.check_repository_config(config)
