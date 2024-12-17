# - Create Delta List
# What would be done?
# also identify gaps, unwanted files and foldersks

# - Write to SD Card
# Check if unwanted files exist on the SD card and warn the user
# Check if Gaps exist in the root directory and subdirs and warn the user
# Check if file needs to be written to SD card
# Check if file exists on SD card (function needs foldernumber / file number)
# Check if file is the same (hash of content) on the SD card
# check tags (function needs tags, foldernumber / file number)
# 1. Write a file to the SD card with
# if anything was written, call sort_fat_root


# - check root for unwanted files
# check if file is in the root
# check if file is in a subdirectory

# create a cli interface that first reads command line arguments handles defaults and mandatory arguments.
# It also prints a help text explaining the cli parameters. Two arguments are: source-folder (default = .)
# and target-folder (mandatory).

from typing import Optional

from src.config.configuration import Configuration
from src.dfplayer_card_manager_interface import DfPlayerCardManagerInterface
from src.mp3.audio_file_manager_interface import AudioFileManagerInterface
from src.repository import repository_finder


class DfPlayerCardManager(DfPlayerCardManagerInterface):
    def __init__(self, config: Configuration, audio_manager: AudioFileManagerInterface):
        self._config = config
        self._config_overrides = config
        self._audio_manager = audio_manager

    def get_target_repository_tree(self) -> list[tuple[str, str]]:
        return repository_finder.get_repository_tree(
            self._config.repository_target.root_dir,
            self._config.repository_target.valid_subdir_pattern,
            self._config.repository_target.valid_subdir_files_pattern,
        )

    def get_source_repository_tree(
        self,
        valid_subdir_files_pattern_overrides: Optional[dict[str, str]] = None,
    ) -> list[tuple[str, str]]:
        return repository_finder.get_repository_tree(
            self._config.repository_source.root_dir,
            self._config.repository_source.valid_subdir_pattern,
            self._config.repository_source.valid_subdir_files_pattern,
            valid_subdir_files_pattern_overrides,
        )
