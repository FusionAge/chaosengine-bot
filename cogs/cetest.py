import discord
from discord.ext import commands
from discord import app_commands, ui, Interaction
import mysql.connector
import os
from typing import Dict

class CeModal(discord.ui.Modal, title="Edit ChaosEngine Clan"):
  def __init__(self, data: Dict[str, str], **kwargs):
    super(CeModal, self).__init__(**kwargs)
    self.gname = ui.TextInput(label="Clan Name",default=f"{data[0][0]}",style=discord.TextStyle.short)
    self.add_item(self.gname)
    self.gserver = ui.TextInput(label="Server Name",default=f"{data[0][1]}",style=discord.TextStyle.short)
    self.add_item(self.gserver)

  async def on_submit(self, interaction: discord.Interaction):
    print(self.gname)
    db = mysql.connector.connect(database=os.environ['dbname'],
                                 host=os.environ['dbhost'],
                                 user=os.environ['dbuser'],
                                 password=os.environ['dbpass'],
                                 port=os.environ['dbport'])
    sql = (f"UPDATE guilds set guildname = %s, guildserver = %s where d_gid = %s")
    val = (str(self.gname),str(self.gserver),str(interaction.guild_id))
    db.reconnect()
    cursor = db.cursor()
    cursor.execute(sql, val)
    db.commit()
    await interaction.response.send_message(f"Clan information updated! Clan: {self.gname}, Server: {self.gserver}")
        
class Cetest(commands.Cog):
    def __init__(self, client: commands.Bot):
      self.client = client
      print("cetest.py LOADED!")

    @app_commands.command(
      name="cetest",
      description="Command I use for testing stuff. Probably does nothing.")
    async def start(self, interaction: discord.Interaction):
      #Get the Clan/Discord data
      self.client.db.reconnect()
      qry = (f"SELECT guildname,guildserver from guilds where d_gid = '{interaction.guild_id}'")
      cursor = self.client.db.cursor()
      cursor.execute(qry)
      result = cursor.fetchall()
      cursor.close()
      await interaction.response.send_modal(CeModal(result))

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Cetest(client))
