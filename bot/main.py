# -*- coding: utf-8 -*-
from dotenv import load_dotenv, find_dotenv
from glob import glob
import os

from discord.ext import commands


load_dotenv(find_dotenv())  # load .env file
bot = commands.Bot(command_prefix=';')

COGS = [path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")]

@bot.event
async def on_ready():
    print('Bot successfully started!')

for cog in COGS:
    bot.load_extension(f'cogs.{cog}')
    print(f'Loaded {cog}')


bot.run(os.environ.get('BOT_TOKEN'))  # run bot
