import discord
from discord.ext import commands
from discord import app_commands
import uuid
import os

class Tool(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client
    print("tool.py LOADED!")
      
  @app_commands.command(name="tool",description="Web-based tool for easier updating and additional functions")
  async def tool(self, interaction: discord.Interaction):
    #SETUP
    channel = self.client.get_channel(int(os.environ['CHAN_ERRORS'])) 
    data = self.client.db
    data.reconnect()
    cursor = data.cursor()
    #Make Sure this is a valid Server & user is registered
    qry = (f"SELECT count(*) from guilds where d_gid = '{interaction.guild_id}'")
    cursor = self.client.db.cursor()
    cursor.execute(qry)
    if cursor.fetchall()[-1][-1] > 0:
      #VALID Clan
        qry = (f"SELECT count(*) from users where d_gid = '{interaction.guild_id}' and d_uid = '{interaction.user.id}'")
        cursor = self.client.db.cursor()
        cursor.execute(qry)
        if cursor.fetchall()[-1][-1] == 0:
          #INVALID User
          await interaction.response.send_message(f'You appear to be unregistered, have you tried `/register`?')
        else:
          #VALID User
          #CLEAR ANY EXISTING SESSIONS
          delqry = f"DELETE FROM tmp_weblinks WHERE uid in (SELECT uid from users where d_uid = '{interaction.user.id}' and d_gid = '{str(interaction.guild.id)}')"
          try:
            cursor.execute(delqry)
            data.commit()
          except:
            await channel.send(content=f"Error in tool.py deleting session. Query: {delqry} with values")
            await interaction.response.send_message(f'ERROR! Something went wrong deleting old sessions. Sorry about that. The Botmaster has been notified.')
          else:
            thisuuid = uuid.uuid1()
            insqry = f"INSERT INTO tmp_weblinks(tmp_uuid,uid) SELECT '{thisuuid}',uid from users where d_uid ='{str(interaction.user.id)}' and d_gid ='{str(interaction.guild.id)}'"
            try:
              cursor.execute(insqry)
              data.commit()
            except:
              await channel.send(content=f"Error in tool.py creating session. Query: {insqry}")
              await interaction.response.send_message(f'ERROR! Something went wrong creating a session. Sorry about that. The Botmaster has been notified.')
            else:
              user = self.client.get_user(interaction.user.id)
              dm_channel = await user.create_dm()
              await dm_channel.send(f"Here's your link: {os.environ['BASE_URL']}/mystats/{thisuuid}")
              await interaction.response.send_message(f'Sent you a link via DM!',ephemeral=True)
          finally:
            cursor.close()        
    else:
      #INVALID Clan
      await interaction.response.send_message("This discord/server doesn't exist ChaosEngine! Try `/start`")
    
async def setup(client: commands.Bot) -> None:
  await client.add_cog(Tool(client))