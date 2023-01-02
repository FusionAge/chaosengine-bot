import discord
from discord.ext import commands
from discord import app_commands
from typing import Dict
import mysql.connector
import os
from dotenv import load_dotenv

class StatsModal(discord.ui.Modal, title="Edit Your Basic Stats"):
  def __init__(self, data: Dict[str, str], **kwargs):
    super(StatsModal, self).__init__(**kwargs)
    self.uplvl = discord.ui.TextInput(label="Paragon Level",default=f"{str(data[0][0])}",style=discord.TextStyle.short)
    self.add_item(self.uplvl)
    self.upcr = discord.ui.TextInput(label="Combat Rating",default=f"{data[0][1]}",style=discord.TextStyle.short)
    self.add_item(self.upcr)
    self.updmg = discord.ui.TextInput(label="Damage",default=f"{data[0][2]}",style=discord.TextStyle.short)
    self.add_item(self.updmg)
    self.uplife = discord.ui.TextInput(label="Life",default=f"{data[0][3]}",style=discord.TextStyle.short)
    self.add_item(self.uplife)
    self.upreso = discord.ui.TextInput(label="Resonance",default=f"{data[0][4]}",style=discord.TextStyle.short)
    self.add_item(self.upreso)

  async def on_submit(self, interaction: discord.Interaction):
    #Make Sure they only put in Numbers
    print(f"Paragon:{self.uplvl.value}, CR: {self.upcr.value}, DMG: {self.updmg.value}, LF: {self.uplife.value}, Reso: {self.upreso.value}")
    if isinstance(int(self.uplvl.value), int) and isinstance(int(self.upcr.value),int) and isinstance(int(self.updmg.value),int) and isinstance(int(self.uplife.value),int) and isinstance(int(self.upreso.value), int):
      #Yep, just numbers
      db = mysql.connector.connect(database=  os.environ['DB_NAME'],
                                    host=      os.environ['DB_HOST'],
                                    user=      os.environ['DB_USER'],
                                    password=  os.environ['DB_PASS'],
                                    port=      os.environ['DB_PORT'])
      sql = (f"UPDATE users set plvl = %s, cr = %s, dmg = %s, life = %s, reso = %s where d_uid = '{interaction.user.id}' and d_gid = '{interaction.guild_id}'")
      val = (self.uplvl.value,self.upcr.value,self.updmg.value,self.uplife.value,self.upreso.value)
      db.reconnect()
      cursor = db.cursor()
      cursor.execute(sql, val)
      db.commit()
      await interaction.response.send_message(f"Stats updated! Paragon: {self.uplvl}, Combat Rating: {self.upcr}, Damage: {self.updmg}, Life: {self.uplife}, Resonance: {self.upreso}")
    else:
      #Nope. Tell them to fix it.
      await interaction.response.send_message("Only numbers are allowed!")
      
   

class Stats(commands.Cog):
    def __init__(self, client: commands.Bot):
      self.client = client
      print("stats.py LOADED!")

    @app_commands.command(name="stats",description="Update your Stats")
    async def stats(self, interaction: discord.Interaction):
      # Check if the Clan is Registered
      data = self.client.db
      data.reconnect()
      cursor = data.cursor()
      qry = f"select count(*) from guilds where d_gid = '{interaction.guild_id}'"
      cursor.execute(qry)
      result = cursor.fetchone()
      if result[0] > 0:
        #CLAN is Registered, is USER?
        qry = f"select plvl,cr,dmg,life,reso from users where d_uid = '{interaction.user.id}' and d_gid = '{interaction.guild_id}'"
        cursor.execute(qry)
        results = cursor.fetchall()
        if len(results) > 0:
          #USER is Registered
          await interaction.response.send_modal(StatsModal(results))
        else:
          #USER is Unregistered
          await interaction.response.send_message("ChaosEngine doesn't recognize you, try `/register`") 
      else:
        #CLAN is Unregistered
        await interaction.response.send_message("ChaosEngine doesn't recognize this clan/server, try `/start`") 
    
      

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Stats(client))