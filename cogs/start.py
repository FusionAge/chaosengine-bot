import discord
from discord.ext import commands
from discord import app_commands
import mysql.connector
import os
from dotenv import load_dotenv

class StartModal(discord.ui.Modal, title="New ChaosEngine Clan"):
  gname = discord.ui.TextInput(label="Clan Name",
                               placeholder="Enter your Clan's Name",
                               style=discord.TextStyle.short)
  
  gserver = discord.ui.TextInput(label="Server Name",
                                 placeholder="What Blizzard server does your Clan play on?",
                                 style=discord.TextStyle.short)

  #gtype = discord.ui.Select(placeholder="Select Clan Type",options=GuildTypes)
  async def on_submit(self, interaction: discord.Interaction):
    #Add to the DB
    db = mysql.connector.connect(database=  os.environ['DB_NAME'],
                                  host=      os.environ['DB_HOST'],
                                  user=      os.environ['DB_USER'],
                                  password=  os.environ['DB_PASS'],
                                  port=      os.environ['DB_PORT'])
    db.reconnect()
    sql = (f"CALL create_guild(%s,%s,1,%s,%s,%s)")
    val = (str(interaction.guild_id), str(interaction.guild.name), str(self.gname), str(self.gserver),str(interaction.user.id))
    cursor = db.cursor()
    try:
      cursor.execute(sql, val)
      db.commit()
      botmaster = interaction.client.get_user(int(os.environ['OWNERID']))
      dm_channel = await botmaster.create_dm()
      await dm_channel.send(f"New Clan Added: {self.gname} on {self.gserver} with a DISCORDID of {interaction.guild_id}")
    except mysql.connector.Error as e:
      print(e)
    else:
      #Send Welcome Message
      await interaction.response.send_message(f"Welcome <{self.gname}> playing on {self.gserver}! You and your members can now use `/register` to add yourselves.")
      cursor.close()
      #Send Message to Owner


class Start(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client
    print("start.py LOADED!")

  @app_commands.command(
      name="start",
      description="Adds Clan to ChaosEngine from THIS Discord server.")
  async def start(self, interaction: discord.Interaction):
      #First Make Sure it isn't already there
      self.client.db.reconnect()
      qry = (f"SELECT count(*) from guilds where d_gid = '{interaction.guild_id}'")
      cursor = self.client.db.cursor()
      cursor.execute(qry)
      if cursor.fetchall()[-1][-1] > 0:
          await interaction.response.send_message(
              "This discord/server already exists! Did you mean `/edit`?")

      else:
          await interaction.response.send_modal(StartModal())
      cursor.close()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Start(client))
