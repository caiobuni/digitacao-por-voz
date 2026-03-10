import time
import pyperclip
from pynput.keyboard import Controller, Key

class TextOut:
    def __init__(self):
        self.keyboard = Controller()

    def paste_text(self, text):
        """Copies text to clipboard and simulates Ctrl+V, then restores original clipboard."""
        if not text:
            return
        
        # Save original content
        original_content = pyperclip.paste()
        
        # Set new text
        pyperclip.copy(text)
        
        # Wait a tiny bit for clipboard system
        time.sleep(0.1)
        
        # Command or Control depending on OS? 
        # Since this is Windows-focused, use Key.ctrl
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('v')
            self.keyboard.release('v')
            
        # Give some time for the paste to complete before restoring
        time.sleep(0.5)
        
        # Restore original clipboard
        if original_content:
            pyperclip.copy(original_content)

# Manual test usage:
if __name__ == "__main__":
    t = TextOut()
    print("Will paste 'Hello World' in 2 seconds...")
    time.sleep(2)
    t.paste_text("Olá Mundo do Verbatim!")
