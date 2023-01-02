import discord
from discord.ext import commands
from discord import app_commands, ui, Interaction
import mysql.connector
import os
from dotenv import load_dotenv
from typing import Dict

class EditModal(discord.ui.Modal, title="Edit ChaosEngine Clan"):
  def __init__(self, data: Dict[str, str], **kwargs):
    super(EditModal, self).__init__(**kwargs)
    self.gname = ui.TextInput(label="Clan Name",default=f"{data[0][0]}",style=discord.TextStyle.short)
    self.add_item(self.gname)
    self.gserver = ui.TextInput(label="Server Name",default=f"{data[0][1]}",style=discord.TextStyle.short)
    self.add_item(self.gserver)

  async def on_submit(self, interaction: discord.Interaction):
    db = mysql.connector.connect(database=  os.environ['DB_NAME'],
                                  host=      os.environ['DB_HOST'],
                                  user=      os.environ['DB_USER'],
                                  password=  os.environ['DB_PASS'],
                                  port=      os.environ['DB_PORT'])
    sql = (f"UPDATE guilds set guildname = %s, guildserver = %s where d_gid = %s")
    val = (str(self.gname),str(self.gserver),str(interaction.guild_id))
    db.reconnect()
    cursor = db.cursor()
    cursor.execute(sql, val)
    db.commit()
    await interaction.response.send_message(f"Clan information updated! Clan: {self.gname}, Server: {self.gserver}")
        
class Edit(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client
    print("edit.py LOADED!")

  @app_commands.command(
    name="edit",
    description="Used to edit clan name & server (admin only)")
  async def start(self, interaction: discord.Interaction):
    self.client.db.reconnect()
    #Make Sure the Clan Exists
    qry = (f"SELECT guildname,guildserver from guilds where d_gid = '{interaction.guild_id}'")
    cursor = self.client.db.cursor()
    cursor.execute(qry)
    result = cursor.fetchall()
    rowcount = len(result)
    if rowcount > 0:
      #Check if the caller is an admin
      adminqry = (f"SELECT d_gid,d_uid from guild_admins where d_gid ='{interaction.guild_id}' and d_uid = '{interaction.user.id}'")
      cursor.execute(adminqry)
      adminrow = len(cursor.fetchall())
      if adminrow == 1:
        await interaction.response.send_modal(EditModal(result))
      else:
        await interaction.response.send_message("Only admins can use that command!")  
    else:
      await interaction.response.send_message("This clan/discord server doesn't exist in ChaosEngine! Try `/start`?")
    cursor.close()

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Edit(client))