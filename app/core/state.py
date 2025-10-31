import os
from .scanner import scan_directory


class AppState:
    def __init__(self):
        self.root_path = None
        self.all_files = []
        self.selected_files = set()

        self.tree_structure = {}
        self.file_extensions = {}
        self.generic_files = {}

        self.directory_contents = {}

        self.on_state_change_callbacks = []

    def register_on_change(self, callback):
        self.on_state_change_callbacks.append(callback)

    def _notify_observers(self):
        for callback in self.on_state_change_callbacks:
            callback()

    def set_project_path(self, path, notify=True):
        if not os.path.isdir(path):
            print(f"Error: Path is not a valid directory: {path}")
            return

        self.root_path = path
        scan_data = scan_directory(path)

        self.all_files = scan_data["all_files"]
        self.tree_structure = scan_data["tree"]
        self.file_extensions = scan_data["extensions"]
        self.generic_files = scan_data["generic_files"]
        self.selected_files = set(self.all_files)

        self._build_directory_contents_cache()
        if notify:
            self._notify_observers()

    def _build_directory_contents_cache(self):
        self.directory_contents.clear()
        if not self.root_path:
            return

        for file_path in self.all_files:
            parent = os.path.dirname(file_path)
            while parent != self.root_path and parent not in self.directory_contents:
                self.directory_contents[parent] = set()
                parent = os.path.dirname(parent)
        if self.root_path not in self.directory_contents:
            self.directory_contents[self.root_path] = set()

        for dir_path in self.directory_contents:
            self.directory_contents[dir_path] = {
                f for f in self.all_files if f.startswith(dir_path + os.sep)
            }
        self.directory_contents[self.root_path] = set(self.all_files)

    def update_selection(self, file_path, is_selected, notify=True):
        if is_selected:
            self.selected_files.add(file_path)
        else:
            self.selected_files.discard(file_path)

        if notify:
            self._notify_observers()

    def update_selection_by_extension(self, extension, is_selected):
        extension_lower = extension.lower()
        if extension_lower == "":
            files_to_update = [
                f for f in self.all_files if os.path.splitext(f)[1] == ""
            ]
        else:
            files_to_update = [
                f for f in self.all_files if f.lower().endswith(extension_lower)
            ]

        for file_path in files_to_update:
            self.update_selection(file_path, is_selected, notify=False)
        self._notify_observers()

    def update_selection_by_generic_name(self, filename, is_selected):
        filename_lower = filename.lower()
        for file_path in self.all_files:
            if os.path.basename(file_path).lower() == filename_lower:
                self.update_selection(file_path, is_selected, notify=False)
        self._notify_observers()

    def update_selection_by_path(self, path, is_selected):
        if path in self.directory_contents:
            for file_path in self.directory_contents[path]:
                self.update_selection(file_path, is_selected, notify=False)
        else:
            self.update_selection(path, is_selected, notify=False)
        self._notify_observers()
