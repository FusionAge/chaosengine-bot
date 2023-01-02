import discord
import datetime,time
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

class About(commands.Cog):
    def __init__(self,client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()

    @app_commands.command(name="about", description="About ChaosEngine")
    async def about(self,interaction: discord.Interaction):
      self.client.db.reconnect()
      cursor = self.client.db.cursor()
      cursor.execute("select count(*) from users")
      users = cursor.fetchall()[-1][-1]
      uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
      cursor.close()
      embed = discord.Embed(
          title=f"Chaos Engine",
          description="Clan management tool for Diablo:Immortal",
          color=0x830b13
      )
      embed.set_thumbnail(
          url="https://blz-contentstack-images.akamaized.net/v3/assets/blt77f4425de611b362/blt7dd71188aff1b9cb/6131015b8ae2653b28a72a8c/di-logo-960.png"
      )
      embed.add_field(
          name="Version",
          value= os.environ['VERSION']
      )
      embed.add_field(
          name="Uptime",
          value=uptime
      )
      embed.add_field(
          name="Latency",
          value=round(self.client.latency * 1000)
      )
      embed.add_field(
          name="Clans",
          value=len(self.client.guilds)
      )
      embed.add_field(
          name="Users",
          value=users
      )
      embed.add_field(
          name="Characters",
          value=users
      )
      embed.add_field(
          name="Current Discord",
          value=interaction.guild.name
      )
      embed.add_field(
          name="Discord ID",
          value=interaction.guild_id
      )
      embed.add_field(
          name="Discord Members",
          value=interaction.guild.member_count
      )
      embed.set_footer(
          text="ChaosEngine Developed by: GenXWhatever (Lysander)",
          icon_url="https://cdn.discordapp.com/avatars/386200837896011776/4e381a02c13346fc011f6e862acec87a.png"
      )
      await interaction.response.send_message(embed=embed)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(About(client))