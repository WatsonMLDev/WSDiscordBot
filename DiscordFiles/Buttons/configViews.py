from discord.ui import Button, View, RoleSelect, ChannelSelect
from discord import ui, Interaction, ButtonStyle

class ConfigRoleView(View):
    def __init__(self, bot, ctx):
        super().__init__(timeout=None)
        self.bot = bot
        self.ctx = ctx
        self.ws1_roles = []
        self.ws2_roles = []
        self.ws_channel = None

    @ui.select(cls=RoleSelect, placeholder="Select the WS Slot 1 role(s)...", min_values=1, max_values=25)
    async def ws1_role_select(self, interaction: Interaction, select: RoleSelect):
        self.ws1_roles = [role.id for role in select.values]
        await interaction.response.defer();

    @ui.select(cls=RoleSelect, placeholder="Select the WS Slot 2 role(s)...", min_values=1, max_values=25)
    async def ws2_role_select(self, interaction: Interaction, select: RoleSelect):
        self.ws2_roles = [role.id for role in select.values]
        await interaction.response.defer();

    @ui.select(cls=ChannelSelect, placeholder="Select a channel for the WS queues...")
    async def ws_channel_select(self, interaction: Interaction, select: ChannelSelect):
        self.ws_channel = select.values[0]
        await interaction.response.defer();

    @ui.button(label="Submit", style=ButtonStyle.green)
    async def submit(self, interaction: Interaction, button: Button):

        await interaction.response.defer()
        self.bot.ws_db.set_role_IDs(1, self.ws1_roles)
        self.bot.ws_db.set_role_IDs(2, self.ws2_roles)
        self.bot.ws_db.set_msg_channel(1, self.ws_channel.id)
        self.bot.ws_db.set_msg_channel(2, self.ws_channel.id)


        self.ctx.bot.tree.copy_global_to(guild=self.ctx.guild)
        synced = await self.ctx.bot.tree.sync(guild=self.ctx.guild)

        await self.ctx.send(f"Information Saved, {len(synced)} new commands re-synced with server. Type \`\\\` to see the list", ephemeral=True, delete_after=30)

        self.stop()
        await interaction.message.delete()



