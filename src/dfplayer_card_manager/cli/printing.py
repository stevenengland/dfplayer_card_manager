# ToDo: Tests
import os

from rich import print

from dfplayer_card_manager.repository.compare_result import CompareResult
from dfplayer_card_manager.repository.compare_result_actions import (
    CompareResultAction,
)
from dfplayer_card_manager.repository.repository_element import (
    RepositoryElement,
)


def print_task(message: str) -> None:
    print(f"[bold]Task:[/bold] {message}")


def print_neutral(message: str, is_bullet: bool = False) -> None:
    print(f"{_bullet_prefix(is_bullet)}{message}")


def print_ok(message: str, is_bullet: bool = False) -> None:
    print(f"[green]{_bullet_prefix(is_bullet)}{message}[/green]")


def print_warning(message: str, is_bullet: bool = False) -> None:
    print(f"[yellow]{_bullet_prefix(is_bullet)}{message}[/yellow]")


def print_error(message: str, is_bullet: bool = False) -> None:
    print(f"[red]{_bullet_prefix(is_bullet)}{message}[/red]")


def print_action(compared_item: CompareResult):
    dir_str = str(compared_item.dir_num).zfill(2)
    track_str = str(compared_item.track_num).zfill(3)
    left_path = f"{dir_str}{os.sep}{track_str}"
    if compared_item.action == CompareResultAction.copy_to_target:
        print_warning(
            f"+++ |{left_path}| <-- |{_get_element_relative_path(compared_item.source_element)}|",
        )
    elif compared_item.action == CompareResultAction.delete_from_target:
        print_warning(
            f"--- |{left_path}| <-- X",
        )
    elif compared_item.action == CompareResultAction.no_change:
        print_ok(
            f"ooo |{left_path}| --- |{_get_element_relative_path(compared_item.source_element)}|",
        )
    elif compared_item.action == CompareResultAction.unstuff:
        print_error(
            f"??? |{left_path}| <-- |MISSING FILE|",
        )


def _get_element_relative_path(element: RepositoryElement) -> str:
    return os.path.join(element.dir, element.file_name)


def _bullet_prefix(is_bullet: bool) -> str:
    return "• " if is_bullet else ""
