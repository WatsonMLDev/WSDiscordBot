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
    start_date = ui.TextInput(label='Anticipated Start Date', style=discord.TextStyle.short,
                              placeholder='yyyy-MM-DD',
                              default='2000-01-01', max_length=10)
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
        embed.add_field(name='Anticipated Start Date:', value=self.start_date.value, inline=False)
        embed.add_field(name='White Star Slot:', value=self.ws, inline=False)
        embed.add_field(name='Please enter the queue by pressing the button below', value="_ _", inline=False)
        embed.set_footer(text='# of people in {} queue: {}'.format(self.name.value, 0))

        #send the message and save the WS contents from the modal in the database
        await interaction.response.send_message(embed=embed, ephemeral=False)
        original_message = await interaction.original_response()
        bot.ws_db.set_msgID(self.ws, original_message.id)
        bot.ws_db.set_name(self.ws, self.name.value)
        bot.ws_db.set_startDate(self.ws, self.start_date.value)

        #edit the message to add the buttons
        await original_message.edit(
            view=WsEnterQueue(self.name.value, self.start_date.value, bot, self.ws))


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

        await interaction.response.send_message("Ending WS {}".format(ws.value), ephemeral=True)

        #delete the message and null the WS in the database
        embed_id = self.bot.ws_db.get_msgID(ws.value)
        discord_message = await interaction.channel.fetch_message(embed_id)
        await discord_message.delete()
        bot.ws_db.set_msgID(ws.value, -1)
        bot.ws_db.set_name(ws.value, "")
        bot.ws_db.set_startDate(ws.value, "")
        bot.ws_db.set_players(ws.value, [])

    #TODO: do this automatically, need to have a way of setting user made roles for each WS Slot through a config command
    @app_commands.command(name="ws-add-role", description='adds a role to players in white star queue')
    @admin_only()
    async def ws_add_role(self, interaction: discord.Interaction, ws_id: int, role: discord.Role):
        await interaction.response.send_message("Adding role {} to players in WS {}".format(role.name, ws_id),
                                                ephemeral=True)

        players = self.bot.ws_db.get_players(ws_id)
        for player in players:
            await interaction.guild.get_member(player).add_roles(role)
        await interaction.followup.send(
            "Added role {} to all {} players in WS {}".format(role.name, len(players), ws_id), ephemeral=True)

    #TODO: do this automatically, need to have a way of setting user made roles for each WS Slot through a config command
    @app_commands.command(name="ws-remove-role", description='removes a role from players in white star queue')
    @admin_only()
    async def ws_remove_role(self, interaction: discord.Interaction, ws_id: int, role: discord.Role):
        await interaction.response.send_message("Removing role {} from players in WS {}".format(role.name, ws_id),
                                                ephemeral=True)

        players = self.bot.ws_db.get_players(ws_id)
        for player in players:
            await interaction.guild.get_member(player).remove_roles(role)
        await interaction.followup.send(
            "Removed role {} from all {} players in WS {}".format(role.name, len(players), ws_id), ephemeral=True)


