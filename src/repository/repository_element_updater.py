import re

from src.config.configuration import RepositoryConfig
from src.repository.detection_source import DetectionSource
from src.repository.repository_element import RepositoryElement


def update_element_by_dir(
    element: RepositoryElement,
    effective_config: RepositoryConfig,
) -> None:
    update_title_by_dir(element, effective_config)


def update_title_by_dir(
    element: RepositoryElement,
    effective_config: RepositoryConfig,
) -> None:
    if not effective_config.valid_subdir_pattern:
        raise ValueError("No valid subdir pattern set")
    if not effective_config.title_match or effective_config.title_match < 1:
        raise ValueError("No valid title match set")
    if effective_config.title_source == DetectionSource.dirname:
        title_matched_text = re.search(
            effective_config.valid_subdir_pattern,
            element.dir,
        )
        if title_matched_text:
            if len(title_matched_text.groups()) < effective_config.title_match:
                return
            element.title = title_matched_text.group(effective_config.title_match)
