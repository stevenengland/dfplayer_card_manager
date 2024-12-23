import copy

import pytest

from src.repository.compare_results import CompareResult
from src.repository.diff_modes import DiffMode
from src.repository.repository_comparator import compare_repository_elements
from src.repository.repository_element import RepositoryElement
from tests.factories.repository_element_factory import create_repository_element

pytestmark = pytest.mark.usefixtures("unstub")
e2e = pytest.mark.skipif("not config.getoption('e2e')")


def test_repository_comparison():
    # GIVEN
    source_repo: list[RepositoryElement] = []
    target_repo: list[RepositoryElement] = []

    el_in_source_but_not_in_target = create_repository_element(
        RepositoryElement(dir_number=50, track_number=50),
    )
    source_repo.append(el_in_source_but_not_in_target)
    el_in_target_but_not_in_source = create_repository_element(
        RepositoryElement(dir_number=51, track_number=51),
    )
    target_repo.append(el_in_target_but_not_in_source)

    element_all_the_same = create_repository_element(
        RepositoryElement(dir_number=1, track_number=2),
    )
    source_repo.append(copy.deepcopy(element_all_the_same))
    target_repo.append(copy.deepcopy(element_all_the_same))

    element_with_changed_hash = create_repository_element(
        RepositoryElement(dir_number=1, track_number=3),
    )
    source_repo.append(copy.deepcopy(element_with_changed_hash))
    element_with_changed_hash.hash = "different_hash"
    target_repo.append(copy.deepcopy(element_with_changed_hash))
    element_all_the_same_with_none_tag_value = create_repository_element(
        RepositoryElement(dir_number=1, track_number=4, artist=None),
    )
    source_repo.append(copy.deepcopy(element_all_the_same_with_none_tag_value))
    target_repo.append(copy.deepcopy(element_all_the_same_with_none_tag_value))
    # WHEN
    comparison_results = compare_repository_elements(
        source_repo,
        target_repo,
        DiffMode.hash_and_tags,
    )
    # THEN
    assert (50, 50, CompareResult.copy_to_target) in comparison_results
    assert (51, 51, CompareResult.delete_from_target) in comparison_results
    assert (1, 2, CompareResult.no_change) in comparison_results
    assert (1, 3, CompareResult.copy_to_target) in comparison_results
    assert (1, 4, CompareResult.no_change) in comparison_results
