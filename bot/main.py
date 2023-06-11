# -*- coding: utf-8 -*-

import os
from glob import glob

import discord
import dotenv
from apscheduler.schedulers import asyncio

from db import database

import logging

logger = logging.getLogger(__name__)

dotenv.load_dotenv(dotenv.find_dotenv())
bot = discord.Bot()


@bot.event
async def on_ready():
    # start scheduler to auto save db
    scheduler = asyncio.AsyncIOScheduler()
    database.auto_save(scheduler)
    scheduler.start()
    logger.info("Bot successfully started!")


def main():
    # load cogs into list
    COGS = [path.split(os.sep)[-1][:-3] for path in glob("./bot/cogs/*.py")]

    for cog in COGS:
        if cog == "__init__":
            continue

        bot.load_extension(f"cogs.{cog}")
        logger.info(f"Loaded {cog}")

    bot.run(os.environ.get("BOT_TOKEN"))

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO)
    main()
