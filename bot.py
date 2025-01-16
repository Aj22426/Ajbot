import sys
import glob
import importlib.util
import logging
import logging.config
import pytz
import asyncio
from pathlib import Path
from pyrogram import Client, idle
from datetime import date, datetime
from aiohttp import web

from database.users_chats_db import db
from info import *
from utils import temp
from Script import script
from plugins import web_server
from plugins.clone import restart_bots

from AJ.bot import AJBot
from AJ.util.keepalive import ping_server
from AJ.bot.clients import initialize_clients

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)

ppath = "plugins/*.py"
files = glob.glob(ppath)

AJBot.start()
loop = asyncio.get_event_loop()

async def start():
    print('Initializing Your Bot...')
    bot_info = await AJBot.get_me()
    await initialize_clients()

    for name in files:
        with open(name) as a:
            plugin_name = Path(a.name).stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = f"plugins.{plugin_name}"
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules[import_path] = load
            print(f"AJ Imported => {plugin_name}")

    if ON_HEROKU:
        asyncio.create_task(ping_server())

    b_users, b_chats = await db.get_banned()
    temp.BANNED_USERS = b_users
    temp.BANNED_CHATS = b_chats

    me = await AJBot.get_me()
    temp.BOT = AJBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name

    logging.info(script.LOGO)

    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")

    try:
        await AJBot.send_message(
            chat_id=LOG_CHANNEL,
            text=script.RESTART_TXT.format(today, time)
        )
    except:
        print("Make Your Bot Admin In Log Channel With Full Rights")

    for ch in CHANNELS:
        try:
            k = await AJBot.send_message(chat_id=ch, text="**Bot Restarted**")
            await k.delete()
        except:
            print("Make Your Bot Admin In File Channels With Full Rights")

    try:
        k = await AJBot.send_message(chat_id=AUTH_CHANNEL, text="**Bot Restarted**")
        await k.delete()
    except:
        print("Make Your Bot Admin In Force Subscribe Channel With Full Rights")

    if CLONE_MODE:
        print("Restarting All Clone Bots...")
        await restart_bots()
        print("Restarted All Clone Bots.")

    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    await idle()

if __name__ == '__main__':
    try: 
        loop.run_until_complete(start())
    except KeyboardInterrupt: 
        logging.info('Service Stopped Bye 👋')
  
