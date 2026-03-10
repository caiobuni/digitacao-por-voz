import os
from datetime import datetime

class HistoryLogger:
    def __init__(self, filename="transcriptions.md"):
        self.filename = filename

    def log(self, text):
        """Appends the given text to the history file with a timestamp."""
        if not text:
            return
        
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Check if file exists, if not, create header
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write("# Verbatim Transcription History\n\n")

        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"### {timestamp}\n")
            f.write(f"{text}\n\n")

    def open_log(self):
        """Opens the history file in the default system editor."""
        if os.path.exists(self.filename):
            os.startfile(self.filename)
        else:
            print("History file not found.")

# Manual test usage:
if __name__ == "__main__":
    l = HistoryLogger()
    l.log("Esta é uma transcrição de teste do Verbatim.")
    print("Log saved. Call open_log() to view.")
