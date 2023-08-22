import discord
from discord.ext import commands
from discord import app_commands

from DiscordFiles.Buttons.configViews import ConfigRoleView


async def setup(bot):
    await bot.add_cog(Builder_Utils(bot))


class Builder_Utils(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="ping", description='safe command to use to see if bot is up, also shows latency')
    async def greet(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong!!!, {}'.format(round(self.bot.latency, 1)))







