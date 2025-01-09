import copy

import pytest
from factories.compare_result_factory import create_compare_result
from factories.repository_element_factory import create_repository_element

from dfplayer_card_manager.repository.compare_result_actions import (
    CompareResultAction,
)
from dfplayer_card_manager.repository.diff_modes import DiffMode
from dfplayer_card_manager.repository.repository_comparator import (
    compare_repository_elements,
    stuff_compare_results,
)
from dfplayer_card_manager.repository.repository_element import (
    RepositoryElement,
)

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
    assert len(comparison_results) == 5
    # assert that a specific comparison result is in the list
    expected_results = [
        (50, 50, CompareResultAction.copy_to_target),
        (51, 51, CompareResultAction.delete_from_target),
        (1, 2, CompareResultAction.no_change),
        (1, 3, CompareResultAction.copy_to_target),
        (1, 4, CompareResultAction.no_change),
    ]
    for comparison_index, (dir_num, title_num, action) in enumerate(expected_results):
        assert comparison_results[comparison_index].dir_num == dir_num
        assert comparison_results[comparison_index].track_num == title_num
        assert comparison_results[comparison_index].action == action

    assert comparison_results[0].source_element == el_in_source_but_not_in_target
    assert comparison_results[0].target_element is None
    assert comparison_results[1].source_element is None
    assert comparison_results[1].target_element == el_in_target_but_not_in_source
    assert comparison_results[2].source_element == element_all_the_same
    assert comparison_results[2].target_element == element_all_the_same


def test_stuff_compare_results_returns_correct_list():
    # GIVEN
    unstuffed_compare_results = [
        create_compare_result(
            dir_num=1,
            track_num=1,
        ),  # ok
        create_compare_result(
            dir_num=1,
            track_num=2,
        ),
        create_compare_result(
            dir_num=2,
            track_num=1,
        ),  # need to be stuffed
        create_compare_result(
            dir_num=2,
            track_num=3,
        ),
        create_compare_result(
            dir_num=3,
            track_num=2,
        ),  # need to be stuffed
    ]
    # WHEN
    stuffed_compare_results = stuff_compare_results(unstuffed_compare_results)

    # THEN
    assert len(stuffed_compare_results) == 7
    assert stuffed_compare_results[0].dir_num == 1
    assert stuffed_compare_results[0].track_num == 1
    assert stuffed_compare_results[1].dir_num == 1
    assert stuffed_compare_results[1].track_num == 2

    assert stuffed_compare_results[3].dir_num == 2
    assert stuffed_compare_results[3].track_num == 2
    assert stuffed_compare_results[3].action == CompareResultAction.unstuff

    assert stuffed_compare_results[5].dir_num == 3
    assert stuffed_compare_results[5].track_num == 1
    assert stuffed_compare_results[5].action == CompareResultAction.unstuff
