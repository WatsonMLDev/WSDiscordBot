import datetime

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from DiscordFiles.Buttons.WsModalButtons import WsEnterQueue
from Utils.Checks.checks import admin_only

global bot


async def setup(bot):
    await bot.add_cog(Ws(bot))


class WsStartModal(ui.Modal, title='Questionnaire Response'):

    #items in the White Star Start modal
    name = ui.TextInput(label='White Star Name (ex. Ws1)',
                        style=discord.TextStyle.short, placeholder='Ws1', default='Ws1', min_length=3,
                        max_length=40)
    size = ui.TextInput(label='Anticipated WS Size', style=discord.TextStyle.short, placeholder='5',
                        default='5',
                        min_length=1, max_length=2)
    start_date = ui.TextInput(label='Anticipated Start Date', style=discord.TextStyle.short,
                              placeholder='yyyy-MM-DD',
                              default='2000-01-01', min_length=10, max_length=10)
    ws = ui.TextInput(label='WS Slot (1 or 2):', style=discord.TextStyle.short, placeholder='1', default='1', max_length=1)

    async def on_submit(self, interaction: discord.Interaction):
        #if the user enters an invalid WS slot, send a message and return
        if self.ws.value != '1' and self.ws.value != '2':
            await interaction.response.send_message("Invalid WS Slot", ephemeral=True, delete_after=10)
            return

        #convert the WS slot to an int
        self.ws = int(self.ws.value)

        #if the WS slot is already taken, send a message and return
        if bot.ws_db.get_msgID(self.ws) != -1:
            await interaction.response.send_message("WS Slot already taken", ephemeral=True, delete_after=10)
            return

        #create a new WS message for the WS slot
        embed = discord.Embed(title='White Star Sign Up', description='_ _',
                              timestamp=interaction.created_at, color=discord.Color.green())
        embed.add_field(name='White Star Name:', value=self.name.value, inline=True)
        embed.add_field(name='Anticipated WS Size:', value=self.size.value, inline=True)
        embed.add_field(name='Anticipated Start Date:', value=self.start_date.value, inline=False)
        embed.add_field(name='White Star Slot:', value=self.ws, inline=False)
        embed.add_field(name='Please enter the queue by pressing the button below', value="_ _", inline=False)
        embed.set_footer(text='# of people in {} queue: {}'.format(self.name.value, 0))

        #send the message to the channel in the database and save the WS contents from the modal in the database
        channel = interaction.guild.get_channel(bot.ws_db.get_msg_channel(self.ws))
        msg = await channel.send(embed=embed)
        await interaction.response.send_message("WS {} created".format(self.ws), ephemeral=True)

        original_message = await interaction.original_response()
        bot.ws_db.set_msgID(self.ws, msg.id)
        bot.ws_db.set_name(self.ws, self.name.value)
        bot.ws_db.set_size(self.ws, self.size.value)
        bot.ws_db.set_startDate(self.ws, self.start_date.value)

        #edit the message to add the buttons
        await msg.edit(
            view=WsEnterQueue(self.name.value, self.size.value, self.start_date.value, bot, self.ws))


class Ws(commands.Cog):
    def __init__(self, discord_bot) -> None:
        self.bot = discord_bot

        #set bot object to be global for the modal to access
        global bot
        bot = discord_bot

        super().__init__()

    @app_commands.command(name="ws-start", description='starts a white star queue')
    @admin_only()
    async def ws_start(self, interaction: discord.Interaction):
        await interaction.response.send_modal(WsStartModal())

    @app_commands.command(name="ws-end", description='ends a white star queue')
    @admin_only()
    @app_commands.choices(ws=[
        discord.app_commands.Choice(name="Ws1", value=1),
        discord.app_commands.Choice(name="Ws2", value=2)])
    async def ws_end(self, interaction: discord.Interaction, ws: discord.app_commands.Choice[int]):
        #if the WS slot the user specifys is not active, send an error message and return
        if bot.ws_db.get_msgID(ws.value) == -1:
            await interaction.response.send_message("WS {} is not active".format(ws.value), ephemeral=True)
            return

        await interaction.response.send_message("Ending WS {}, removing WS roles from players".format(ws.value), ephemeral=True)

        #get the players and roles for the WS, remove all roles from the players
        players = bot.ws_db.get_players(ws.value)
        roles = bot.ws_db.get_role_IDs(ws.value)
        roles = [interaction.guild.get_role(role) for role in roles]

        try:
            for player in players:
                member = interaction.guild.get_member(player)
                await member.remove_roles(*roles)
        except(AttributeError):
            await interaction.followup.send("WARNING: Role not found for WS {}, contact server admin to run $config\nSkipped removing roles".format(ws.value))
        except(discord.errors.Forbidden):
            await interaction.followup.send("WARNING: Bot does not have permission to remove roles, contact server admin to run $config and remove admin roles\nSkipped removing roles")

        #delete the message and null the WS in the database
        embed_id = self.bot.ws_db.get_msgID(ws.value)
        discord_message = await interaction.channel.fetch_message(embed_id)
        await discord_message.delete()
        bot.ws_db.set_msgID(ws.value, -1)
        bot.ws_db.set_name(ws.value, "")
        bot.ws_db.set_size(ws.value, 0)
        bot.ws_db.set_startDate(ws.value, "")
        bot.ws_db.set_players(ws.value, [])
