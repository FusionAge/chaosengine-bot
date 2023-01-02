import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import traceback

class BugModal(discord.ui.Modal,title="Submit a Bug Report (or Suggestion!)"):
  bugdesc = discord.ui.TextInput(
    label="Bug / Suggestion",
    placeholder="Describe the issue in as much detail as possible",
    style=discord.TextStyle.long
  )
  
  async def on_submit(self,interaction:discord.Interaction):
    #Send to the ce-bugreports channel
    embed = discord.Embed(
      title="New Bug/Suggestion",
      description=self.bugdesc.value,
      color=discord.Color.yellow()
    )
    embed.set_author(name=self.user)
    await self.chan.send(embed=embed)
    await interaction.response.send_message(f"Thank you {self.user.nick}-- your message has been sent!",ephemeral=True)

  async def on_error(self,interaction:discord.Interaction, error:Exception):
    traceback.print_tb(error.__traceback__)
    
class Bug(commands.Cog):
    def __init__(self,client: commands.Bot):
        self.client = client
        print("bugreport.py LOADED!")   
      
    @app_commands.command(name="bugreport", description="Found a bug or have a suggestion? Use this command!")
    async def start(self,interaction: discord.Interaction):
      bugmodal = BugModal()
      bugmodal.chan = self.client.get_channel(int(os.environ['chan_bugreports']))
      bugmodal.user = interaction.user
      await interaction.response.send_modal(bugmodal)
      
async def setup(client:commands.Bot) -> None:
    await client.add_cog(Bug(client))