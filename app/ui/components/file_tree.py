import customtkinter as ctk
import os
from PIL import Image

from app.core.state import AppState
from app.core.utils import resource_path


class TreeNode(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        text,
        path,
        is_folder,
        assets,
        on_toggle,
        on_check,
        depth,
        is_last_list,
        initial_state,
    ):
        super().__init__(parent, fg_color="#000000", height=24)
        self.path = path
        self.is_folder = is_folder
        self.assets = assets
        self.on_toggle = on_toggle
        self.on_check = on_check
        self.children_nodes = []
        self.is_expanded = False
        self.state = initial_state

        TREE_X_OFFSET = 32
        INDENT_WIDTH = 100
        HORIZONTAL_LINE_LENGTH = 25
        LINE_COLOR = "#3a7ebf"

        canvas_width = 0
        if depth > 0:
            canvas_width = (
                TREE_X_OFFSET
                + ((depth - 1) * INDENT_WIDTH)
                + (INDENT_WIDTH / 2)
                + HORIZONTAL_LINE_LENGTH
            )
        canvas = ctk.CTkCanvas(
            self, width=canvas_width, height=24, bg="#000000", highlightthickness=0
        )
        canvas.pack(side="left", fill="y")

        if depth > 0:
            for i in range(depth - 1):
                if not is_last_list[i]:
                    x = TREE_X_OFFSET + (i * INDENT_WIDTH) + (INDENT_WIDTH / 2)
                    canvas.create_line(x, 0, x, 24, fill=LINE_COLOR)
            is_last_node = is_last_list[-1]
            parent_x = TREE_X_OFFSET + ((depth - 1) * INDENT_WIDTH) + (INDENT_WIDTH / 2)
            y_mid = 12
            canvas.create_line(
                parent_x,
                y_mid,
                parent_x + HORIZONTAL_LINE_LENGTH,
                y_mid,
                fill=LINE_COLOR,
            )
            if is_last_node:
                canvas.create_line(parent_x, 0, parent_x, y_mid, fill=LINE_COLOR)
            else:
                canvas.create_line(parent_x, 0, parent_x, 24, fill=LINE_COLOR)

        image = (
            self.assets["indeterminate"]
            if self.state == 2
            else self.assets["checked"] if self.state == 1 else self.assets["unchecked"]
        )

        self.checkbox_button = ctk.CTkButton(
            self,
            text="",
            width=24,
            height=24,
            fg_color="transparent",
            hover=False,
            image=image,
            command=self._on_check_callback,
        )
        self.checkbox_button.pack(side="left", padx=2)

        if self.is_folder:
            self.toggle_button = ctk.CTkButton(
                self,
                text=f" {text}",
                fg_color="transparent",
                hover_color="#202020",
                text_color="#FFFFFF",
                anchor="w",
                image=assets["arrow_right"],
                command=self._toggle,
            )
            self.toggle_button.pack(side="left", fill="x", expand=True, padx=(2, 0))
        else:
            spacer = ctk.CTkFrame(self, width=22, height=24, fg_color="transparent")
            spacer.pack(side="left")
            self.label = ctk.CTkLabel(
                self, text=f" {text}", anchor="w", text_color="#FFFFFF"
            )
            self.label.pack(side="left", fill="x", expand=True)

    def _toggle(self):
        self.is_expanded = not self.is_expanded
        self.toggle_button.configure(
            image=(
                self.assets["arrow_down"]
                if self.is_expanded
                else self.assets["arrow_right"]
            )
        )
        self.on_toggle(self)

    def _on_check_callback(self):
        self.on_check(self.path, not bool(self.state))

    def set_check_state(self, state: int):
        if self.state == state:
            return
        self.state = state
        image = (
            self.assets["indeterminate"]
            if state == 2
            else self.assets["checked"] if state == 1 else self.assets["unchecked"]
        )
        self.checkbox_button.configure(image=image)


class FileTree(ctk.CTkScrollableFrame):
    def __init__(self, parent, app_state: AppState):
        super().__init__(parent, fg_color="#000000", label_text_color="#FFFFFF")
        self.app_state = app_state
        self.app_state.register_on_change(self._update_checkbox_states)
        self._nodes = {}
        self._load_assets()

    def show_loading(self):
        self._clear_tree()

        loading_label = ctk.CTkLabel(
            self, text="Loading...", font=ctk.CTkFont(size=18), text_color="gray60"
        )

        self.update_idletasks()
        loading_label.update_idletasks()

        panel_height = self.winfo_height()
        label_height = loading_label.winfo_height()

        spacer_height = panel_height / 2
        spacer_height = max(0, spacer_height)

        ctk.CTkFrame(self, fg_color="transparent", height=int(spacer_height)).pack()
        loading_label.pack()

    def hide_loading_and_rebuild(self):
        self._build_tree()

    def _load_assets(self):
        self.assets = {}
        assets_dir = resource_path("app/ui/assets")
        image_files = {
            "checked": "checkbox_checked.png",
            "unchecked": "checkbox_unchecked.png",
            "indeterminate": "checkbox_indeterminate.png",
            "arrow_right": "arrow_right.png",
            "arrow_down": "arrow_down.png",
        }
        for name, filename in image_files.items():
            self.assets[name] = ctk.CTkImage(
                Image.open(os.path.join(assets_dir, filename)), size=(20, 20)
            )

    def _clear_tree(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._nodes.clear()

    def _build_tree(self):
        self._clear_tree()
        if not self.app_state.root_path:
            return
        root_name = os.path.basename(self.app_state.root_path)
        self._add_nodes_recursively(
            {root_name: self.app_state.tree_structure}, self.app_state.root_path, 0, []
        )
        if self.app_state.root_path in self._nodes:
            self._nodes[self.app_state.root_path]._toggle()

    def _add_nodes_recursively(
        self, directory_dict, current_path, depth, parent_is_last_list
    ):
        items = sorted(
            directory_dict.items(),
            key=lambda item: (
                (0, item[0]) if isinstance(item[1], dict) else (1, item[0])
            ),
        )
        children = []
        for i, (name, content) in enumerate(items):
            full_path = current_path if depth == 0 else os.path.join(current_path, name)
            is_folder = isinstance(content, dict)
            is_last = i == len(items) - 1
            state = 0
            if is_folder:
                all_children = self.app_state.directory_contents.get(full_path, set())
                if all_children:
                    selected_children = all_children.intersection(
                        self.app_state.selected_files
                    )
                    if not selected_children:
                        state = 0
                    elif len(selected_children) == len(all_children):
                        state = 1
                    else:
                        state = 2
                else:
                    if full_path in self.app_state.selected_files:
                        state = 1
            else:
                if full_path in self.app_state.selected_files:
                    state = 1

            node = TreeNode(
                self,
                name,
                full_path,
                is_folder,
                self.assets,
                self._toggle_node,
                self.app_state.update_selection_by_path,
                depth + 1,
                parent_is_last_list + [is_last],
                initial_state=state,
            )
            node.pack(fill="x", expand=True, pady=0, padx=0)
            self._nodes[full_path] = node
            children.append(node)
            if is_folder:
                node.children_nodes = self._add_nodes_recursively(
                    content, full_path, depth + 1, parent_is_last_list + [is_last]
                )
                for child_node in node.children_nodes:
                    child_node.pack_forget()
        return children

    def _toggle_node(self, node):
        if not node.is_folder:
            return
        last_packed_widget = node
        for child in node.children_nodes:
            if node.is_expanded:
                child.pack(
                    fill="x", expand=True, pady=0, padx=0, after=last_packed_widget
                )
                last_packed_widget = child
            else:
                self._recursively_hide(child)

    def _recursively_hide(self, node):
        node.pack_forget()
        if node.is_folder and node.is_expanded:
            node.is_expanded = False
            node.toggle_button.configure(image=self.assets["arrow_right"])
            for child in node.children_nodes:
                self._recursively_hide(child)

    def _update_checkbox_states(self):
        for path, node in self._nodes.items():
            if not node.winfo_exists():
                continue
            state = 0
            if node.is_folder:
                all_children_files = self.app_state.directory_contents.get(path, set())
                if not all_children_files:
                    if path in self.app_state.selected_files:
                        state = 1
                else:
                    selected_children_files = all_children_files.intersection(
                        self.app_state.selected_files
                    )
                    if not selected_children_files:
                        state = 0
                    elif len(selected_children_files) == len(all_children_files):
                        state = 1
                    else:
                        state = 2
            else:
                if path in self.app_state.selected_files:
                    state = 1
            node.set_check_state(state)
