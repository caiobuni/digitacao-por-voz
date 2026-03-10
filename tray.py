import pystray
from PIL import Image, ImageDraw
import threading

class TrayApp:
    def __init__(self, on_open_log=None, on_quit=None):
        self.on_open_log = on_open_log
        self.on_quit = on_quit
        self.icon = None
        self._create_icon()

    def _create_icon(self):
        # Create a simple icon (Circle with a V for Verbatim)
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), (30, 30, 30))
        dc = ImageDraw.Draw(image)
        # Draw a circle
        dc.ellipse([5, 5, 59, 59], fill=(0, 150, 255))
        # Draw a 'V'
        dc.text((25, 20), "V", fill="white")
        
        self.icon = pystray.Icon(
            "verbatim",
            image,
            "Verbatim Dictation",
            menu=pystray.Menu(
                pystray.MenuItem("Abrir Histórico", self._handle_open_log),
                pystray.MenuItem("Sair", self._wrapper_quit)
            )
        )

    def _handle_open_log(self, icon, item):
        if self.on_open_log:
            self.on_open_log()

    def _wrapper_quit(self, icon, item):
        if self.on_quit:
            self.on_quit()
        icon.stop()

    def run(self):
        # Running icon in the main thread (or separate if needed)
        self.icon.run()

    def stop(self):
        if self.icon:
            self.icon.stop()

# Manual test usage:
if __name__ == "__main__":
    def test_log(): print("Opening Log...")
    def test_quit(): print("Quitting...")
    app = TrayApp(test_log, test_quit)
    app.run()
