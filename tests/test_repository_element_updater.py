import pytest

from src.config.configuration import RepositoryConfig
from src.repository import repository_element_updater
from src.repository.detection_source import DetectionSource
from src.repository.repository_element import RepositoryElement

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


class TestElementUpdates:
    def test_element_updates(self, when):
        # GIVEN
        element = RepositoryElement()
        element.dir = "01.no.yes.loremipsum"
        config = RepositoryConfig(
            valid_subdir_pattern=r"^\d{2}\.(no)\.(yes).*$",
            album_match=2,
            artist_match=2,
            title_match=2,
            album_source=DetectionSource.dirname,
            artist_source=DetectionSource.dirname,
            title_source=DetectionSource.dirname,
        )
        # WHEN
        repository_element_updater.update_element_by_dir(
            element,
            config,
        )
        # THEN
        assert element.title == "yes"
        assert element.artist == "yes"
        assert element.album == "yes"


class TestElementTitleUpdates:
    def test_title_gets_updated(self, when):
        # GIVEN
        element = RepositoryElement()
        element.dir = "01.no.yes.loremipsum"
        # WHEN
        repository_element_updater.update_element_title_by_dir(
            element,
            r"^\d{2}\.(no)\.(yes).*$",
            2,
        )
        # THEN
        assert element.title == "yes"

    def test_title_gets_updated_raises_when_title_match_lt_1(self):
        # GIVEN
        element = RepositoryElement()
        # WHEN
        # THEN
        with pytest.raises(ValueError, match="Match"):
            repository_element_updater.update_element_title_by_dir(
                element,
                r"^\d{2}\.(no)\.(yes).*$",
                0,
            )

    def test_title_isnt_updated_when_title_match_is_too_large(self):
        # GIVEN
        element = RepositoryElement()
        element.dir = "01.no.yes.loremipsum"
        # WHEN
        repository_element_updater.update_element_title_by_dir(
            element,
            r"^\d{2}\.(no)\.(yes).*$",
            99,
        )
        # THEN
        assert element.title is None


class TestElementAlbumUpdates:
    def test_album_gets_updated(self, when):
        # GIVEN
        element = RepositoryElement()
        element.dir = "01.no.yes.loremipsum"
        # WHEN
        repository_element_updater.update_element_album_by_dir(
            element,
            r"^\d{2}\.(no)\.(yes).*$",
            1,
        )
        # THEN
        assert element.album == "no"

    def test_album_gets_updated_raises_when_album_match_lt_1(self):
        # GIVEN
        element = RepositoryElement()
        # WHEN
        # THEN
        with pytest.raises(ValueError, match="Match"):
            repository_element_updater.update_element_album_by_dir(
                element,
                r"^\d{2}\.(no)\.(yes).*$",
                0,
            )

    def test_album_isnt_updated_when_album_match_is_too_large(self):
        # GIVEN
        element = RepositoryElement()
        element.dir = "01.no.yes.loremipsum"
        # WHEN
        repository_element_updater.update_element_album_by_dir(
            element,
            r"^\d{2}\.(no)\.(yes).*$",
            99,
        )
        # THEN
        assert element.album is None


class TestElementArtistUpdates:
    def test_artist_gets_updated(self, when):
        # GIVEN
        element = RepositoryElement()
        element.dir = "01.no.yes.loremipsum"
        # WHEN
        repository_element_updater.update_element_artist_by_dir(
            element,
            r"^\d{2}\.(no)\.(yes).*$",
            1,
        )
        # THEN
        assert element.artist == "no"

    def test_artist_gets_updated_raises_when_artist_match_lt_1(self):
        # GIVEN
        element = RepositoryElement()
        # WHEN
        # THEN
        with pytest.raises(ValueError, match="Match"):
            repository_element_updater.update_element_artist_by_dir(
                element,
                r"^\d{2}\.(no)\.(yes).*$",
                0,
            )

    def test_artist_isnt_updated_when_artist_match_is_too_large(self):
        # GIVEN
        element = RepositoryElement()
        element.dir = "01.no.yes.loremipsum"
        # WHEN
        repository_element_updater.update_element_artist_by_dir(
            element,
            r"^\d{2}\.(no)\.(yes).*$",
            99,
        )
        # THEN
        assert element.artist is None
