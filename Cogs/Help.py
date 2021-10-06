import discord
import asyncio
from discord.ext import commands
from discord_components import Select, SelectOption, InteractionType


# ==> HELP CLASS
# =============================================================================================

class Help(commands.HelpCommand):

    def get_command_signature(self, command) -> str:
        return f'{self.clean_prefix}{command.qualified_name} {command.signature}'

    async def send_bot_help(self, mapping: dict) -> None:
        channel = self.get_destination()
        pages = {}
        ctx = self.context

        for cog, command in mapping.items():
            filt = await self.filter_commands(command, sort=True)
            cmd_sign = [k.name for k in filt]
            if cmd_sign:
                name = getattr(cog, 'qualified_name', 'No Category')
                pages[name] = discord.Embed(
                    title=name,
                    description="\n\n".join(
                        [
                            f"• __**{self.get_command_signature(k)}**__\n{str(k.help).replace('~p~', self.clean_prefix)}\n" for k in filt
                        ]
                    ),
                    color=discord.Color.from_rgb(46, 49, 54)
                )
        del pages["No Category"], pages["HelpCog"]

        selectsOpts = []
        for i in range(len(pages)):
            title = pages[list(pages.keys())[i]].title
            selectsOpts.append(
                SelectOption(
                    label=title,
                    description=f"To get Help with {pages[list(pages.keys())[i]].title}",
                    value=title
                )
            )

        select = Select(
            options=selectsOpts
        )

        await channel.send(
            embed=pages[list(pages.keys())[0]],
            components=[select]
        )

        while True:
            try:
                reaction = await ctx.bot.wait_for(
                    "select_option",
                    timeout=60.0,
                    check=lambda i: i.user == ctx.author
                )
            except asyncio.TimeoutError:
                return

            try:
                await reaction.respond(
                    type=InteractionType.UpdateMessage,
                    embed=pages[reaction.component[0].label]
                )
            except discord.NotFound:
                pass
            except discord.HTTPException:
                pass


# =============================================================================================

# ==> COG
# =============================================================================================

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:

        self.bot = bot

        # ==> CHANGE HELP COMMAND
        # ============================================

        help_command = Help()
        help_command.cog = self
        bot.help_command = help_command

        # ============================================


# =============================================================================================

def setup(bot: commands.Bot) -> None:
    bot.add_cog(HelpCog(bot))
