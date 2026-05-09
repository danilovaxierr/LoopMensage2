import os
import time
import json
import logging
import asyncio
import urllib.request
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID", "-1001234567890"))

MESSAGES = [
    "💎 Loop 1",
    "🔥 Loop 2",
    "🚀 Loop 3"
]

loop_ativo = False
last_update_id = 0


def carregar_env_local():
    """
    Lê o arquivo .env quando estiver rodando no PC.
    No Render, ele usa as Environment Variables.
    """
    if not os.path.exists(".env"):
        return

    with open(".env", "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue

            chave, valor = linha.split("=", 1)
            os.environ.setdefault(chave.strip(), valor.strip())


def telegram_request(method, params=None):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"

    if params:
        data = urllib.parse.urlencode(params).encode()
    else:
        data = None

    req = urllib.request.Request(url, data=data)

    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode())


def send_text(chat_id, text):
    try:
        telegram_request("sendMessage", {
            "chat_id": chat_id,
            "text": text
        })
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem: {e}")


async def enviar_loop():
    global loop_ativo

    while True:
        if loop_ativo:
            try:
                index = datetime.now().minute % len(MESSAGES)
                text = MESSAGES[index]

                send_text(TARGET_CHAT_ID, text)
                logging.info("✅ Msg enviada!")

            except Exception as e:
                logging.error(f"❌ Erro no loop: {e}")

        await asyncio.sleep(300)


async def polling():
    global last_update_id
    global loop_ativo

    logging.info("🤖 Bot iniciado em polling")

    while True:
        try:
            result = telegram_request("getUpdates", {
                "offset": last_update_id + 1,
                "timeout": 25
            })

            updates = result.get("result", [])

            for update in updates:
                last_update_id = update["update_id"]

                message = update.get("message")
                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text", "")

                if text.startswith("/start"):
                    send_text(chat_id, "🚀 LoopBot v4 UP! Use /loop")

                elif text.startswith("/loop"):
                    if not loop_ativo:
                        loop_ativo = True
                        send_text(chat_id, "🔄 Loops ON! Use /stop")
                    else:
                        send_text(chat_id, "⚠️ O loop já está ligado.")

                elif text.startswith("/stop"):
                    loop_ativo = False
                    send_text(chat_id, "⏹️ Loops OFF!")

        except Exception as e:
            logging.error(f"Erro no polling: {e}")
            await asyncio.sleep(5)


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot online!")

    def log_message(self, format, *args):
        return


def start_webserver():
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    logging.info(f"🌐 Web server rodando na porta {port}")
    server.serve_forever()


async def main():
    global TOKEN
    global TARGET_CHAT_ID

    carregar_env_local()

    TOKEN = os.getenv("BOT_TOKEN")
    TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID", "-1001234567890"))

    if not TOKEN:
        raise ValueError("BOT_TOKEN não encontrado")

    Thread(target=start_webserver, daemon=True).start()

    await asyncio.gather(
        polling(),
        enviar_loop()
    )


if __name__ == "__main__":
    asyncio.run(main())
