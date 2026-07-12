import re

from app.infrastructure.ai.gemini_client import GeminiClient
from app.domain.persona import PERSONA_PROMPT

# Sinais de que a resposta vazou raciocínio, formato interno, ou fugiu do personagem.
# Qualquer match aqui = descarta a resposta inteira, não envia nada.
_LEAK_PATTERNS = [
    r"\bTHOUGHT\b",
    r"\bfinal check\b",
    r"\bidentidade\b",
    r"\bregras absolutas\b",
    r"\bpersona\b",
    r"\bcomo uma ia\b",
    r"\bcomo um modelo\b",
    r"\bnão posso\b.{0,30}\bIA\b",
    r"\bassistente\b",
    r"^\s*\{",       # JSON solto
    r"^\s*```",      # bloco de código solto
]

_LEAK_RE = re.compile("|".join(_LEAK_PATTERNS), flags=re.IGNORECASE)


def _sanitizar(texto: str):
    """
    Recebe o texto bruto do modelo e retorna a lista de fragmentos válidos,
    ou None se a resposta deve ser descartada (não enviar nada).
    """
    if not texto or not texto.strip():
        return None

    if _LEAK_RE.search(texto):
        return None

    fragmentos = [f.strip() for f in texto.split("|||") if f.strip()]

    if not fragmentos:
        return None

    return fragmentos


class ChatService:
    def __init__(self):
        self.client = GeminiClient(PERSONA_PROMPT)
        self.history = []

    def gerar_resposta(self, mensagem: str):
        contents = []

        for m, r in self.history[-6:]:
            contents.append({"role": "user", "parts": [{"text": m}]})
            contents.append({"role": "model", "parts": [{"text": " ".join(r)}]})

        contents.append({"role": "user", "parts": [{"text": mensagem}]})

        try:
            texto_bruto = self.client.generate(contents)
        except Exception:
            # Falha de API/timeout/etc -> não manda nada, sem mensagem de erro visível
            return []

        fragmentos = _sanitizar(texto_bruto)

        if fragmentos is None:
            # Resposta vazia, vazou raciocínio, ou veio em formato inválido
            # -> não manda nada, e não contamina o histórico com lixo
            return []

        # só entra no histórico o que realmente foi validado e (presumivelmente) enviado
        self.history.append((mensagem, fragmentos))

        return fragmentos