import pystray
from PIL import Image, ImageDraw

from config import get_input_device_index, list_input_devices, set_input_device_index


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

    def _mic_items(self):
        items = []
        current = get_input_device_index()
        for dev in list_input_devices():
            items.append(pystray.MenuItem(
                dev["label"],
                self._make_select(dev["index"]),
                checked=self._make_checked(dev["index"], current),
                radio=True
            ))
        if not items:
            items.append(pystray.MenuItem("Nenhum microfone", None, enabled=False))
        return items

    def _make_select(self, index):
        def _select(icon, item):
            set_input_device_index(index)
            if self.icon:
                self.icon.update_menu()
        return _select

    def _make_checked(self, index, current):
        def _checked(item):
            return get_input_device_index() == index
        return _checked

    def _create_icon(self):
        self.icon = pystray.Icon(
            "verbatim",
            self._idle_image,
            "Verbatim Dictation",
            menu=pystray.Menu(
                pystray.MenuItem("Abrir Histórico", self._handle_open_log),
                pystray.MenuItem("Abrir dicionário", self._handle_open_dict),
                pystray.MenuItem("Abrir lista negra", self._handle_open_blacklist),
                pystray.MenuItem("Microfone", pystray.Menu(lambda: self._mic_items())),
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
