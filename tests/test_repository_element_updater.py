import hashlib

import pytest

from src.config.configuration import RepositoryConfig
from src.mp3.tag_collection import TagCollection
from src.repository import repository_element_updater
from src.repository.detection_source import DetectionSource
from src.repository.repository_element import RepositoryElement

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


class TestElementUpdates:
    def test_element_updates_by_dir(self, when):
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

    def test_element_updates_by_filename(self, when):
        # GIVEN
        element = RepositoryElement()
        element.dir = "01.no.yes.loremipsum"
        config = RepositoryConfig(
            valid_subdir_files_pattern=r"^(\d{2})\.(no)\.(yes).*$",
            album_match=3,
            artist_match=3,
            title_match=3,
            track_number_match=1,
            track_number_source=DetectionSource.filename,
            album_source=DetectionSource.filename,
            artist_source=DetectionSource.filename,
            title_source=DetectionSource.filename,
        )
        # WHEN
        repository_element_updater.update_element_by_filename(
            element,
            config,
        )
        # THEN
        assert element.title == "yes"
        assert element.artist == "yes"
        assert element.album == "yes"
        assert element.track_number == 1

    def test_element_updates_by_tags(self, when):
        # GIVEN
        element = RepositoryElement()
        id3_tags = TagCollection()
        id3_tags.title = "test_title"
        id3_tags.artist = "test_artist"
        id3_tags.album = "test_album"
        id3_tags.track_number = 66
        config = RepositoryConfig(
            album_source=DetectionSource.tag,
            artist_source=DetectionSource.tag,
            title_source=DetectionSource.tag,
            track_number_source=DetectionSource.tag,
        )
        # WHEN
        repository_element_updater.update_element_by_tags(
            element,
            config,
            id3_tags,
        )
        # THEN
        assert element.title == "test_title"
        assert element.artist == "test_artist"
        assert element.album == "test_album"
        assert element.track_number == 66

    def test_element_updates_by_audio_content(self, when):
        # GIVEN
        element = RepositoryElement()
        audio_content = b"test_audio_content"
        audio_content_hash = hashlib.md5(
            audio_content,
            usedforsecurity=False,
        ).hexdigest()
        # WHEN
        repository_element_updater.update_element_by_audio_content(
            element,
            audio_content,
        )
        # THEN
        assert element.hash == audio_content_hash


class TestElementTitleUpdates:
    def test_title_gets_updated(self, when):
        # GIVEN
        element = RepositoryElement()
        element.dir = "01.no.yes.loremipsum"
        # WHEN
        repository_element_updater.update_element_title_by_fs(
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
            repository_element_updater.update_element_title_by_fs(
                element,
                r"^\d{2}\.(no)\.(yes).*$",
                0,
            )

    def test_title_isnt_updated_when_title_match_is_too_large(self):
        # GIVEN
        element = RepositoryElement()
        element.dir = "01.no.yes.loremipsum"
        # WHEN
        repository_element_updater.update_element_title_by_fs(
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
        repository_element_updater.update_element_album_by_fs(
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
            repository_element_updater.update_element_album_by_fs(
                element,
                r"^\d{2}\.(no)\.(yes).*$",
                0,
            )

    def test_album_isnt_updated_when_album_match_is_too_large(self):
        # GIVEN
        element = RepositoryElement()
        element.dir = "01.no.yes.loremipsum"
        # WHEN
        repository_element_updater.update_element_album_by_fs(
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
        repository_element_updater.update_element_artist_by_fs(
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
            repository_element_updater.update_element_artist_by_fs(
                element,
                r"^\d{2}\.(no)\.(yes).*$",
                0,
            )

    def test_artist_isnt_updated_when_artist_match_is_too_large(self):
        # GIVEN
        element = RepositoryElement()
        element.dir = "01.no.yes.loremipsum"
        # WHEN
        repository_element_updater.update_element_artist_by_fs(
            element,
            r"^\d{2}\.(no)\.(yes).*$",
            99,
        )
        # THEN
        assert element.artist is None
