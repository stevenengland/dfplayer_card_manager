import pytest
from factories.configuration_factory import (
    create_processing_config,
    create_source_repo_config,
    create_target_repo_config,
)

from dfplayer_card_manager.config import config_checker
from dfplayer_card_manager.config.configuration import (
    Configuration,
    RepositoryConfig,
)
from dfplayer_card_manager.repository.detection_source import DetectionSource

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture(scope="function", name="sut")
def base_config() -> Configuration:
    sut = Configuration()
    sut.repository_source = create_source_repo_config()
    sut.repository_target = create_target_repo_config()
    sut.repository_processing = create_processing_config()
    return sut


@pytest.mark.parametrize(
    "config, expected_error",
    [
        (
            create_source_repo_config(
                RepositoryConfig(track_number_source=DetectionSource.dirname),
            ),
            "Track number cannot",
        ),
        (
            create_source_repo_config(
                RepositoryConfig(
                    track_number_source=DetectionSource.filename,
                    track_number_match=0,
                ),
            ),
            "Track number match",
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
        (
            create_source_repo_config(
                RepositoryConfig(dir_number_source=DetectionSource.tag),
            ),
            "Directory number cannot",
        ),
        (
            create_source_repo_config(
                RepositoryConfig(
                    dir_number_source=DetectionSource.filename,
                    dir_number_match=0,
                ),
            ),
            "Directory number match",
        ),
    ],
)
def test_repository_config_check_raises(config: RepositoryConfig, expected_error: str):
    with pytest.raises(ValueError, match=expected_error):
        config_checker.check_repository_config(config)


def test_config_check_raises_if_source_repo_is_not_set(sut: Configuration):
    sut.repository_source = None
    with pytest.raises(ValueError, match="source repository"):
        config_checker.check_config(sut)


def test_config_check_raises_if_target_repo_is_not_set(sut: Configuration):
    sut.repository_target = None
    with pytest.raises(ValueError, match="target repository"):
        config_checker.check_config(sut)


def test_config_check_raises_if_processing_repo_is_not_set(sut: Configuration):
    sut.repository_processing = None
    with pytest.raises(ValueError, match="processing repository"):
        config_checker.check_config(sut)
