import time
import logging
import pyperclip
from pynput.keyboard import Controller, Key

logger = logging.getLogger(__name__)

class TextOut:
    def __init__(self):
        self.keyboard = Controller()

    def paste_text(self, text):
        if not text:
            return

        original_content = pyperclip.paste()

        pyperclip.copy(text)

        clipboard_ok = False
        for _ in range(3):
            time.sleep(0.05)
            try:
                if pyperclip.paste() == text:
                    clipboard_ok = True
                    break
            except Exception:
                pass

        if not clipboard_ok:
            logger.error("Clipboard verification failed after retries. Paste aborted.")
            return

        time.sleep(0.2)

        paste_success = False
        try:
            with self.keyboard.pressed(Key.ctrl):
                self.keyboard.press('v')
                self.keyboard.release('v')
            time.sleep(0.5)
            paste_success = True
        except Exception as e:
            logger.error(f"Ctrl+V failed: {e}")

        if paste_success and original_content:
            pyperclip.copy(original_content)

# Manual test usage:
if __name__ == "__main__":
    t = TextOut()
    print("Will paste 'Hello World' in 2 seconds...")
    time.sleep(2)
    t.paste_text("Olá Mundo do Verbatim!")
