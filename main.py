import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time
import platform
import os
import socket
#import asyncio
import mysql.connector

class Client(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix=commands.when_mentioned_or('!'),intents=discord.Intents().all())

  async def setup_hook(self):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

  async def on_ready(self):
      prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC",time.gmtime()) + Back.RESET +Fore.WHITE + " ")
      print(prfx + "Bot ID:" + Fore.YELLOW + str(client.user.id))
      print(prfx + "Discord Version:" + Fore.YELLOW + discord.__version__)
      print(prfx + "Python Version:" + Fore.YELLOW + str(platform.python_version()))
      print(prfx + "Node:" + Fore.YELLOW + str(platform.node()))
      print(prfx + "IP:" + Fore.YELLOW + str(socket.gethostbyname(socket.gethostname())))
      synced = await client.tree.sync()
      print(prfx + "Slash CMDs Synced:" + Fore.YELLOW + str(len(synced)) + " Commands")
      print(prfx + "Logging to Channel: " + Fore.YELLOW + os.environ['chan_logs'])

try:
  client = Client()
  client.db = mysql.connector.connect(
    database=  os.environ['dbname'],
    host=      os.environ['dbhost'],
    user=      os.environ['dbuser'],
    password=  os.environ['dbpass'],
    port=      os.environ['dbport']
  )
  client.run(os.environ['discordkey'])
  
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e