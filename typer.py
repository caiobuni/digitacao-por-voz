import time
import ctypes
import logging
from ctypes import wintypes

logger = logging.getLogger(__name__)

INPUT_KEYBOARD = 1
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_KEYUP = 0x0002

user32 = ctypes.WinDLL("user32", use_last_error=True)


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]


class INPUTUNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]


class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("u", INPUTUNION),
    ]


def _send_unicode_key(code, flags):
    inp = INPUT()
    inp.type = INPUT_KEYBOARD
    inp.ki.wVk = 0
    inp.ki.wScan = code
    inp.ki.dwFlags = flags
    inp.ki.time = 0
    inp.ki.dwExtraInfo = None
    sent = user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
    if sent != 1:
        logger.error(f"SendInput failed with code {ctypes.get_last_error()}")
        return False
    return True


class TextOut:
    def __init__(self, char_delay=0.03, key_press_delay=0.01):
        self.char_delay = char_delay
        self.key_press_delay = key_press_delay

    def insert_text(self, text):
        if not text:
            return
        for char in text:
            if char == '\n':
                char = '\r'
            code = ord(char)
            if not _send_unicode_key(code, KEYEVENTF_UNICODE):
                return
            time.sleep(self.key_press_delay)
            _send_unicode_key(code, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP)
            time.sleep(self.char_delay)


if __name__ == "__main__":
    t = TextOut()
    print("Will type in 2 seconds...")
    time.sleep(2)
    t.insert_text("Olá Mundo do Verbatim!")
