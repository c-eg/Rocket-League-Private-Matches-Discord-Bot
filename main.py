import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv()) # load .env file
client = commands.Bot(command_prefix = ';')

@client.event
async def on_ready():
    print('Bot successfully started!')

# Load cogs into client
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')
        print(f'Loaded {file}')

client.run(os.environ.get('BOT_TOKEN'))