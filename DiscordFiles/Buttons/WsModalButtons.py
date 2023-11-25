import discord


class WsEnterQueue(discord.ui.View):
    def __init__(self, name, start_date, bot, ws):
        super().__init__(timeout=None)
        self.name = name
        self.start_date = start_date
        self.bot = bot
        self.ws = ws

    @discord.ui.button(label='Enter/Exit Ws Queue', style=discord.ButtonStyle.green, custom_id='ws_queue')
    async def enter_queue(self, interaction: discord.Interaction, button: discord.ui.Button):

        already_in_queue = self.bot.ws_db.get_players(self.ws)

        bugged_role = False
        bad_permissions = False
        if interaction.user.id not in already_in_queue:

            self.bot.ws_db.add_player(self.ws, interaction.user.id)

            roles = self.bot.ws_db.get_role_IDs(self.ws)
            roles = [interaction.guild.get_role(role) for role in roles]
            for role in roles:
                try:
                    await interaction.user.add_roles(role)
                except (AttributeError):
                    bugged_role = True
                except (discord.errors.Forbidden):
                    bad_permissions = True


            await interaction.response.send_message('You have entered the queue', ephemeral=True, delete_after=30)
        else:
            self.bot.ws_db.remove_player(self.ws, interaction.user.id)

            roles = self.bot.ws_db.get_role_IDs(self.ws)
            roles = [interaction.guild.get_role(role) for role in roles]
            for role in roles:
                try:
                    await interaction.user.remove_roles(role)
                except (AttributeError):
                    bugged_role = True
                except (discord.errors.Forbidden):
                    bad_permissions = True

            await interaction.response.send_message('You have exited the queue', ephemeral=True, delete_after=30)

        embed = discord.Embed(title='White Star Sign Up', description='_ _',
                              timestamp=interaction.created_at, color=discord.Color.green())
        embed.add_field(name='White Star Name:', value=self.name, inline=True)
        embed.add_field(name='Anticipated Start Date:', value=self.start_date, inline=False)
        embed.add_field(name='White Star Slot:', value=self.ws, inline=False)
        embed.add_field(name='Please enter the queue by pressing the button below', value="_ _", inline=False)
        embed.set_footer(text='# of people in {} queue: {}'.format(self.name, len(self.bot.ws_db.get_players(self.ws))))

        embed_id = self.bot.ws_db.get_msgID(self.ws)
        discord_message = await interaction.channel.fetch_message(embed_id)
        await discord_message.edit(embed=embed)

        if bugged_role:
            await interaction.followup.send('There was an error with the role assignment. Please contact an admin to run $config.')
        if bad_permissions:
            await interaction.followup.send('Missing permissions to assign roles. Please contact an admin to run $config and assign non-admin roles.')

    @discord.ui.button(label='WS List', style=discord.ButtonStyle.blurple, custom_id='ws_list')
    async def ws_list(self, interaction: discord.Interaction, button: discord.ui.Button):
        players = self.bot.ws_db.get_players(self.ws)
        embed = discord.Embed(title='Players in WS: {}'.format(self.bot.ws_db.get_name(self.ws)), description='_ _',
                              timestamp=interaction.created_at, color=discord.Color.green())
        for index, player in enumerate(players):
            nickname = interaction.guild.get_member(player).nick
            nickname = nickname if nickname is not None else interaction.guild.get_member(player).display_name
            embed.add_field(name="{}. @{}\n".format(index + 1, nickname), value="_ _", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=120)
