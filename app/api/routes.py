from fastapi import APIRouter, Request
from app.application.chat_service import ChatService
from app.utils.delay import calcular_delay
import asyncio
import httpx
import os

router = APIRouter()
chat_service = ChatService()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

print("TOKEN EXISTE:", TELEGRAM_TOKEN is not None)


@router.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        return {"ok": True}

    mensagem = data.get("message", {}).get("text", "")
    chat_id = data.get("message", {}).get("chat", {}).get("id")

    print("Mensagem recebida:", mensagem)
    print("Chat ID:", chat_id)

    if not mensagem or not chat_id:
        print("Mensagem ou chat_id vazio")
        return {"ok": True}

    respostas = chat_service.gerar_resposta(mensagem)

    print("Respostas geradas:", respostas)

    async with httpx.AsyncClient() as client:
        for r in respostas:
            await asyncio.sleep(calcular_delay(r))

            response = await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": r
                }
            )

            print("Status Telegram:", response.status_code)
            print("Resposta Telegram:", response.text)

    return {"ok": True}