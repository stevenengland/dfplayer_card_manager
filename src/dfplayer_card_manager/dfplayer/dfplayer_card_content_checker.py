import os
import re


# ToDo: Maybe refactor into checker and cleaner classes
class DfPlayerCardContentChecker:  # noqa: WPS214

    def __init__(
        self,
        valid_root_dir_pattern: str,
        valid_subdir_files_pattern: str,
        valid_subdir_files_track_number_match: int,
        root_dir_exceptions: set[str],
    ) -> None:
        self._valid_root_dir_pattern = re.compile(valid_root_dir_pattern)
        self._valid_subdir_files_pattern = re.compile(valid_subdir_files_pattern)
        self._valid_subdir_files_track_number_match = (
            valid_subdir_files_track_number_match
        )
        self._root_dir_exceptions = root_dir_exceptions

    def get_unwanted_root_dir_entries(  # noqa: WPS231
        self,
        sd_root_path: str,
    ) -> list[str]:
        entries = os.listdir(sd_root_path)
        errors = []
        for entry in entries:
            if os.path.isfile(entry):
                errors.append(entry)
            elif entry in self._root_dir_exceptions:
                continue
            elif not re.match(self._valid_root_dir_pattern, entry):
                errors.append(entry)
        return errors

    def get_unwanted_subdir_entries(self, sd_root_path: str) -> list[tuple[str, str]]:
        entries = os.listdir(sd_root_path)
        subdirs = self._get_valid_subdirs(entries)
        errors = []

        for sub_dir in subdirs:
            sub_dir_path = os.path.join(sd_root_path, sub_dir)
            files = os.listdir(sub_dir_path)
            unwanted_entries = [
                (sub_dir, dir_entry)
                for dir_entry in files
                if not re.match(self._valid_subdir_files_pattern, dir_entry)
            ]
            errors.extend(unwanted_entries)

        return errors

    # Must be handled as a warning, not an error
    def get_root_dir_numbering_gaps(self, sd_root_path: str) -> list[int]:
        entries = os.listdir(sd_root_path)
        gaps = []
        numbers = []
        for entry in entries:
            if re.match(self._valid_root_dir_pattern, entry):
                numbers.append(int(entry))
        numbers.sort()
        if not numbers:
            return []
        # Get the highest number in the list, then get the range from 1 to that number
        for expected_number in range(1, numbers[-1]):
            if expected_number not in numbers:
                gaps.append(expected_number)

        return gaps

    # Must be handled as errors
    def get_subdir_numbering_gaps(self, sd_root_path: str) -> list[tuple[int, int]]:
        entries = os.listdir(sd_root_path)
        subdirs = self._get_valid_subdirs(entries)
        gaps = []

        for sub_dir in subdirs:
            sub_dir_path = os.path.join(sd_root_path, sub_dir)
            files = os.listdir(sub_dir_path)
            gaps.extend(self._find_gaps_in_subdir(sub_dir, files))

        return gaps

    def delete_unwanted_root_dir_entries(self, sd_root_path) -> list[str]:
        unwanted_entries = self.get_unwanted_root_dir_entries(sd_root_path)
        for file_path in unwanted_entries:
            self._delete_entry(os.path.join(sd_root_path, file_path))
        return unwanted_entries

    def delete_unwanted_subdir_entries(self, sd_root_path) -> list[str]:
        entries = os.listdir(sd_root_path)
        subdirs = self._get_valid_subdirs(entries)
        deleted_entries = []
        for sub_dir in subdirs:
            sub_dir_path = os.path.join(sd_root_path, sub_dir)
            files = os.listdir(sub_dir_path)
            unwanted_entries = [
                dir_entry
                for dir_entry in files
                if not re.match(self._valid_subdir_files_pattern, dir_entry)
            ]
            for file_path in unwanted_entries:
                self._delete_entry(os.path.join(sub_dir_path, file_path))
                deleted_entries.append(os.path.join(sub_dir_path, file_path))
        return deleted_entries

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

    def _get_valid_subdirs(self, entries: list[str]) -> list[str]:
        subdirs = [
            entry for entry in entries if re.match(self._valid_root_dir_pattern, entry)
        ]
        subdirs.sort()
        return subdirs

    def _find_gaps_in_subdir(
        self,
        sub_dir: str,
        files: list[str],
    ) -> list[tuple[int, int]]:
        numbers = []
        for file_name in files:
            field_matched_text = re.search(self._valid_subdir_files_pattern, file_name)
            if field_matched_text:
                if (
                    len(field_matched_text.groups())
                    >= self._valid_subdir_files_track_number_match
                ):
                    numbers.append(
                        int(
                            field_matched_text.group(
                                self._valid_subdir_files_track_number_match,
                            ),
                        ),
                    )
        numbers.sort()
        if not numbers:
            return []
        return [
            (int(sub_dir), expected_number)
            for expected_number in range(1, numbers[-1])
            if expected_number not in numbers
        ]
