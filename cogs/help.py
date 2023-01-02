import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        print("help.py LOADED!")

    @app_commands.command(name="help", description="ChaosEngine help")
    async def edit(self, interaction: discord.Interaction):
      await interaction.response.send_message("""
      ```
      COMMAND          WHAT IT DOES
      ===============  ========================================================
      /about           Shows some information about ChaosEngine
      /start           The first command you run! Registers this discord server with ChaosEngine
      /register        Allows users to register with this clan/discord server
      /tool            Sends the user a link to edit their information (easy mode!)
      /stats           Update ALL your stats with one command
      /paragon         Update your Paragon Level
      /cr              Update your combat rating
      /reso            Update your Resonance value
      /damage          Update your Damage value
      /life            Update your Life value
      /setinfo         Look up information about Set Items
      /bugreport       Send a bug report or suggestion
      ```
      """)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Help(client))