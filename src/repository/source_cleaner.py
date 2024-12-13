import os
import re

from src.repository.source_cleaner_interface import SourceCleanerInterface


class SdCardCleaner(SourceCleanerInterface):
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
            elif not re.match(r"^\d{2}$", entry):
                errors.append(entry)
        return errors

    def delete_unwanted_root_dir_entries(self, sd_root_path) -> None:
        unwanted_entries = self.get_unwanted_root_dir_entries(sd_root_path)
        for file_path in unwanted_entries:
            self._delete_entry(file_path)

    def _delete_entry(self, file_path: str) -> None:
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            self._delete_directory(file_path)

    def _delete_directory(self, dir_path: str) -> None:
        if os.listdir(dir_path):
            self._delete_directory_contents(dir_path)
        os.rmdir(dir_path)

    def _delete_directory_contents(self, dir_path: str) -> None:
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for dir_name in dirs:
                os.rmdir(os.path.join(root, dir_name))

    def get_root_dir_numbering_gaps(self, sd_root_path: str) -> list[int]:
        entries = os.listdir(sd_root_path)
        gaps = []
        numbers = []
        for entry in entries:
            if re.match(r"^\d{2}$", entry):
                numbers.append(int(entry))
        numbers.sort()
        # Get the highest number in the list, then get the range from 1 to that number
        for expected_number in range(1, numbers[-1]):
            if expected_number not in numbers:
                gaps.append(expected_number)

        return gaps

    def get_subdir_numbering_gaps(self, sd_root_path: str) -> list[tuple[int, int]]:
        entries = os.listdir(sd_root_path)
        gaps = []
        subdir = []
        for entry in entries:
            if re.match(r"^\d{2}$", entry):
                subdir.append(entry)
        subdir.sort()

        for sub_dir in subdir:
            sub_dir_path = os.path.join(sd_root_path, sub_dir)
            files = os.listdir(sub_dir_path)
            numbers = []
            for numbered_file in files:
                if re.match(r"^\d{3}$", numbered_file):
                    numbers.append(int(numbered_file))
            numbers.sort()
            for expected_number in range(1, numbers[-1]):
                if expected_number not in numbers:
                    gaps.append((int(sub_dir), expected_number))

        return gaps
