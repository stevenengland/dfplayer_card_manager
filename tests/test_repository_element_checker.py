import pytest

from src.repository import repository_element_checker
from src.repository.repository_element import RepositoryElement
from tests.factories.repository_element_factory import create_repository_element

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


class TestRepositoryElementChecks:

    @pytest.mark.parametrize(
        "element, expected_error",
        [
            (
                create_repository_element(
                    RepositoryElement(track_number=256),
                ),
                "Track number",
            ),
            (
                create_repository_element(
                    RepositoryElement(track_number=0),
                ),
                "Track number",
            ),
            (
                create_repository_element(
                    RepositoryElement(
                        dir_number=100,
                    ),
                ),
                "Directory number",
            ),
            (
                create_repository_element(
                    RepositoryElement(
                        dir_number=-1,
                    ),
                ),
                "Directory number",
            ),
            (
                RepositoryElement(
                    track_number=1,
                    dir_number=1,
                    file_type=None,
                ),
                "File type",
            ),
        ],
    )
    def test_element_checks_by_dir(self, element, expected_error):
        # GIVEN
        # WHEN
        # THEN
        with pytest.raises(ValueError, match=expected_error):
            repository_element_checker.check_element(element)
