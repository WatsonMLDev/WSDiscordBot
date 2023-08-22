import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Greedy, Context
from typing import Optional, Literal
import Utils.Database.wsDb as wsDb
from DiscordFiles.Buttons.WsModalButtons import WsEnterQueue
from DiscordFiles.Buttons.configViews import ConfigRoleView
from Utils.Token.Token import get_token

intents = discord.Intents(bans=True, emojis=True, emojis_and_stickers=True, guild_messages=True,
                          guild_reactions=True, guilds=True, integrations=True, members=True, messages=True,
                          presences=True, reactions=True, message_content=True)


class Main(commands.Bot):
    def __init__(self):
        # loads the bot with the prefix $ and the intents
        super().__init__(command_prefix="$", intents=intents)

        # initializes the session and Cogs
        self.session = None
        self.initial_extensions = ['DiscordFiles.Cogs.UtilCommands', 'DiscordFiles.Cogs.WsCog']

        # initializes the WS database
        self.ws_db = wsDb.WsDb()

    async def setup_hook(self) -> None:

        # loads the Cogs
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        # loads PRE-EXISTING WS messages and re-attaches button functionality to them
        for ws in self.ws_db.get_all_ws():
            if ws['msgID'] == -1:
                continue
            name = ws['name']
            size = ws['size']
            start_date = ws['startDate']
            wsID = ws.doc_id

            # adds the button functionality back to the message
            self.add_view(WsEnterQueue(name, size, start_date, self, wsID), message_id=ws['msgID'])

    async def close(self):
        # self.google_drive.upload_db_files()
        await super().close()
        await self.session.close()

bot = Main()

# command to sync the slash commands to the discord server (created by Rapptz)
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
        ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    await ctx.send("Syncing commands...")

    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

@bot.command()
async def config(ctx: Context,):
    await ctx.send('Configuring bot...', ephemeral=True, delete_after=5*60, view=ConfigRoleView(bot, ctx))

bot.run(get_token())