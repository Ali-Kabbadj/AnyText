import os


def generate_output(root_path: str, selected_files: set) -> str:
    if not selected_files:
        return ""

    tree_structure = {}
    for file_path in sorted(list(selected_files)):
        relative_path = os.path.relpath(file_path, root_path)
        parts = relative_path.split(os.sep)
        current_level = tree_structure
        for part in parts[:-1]:
            current_level = current_level.setdefault(part, {})
        current_level[parts[-1]] = None

    tree_string = f"{os.path.basename(root_path)} Files Directory Structure:\n\n"

    def build_tree_string(directory, prefix=""):
        nonlocal tree_string
        items = sorted(directory.items())
        for i, (name, content) in enumerate(items):
            is_last = i == (len(items) - 1)
            tree_string += prefix
            if is_last:
                tree_string += "└── "
                next_prefix = prefix + "    "
            else:
                tree_string += "├── "
                next_prefix = prefix + "│   "
            tree_string += name + "\n"
            if isinstance(content, dict):
                build_tree_string(content, next_prefix)

    build_tree_string({".": tree_structure}, "")

    output_parts = [tree_string]
    for file_path in sorted(list(selected_files)):
        relative_path = os.path.relpath(file_path, root_path).replace("\\", "/")
        header = f"\n\n--- File : ./{relative_path} ---\n\n"
        output_parts.append(header)
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                output_parts.append(f.read())
        except Exception as e:
            output_parts.append(f"Error reading file: {e}")

    return "".join(output_parts)
