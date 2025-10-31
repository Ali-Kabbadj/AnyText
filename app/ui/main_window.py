import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import threading
from PIL import Image

from app.ui.components.filter_panel import FilterPanel
from ..core.state import AppState
from ..core.generator import generate_output
from ..core.tokenizer import estimate_tokens
from ..core.utils import resource_path
from ..core.scanner import scan_directory
from .components.file_tree import FileTree
from .components.save_dialog import SaveDialog
from .components.preview_window import PreviewWindow
from .components.notification import Notification


class MainWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.app_state = AppState()
        self.output_content = ""
        self.preview_window: PreviewWindow | None = None

        self.generate_button: ctk.CTkButton | None = None
        self.copy_button: ctk.CTkButton | None = None
        self.save_button: ctk.CTkButton | None = None
        self.preview_button: ctk.CTkButton | None = None
        self.stats_frame: ctk.CTkFrame | None = None
        self.file_tree: FileTree | None = None
        self.extension_filter_panel: FilterPanel | None = None
        self.generic_filter_panel: FilterPanel | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=0)
        title_group_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_group_frame.grid(row=0, column=0)
        try:
            logo_path = resource_path("assets/logo.png")
            logo_image = ctk.CTkImage(Image.open(logo_path), size=(48, 48))
            logo_label = ctk.CTkLabel(title_group_frame, image=logo_image, text="")
            logo_label.grid(row=0, column=0, padx=(0, 15))
        except Exception as e:
            print(f"Could not load logo image: {e}")
        title_font = ctk.CTkFont(family="Roboto", size=28, weight="bold")
        title_label = ctk.CTkLabel(title_group_frame, text="ANYTEXT", font=title_font)
        title_label.grid(row=0, column=1)

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        left_container = ctk.CTkFrame(main_frame, fg_color="transparent", width=300)
        left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left_container.grid_propagate(False)
        left_container.grid_rowconfigure(1, weight=1)
        left_container.grid_rowconfigure(2, weight=1)
        left_container.grid_columnconfigure(0, weight=1)

        select_folder_btn = ctk.CTkButton(
            left_container, text="Select Project Folder", command=self.on_select_folder
        )
        select_folder_btn.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.extension_filter_panel = FilterPanel(
            parent=left_container,
            app_state=self.app_state,
            title="Filter by Extension",
            get_items_func=lambda: self.app_state.file_extensions,
            update_func=self.app_state.update_selection_by_extension,
            get_item_state_func=self._get_extension_filter_state,
        )
        self.extension_filter_panel.grid(row=1, column=0, sticky="nsew", pady=(0, 5))

        self.generic_filter_panel = FilterPanel(
            parent=left_container,
            app_state=self.app_state,
            title="Filter Generic Files",
            get_items_func=lambda: self.app_state.generic_files,
            update_func=self.app_state.update_selection_by_generic_name,
            get_item_state_func=self._get_generic_filter_state,
        )
        self.generic_filter_panel.grid(row=2, column=0, sticky="nsew", pady=(5, 0))

        tree_container_frame = ctk.CTkFrame(main_frame, fg_color="#000000")
        tree_container_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        tree_container_frame.grid_rowconfigure(1, weight=1)
        tree_container_frame.grid_columnconfigure(0, weight=1)

        tree_title_label = ctk.CTkLabel(
            tree_container_frame,
            text="Project Structure",
            font=ctk.CTkFont(weight="bold"),
            text_color="#FFFFFF",
        )
        tree_title_label.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 0))

        self.file_tree = FileTree(tree_container_frame, self.app_state)
        self.file_tree.grid(row=1, column=0, sticky="nsew")

        actions_area_container = ctk.CTkFrame(
            self, fg_color="#000000", corner_radius=10
        )
        actions_area_container.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        actions_area_container.grid_columnconfigure(0, weight=1)

        self.stats_frame = ctk.CTkFrame(actions_area_container, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.stats_frame.grid_columnconfigure(0, weight=1)
        self._clear_stats_display()

        button_frame = ctk.CTkFrame(actions_area_container, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.generate_button = ctk.CTkButton(
            button_frame, text="Generate", state="disabled", command=self.on_generate
        )
        self.generate_button.grid(
            row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10)
        )
        self.copy_button = ctk.CTkButton(
            button_frame,
            text="Copy to Clipboard",
            state="disabled",
            command=self.on_copy,
        )
        self.copy_button.grid(row=1, column=0, sticky="ew", padx=(0, 5))
        self.save_button = ctk.CTkButton(
            button_frame, text="Save to File", state="disabled", command=self.on_save
        )
        self.save_button.grid(row=1, column=1, sticky="ew", padx=5)
        self.preview_button = ctk.CTkButton(
            button_frame,
            text="Preview Output",
            state="disabled",
            command=self.on_preview,
        )
        self.preview_button.grid(row=1, column=2, sticky="ew", padx=(5, 0))

    def on_select_folder(self):
        path = filedialog.askdirectory(title="Select a Project Folder")
        if not path:
            return

        self.output_content = ""
        if self.preview_window and self.preview_window.winfo_exists():
            self.preview_window.destroy()
            self.preview_window = None
        self._clear_stats_display()

        if self.extension_filter_panel:
            self.extension_filter_panel.show_loading()
        if self.generic_filter_panel:
            self.generic_filter_panel.show_loading()
        if self.file_tree:
            self.file_tree.show_loading()

        self.update_idletasks()

        def heavy_load_task():
            scan_data = scan_directory(path)

            def on_done():
                self.app_state.root_path = path
                self.app_state.all_files = scan_data["all_files"]
                self.app_state.tree_structure = scan_data["tree"]
                self.app_state.file_extensions = scan_data["extensions"]
                self.app_state.generic_files = scan_data["generic_files"]
                self.app_state.selected_files = set(self.app_state.all_files)
                self.app_state._build_directory_contents_cache()

                if self.extension_filter_panel:
                    self.extension_filter_panel.hide_loading_and_rebuild()
                if self.generic_filter_panel:
                    self.generic_filter_panel.hide_loading_and_rebuild()
                if self.file_tree:
                    self.file_tree.hide_loading_and_rebuild()

                if not self.app_state.all_files:
                    dialog = ctk.CTkToplevel(self)
                    dialog.title("No Files Found")
                    dialog.geometry("350x120")
                    dialog.transient(self.winfo_toplevel())
                    dialog.grab_set()
                    label = ctk.CTkLabel(
                        dialog,
                        text="The selected folder contains no valid files to process.",
                    )
                    label.pack(padx=20, pady=20, expand=True)
                    close_button = ctk.CTkButton(
                        dialog, text="Close", command=dialog.destroy
                    )
                    close_button.pack(padx=20, pady=(0, 20), side="bottom")
                self._update_button_states()

            self.after(0, on_done)

        threading.Thread(target=heavy_load_task, daemon=True).start()

    def _get_extension_filter_state(self, ext: str) -> int:
        ext_lower = ext.lower()
        if ext_lower == "":
            total_files = [
                f for f in self.app_state.all_files if os.path.splitext(f)[1] == ""
            ]
            selected_files = [
                f for f in self.app_state.selected_files if os.path.splitext(f)[1] == ""
            ]
        else:
            total_files = [
                f for f in self.app_state.all_files if f.lower().endswith(ext_lower)
            ]
            selected_files = [
                f
                for f in self.app_state.selected_files
                if f.lower().endswith(ext_lower)
            ]
        if not total_files:
            return 0
        selected_count = len(selected_files)
        total_count = len(total_files)
        if selected_count == 0:
            return 0
        elif selected_count == total_count:
            return 1
        else:
            return 2

    def _get_generic_filter_state(self, filename: str) -> int:
        filename_lower = filename.lower()
        total_files = [
            f
            for f in self.app_state.all_files
            if os.path.basename(f).lower() == filename_lower
        ]
        selected_files = [
            f
            for f in self.app_state.selected_files
            if os.path.basename(f).lower() == filename_lower
        ]
        if not total_files:
            return 0
        selected_count = len(selected_files)
        total_count = len(total_files)
        if selected_count == 0:
            return 0
        elif selected_count == total_count:
            return 1
        else:
            return 2

    def _update_button_states(self):
        has_content = bool(self.output_content)
        has_project = bool(self.app_state.root_path)
        if self.generate_button:
            self.generate_button.configure(
                state="normal" if has_project else "disabled"
            )
        if self.copy_button:
            self.copy_button.configure(state="normal" if has_content else "disabled")
        if self.save_button:
            self.save_button.configure(state="normal" if has_content else "disabled")
        if self.preview_button:
            self.preview_button.configure(state="normal" if has_content else "disabled")

    def _clear_stats_display(self):
        if not self.stats_frame:
            return
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        label = ctk.CTkLabel(
            self.stats_frame,
            text="Select a project folder to begin.",
            text_color="gray60",
        )
        label.grid(row=0, column=0, sticky="nsew")

    def _update_stats_display(self):
        if not self.stats_frame:
            return
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        self.stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        files = len(self.app_state.selected_files)
        lines = len(self.output_content.splitlines())
        chars = len(self.output_content)
        tokens = estimate_tokens(self.output_content)
        stats = {
            "Selected Files": f"{files:,}",
            "Total Lines": f"{lines:,}",
            "Characters": f"{chars:,}",
            "Est. Tokens": f"{tokens:,}",
        }
        col = 0
        for name, value in stats.items():
            name_label = ctk.CTkLabel(
                self.stats_frame,
                text=name,
                text_color="gray60",
                font=ctk.CTkFont(size=12),
            )
            name_label.grid(row=0, column=col, sticky="s", padx=10)
            value_label = ctk.CTkLabel(
                self.stats_frame,
                text=value,
                text_color="#FFFFFF",
                font=ctk.CTkFont(size=16, weight="bold"),
            )
            value_label.grid(row=1, column=col, sticky="n", padx=10)
            col += 1

    def on_generate(self):
        if not self.app_state.root_path or not self.generate_button:
            return
        self.generate_button.configure(state="disabled", text="Generating...")
        root_path = self.app_state.root_path

        def generation_task():
            self.output_content = generate_output(
                root_path, self.app_state.selected_files
            )
            self._update_stats_display()
            if self.generate_button:
                self.generate_button.configure(state="normal", text="Generate")
            self._update_button_states()
            line_count = len(self.output_content.splitlines())
            Notification(
                self.winfo_toplevel(), f"Generation Complete! ({line_count:,} lines)"
            ).show()

        self.after(100, generation_task)

    def on_preview(self):
        if not self.output_content:
            return
        if self.preview_window is None or not self.preview_window.winfo_exists():
            self.preview_window = PreviewWindow(self, self.output_content)
        else:
            self.preview_window.focus()

    def on_copy(self):
        if not self.output_content or not self.copy_button:
            return
        self.clipboard_clear()
        self.clipboard_append(self.output_content)
        Notification(self.winfo_toplevel(), "Copied to clipboard!").show()

    def on_save(self):
        if not self.app_state.root_path:
            return
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        default_filename = f"{os.path.basename(self.app_state.root_path)}.txt"
        SaveDialog(
            self,
            default_filename,
            desktop_path,
            self.output_content,
            self.winfo_toplevel(),
        )
