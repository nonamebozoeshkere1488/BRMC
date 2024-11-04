import customtkinter as ctk
import os
from log_display_app import LogDisplayApp


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    log_file_path = os.path.join(
        os.getenv("APPDATA"),
        "Godot",
        "app_userdata",
        "Buckshot Roulette",
        "logs",
        "godot.log",
    )

    app = LogDisplayApp(root, log_file_path)
    root.mainloop()
