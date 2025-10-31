import customtkinter as ctk
import threading
import winsound
from ...core.utils import resource_path


class Notification(ctk.CTkToplevel):
    def __init__(self, parent, message: str, duration: int = 2500):
        super().__init__(parent)
        self.duration = duration

        self.overrideredirect(True)

        self.container = ctk.CTkFrame(
            self,
            bg_color="#000000",
            fg_color="#2b2b2b",
            border_color="#3a7ebf",
            border_width=1,
            corner_radius=10,
            
        )
        self.container.pack(fill="both", expand=True)

        self.label = ctk.CTkLabel(self.container, text=message, text_color="gray90")
        self.label.pack(padx=20, pady=10)

        self.alpha = 0.0
        self.attributes("-alpha", self.alpha)

    def _play_sound(self):
        try:
            sound_path = resource_path("app/ui/assets/notification.wav")
            winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)
            print(f"Could not play custom notification sound: {e}")

    def show(self):
        sound_thread = threading.Thread(target=self._play_sound, daemon=True)
        sound_thread.start()

        parent_x = self.master.winfo_x()
        parent_y = self.master.winfo_y()
        parent_width = self.master.winfo_width()

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()

        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_width // 2) - (height // 2)

        self.geometry(f"+{x}+{y}")
        self.lift()
        self._fade_in()

    def _fade_in(self):
        if self.alpha < 1.0:
            self.alpha = min(self.alpha + 0.1, 1.0)
            self.attributes("-alpha", self.alpha)
            self.after(15, self._fade_in)
        else:
            self.after(self.duration, self._fade_out)

    def _fade_out(self):
        if self.alpha > 0.0:
            self.alpha = max(self.alpha - 0.1, 0.0)
            self.attributes("-alpha", self.alpha)
            self.after(15, self._fade_out)
        else:
            self.destroy()
