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
    chat_id = data.get("message", {}).get("chat", {}).get("id")

    if not mensagem:
        return {"ok": True}

    respostas = chat_service.gerar_resposta(mensagem)

    async with httpx.AsyncClient() as client:
        for r in respostas:
            await asyncio.sleep(calcular_delay(r))

            await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": r
                }
            )

    return {"ok": True}
