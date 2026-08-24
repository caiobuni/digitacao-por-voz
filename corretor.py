import json
import logging
import re
import os

logger = logging.getLogger(__name__)

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "correcoes.json")


class Corretor:
    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self._rules = []
        self._vocabulary = []
        self._mtime = None
        self._load()

    def _load(self):
        try:
            mtime = os.path.getmtime(self.path)
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Falha ao carregar correcoes.json: {e}")
            return

        rules = []
        vocabulary = []
        for correto, errados in data.items():
            vocabulary.append(correto)
            for errado in errados:
                pattern = re.compile(rf"\b{re.escape(errado)}\b", re.IGNORECASE)
                rules.append((len(errado), pattern, correto))
        rules.sort(key=lambda r: r[0], reverse=True)
        self._rules = rules
        self._vocabulary = vocabulary
        self._mtime = mtime

    def _reload_if_changed(self):
        try:
            mtime = os.path.getmtime(self.path)
        except OSError:
            return
        if self._mtime is None or mtime != self._mtime:
            self._load()

    def corrigir(self, texto):
        self._reload_if_changed()
        if not texto:
            return texto
        for _, pattern, correto in self._rules:
            texto = pattern.sub(correto, texto)
        return texto

    @property
    def vocabulary(self):
        return list(self._vocabulary)


if __name__ == "__main__":
    c = Corretor()
    frases = [
        "A empresa creditos cresceu e creditus também",
        "falei com a zapa sobre o zapaia",
        "a envenia entregou o relatório",
        "o documento cetec foi aprovado",
        "dinkra e adinca e dincra e dinca e adin",
        "vamos no go paraguai amanhã",
        "meu sobrenome é bune",
        "nada de zapa dentro de zapaia ou vasculhar",
    ]
    for f in frases:
        print(f"IN : {f}")
        print(f"OUT: {c.corrigir(f)}")
        print()
    print("VOCABULARY:", c.vocabulary)
