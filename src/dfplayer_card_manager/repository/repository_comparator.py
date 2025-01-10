from dfplayer_card_manager.repository.compare_result import CompareResult
from dfplayer_card_manager.repository.compare_result_actions import (
    CompareResultAction,
)
from dfplayer_card_manager.repository.diff_modes import DiffMode
from dfplayer_card_manager.repository.repository_element import (
    RepositoryElement,
)


# ToDo: Refactor this function to make it less complex and more efficient.
def stuff_compare_results(  # noqa: WPS231
    unstuffed_compare_results: list[CompareResult],
) -> list[CompareResult]:
    # get all distinct dir_num values from the list of CompareResult objects
    dir_nums = sorted(
        {compare_result.dir_num for compare_result in unstuffed_compare_results},
    )
    # get the highest track_num value for each dir_num
    highest_track_num_per_dir = {
        dir_num: max(
            compare_result.track_num
            for compare_result in unstuffed_compare_results
            if compare_result.dir_num == dir_num
        )
        for dir_num in dir_nums
    }

    # for every dir_num, check if there is a CompareResult object from track_num 1 to the highest track_num value.
    # If yes, add it to the stuffed_compare_results list.
    # If not, add a CompareResult object with action set to "delete_from_target" to the stuffed_compare_results list.
    stuffed_compare_results = []
    for dir_num in dir_nums:
        for track_num in range(1, highest_track_num_per_dir[dir_num] + 1):
            found = False
            for compare_result in unstuffed_compare_results:
                if (
                    compare_result.dir_num == dir_num
                    and compare_result.track_num == track_num
                ):
                    stuffed_compare_results.append(compare_result)
                    found = True
                    break
            if not found:
                stuffed_compare_results.append(
                    CompareResult(
                        dir_num=dir_num,
                        track_num=track_num,
                        action=CompareResultAction.unstuff,
                    ),
                )

    return stuffed_compare_results


def compare_repository_elements(
    source: list[RepositoryElement],
    target: list[RepositoryElement],
    diff_mode: DiffMode,
) -> list[CompareResult]:
    comparison_results = []

    source_dict = {
        (element.dir_number, element.track_number): element
        for element in source
        if element.dir_number is not None and element.track_number is not None
    }
    target_dict = {
        (element.dir_number, element.track_number): element
        for element in target
        if element.dir_number is not None and element.track_number is not None
    }

    for source_key, _source_target in source_dict.items():
        if source_key not in target_dict:
            comparison_results.append(
                CompareResult(
                    dir_num=source_key[0],
                    track_num=source_key[1],
                    source_element=source_dict[source_key],
                    action=CompareResultAction.copy_to_target,
                ),
            )

    for target_key, _target_value in target_dict.items():
        if target_key not in source_dict:
            comparison_results.append(
                CompareResult(
                    dir_num=target_key[0],
                    track_num=target_key[1],
                    target_element=target_dict[target_key],
                    action=CompareResultAction.delete_from_target,
                ),
            )
        else:
            if _should_copy_to_target(
                diff_mode,
                source_dict[target_key],
                target_dict[target_key],
            ):
                comparison_results.append(
                    CompareResult(
                        dir_num=target_key[0],
                        track_num=target_key[1],
                        source_element=source_dict[target_key],
                        action=CompareResultAction.copy_to_target,
                    ),
                )
            else:
                comparison_results.append(
                    CompareResult(
                        dir_num=target_key[0],
                        track_num=target_key[1],
                        source_element=source_dict[target_key],
                        target_element=target_dict[target_key],
                        action=CompareResultAction.no_change,
                    ),
                )

    return comparison_results


def _is_hash_different(
    source_element: RepositoryElement,
    target_element: RepositoryElement,
) -> bool:
    return source_element.hash != target_element.hash


def _should_copy_to_target(
    diff_mode: DiffMode,
    source_element: RepositoryElement,
    target_element: RepositoryElement,
) -> bool:
    if diff_mode == DiffMode.hash_and_tags:
        return _is_hash_different(
            source_element,
            target_element,
        ) or _are_tags_different(source_element, target_element)
    elif diff_mode == DiffMode.hash:
        return _is_hash_different(source_element, target_element)
    elif diff_mode == DiffMode.tags:
        return _are_tags_different(source_element, target_element)
    return False


def _are_tags_different(
    source_element: RepositoryElement,
    target_element: RepositoryElement,
) -> bool:
    if _are_none_tags_different(source_element.artist, target_element.artist):
        return True
    if _are_none_tags_different(source_element.title, target_element.title):
        return True
    if _are_none_tags_different(source_element.album, target_element.album):
        return True
    if _are_none_tags_different(
        source_element.track_number,
        target_element.track_number,
    ):
        return True

    return (
        source_element.artist != target_element.artist
        or source_element.title != target_element.title
        or source_element.album != target_element.album
        or source_element.track_number != target_element.track_number
    )


def _are_none_tags_different(
    source_tag: str | int | None,
    target_tag: str | int | None,
) -> bool:
    return (source_tag is None) != (target_tag is None)
