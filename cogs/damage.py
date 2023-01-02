import discord
from discord.ext import commands
from discord import app_commands

class Damage(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client
    print("damage.py LOADED!")

  @app_commands.command(
    name="damage",
    description="Update your Damage rating")

  async def damage(self, interaction: discord.Interaction,damage: int):
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
        qry = (f"update users set dmg = {damage} where d_uid = %s and d_gid = %s")
        val = (str(interaction.user.id), str(interaction.guild_id))
        try:
          cursor.execute(qry,val)
          data.commit()
        except:
          await interaction.response.send_message(f'ERROR! Something went wrong. Sorry about that. The Botmaster has been notified.')
        else:
          await interaction.response.send_message(f'Damage rating updated to {damage}!')
        finally:
          cursor.close()
      else:
        #USER is Unregistered
        await interaction.response.send_message("ChaosEngine doesn't recognize you, try `/register`") 
    else:
      #CLAN is Unregistered
      await interaction.response.send_message("ChaosEngine doesn't recognize this clan/server, try `/start`")  

async def setup(client: commands.Bot) -> None:
  await client.add_cog(Damage(client))