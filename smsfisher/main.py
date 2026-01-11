from telethon import TelegramClient, events
from telethon.tl.types import InputPeerChannel
from dotenv import load_dotenv
import os
import asyncio
import aiohttp

import requests

import sys

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
stm_access_hash = int(os.getenv("STM_ACCESS_HASH"))
stm_id_real = int(os.getenv("STM_ID_REAL"))
webhook_url_n8n = os.getenv("WEBHOOK_URL_TEST")

sys.stdout.reconfigure(line_buffering=True)
print("começando")

client = TelegramClient(
    "/app/session/smsfisher",
    api_id,
    api_hash
)

channel = InputPeerChannel(
    stm_id_real,
    stm_access_hash
)

@client.on(events.NewMessage(chats=channel))
async def handler(event):
    if not event.text:
        return

    print ("Mensagem recebida ", event.text)

    payload = {"sms": event.text}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url_n8n, json=payload) as res:
                if res.status == 200:
                    print("Dados enviados ao n8n")
                else:
                    print(f"Erro ao enviar ao n8n: {res.status}")
    except Exception as e:
        print(f"Erro ao enviar dados: {e}")

async def main():

    await client.start()
    print("Cliente conectado!")
    print("Esperando mensagens...")
    
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())