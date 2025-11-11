# shared_client.py (fixed)
from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN, STRING
from pyrogram import Client
import asyncio

# create client instances (do not start them here)
telethon_client = TelegramClient("telethonbot", API_ID, API_HASH)
pyro_app = Client("pyrogrambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = None
if STRING:
    # userbot uses session string if provided
    userbot = Client("4gbbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

async def start_client():
    """
    Start all configured clients. Raises RuntimeError on fatal startup errors
    instead of exiting the process directly.
    """
    # Telethon bot (if configured)
    try:
        # Telethon: ensure connection. start() is a coroutine
        if not await telethon_client.is_connected():
            await telethon_client.start(bot_token=BOT_TOKEN)
        print("Telethon bot started...")
    except Exception as e:
        # raise so caller can decide what to do (and allow graceful shutdown)
        raise RuntimeError(f"Failed to start Telethon client: {e}") from e

    # userbot (optional)
    if userbot is not None:
        try:
            await userbot.start()
            print("Userbot started...")
        except Exception as e:
            raise RuntimeError(f"Userbot session invalid or expired: {e}") from e

    # Pyrogram bot/app
    try:
        await
