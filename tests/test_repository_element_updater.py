import pytest

from src.config.configuration import RepositoryConfig
from src.repository import repository_element_updater
from src.repository.detection_source import DetectionSource
from src.repository.repository_element import RepositoryElement
from tests.factories.configuration_factory import create_source_repo_config

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


class TestElementUpdates:
    def test_title_gets_updated(self, when):
        # GIVEN
        config = RepositoryConfig()
        config.valid_subdir_pattern = r"^\d{2}\.(no)\.(yes).*$"
        config.title_source = DetectionSource.dirname
        config.title_match = 2
        element = RepositoryElement()
        element.dir = "01.no.yes.loremipsum"
        # WHEN
        repository_element_updater.update_title_by_dir(element, config)
        # THEN
        assert element.title == "yes"

    def test_title_gets_updated_raises_when_title_match_is_0(self):
        # GIVEN
        config = create_source_repo_config()
        config.title_source = DetectionSource.dirname
        config.title_match = 0
        element = RepositoryElement()
        # WHEN
        # THEN
        with pytest.raises(ValueError, match="match"):
            repository_element_updater.update_title_by_dir(element, config)

    def test_title_gets_updated_raises_when_title_match_is_none(self):
        # GIVEN
        config = create_source_repo_config()
        config.title_source = DetectionSource.dirname
        config.title_match = None
        element = RepositoryElement()
        # WHEN
        # THEN
        with pytest.raises(ValueError, match="match"):
            repository_element_updater.update_title_by_dir(element, config)

    def test_title_gets_updated_raises_when_valid_subdir_pattern_is_none(self):
        # GIVEN
        config = create_source_repo_config()
        config.valid_subdir_pattern = None
        element = RepositoryElement()
        # WHEN
        # THEN
        with pytest.raises(ValueError, match="pattern"):
            repository_element_updater.update_title_by_dir(element, config)

    def test_title_isnt_updated_when_title_match_is_too_large(self):
        # GIVEN
        config = RepositoryConfig()
        config.valid_subdir_pattern = r"^\d{2}\.(no)\.(yes).*$"
        config.title_source = DetectionSource.dirname
        config.title_match = 99
        element = RepositoryElement()
        before = element.title
        element.dir = "01.no.yes.loremipsum"
        # WHEN
        repository_element_updater.update_title_by_dir(element, config)
        # THEN
        assert element.title == before
