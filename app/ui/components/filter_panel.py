import customtkinter as ctk
import os
from PIL import Image

from app.core.state import AppState
from app.core.utils import resource_path


class FilterListItem(ctk.CTkFrame):
    def __init__(self, parent, item_name, count, command, initial_state):
        super().__init__(parent, fg_color="transparent", corner_radius=6)

        self.assets = {
            "checked": ctk.CTkImage(
                Image.open(resource_path("app/ui/assets/checkbox_checked.png")),
                size=(20, 20),
            ),
            "unchecked": ctk.CTkImage(
                Image.open(resource_path("app/ui/assets/checkbox_unchecked.png")),
                size=(20, 20),
            ),
            "indeterminate": ctk.CTkImage(
                Image.open(resource_path("app/ui/assets/checkbox_indeterminate.png")),
                size=(20, 20),
            ),
        }
        self.item_name = item_name
        self.command = command
        self.state = initial_state
        self.grid_columnconfigure(2, weight=1)
        self.checkbox_button = ctk.CTkButton(
            self,
            text="",
            width=24,
            height=24,
            fg_color="transparent",
            hover=False,
            image=self._get_image_for_state(),
            command=self.toggle,
        )
        self.checkbox_button.grid(row=0, column=0, sticky="w", padx=(10, 5), pady=5)
        display_name = item_name if item_name != "" else "(No Extension)"
        self.name_label = ctk.CTkLabel(
            self, text=display_name, text_color="#FFFFFF", anchor="w"
        )
        self.name_label.grid(row=0, column=1, sticky="w")
        self.count_label = ctk.CTkLabel(
            self, text=str(count), text_color="gray60", anchor="e"
        )
        self.count_label.grid(row=0, column=3, sticky="e", padx=(0, 10), pady=5)
        for widget in [self, self.name_label, self.count_label]:
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-1>", self._on_click)

    def _get_image_for_state(self):
        if self.state == 1:
            return self.assets["checked"]
        elif self.state == 2:
            return self.assets["indeterminate"]
        else:
            return self.assets["unchecked"]

    def toggle(self):
        new_state_bool = self.state != 1
        self.command(self.item_name, new_state_bool)

    def set_state(self, state: int):
        if self.state != state:
            self.state = state
            self.checkbox_button.configure(image=self._get_image_for_state())

    def _on_enter(self, event=None):
        self.configure(fg_color="#202020")

    def _on_leave(self, event=None):
        self.configure(fg_color="transparent")

    def _on_click(self, event=None):
        self.toggle()


class FilterPanel(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        app_state: AppState,
        title: str,
        get_items_func,
        update_func,
        get_item_state_func,
    ):
        super().__init__(parent, fg_color="#000000", corner_radius=10)
        self.app_state = app_state
        self.title = title
        self.get_items_func = get_items_func
        self.update_func = update_func
        self.get_item_state_func = get_item_state_func

        self.app_state.register_on_change(self._update_checkbox_states)
        self.list_items = {}
        self._is_rebuilding = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._create_widgets()

    def _create_widgets(self):
        ctk.CTkLabel(
            self,
            text=self.title,
            font=ctk.CTkFont(weight="bold"),
            text_color="#FFFFFF",
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(5, 0))
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    def show_loading(self):
        self._clear_all_content()

        loading_label = ctk.CTkLabel(
            self.scroll_frame,
            text="Loading...",
            font=ctk.CTkFont(size=16),
            text_color="gray60",
        )

        self.scroll_frame.update_idletasks()
        loading_label.update_idletasks()

        panel_height = self.scroll_frame.winfo_height()
        label_height = loading_label.winfo_height()

        spacer_height = (panel_height / 2) - (label_height / 2)
        spacer_height = max(0, spacer_height)

        ctk.CTkFrame(
            self.scroll_frame, fg_color="transparent", height=int(spacer_height)
        ).pack()
        loading_label.pack()

    def hide_loading_and_rebuild(self):
        self._rebuild_list()

    def _clear_all_content(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.list_items.clear()

    def _rebuild_list(self):
        self._is_rebuilding = True
        try:
            self._clear_all_content()
            items = self.get_items_func().items()
            for item_name, count in items:
                initial_state = self.get_item_state_func(item_name)
                list_item = FilterListItem(
                    parent=self.scroll_frame,
                    item_name=item_name,
                    count=count,
                    command=self.update_func,
                    initial_state=initial_state,
                )
                list_item.pack(fill="x", padx=2, pady=1)
                self.list_items[item_name] = list_item
        finally:
            self._is_rebuilding = False

    def _update_checkbox_states(self):
        if self._is_rebuilding:
            return
        for item_name, list_item_widget in self.list_items.items():
            if list_item_widget.winfo_exists():
                state = self.get_item_state_func(item_name)
                list_item_widget.set_state(state)
