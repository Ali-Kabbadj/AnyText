import customtkinter as ctk
from .ui.main_window import MainWindow
from .core.utils import resource_path

ctk.set_appearance_mode("light")
try:
    theme_path = resource_path("assets/custom_theme.json")
    ctk.set_default_color_theme(theme_path)
except Exception as e:
    print(f"Could not load custom theme: {e}")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AnyText")
        self.geometry("1200x900")

        try:
            icon_path = resource_path("assets/logo.ico")
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not load application icon: {e}")

        self.minsize(width=800, height=600)

        self.main_window = MainWindow(self)
        self.main_window.pack(side="top", fill="both", expand=True)
