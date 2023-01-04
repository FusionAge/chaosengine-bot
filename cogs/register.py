import discord
from discord.ext import commands
from discord import app_commands
import uuid


class Register(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client
    print("register.py LOADED!")
      
  @app_commands.command(
    name="register",
    description="Register yourself with this Discord Server/Clan")
  @app_commands.describe(character_class='Choose a Class')
  @app_commands.choices(character_class=[
    discord.app_commands.Choice(name='Barbarian', value=1),
    discord.app_commands.Choice(name='Crusader', value=2),
    discord.app_commands.Choice(name='Dungeon Hunter', value=3),
    discord.app_commands.Choice(name='Monk', value=4),
    discord.app_commands.Choice(name='Necromancer', value=5),
    discord.app_commands.Choice(name='Wizard', value=6)
  ])
  async def register(self, 
                     interaction: discord.Interaction,
                     character_class: discord.app_commands.Choice[int],
                     character_name: str):
    data = self.client.db
    #Check if they're already registered
    data.reconnect()
    qry = (f"SELECT count(*) from users where d_uid = '{interaction.user.id}' and d_gid = '{interaction.guild_id}'")
    cursor = data.cursor()
    cursor.execute(qry)

    if cursor.fetchall()[-1][-1] > 0:
      #Already Registered
      await interaction.response.send_message("You're already registered! Try `/help` for more commands.")
      cursor.close()
    else:
      #Not Registered Yet
      #Does the Clan Exist yet?
      qry = (f"select count(*) from guilds where d_gid = '{interaction.guild_id}'")
      cursor.execute(qry)
      if cursor.fetchall()[-1][-1] > 0:
        #Clan Exists
        qry = (f"INSERT into users(d_uid,d_unm,d_gid,charname,classid,userid) VALUES(%s,%s,%s,%s,%s,%s)")
        val = (str(interaction.user.id), str(interaction.user),
               str(interaction.guild_id), str(character_name),
               str(character_class.value), str(uuid.uuid1()))
        data.reconnect()
        cursor.execute(qry, val)
        try:
          data.commit()
        except:
          await interaction.response.send_message(f'ERROR! Something went wrong. Sorry about that. The Botmaster has been notified.')
        else:
          await interaction.response.send_message(f'{character_name} ({character_class.name}) added successfully, use `/stats` to add your stats, or `/tool` to launch the interactive Character Editor or add your data directly (see `/help`)')
        finally:
          cursor.close()
      else:
        #Clan Doesn't Exist
        cursor.close()
        await interaction.response.send_message(f"This Clan/Discord server hasn't been setup in ChaosEngine. Try `/start`")
            
async def setup(client: commands.Bot) -> None:
  await client.add_cog(Register(client))
