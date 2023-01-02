import discord
from discord.ext import commands
from discord import app_commands

class TopTen(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        print("register.py LOADED!")

    @app_commands.command(name="top", description="Top 10 Players in your Clan")
    @app_commands.describe(stat='by Stat')
    @app_commands.choices(stat=[
        discord.app_commands.Choice(name='Paragon', value="plvl"),
        discord.app_commands.Choice(name='Combat Rating', value="cr"),
        discord.app_commands.Choice(name='Resonance', value="reso"),
        discord.app_commands.Choice(name='Damage', value="dmg"),
        discord.app_commands.Choice(name='Life', value="life")
    ])
    async def topten(self, interaction: discord.Interaction, stat: discord.app_commands.Choice[str]):
        data = self.client.db
        #Check if they're a valid (registered)
        data.reconnect()
        qry = (f"SELECT count(*) from users where d_uid = '{interaction.user.id}' and d_gid = '{interaction.guild_id}'")
        cursor = data.cursor()
        cursor.execute(qry)
        if cursor.fetchall()[-1][-1] > 0:
            #Already Registered -- DO THE THING
            qry = (f"select charname,plvl,dmg,life,cr,reso from users where d_gid = '{interaction.guild_id}' order by {stat.value} DESC LIMIT 10")
            cursor.execute(qry)
            results = cursor.fetchall()
            if stat.value == "plvl":
                sort_type = "PARAGON LEVEL"
            elif stat.value == "dmg":
                sort_type = "DAMAGE"
            elif stat.value == "life":
                sort_type = "LIFE"
            elif stat.value == "cr":
                sort_type = "COMBAT RATING"
            elif stat.value == "reso":
                sort_type = "RESONANCE"
            brk = "+----+-------------------+---------+---------+---------+---------+---------+\n"
            msg = f"Top 10 Players **BY {sort_type}**\n```{brk}| ## | PlayerName        | Paragon | CR      | Dmg     | Life    | Reso    |\n{brk}"
            for i, player in enumerate(results, start=1):
                msg = msg + f"""| {i:<2} | {player[0]:<17} | {player[1]:<7} | {player[2]:<7} | {player[3]:<7} | {player[4]:<7} | {player[5]:<7} |\n{brk}"""
            msg = msg + "```"
            await interaction.response.send_message(msg)
        else:
            #Not Registered Yet
            await interaction.response.send_message(f"You're not registered yet, try `/register`")
        cursor.close()

async def setup(client: commands.Bot) -> None:
  await client.add_cog(TopTen(client))