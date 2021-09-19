import discord, json, asyncio, sqlite3
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        ## ==> DATA FROM CONFIG
        # ============================================

        with open("Configuration/config.json") as f:
            cfg = json.load(f)
            self.fail_emoji = cfg["fail_emoji"]
            self.success_emoji = cfg["success_emoji"]
            self.stonks_emoji = cfg["stonks_emoji"]
            embed_color = cfg["embed_color"]
            self.r = embed_color[0]
            self.g = embed_color[1]
            self.b = embed_color[2]

        # ============================================

        ## ==> ILLEGAL WORDS
        self.illegal_words = ['Nigger', 'Nigga', 'N1gg3r', 'N1gger', 'Nigg3r', 'N1gga', 'N1gg@', 'Dick', 'Fuck', 'F U C K', 'f u c k', 'gandu', 'gaandu', 'gaamdu', 'fuck', 'nigger', 'nigga', 'n1gg3r', 'n1gga', 'n1gg@', 'dick']

        self.conn = sqlite3.Connection("Configuration/Moderation.db")

    ## ==> ON MESSAGE
    # =============================================================================================

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot: return

        c = self.conn.cursor()

        c.execute(
            """
            SELECT "automod" FROM "moderation"
            WHERE guild_id = :guild_id
            """,
            {"guild_id": str(message.guild.id)}
        )

        if (fetches := c.fetchall()) is None: return

        elif fetches[0] == 1:
            ## ==> IF THE MESSAGE CONTAINS ILLEGAL WORDS
            if any(word in message.content for word in self.illegal_words):
                user = message.author

                ## ==> DELETING MESSAGE
                await message.delete()

                ## ==> MUTED ROLE
                role = discord.utils.get(message.guild.roles,name='Muted')

                ## ==> IF MUTED ROLE DOESN'T EXIST, BOT CREATES IT
                if role is None:

                    ## ==> CREATE ROLE
                    role = await message.author.guild.create_role(name="Muted")

                    ## ==> CHANGE PERMS
                    for channel in message.author.guild.channels:
                        await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

                ## ==> ADD ROLES
                if role not in message.author.roles:
                    await message.author.add_roles(role)

                ## ==> DM'ing THE USER
                await user.send('Your message was deleted due to use of profane and illegal words and you are temporarily muted for 10 minutes.')

                ## ==> TIMER
                await asyncio.sleep(600.0)

                ## ==> REMOVE ROLE
                if role in message.author.roles:
                    try: await message.author.remove_roles(role)
                    except Exception: pass

        elif f"<@!{self.bot.user.id}>" in message.content:
            try:
                await message.channel.send(
                    embed=discord.Embed(
                        title=f"Hi! I'm {str(self.bot.user.name)}",
                        description=f"You can use `{self.bot.command_prefix(self.bot, message)}help` to get help with my commands",
                        color=discord.Color.from_rgb(self.r, self.g, self.b)
                    )
                )
            except discord.Forbidden:
                pass

    # =============================================================================================
    
    ## ==> KICK
    # =============================================================================================

    @commands.command(
        help="""
` `- **To Kick a member**
"""
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, user: commands.MemberConverter, reason=None):
        if user == ctx.author:
            await ctx.send("You can't kick yourself!")
            return
        await user.kick(reason=reason)
        await ctx.send(f"{user} has been Kicked")

    # =============================================================================================

    ## ==> BAN
    # =============================================================================================

    @commands.command(
        help="""
` `- **To Ban a member**
"""
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: commands.MemberConverter, *, reason=None) -> None:
        if user == ctx.author:
            await ctx.send("You can't ban yourself!")
            return
        await user.ban(reason=reason)
        await ctx.send(f'The Ban hammer was used on {user}')

    # =============================================================================================

    ## ==> UNBAN
    # =============================================================================================

    @commands.command(
        help="""
` `- **To Unban a member**
` `
` `- Pass either the user ID or the username#discriminator
"""
    )
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, *, member) -> None:

        banned_users = await ctx.guild.bans()

        ## ==> BAN WITH ID
        # ============================================

        if member.isdigit():
            member = await self.bot.fetch_user(member)
            if member in banned_users:
                await ctx.send(f"{member.name} is not banned!")
            else:
                await ctx.guild.unban(member)
                await ctx.send(f"Unbanned {member.name}")

        # ============================================

        ## ==> BAN WITH USERNAME
        # ============================================
        else:
            member_name, member_disc = member.split('#')

            for banned_entry in banned_users:

                user = banned_entry.user

                if (user.name, user.discriminator) == (member_name, member_disc):
                    await ctx.guild.unban(user)
                    await ctx.send(f'{user.name} has been unbanned')
                    return

            await ctx.send(member+'was not found')

        # ============================================

    # =============================================================================================

    ## ==> MUTE
    # =============================================================================================

    @commands.command(
        help="""
` `- **To Mute a member**
"""
    )
    @commands.has_guild_permissions(mute_members=True)
    async def mute(self, ctx, user: commands.MemberConverter = None, time=None, *, reason=None):

        ## ==> CHECKS
        # ============================================

        if user is None:
            await ctx.send("You must mention a member to mute!")
            return
        elif time is None:
            await ctx.send("Please mention a time!")
            return

        count = 0
        for i in time:
            if i.isalpha():
                count += 1
        if count > 1:
            await ctx.send("Please mention a valid time!")
        elif user == ctx.author:
            await ctx.send("You can't mute yourself!")

        # ============================================

        else:
            if reason is None:
                reason = "Unspecified"

            ## ==> CHANGE time TO SECONDS
            # ============================================

            digits = time[:-1]
            duration = time[-1]
            if duration == 's':
                seconds = digits
            elif duration == 'm':
                seconds = int(digits) * 60
            elif duration == 'h':
                seconds = int(digits) * 3600
            elif duration == 'd':
                seconds = int(digits) * 86400
            elif duration == 'w':
                seconds = int(digits) * 604800
            else:
                await ctx.send("Invalid duration input")
                return

            # ============================================

            ## ==> MUTED ROLE
            # ============================================

            Muted = discord.utils.get(ctx.guild.roles, name="Muted")
            if Muted is None:
                Muted = await ctx.guild.create_role(name="Muted")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(Muted, speak=False, send_messages=False)

            # ============================================

            ## ==> MUTE USER
            # ============================================

            if Muted not in user.roles:
                await user.add_roles(Muted)
                await ctx.send(f"{str(user)[:-5]} has been muted for {time}.")
                await user.send(f"You are muted from the server for {time}\nReason: {reason}")
                await asyncio.sleep(int(seconds))
            else:
                await ctx.send("Member is already muted")
                return

            if Muted in user.roles:
                await user.remove_roles(Muted)
                await ctx.send(f"{str(user)[:-5]} has been unmuted after {time}.")
                await user.send(f"You have been unmuted from {ctx.guild.name}")
            return

            # ============================================

    # =============================================================================================

    ## ==> AUTOMOD CONFIG
    # =============================================================================================

    @commands.command(
        help="""
` `- **To Toggle Automod**
"""
    )
    @commands.has_permissions(manage_messages=True)
    async def ToggleAutoMod(self, ctx: commands.Context) -> None:

        ## ==> CHECKS
        if ctx.author.bot(): return

        c = self.conn.cursor()

        ## ==> CHECK IF IN GUILD IN DATA BASE
        # ============================================

        c.execute(
            """
            SELECT * FROM "moderation"
            WHERE guild_id = :guild_id
            """,
            {"guild_id": str(ctx.guild.id)}
        )

        # ============================================

        ## ==> IF DATA IN DB
        # ============================================

        if (fetches := c.fetchone()) is None:
            c.execute(
                """
                INSERT INTO "moderation" VALUES (
                    :guild_id,
                    :logs_channel,
                    :logs_enabled,
                    :automod
                )
                """,
                {
                    "guild_id": str(ctx.guild.id),
                    "logs_channel": None,
                    "logs_enabled": False,
                    "automod": (enabled := True)
                }
            )

        # ============================================

        ## ==> IF GUILD IN DB
        # ============================================

        else:
            c.execute(
                """
                UPDATE "moderation"
                SET automod = :automod
                WHERE guild_id = :guild_id
                """,
                {
                    "automod": (enabled := False if fetches[-1] == 1 else True),
                    "guild_id": str(ctx.guild.id)
                }
            )

        # ============================================

        ## ==> SEND EMBED
        # ============================================

        emoji = self.success_emoji if enabled else self.fail_emoji

        await ctx.send(
            embed=discord.Embed(
                title="AUTOMOD",
                description=f"{emoji} Automod has been {'Enabled!' if enabled else 'Disabled'}"
            )
        )

        # ============================================

    # =============================================================================================

    ## ==> UNMUTE
    # =============================================================================================

    @commands.command(
        help="""
` `- **To Unmute a member**
"""
    )
    @commands.has_guild_permissions(mute_members=True)
    async def unmute(self, ctx, user: commands.MemberConverter = None):

        ## ==> CHECKS
        # ============================================

        if user is None:
            await ctx.send("Please provide a user!")
            return

        # ============================================

        ## ==> UNMUTE
        # ============================================

        Muted = discord.utils.get(ctx.guild.roles, name="Muted")
        if Muted in user.roles:
            await user.remove_roles(Muted)
            await ctx.send(f"{str(user)[:-5]} has been unmuted.")
            await user.send(f"You have been unmuted from {ctx.guild.name}")
        else:
            await ctx.send("Member is not muted!")

        # ============================================

    # =============================================================================================

    ## ==> PURGE MESSAGES
    # =============================================================================================

    @commands.command(
        aliases=['purge'],
        help="""
` `- **To Clear some number of messages**
"""
    )
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount=5) -> None:

        ## ==> PURGE MESSAGES
        await ctx.channel.purge(limit=amount+1)

        ## ==> NOTIFY USER
        msg = await ctx.send(f'Successfully deleted {amount} messages.')

        ## ==> DELETE MSG
        await asyncio.sleep(3.0)

        try:
            await msg.delete()
        except discord.NotFound:
           return

    # =============================================================================================


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Moderation(bot))
