from app.infrastructure.ai.gemini_client import GeminiClient
from app.domain.persona import PERSONA_PROMPT

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
            texto = self.client.generate(contents)
        except Exception:
            texto = "erro|||não consegui responder"

        fragmentos = [f.strip() for f in texto.split("|||") if f.strip()]

        self.history.append((mensagem, fragmentos))

        return fragmentos
