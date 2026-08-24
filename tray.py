import pystray
from PIL import Image, ImageDraw


def _draw_mic(color):
    image = Image.new("RGB", (64, 64), (30, 30, 30))
    dc = ImageDraw.Draw(image)
    dc.rounded_rectangle([22, 6, 42, 34], radius=10, fill=color)
    dc.arc([14, 20, 50, 48], start=0, end=180, fill=color, width=3)
    dc.line([(32, 48), (32, 56)], fill=color, width=3)
    dc.line([(22, 56), (42, 56)], fill=color, width=3)
    return image


class TrayApp:
    def __init__(self, on_open_log=None, on_open_dict=None, on_open_blacklist=None, on_quit=None):
        self.on_open_log = on_open_log
        self.on_open_dict = on_open_dict
        self.on_open_blacklist = on_open_blacklist
        self.on_quit = on_quit
        self.icon = None
        self._idle_image = _draw_mic((200, 220, 255))
        self._rec_image = _draw_mic((220, 60, 70))
        self._create_icon()

    def _create_icon(self):
        self.icon = pystray.Icon(
            "verbatim",
            self._idle_image,
            "Verbatim Dictation",
            menu=pystray.Menu(
                pystray.MenuItem("Abrir Histórico", self._handle_open_log),
                pystray.MenuItem("Abrir dicionário", self._handle_open_dict),
                pystray.MenuItem("Abrir lista negra", self._handle_open_blacklist),
                pystray.MenuItem("Sair", self._wrapper_quit)
            )
        )

    def set_recording(self, recording):
        if not self.icon:
            return
        try:
            self.icon.icon = self._rec_image if recording else self._idle_image
        except Exception:
            pass

    def _handle_open_log(self, icon, item):
        if self.on_open_log:
            self.on_open_log()

    def _handle_open_dict(self, icon, item):
        if self.on_open_dict:
            self.on_open_dict()

    def _handle_open_blacklist(self, icon, item):
        if self.on_open_blacklist:
            self.on_open_blacklist()

    def _wrapper_quit(self, icon, item):
        if self.on_quit:
            self.on_quit()
        icon.stop()

    def run(self):
        self.icon.run()

    def stop(self):
        if self.icon:
            self.icon.stop()


if __name__ == "__main__":
    def test_log(): print("Opening Log...")
    def test_dict(): print("Opening dict...")
    def test_quit(): print("Quitting...")
    app = TrayApp(test_log, test_dict, test_quit)
    app.run()
