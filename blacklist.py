import json
import logging
import os
import re
import unicodedata

logger = logging.getLogger(__name__)

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blacklist.json")


def normalize(text):
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text).lower().strip()
    text = re.sub(r"[.!?…,;:]+$", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


class Blacklist:
    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self._exact = set()
        self._contains = []
        self._mtime = None
        self._load()

    def _load(self):
        try:
            mtime = os.path.getmtime(self.path)
            with open(self.path, "r", encoding="utf-8") as f:
                items = json.load(f)
        except Exception as e:
            logger.error(f"Falha ao carregar blacklist.json: {e}")
            return

        exact = set()
        contains = []
        for raw in items:
            phrase = normalize(raw)
            if not phrase:
                continue
            words = phrase.split()
            if len(words) <= 3 and "." not in phrase:
                exact.add(phrase)
            else:
                contains.append(phrase)
        self._exact = exact
        self._contains = contains
        self._mtime = mtime

    def _reload_if_changed(self):
        try:
            mtime = os.path.getmtime(self.path)
        except OSError:
            return
        if self._mtime is None or mtime != self._mtime:
            self._load()

    def is_blocked(self, text):
        self._reload_if_changed()
        norm = normalize(text)
        if not norm:
            return False
        if norm in self._exact:
            return True
        return any(phrase in norm for phrase in self._contains)


if __name__ == "__main__":
    b = Blacklist()
    samples = [
        ("Obrigado!", True),
        ("tudo bem?", True),
        ("tudo bem com o contrato", False),
        ("Acesse o site www.sara.org.br para mais informações.", True),
        ("Aprende com o curso!", True),
        ("vamos revisar o contrato", False),
        ("Atenção.", True),
    ]
    for text, expected in samples:
        got = b.is_blocked(text)
        print(f"{'OK' if got == expected else 'FAIL'} {text!r} -> {got}")
