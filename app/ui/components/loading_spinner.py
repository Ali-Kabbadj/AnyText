import customtkinter as ctk
import math


class LoadingSpinner(ctk.CTkFrame):
    def __init__(self, parent, size=60, color="#3a7ebf", thickness=6):
        super().__init__(parent, fg_color="transparent")
        self.size = size
        self.color = color
        self.thickness = thickness
        self.hiding = False

        self.canvas = ctk.CTkCanvas(
            self, width=self.size, height=self.size, bg="#000000", highlightthickness=0
        )
        self.canvas.pack(expand=True)

        self.start_angle = 0
        self.arc_id = None

    def start(self):
        self.hiding = False
        self.start_angle = 0
        self._animate()

    def stop(self):
        self.hiding = True

    def _animate(self):
        if self.hiding:
            self.destroy()
            return

        if self.arc_id:
            self.canvas.delete(self.arc_id)

        self.arc_id = self.canvas.create_arc(
            self.thickness // 2,
            self.thickness // 2,
            self.size - self.thickness // 2,
            self.size - self.thickness // 2,
            start=self.start_angle,
            extent=270,
            style=ctk.ARC,
            outline=self.color,
            width=self.thickness,
        )

        self.start_angle = (self.start_angle - 15) % 360
        self.after(30, self._animate)
