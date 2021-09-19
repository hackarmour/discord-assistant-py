import discord, sys, datetime, json, asyncio
from discord.ext import commands
from time import time
from discord_components import Button, ButtonStyle, Select, SelectOption, InteractionType


class Miscellaneous(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        with open("Configuration/config.json") as f:
            cfg = json.load(f)
            self.fail_emoji = cfg["fail_emoji"]
            self.success_emoji = cfg["success_emoji"]
            embed_color = cfg["embed_color"]
            self.r = embed_color[0]
            self.g = embed_color[1]
            self.b = embed_color[2]
            self.STARTTIME = cfg["starttime"]

    ## ==> AVATAR
    # =============================================================================================

    @commands.command(
        aliases=['av'],
        help="""
` `- **To get the profile picture of a member**
` `
` `- If you don't pass the user, your profile picture will be given
"""
    )
    async def avatar(self, ctx: commands.Context, *, user: commands.MemberConverter = None) -> None:
        if user is None: user = ctx.author
        embed = disco
        rd.Embed(color=user.color, title="AVATAR")
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    # =============================================================================================

    ## ==> HELP COMMAND
    # =============================================================================================

#     @commands.command()
#     async def help(self, ctx: commands.Context) -> None:
#
#         ## ==> SELECT WIDGET
#         # ============================================
#
#         select = Select(
#             placeholder="Choose what you want help with!",
#             options=[
#                 SelectOption(
#                     label="Moderation",
#                     value="Moderation",
#                     description="Get help with Moderation",
#                     emoji="🧐"
#                 ),
#                 SelectOption(
#                     label="Logs",
#                     value="Logs",
#                     description="Get help with Logs",
#                     emoji="🔍"
#                 ),
#                 SelectOption(
#                     label="Fun",
#                     value="Fun",
#                     description="Get help with Fun",
#                     emoji="😄"
#                 ),
#                 SelectOption(
#                     label="Leveling"
#                     value="Leveling",
#                     description="Get help with Leveling",
#                     emoji="📈"
#                 ),
#                 SelectOption(
#                     label="Music",
#                     value="Music",
#                     description="Get help with Music",
#                     emoji="🎶"
#                 ),
#                 SelectOption(
#                     label="LON",
#                     value="LON",
#                     description="Get help with LON",
#                     emoji="😃"
#                 ),
#                 SelectOption(
#                     label="Miscellaneous",
#                     value="Miscellaneous",
#                     description="Get help with Other Commands",
#                     emoji="⚪"
#                 ),
#                 SelectOption(
#                     label="Configuration",
#                     value="Configuration",
#                     description="Get help with Configuration",
#                     emoji="⚙"
#                 )
#             ]
#         )
#
#         # ============================================
#
#         ## ==> EMBEDS DICTIONARY
#         # ============================================
#
#         embeds = {
#             "Configuration": discord.Embed(
#                 title="WELCOMER",
#                 color=discord.Color.from_rgb(self.r, self.g, self.b),
#                 description=f"""
# **Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**
#
# • <a:gearSpinning:873882264134643712> `welcomer [configuration] [value]`
# ```
# To Configure Welcomer
#
# Needs Administrator Permission
#
# Examples:
# {self.bot.command_prefix(self.bot, ctx.message)}welcomer welcome-message Hey |user|, Welcome to |guild|^
# {self.bot.command_prefix(self.bot, ctx.message)}welcomer leave-message |user| left |guild|^
# {self.bot.command_prefix(self.bot, ctx.message)}welcomer channel #welcomer
# {self.bot.command_prefix(self.bot, ctx.message)}welcomer enable true
# {self.bot.command_prefix(self.bot, ctx.message)}welcomer enable false
# ```
#
# • <a:gearSpinning:873882264134643712> `logs [configuration] [value]`
# ```
# To Configure Logs
#
# Needs Administrator Permsission
#
# Examples:
# {self.bot.command_prefix(self.bot, ctx.message)}logs channel #logs
# {self.bot.command_prefix(self.bot, ctx.message)}logs enable true
# {self.bot.command_prefix(self.bot, ctx.message)}logs enable false
# ```
#
# • :bar_chart: `ToggleLeveling`
# ```
# To Toggle Leveling
#
# Needs Administrator Permission
# ```
#
# • :face_with_symbols_over_mouth: `ToggleAutoMod`
# ```
# To Toggle AutoMod
#
# Needs Manage Messages Permission
# ```
# """
#             ).set_footer(text="^ \"|user|\" and \"|guild|\" are keywords and are required in these configurations"),
#             "Moderation": discord.Embed(
#                 title="MODERATION",
#                 color=discord.Color.from_rgb(self.r, self.g, self.b),
#                 description="""
# **Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**
#
# • :x: `ban [member] (reason)`
# ```
# To Ban a member
#
# Needs Ban Members Permission
# ```
#
# • :rage: `kick [member] (reason)`
# ```
# To Kick a member
#
# Needs Kick Members Permission
# ```
#
# • :white_check_mark: `unban [[username#discriminator] OR [UserID]]`
# ```
# To Unban a member
#
# Needs Unban Members Permission
# ```
#
# • :mute: `mute [member] [time] (reason)`
# ```
# To Mute a member
#
# Needs Mute Members Permission
#
# time:
# s, m, h, d, w
# ```
#
# • :loud_sound: `unmute [member]`
# ```
# To Unmute a member
#
# Needs Mute Members Permission
# ```
#
# • :x: `purge (number)`
# ```
# To clear number amount of messages
#
# Needs Manage Messages Permission
#
# default is 5
# ```
# """
#             ),
#             "Fun": discord.Embed(
#                 title="FUN",
#                 color=discord.Color.from_rgb(self.r, self.g, self.b),
#                 description="""
# **Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**
#
# • :rock: `rps [member]`
# ```
# To play Rock-Paper-Scissors with a member
# ```
#
# • :o:`ttt [member]`
# ```
# To play Tic-Tac-Toe with a member
# ```
#
# • :question: `8ball [question]`
# ```
# Get a random answer of your question
# ```
#
# • :coin: `coin`
# ```
# Tosses an imaginary coin
# ```
#
# • :regional_indicator_f: `f (reason)`
# ```
# press F to pay respect
# ```
#
# • :joy: `meme`
# ```
# I will meme for you
# ```
# """
#             ),
#             "Leveling": discord.Embed(
#                 title="LEVELING",
#                 color=discord.Color.from_rgb(self.r, self.g, self.b),
#                 description="""
# **Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**
#
# • :chart_with_upwards_trend: `rank (member)`
# ```
# To get the rank card of a member
#
# Defaults to the member who ran the command
# ```
#
# • :chart_with_upwards_trend: `lb`
# ```
# To get the leaderboards of your server
# ```
# """
#             ),
#
#             "Music": discord.Embed(
#                 title="MUSIC",
#                 color=discord.Color.from_rgb(self.r, self.g, self.b),
#                 description="""
# **Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**
#
# • :notes: `p [Music Name]`
# ```
# To Play Music
#
# You need to be connected to a VC before running this
# ```
#
# • :notepad_spiral: `q`
# ```
# To get the current queue
# ```
#
# • :arrow_right: `skip`
# ```
# To Skip the current song
# ```
#
# • :pause_button: `pause`
# ```
# To pause the playback of music
# ```
#
# • :arrow_forward: `resume`
# ```
# To resume the playback of music
# ```
#
# • :no_entry_sign: `disconnect`
# ```
# To stop the music and disconnect from your VC
# ```
# """
#             ),
#             "LON": discord.Embed(
#                 title="**L**ACK **O**F **N**ITRO",
#                 color=discord.Color.from_rgb(self.r, self.g, self.b),
#                 description="""
# **Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**
#
# • :smile: `LON [emoji name]`
# ```
# To send a webhook with emoji
# ```
#
# • :smile: `LONall`
# ```
# To send all available emojis
# ```
# """
#             ),
#             "Miscellaneous": discord.Embed(
#                 title="MISCELLANEOUS",
#                 color=discord.Color.from_rgb(self.r, self.g, self.b),
#                 description="""
# **Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**
#
# • :sunglasses: `avatar (member)`
# ```
# To get the avatar of a member
#
# Defaults to the person who ran this command
# ```
#
# • :diamond_shape_with_a_dot_inside: `help`
# ```
# This command
# ```
#
# • :grey_question: `about (member)`
# ```
# To get the Info about a member
#
# Defaults to the person who ran this command
# ```
#
# • :grey_exclamation: `stats`
# ```
# To get my stats
# ```
# """
#             )
#         }
#
#         # ============================================
#
#         ## ==> SEND MESSAGE
#         # ============================================
#
#         msg = await ctx.send(
#             embed=discord.Embed(
#                 title="HELP",
#                 color=discord.Color.from_rgb(self.r, self.g, self.b),
#                 description="What do you want help with?"
#             ),
#             components=[
#                 select,
#                 [
#                     Button(
#                         label="Vote On Top.gg",
#                         style=ButtonStyle.URL,
#                         url="https://top.gg/bot/845154524997877770",
#                         emoji="🔗"
#                     )
#                 ]
#             ]
#         )
#
#         # ============================================
#
#         ## ==> CHECK FOR REACTION AND EDIT THE EMBED
#         # ============================================
#
#         while True:
#             try:
#                 reaction = await self.bot.wait_for(
#                     "select_option",
#                     timeout=60.0,
#                     check=lambda i: i.user == ctx.author
#                 )
#             except asyncio.TimeoutError:
#                 select.disabled = True
#                 await msg.edit(components=[select])
#                 break
#             except discord.HTTPException:
#                 pass
#             try:
#                 await reaction.respond(
#                     type=InteractionType.UpdateMessage,
#                     embed=embeds[reaction.component[0].label]
#                 )
#             except discord.NotFound: pass
#             except discord.HTTPException:
#                 pass

        # ============================================

    # =============================================================================================

    ## ==> STATS
    # =============================================================================================

    @commands.command(
        help="""
` `- **To get the stats of Assistant**
"""
    )
    async def stats(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title="STATS",
            color=discord.Color.from_rgb(self.r, self.g, self.b),
            inline=False
        )
        embed.add_field(
            inline=False,
            name=":arrow_up: UPTIME",
            value=f"```\n{str(datetime.timedelta(seconds=int(round(time() - self.STARTTIME))))}\n```"
        )
        embed.add_field(
            inline=False,
            name=":ping_pong: PING",
            value=f"```\n{round(self.bot.latency * 1000)}ms\n```"
        )
        embed.add_field(
            inline=False,
            name="<:Discordlogo:843715679920193596> DISCORD.PY VERSION",
            value=f"```\n{discord.__version__}\n```"
        )
        embed.add_field(
            inline=False,
            name="<:pythonlogo:843714646832709673> PYTHON VERSION",
            value=f"```\n{str(sys.version[:6])}\n```"
        )
        embed.add_field(
            inline=False,
            name="<:HomeServerLogo:843716672094339073> SERVER",
            value=f"```\n{ctx.guild}\n```"
        )
        embed.add_field(
            inline=False,
            name='<:HomeServerLogo:843716672094339073> TOTAL SERVERS',
            value=f'```\n{str(len(self.bot.guilds))}\n```'
        )
        devs = [
            str(await self.bot.fetch_user(754894159403286531)),
            str(await self.bot.fetch_user(510480545160101898)),
            str(await self.bot.fetch_user(628575263818514444))
        ]
        embed.add_field(
            inline=False,
            name="<:source_code1600:843715185277534238> DEVELOPERS",
            value="```\n{}\n```".format("\n".join(devs))
        )
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/616315208251605005/616319462349602816/Tw.gif")
        await ctx.send(
            embed=embed,
            components=[[
                Button(
                    label="Invite",
                    style=ButtonStyle.URL,
                    url="https://discord.com/oauth2/authorize?client_id=845154524997877770&permissions=-9&scope=bot",
                    emoji="🔗"
                ),
                Button(
                    label="Patreon",
                    style=ButtonStyle.URL,
                    url="https://www.patreon.com/hackarmour",
                    emoji="🔗"
                )
            ]]
        )

    # =============================================================================================

    ## ==> USER INFO
    # =============================================================================================

    @commands.command(
        aliases=['abt'],
        help="""
` `- **To get info about a member**
` `
` `- **If nothing is passed then info on author will be given**
"""
    )
    async def about(self, ctx: commands.Context, user: commands.MemberConverter = None) -> None:
        if user is None: user = ctx.author

        embed = discord.Embed(title=f"{str(user).upper()}", color=user.color)
        embed.add_field(name="Discriminator", value=str(user.discriminator))
        embed.add_field(name="User ID", value=str(user.id))
        embed.add_field(name="Created at", value=str(user.created_at.strftime("%a %#d %B %Y, %I:%M %p UTC")))
        embed.add_field(name="Joined at", value=str(user.joined_at.strftime("%a %#d %B %Y, %I:%M %p UTC")))
        try: embed.add_field(name="Roles", inline=False, value=str(" **|** ".join(j.mention for j in [i for i in user.roles])))
        except Exception:
            embed.add_field(name="Roles", inline=False, value="Too Many Roles")
        embed.add_field(name="Top Role", value=str(user.top_role.mention))
        if user.guild.owner.id == user.id:
            embed.add_field(name="Owner", value=f"{user.mention} is the owner of {user.guild}", inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/616315208251605005/616319462349602816/Tw.gif")
        await ctx.send(embed=embed)

    # =============================================================================================


## ==> ADDING THE COG TO BOT
# =============================================================================================

def setup(bot: commands.Bot) -> None: bot.add_cog(Miscellaneous(bot))

# =============================================================================================
