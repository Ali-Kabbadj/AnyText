import customtkinter as ctk
from .ui.main_window import MainWindow


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Local Repo to Text")
        self.geometry("1200x900")

        self.minsize(width=800, height=600)

        self.main_window = MainWindow(self)
        self.main_window.pack(side="top", fill="both", expand=True)
