import os
import re

from src.repository.source_cleaner_interface import SdCardCleanerInterface


class SdCardCleaner(SdCardCleanerInterface):
    def get_unwanted_root_dir_entries(  # noqa: WPS231
        self,
        sd_root_path: str,
    ) -> list[str]:
        entries = os.listdir(sd_root_path)
        errors = []
        for entry in entries:
            if os.path.isfile(entry):
                errors.append(entry)
            elif entry in {"mp3", "advertisment"}:
                continue
            elif not re.match(r"^\d{2}\..*$", entry):
                errors.append(entry)
        return errors
