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

    @app_commands.command(name="help", description='shows a list of commands')
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Commands", description="List of commands", color=0x00ff00)
        embed.add_field(name="ping", value="safe command to use to see if bot is up, also shows latency", inline=False)
        embed.add_field(name="help", value="shows a list of commands", inline=False)
        embed.add_field(name="ws-start", value="starts a white star for a given slot", inline=False)
        embed.add_field(name="ws-end", value="ends a specific white star and removed ws roles", inline=False)






