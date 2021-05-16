import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())  # load .env file
bot = commands.Bot(command_prefix=';')


@bot.event
async def on_ready():
    print('Bot successfully started!')

# Load cogs into client
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')
        print(f'Loaded cogs/{file}')

bot.run(os.environ.get('BOT_TOKEN'))
