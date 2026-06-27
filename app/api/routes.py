from fastapi import APIRouter, Request
from app.application.chat_service import ChatService
from app.utils.delay import calcular_delay
import asyncio

router = APIRouter()
chat_service = ChatService()

@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    mensagem = data.get("message", {}).get("text", "")

    if not mensagem:
        return {"ok": True}

    respostas = chat_service.gerar_resposta(mensagem)

    for r in respostas:
        await asyncio.sleep(calcular_delay(r))
        print(f"Resposta: {r}")  # aqui você pode integrar com Telegram depois

    return {"ok": True}
