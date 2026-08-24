import json
import logging
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

OPENCODE_AUTH = Path.home() / ".local" / "share" / "opencode" / "auth.json"
OPENCODE_URL = "https://opencode.ai/zen/v1/chat/completions"
OPENCODE_MODEL = "deepseek-v4-flash"
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"
TIMEOUT = 2.0
MAX_GROWTH = 1.4

SYSTEM_PROMPT = (
    "Você é um editor conservador de ditado em português do Brasil. "
    "Regras obrigatórias:\n"
    "- Não invente fatos, nomes, frases ou conteúdo.\n"
    "- Não apague nem altere nomes próprios e termos do vocabulário fornecido.\n"
    "- Remova fillers: né, tipo, então assim, tá, ahn, eh, hum.\n"
    "- Remova repetições desnecessárias.\n"
    "- Se o falante se corrigir (ex: 'não, quis dizer X'), fique só com a versão final.\n"
    "- Se houver enumeração, formate como lista com '- '.\n"
    "- Devolva APENAS o texto final, sem aspas, sem explicação e sem prefixos."
)


def _extract_key(entry):
    if not isinstance(entry, dict):
        return None
    for field in ("key", "apiKey", "token", "access"):
        value = entry.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _opencode_key():
    env_key = os.getenv("OPENCODE_API_KEY")
    if env_key:
        return env_key.strip()
    try:
        data = json.loads(OPENCODE_AUTH.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    for name in ("opencode-go", "opencode", "opencode-zen"):
        key = _extract_key(data.get(name))
        if key:
            return key
    return None


def _build_routes():
    routes = []
    go_key = _opencode_key()
    if go_key:
        routes.append((OPENCODE_URL, OPENCODE_MODEL, go_key))
    official = os.getenv("DEEPSEEK_API_KEY")
    if official:
        routes.append((DEEPSEEK_URL, DEEPSEEK_MODEL, official.strip()))
    return routes


def _looks_bad(original, edited):
    if not edited:
        return True
    lowered = edited.lower().strip()
    prefixes = (
        "aqui está",
        "aqui esta",
        "texto editado",
        "claro,",
        "certo,",
        "segue o texto",
    )
    if any(lowered.startswith(p) for p in prefixes):
        return True
    if len(edited) > len(original) * MAX_GROWTH + 12:
        return True
    return False


class TextEditor:
    def __init__(self, vocabulary=None):
        self.vocabulary = list(vocabulary or [])
        self.enabled = os.getenv("EDITOR_ENABLED", "1") != "0"
        self._routes = _build_routes() if self.enabled else []
        if self.enabled and not self._routes:
            logger.warning("Editor Deepseek desligado: nenhuma chave encontrada.")
            self.enabled = False

    def edit(self, text):
        if not self.enabled or not text:
            return text

        vocab = ""
        if self.vocabulary:
            vocab = " Vocabulário protegido: " + ", ".join(self.vocabulary) + "."
        payload = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT + vocab},
                {"role": "user", "content": text},
            ],
            "temperature": 0,
            "max_tokens": 400,
        }

        for url, model, key in self._routes:
            try:
                body = dict(payload)
                body["model"] = model
                response = httpx.post(
                    url,
                    headers={
                        "Authorization": f"Bearer {key}",
                        "Content-Type": "application/json",
                    },
                    json=body,
                    timeout=TIMEOUT,
                )
                if response.status_code >= 500 or response.status_code in (401, 403, 429):
                    logger.warning(f"Editor {model} status {response.status_code}, tentando fallback.")
                    continue
                response.raise_for_status()
                edited = response.json()["choices"][0]["message"]["content"].strip()
                if _looks_bad(text, edited):
                    logger.warning("Editor descartou resposta inválida.")
                    return text
                return edited
            except Exception as e:
                logger.warning(f"Editor falhou em {model}: {e}")
                continue
        return text
