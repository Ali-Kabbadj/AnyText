import customtkinter as ctk
import os
import tkinter as tk
from ...core.state import AppState
from .loading_spinner import LoadingSpinner


class FilterPanel(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        app_state: AppState,
        title: str,
        get_items_func,
        update_func,
        is_selected_func,
    ):
        super().__init__(parent, fg_color="#000000", corner_radius=10)
        self.app_state = app_state
        self.title = title
        self.get_items_func = get_items_func
        self.update_func = update_func
        self.is_selected_func = is_selected_func

        self.app_state.register_on_change(self._update_checkbox_states)
        self.checkbox_widgets = {}
        self.loading_spinner: LoadingSpinner | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_widgets()

    def _create_widgets(self):
        ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, sticky="w", padx=10, pady=(5, 0)
        )
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    def show_loading(self):
        self._clear_all_content()
        if self.loading_spinner is None or not self.loading_spinner.winfo_exists():
            self.loading_spinner = LoadingSpinner(self.scroll_frame)
            self.loading_spinner.pack(pady=40, expand=True)
            self.loading_spinner.start()

    def hide_loading_and_rebuild(self):
        if self.loading_spinner and self.loading_spinner.winfo_exists():
            self.loading_spinner.stop()
            self.loading_spinner = None
        self._rebuild_checkboxes()

    def _clear_all_content(self):
        for _, widget in self.checkbox_widgets.values():
            widget.destroy()
        self.checkbox_widgets.clear()

    def _rebuild_checkboxes(self):
        self._clear_all_content()
        items = self.get_items_func().items()

        for item_name, count in items:
            display_name = item_name if item_name != "" else "(No Extension)"
            var = ctk.BooleanVar(value=True)
            cb = ctk.CTkCheckBox(
                self.scroll_frame,
                text=f"{display_name} ({count})",
                variable=var,
                command=lambda name=item_name, v=var: self.update_func(name, v.get()),
                checkbox_width=18,
                checkbox_height=18,
            )
            cb.pack(anchor="w", fill="x", expand=True, padx=5, pady=2)
            self.checkbox_widgets[item_name] = (var, cb)

    def _update_checkbox_states(self):
        for item_name, (var, widget) in self.checkbox_widgets.items():
            if widget.winfo_exists():
                is_checked = self.is_selected_func(item_name)
                if var.get() != is_checked:
                    var.set(is_checked)
