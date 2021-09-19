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
        embed = discord.Embed(color=user.color, title="AVATAR")
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    # =============================================================================================

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
