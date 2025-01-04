from dfplayer_card_manager.repository.compare_result import CompareResult
from dfplayer_card_manager.repository.compare_result_actions import (
    CompareResultAction,
)
from dfplayer_card_manager.repository.diff_modes import DiffMode
from dfplayer_card_manager.repository.repository_element import (
    RepositoryElement,
)


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
                        target_element=target_dict[target_key],
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
