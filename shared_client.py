# shared_client.py (replace entire file)
from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN, STRING
from pyrogram import Client

telethon_client = TelegramClient("telethonbot", API_ID, API_HASH)
pyro_app = Client("pyrogrambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = None
if STRING:
    userbot = Client("4gbbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

async def start_client():
    """Start all configured clients. Raise on failure so caller can handle shutdown."""
    # Telethon (is_connected may be coroutine in some versions)
    try:
        if not await telethon_client.is_connected():
            await telethon_client.start(bot_token=BOT_TOKEN)
        print("Telethon bot started...")
    except Exception as e:
        raise RuntimeError(f"Failed to start Telethon client: {e}") from e

    # optional userbot
    if userbot is not None:
        try:
            await userbot.start()
            print("Userbot started...")
        except Exception as e:
            raise RuntimeError(f"Userbot start failed: {e}") from e

    # pyrogram app
    try:
        await pyro_app.start()
        print("Pyrogram app started...")
    except Exception as e:
        raise RuntimeError(f"Failed to start Pyrogram app: {e}") from e

    return telethon_client, pyro_app, userbot

async def stop_client():
    """Stop clients cleanly."""
    try:
        await pyro_app.stop()
    except Exception:
        pass

    if userbot is not None:
        try:
            await userbot.stop()
        except Exception:
            pass

    try:
        await telethon_client.disconnect()
    except Exception:
        pass

    print("All clients stopped.")
