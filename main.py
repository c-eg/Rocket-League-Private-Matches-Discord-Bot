# -*- coding: utf-8 -*-

from glob import glob
import os

from apscheduler.schedulers import asyncio
import dotenv
from db import database

from discord.ext import commands

dotenv.load_dotenv(dotenv.find_dotenv())  # load .env file
bot = commands.Bot(command_prefix=os.environ.get('COMMAND_PREFIX'))

# load cogs into list
COGS = [path.split(os.sep)[-1][:-3] for path in glob('./cogs/*.py')]


@bot.event
async def on_ready():
    # start scheduler to auto save db
    scheduler = asyncio.AsyncIOScheduler()
    database.auto_save(scheduler)
    scheduler.start()
    print('Bot successfully started!')


for cog in COGS:
    if cog == "__init__":
        continue

    bot.load_extension(f'cogs.{cog}')
    print(f'Loaded {cog}')


bot.run(os.environ.get('BOT_TOKEN'))  # run bot
