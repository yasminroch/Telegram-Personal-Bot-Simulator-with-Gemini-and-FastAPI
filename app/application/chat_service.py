import re

from app.infrastructure.ai.gemini_client import GeminiClient
from app.domain.persona import PERSONA_PROMPT


# Detecta vazamentos claros de raciocínio interno ou formatos indevidos.
# Deve bloquear apenas padrões muito específicos.
_LEAK_PATTERNS = [
    r"^\s*THOUGHT\s*:",
    r"^\s*FINAL CHECK\s*:",
    r"^\s*ANALYSIS\s*:",
    r"^\s*REASONING\s*:",
    r"^\s*\{.*\}\s*$",          # JSON puro
    r"^\s*```",                 # bloco de código
    r"^yasmin\s*:",             # modelo colocando nome como prefixo
]

_LEAK_RE = re.compile(
    "|".join(_LEAK_PATTERNS),
    flags=re.IGNORECASE | re.DOTALL
)


def _sanitizar(texto: str):
    """
    Valida a resposta do modelo antes de enviar ao Telegram.
    Retorna lista de mensagens ou None quando deve ser descartada.
    """

    if not texto or not texto.strip():
        print("Gemini retornou vazio")
        return None

    texto = texto.strip()

    # Bloqueia apenas vazamentos claros
    if _LEAK_RE.search(texto):
        print("Resposta bloqueada pelo guardrail:")
        print(texto)
        return None

    fragmentos = [
        f.strip()
        for f in texto.split("|||")
        if f.strip()
    ]

    if not fragmentos:
        print("Nenhum fragmento válido encontrado")
        return None

    return fragmentos


class ChatService:
    def __init__(self):
        self.client = GeminiClient(PERSONA_PROMPT)
        self.history = []

    def gerar_resposta(self, mensagem: str):

        contents = []

        for m, r in self.history[-6:]:
            contents.append({
                "role": "user",
                "parts": [{"text": m}]
            })

            contents.append({
                "role": "model",
                "parts": [{"text": " ".join(r)}]
            })

        contents.append({
            "role": "user",
            "parts": [{"text": mensagem}]
        })

        try:
            texto_bruto = self.client.generate(contents)

            print("Resposta bruta Gemini:")
            print(repr(texto_bruto))

        except Exception as e:
            print("Erro Gemini:", e)
            return []

        fragmentos = _sanitizar(texto_bruto)

        if fragmentos is None:
            return []

        self.history.append((mensagem, fragmentos))

        return fragmentos