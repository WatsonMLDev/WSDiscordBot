from discord import app_commands
import discord


def owner_only():
    async def actual_check(interaction: discord.Interaction):
        return interaction.guild.owner_id == interaction.user.id

    return app_commands.check(actual_check)


def admin_only():
    async def actual_check(interaction: discord.Interaction):
        return interaction.user.guild_permissions.administrator

    return app_commands.check(actual_check)


