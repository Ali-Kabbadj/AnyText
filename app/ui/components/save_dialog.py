import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import sys
import subprocess


class SaveDialog(ctk.CTkToplevel):
    def __init__(
        self,
        parent,
        default_filename: str,
        default_path: str,
        content_to_save: str,
        toplevel_parent,
    ):
        super().__init__(parent)
        self.content_to_save = content_to_save
        self.toplevel_parent = toplevel_parent

        self.title("Save Output")
        self.geometry("500x200")
        self.transient(self.toplevel_parent)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="File Name:").grid(
            row=0, column=0, padx=20, pady=(10, 0), sticky="w"
        )
        self.filename_var = tk.StringVar(value=default_filename)
        filename_entry = ctk.CTkEntry(self, textvariable=self.filename_var)
        filename_entry.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        ctk.CTkLabel(self, text="Save Location:").grid(
            row=2, column=0, padx=20, pady=(10, 0), sticky="w"
        )
        path_frame = ctk.CTkFrame(self, fg_color="transparent")
        path_frame.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        path_frame.grid_columnconfigure(0, weight=1)

        self.path_var = tk.StringVar(value=default_path)
        path_entry = ctk.CTkEntry(
            path_frame, textvariable=self.path_var, state="disabled"
        )
        path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        browse_button = ctk.CTkButton(
            path_frame, text="Browse...", command=self._browse_path
        )
        browse_button.grid(row=0, column=1, sticky="e")

        save_button_dialog = ctk.CTkButton(
            self, text="Save", command=self._perform_save
        )
        save_button_dialog.grid(row=4, column=0, padx=20, pady=(15, 10), sticky="se")

    def _browse_path(self):
        path = filedialog.askdirectory(initialdir=self.path_var.get())
        if path:
            self.path_var.set(path)

    def _open_file_location(self, file_path: str):
        try:
            abs_path = os.path.abspath(file_path)
            if sys.platform == "win32":
                subprocess.Popen(["explorer", "/select,", os.path.normpath(abs_path)])
            elif sys.platform == "darwin":
                subprocess.Popen(["open", "-R", abs_path])
            else:
                subprocess.Popen(["xdg-open", os.path.dirname(abs_path)])
        except Exception as e:
            print(f"Could not open file location: {e}")

    def _perform_save(self):
        save_path = os.path.join(self.path_var.get(), self.filename_var.get())
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(self.content_to_save)

            self._open_file_location(save_path)
            self.after(10, self.destroy)
        except Exception as e:
            print(f"Error saving file: {e}")
