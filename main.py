# -*- coding: utf-8 -*-
from glob import glob
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv, find_dotenv
from db import database

from discord.ext import commands

load_dotenv(find_dotenv())  # load .env file
bot = commands.Bot(command_prefix=';')

COGS = [path.split(os.sep)[-1][:-3] for path in glob("./cogs/*.py")]


@bot.event
async def on_ready():
    scheduler = AsyncIOScheduler()
    database.auto_save(scheduler)
    scheduler.start()
    print('Bot successfully started!')

for cog in COGS:
    if cog != "__init__":
        bot.load_extension(f'cogs.{cog}')
        print(f'Loaded {cog}')


bot.run(os.environ.get('BOT_TOKEN'))  # run bot
