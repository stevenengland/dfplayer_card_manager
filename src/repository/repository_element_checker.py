from src.repository.repository_element import RepositoryElement


def check_element(element: RepositoryElement) -> None:
    if (
        not element.track_number
        or element.track_number < 1
        or element.track_number > 255  # noqa: WPS432
    ):
        raise ValueError("Track number must be between 1 and 255")
    if (
        not element.dir_number
        or element.dir_number < 0
        or element.dir_number > 99  # noqa: WPS432
    ):
        raise ValueError("Directory number must be between 0 and 99")
