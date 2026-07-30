import time
import logging
import win32clipboard
import win32con
from pynput.keyboard import Controller, Key

logger = logging.getLogger(__name__)

class TextOut:
    def __init__(self):
        self.keyboard = Controller()

    def _set_clipboard(self, text):
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
            win32clipboard.CloseClipboard()
            return True
        except Exception as e:
            logger.error(f"Failed to set clipboard: {e}")
            try:
                win32clipboard.CloseClipboard()
            except:
                pass
            return False

    def _get_clipboard(self):
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            return data
        except Exception as e:
            logger.error(f"Failed to get clipboard: {e}")
            try:
                win32clipboard.CloseClipboard()
            except:
                pass
            return None

    def paste_text(self, text):
        if not text:
            return

        original_content = self._get_clipboard()

        if not self._set_clipboard(text):
            logger.error("Failed to copy text to clipboard. Paste aborted.")
            return

        clipboard_ok = False
        for attempt in range(5):
            time.sleep(0.1)
            current = self._get_clipboard()
            if current == text:
                clipboard_ok = True
                break
            else:
                logger.warning(f"Clipboard verification attempt {attempt + 1}/5 failed")

        if not clipboard_ok:
            logger.error("Clipboard verification failed after 5 attempts. Paste aborted.")
            return

        time.sleep(0.3)

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
            time.sleep(0.2)
            self._set_clipboard(original_content)

if __name__ == "__main__":
    t = TextOut()
    print("Will paste 'Hello World' in 2 seconds...")
    time.sleep(2)
    t.paste_text("Olá Mundo do Verbatim!")
