import os
import re

from src.repository.repository_element import RepositoryElement
from src.repository.repository_tree_interface import RepositoryTreeInterface


class TargetRepositoryTree(RepositoryTreeInterface):

    def get_target_tree(self, root_dir: str) -> list[str]:
        return os.listdir(root_dir)  # Fake implementation

    def get_valid_root_dirs(self, root_dir: str, valid_dir_pattern: str) -> list[str]:
        subdirs = [
            entry
            for entry in os.listdir(root_dir)
            if re.match(valid_dir_pattern, entry)
            and os.path.isdir(os.path.join(root_dir, entry))  # noqa: WPS221
        ]
        subdirs.sort()
        return subdirs

    def get_valid_subdir_files(self, subdir: str, valid_file_pattern: str) -> list[str]:
        valid_files = [
            entry
            for entry in os.listdir(subdir)
            if re.match(valid_file_pattern, entry)
            and os.path.isfile(os.path.join(subdir, entry))  # noqa: WPS221
        ]
        valid_files.sort()
        return valid_files

    def get_repository_tree(self, root_dir: str) -> list[RepositoryElement]:
        repository_tree = []
        # get valid root dirs
        valid_root_dirs = self.get_valid_root_dirs(root_dir, r"^\d{2}$")
        for valid_root_dir in valid_root_dirs:
            # get valid files in subdir
            subdir = os.path.join(root_dir, valid_root_dir)
            valid_files = self.get_valid_subdir_files(subdir, r"^\d{3}\.mp3$")
            for valid_file in valid_files:
                element = RepositoryElement()
                element.tree_id = f"{valid_root_dir}_{valid_file}"
                element.dir = valid_root_dir
                element.file_name = valid_file
                repository_tree.append(element)
        return repository_tree
