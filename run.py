"""import uvicorn
from pyngrok import ngrok
from app.core.config import NGROK_AUTH_TOKEN

if __name__ == "__main__":
    # inicia ngrok
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    public_url = ngrok.connect(8000)
    print(f"URL pública: {public_url}/webhook")

    # inicia FastAPI
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)"""