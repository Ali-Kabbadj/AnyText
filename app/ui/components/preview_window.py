import customtkinter as ctk


class PreviewWindow(ctk.CTkToplevel):
    def __init__(self, parent, content_to_display: str):
        super().__init__(parent)

        self.title("Output Preview")
        self.geometry("900x700")

        self.transient(self.master.winfo_toplevel())
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        textbox = ctk.CTkTextbox(self, corner_radius=0)
        textbox.grid(row=0, column=0, sticky="nsew")

        textbox.configure(
            fg_color="#000000",
            bg_color="#000000",
            text_color="#FFFFFF",
            border_color="#000000",
        )

        textbox.insert("1.0", content_to_display)
        textbox.configure(state="disabled")

        self.protocol("WM_DELETE_WINDOW", self.destroy)
