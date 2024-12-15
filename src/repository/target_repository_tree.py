import os
import re

from src.repository.repository_tree_interface import RepositoryTreeInterface


class TargetRepositoryTree(RepositoryTreeInterface):

    def get_target_tree(self, root_dir: str) -> list[str]:
        return os.listdir(root_dir)  # Fake implementation

    def get_valid_subdirs(self, root_dir: str, pattern: str) -> list[str]:
        subdirs = [
            entry
            for entry in os.listdir(root_dir)
            if re.match(pattern, entry) and os.path.isdir(os.path.join(root_dir, entry))
        ]
        subdirs.sort()
        return subdirs
