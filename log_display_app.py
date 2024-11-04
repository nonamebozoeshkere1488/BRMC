import json
from datetime import datetime
import customtkinter as ctk
from log_monitor import LogMonitor


class LogDisplayApp:
    def __init__(self, root, log_file_path):
        self.root = root
        self.root.title("Buckshot Roulette Multiplayer Cheat")
        self.root.geometry("600x125")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.sequence_text = ctk.CTkTextbox(
            root, height=50, width=600, state="disabled"
        )
        self.sequence_text.pack(pady=10)

        self.current_shell_text = ctk.CTkTextbox(
            root, height=40, width=600, state="disabled"
        )
        self.current_shell_text.pack(pady=10)

        self.monitor = LogMonitor(log_file_path, self.parse_log_line)
        self.monitor.start()

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def parse_log_line(self, line):
        try:
            start = line.index("{")
            json_data = json.loads(line[start:])
            timestamp = self.get_current_timestamp()

            if "sequence_in_shotgun" in json_data:
                sequence = json_data["sequence_in_shotgun"]
                sequence_str = ", ".join(
                    "Live" if shell == "live" else "Blank" for shell in sequence
                )
                self.update_text_widget(
                    self.sequence_text, f"{timestamp} - Sequence: {sequence_str}"
                )

            if "current_shell_in_chamber" in json_data:
                shell = json_data["current_shell_in_chamber"]
                shell_str = "Live" if shell == "live" else "Blank"
                self.update_text_widget(
                    self.current_shell_text, f"{timestamp} - Current shell: {shell_str}"
                )

        except (ValueError, json.JSONDecodeError):
            pass

    @staticmethod
    def get_current_timestamp():
        return datetime.now().strftime("[%H:%M:%S]")

    @staticmethod
    def update_text_widget(widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", ctk.END)
        widget.insert(ctk.END, text)
        widget.configure(state="disabled")

    def on_closing(self):
        self.monitor.stop()
        self.root.destroy()
