# -*- coding: utf-8 -*-

import os
from glob import glob

import discord
import dotenv
from apscheduler.schedulers import asyncio

from db import database

dotenv.load_dotenv(dotenv.find_dotenv())
bot = discord.Bot()

# load cogs into list
COGS = [path.split(os.sep)[-1][:-3] for path in glob("./cogs/*.py")]


@bot.event
async def on_ready():
    # start scheduler to auto save db
    scheduler = asyncio.AsyncIOScheduler()
    database.auto_save(scheduler)
    scheduler.start()
    print("Bot successfully started!")


for cog in COGS:
    if cog == "__init__":
        continue

    bot.load_extension(f"cogs.{cog}")
    print(f"Loaded {cog}")


bot.run(os.environ.get("BOT_TOKEN"))
