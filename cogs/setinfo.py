import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

class ClassIDConverter(commands.Converter):
  async def convert(self,ctx,argument):
    data = self.client.db
    data.reconnect()
    cursor = data.cursor()
    cursor.execute('SELECT classid, classname FROM ref_classes')
    count = cursor.fetchone()[0]
    if count == 0:
      raise commands.BadArgument('Invalid class ID')
    return argument

class Setinfo(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        print("setinfo.py LOADED!")

    @app_commands.command(
        name="setinfo",
        description="Get information on Set Items")
    @app_commands.describe(set='Select a Set',slot='Select a Slot (Optional)')
    @app_commands.choices(
      set=[
        discord.app_commands.Choice(name="Feasting Baron's Pack", value=1),
        discord.app_commands.Choice(name="Grace of the Flagellant", value=2),
        discord.app_commands.Choice(name="Isstar Imbued", value=3),
        discord.app_commands.Choice(name="Shepherd's Call to Wolves", value=4),
        discord.app_commands.Choice(name="Untouchable Mountebank", value=5),
        discord.app_commands.Choice(name="Vithu's Urges", value=6),
        discord.app_commands.Choice(name="War Rags of Shal'baas", value=7),
        discord.app_commands.Choice(name="Windloft Perfection", value=8),
        discord.app_commands.Choice(name="Gloomguide's Prize", value=9)
      ],
      slot=[
        discord.app_commands.Choice(name="Neck", value=1),
        discord.app_commands.Choice(name="Finger1", value=2),
        discord.app_commands.Choice(name="Finger2", value=12),
        discord.app_commands.Choice(name="Hands", value=3),
        discord.app_commands.Choice(name="Waist", value=4),
        discord.app_commands.Choice(name="Feet", value=5)
      ]
    )
    async def setinfo(self,interaction: discord.Interaction,set: discord.app_commands.Choice[int],slot: Optional[discord.app_commands.Choice[int]]):
      data = self.client.db
      data.reconnect()
      cursor = data.cursor()
      if slot == None:
        #Show the whole set
        qry = (
            f"""select s.setname,s.setbonus_2,s.setbonus_4,s.setbonus_6,si.setitemname,d.dungeonname,d.areaname,sl.slotname
                FROM ref_sets s
                LEFT JOIN ref_setitems si ON s.setid = si.setid
                LEFT JOIN ref_dungeons d  ON si.dungeonid = d.dungeonid
                LEFT JOIN ref_slots sl ON si.slotid = sl.slotid
                WHERE s.setid = {int(set.value)}"""
        )
        cursor.execute(qry)
        result = cursor.fetchall()
        s_name = result[0][0]
        s_bon2 = result[0][1]
        s_bon4 = result[0][2]
        s_bon6 = result[0][3]
        
        embed = discord.Embed(
          title=f"**{s_name}**",
          description="",
          color=0x00bb35
        )
        #embed.set_thumbnail(
        #    url="https://blz-contentstack-images.akamaized.net/v3/assets/blt77f4425de611b362/blt7dd71188aff1b9cb/6131015b8ae2653b28a72a8c/di-logo-960.png"
        #)
        embed.add_field(
            name="Set Bonus (2 Items)",
            value= s_bon2,
            inline= False
        )
        embed.add_field(
            name="Set Bonus (4 Items)",
            value= s_bon4,
            inline= False
        )
        embed.add_field(
            name="Set Bonus (6 Items)",
            value= s_bon6,
            inline= False
        )
        for i in range(6):
          
          embed.add_field(
              name=f"{result[i][7].upper()}",
              value= f"> **{result[i][4]}** \n > **Dungeon:** {result[i][5]} \n > **Zone:** {result[i][6]}"
          ) 
          if i%2:
            embed.add_field(name='\u200b',value='\u200b',inline=False)
        cursor.close()
      else:
        #Show the slot 
        qry = (
          f"""select s.setname,si.setitemname,d.dungeonname,d.areaname,sl.slotname
              FROM ref_sets s
              LEFT JOIN ref_setitems si ON s.setid = si.setid
              LEFT JOIN ref_dungeons d  ON si.dungeonid = d.dungeonid
              LEFT JOIN ref_slots sl ON si.slotid = sl.slotid
              WHERE s.setid = {int(set.value)} AND sl.slotid = {int(slot.value)}"""
        )
        cursor.execute(qry)
        result = cursor.fetchone()
        s_name = result[0]
        si_name = result[1]
        si_dung = result[2]
        si_area = result[3]
        si_slot = result[4]
        
        embed = discord.Embed(
            title=f"{si_name} ({si_slot})",
            description=f"**SET:** {s_name}",
            color=0x00bb35
        )
        embed.add_field(
            name="DUNGEON",
            value= f"> {si_dung}"
        )
        embed.add_field(
            name="ZONE",
            value= f"> {si_area}"
        )
        cursor.close()
      embed.set_footer(
          text="ChaosEngine Developed by: GenXWhatever (Lysander)",
          icon_url="https://cdn.discordapp.com/avatars/386200837896011776/4e381a02c13346fc011f6e862acec87a.png"
      )
      await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Setinfo(client))