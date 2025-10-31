import os
from collections import defaultdict
from ..config.settings import (
    EXCLUDED_DIRS,
    EXCLUDED_EXTENSIONS,
    GENERIC_FILENAMES,
)


def _prune_empty_directories(directory: dict) -> dict:
    pruned_directory = {}
    for name, content in directory.items():
        if isinstance(content, dict): 
            pruned_content = _prune_empty_directories(content)
            if pruned_content: 
                pruned_directory[name] = pruned_content
        else: 
            pruned_directory[name] = content
    return pruned_directory


def scan_directory(root_path: str) -> dict:
    all_files = []
    tree = {}
    extensions = defaultdict(int)
    filename_counts = defaultdict(int)

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]

        relative_dir_path = os.path.relpath(dirpath, root_path)
        current_level = tree
        if relative_dir_path != ".":
            for part in relative_dir_path.split(os.sep):
                current_level = current_level.setdefault(part, {})

        sorted_filenames = sorted(filenames)
        for filename in sorted_filenames:
            filename_lower = filename.lower()
            _, ext = os.path.splitext(filename_lower)

            if ext in EXCLUDED_EXTENSIONS or filename_lower in EXCLUDED_EXTENSIONS:
                continue

            full_path = os.path.join(dirpath, filename)
            all_files.append(full_path)

            filename_counts[filename_lower] += 1
            extensions[ext] += 1
            current_level[filename] = None  

    pruned_tree = _prune_empty_directories(tree)

    generic_files_found = {}
    for generic_name in sorted(list(GENERIC_FILENAMES)):
        if generic_name in filename_counts:
            generic_files_found[generic_name] = filename_counts[generic_name]

    return {
        "all_files": sorted(all_files),
        "tree": pruned_tree,
        "extensions": dict(sorted(extensions.items())),
        "generic_files": generic_files_found,
    }
