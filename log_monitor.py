import json
import time
import threading
import os


class LogMonitor:
    def __init__(self, log_file_path, callback):
        self.log_file_path = log_file_path
        self.callback = callback
        self.last_position = 0
        self.monitoring = False

    def start(self):
        self.monitoring = True
        monitor_thread = threading.Thread(target=self._monitor_log_file, daemon=True)
        monitor_thread.start()

    def stop(self):
        self.monitoring = False
        self._delete_log_file()

    def _monitor_log_file(self):
        while self.monitoring:
            try:
                with open(self.log_file_path, "r") as file:
                    file.seek(self.last_position)
                    new_lines = file.readlines()
                    self.last_position = file.tell()

                    for line in new_lines:
                        self.callback(line)

                time.sleep(1)
            except FileNotFoundError:
                time.sleep(1)

    def _delete_log_file(self):
        try:
            if os.path.exists(self.log_file_path):
                os.remove(self.log_file_path)
        except Exception as e:
            print(f"Failed to delete log file: {e}")
