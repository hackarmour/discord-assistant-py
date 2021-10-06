import discord, json, sqlite3
from discord.ext import commands
from easy_pil import Canvas, Editor, load_image_async, Font


class Welcomer(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        ## ==> GET EMOJIS AND OTHER STUFF FROM THE CFG FILE
        with open("Configuration/config.json") as f:
            cfg = json.load(f)
            self.fail_emoji = cfg["fail_emoji"]
            self.success_emoji = cfg["success_emoji"]
            self.stonks_emoji = cfg["stonks_emoji"]
            embed_color = cfg["embed_color"]
            self.r = embed_color[0]
            self.g = embed_color[1]
            self.b = embed_color[2]

        ## ==> DATABASE
        self.conn = sqlite3.Connection("Configuration/Welcomer.db")

        ## ==> CONFIG ARGS
        self.args = [
            "welcome-message", "welcome", "welcome_message",
            "leave-message", "leave", "leave_message",
            "channel", "welcomer-channel", "welcomer_channel",
            "enable",
            "welcome-card", "welcome_card", "card"
        ]

    ## ==> CARD
    # =============================================================================================

    async def card(self, member: discord.Member) -> discord.File:

        bg = Editor(canvas=Canvas((1000, 300), "#000000"))

        pfp = await load_image_async(str(member.avatar_url))

        pfp = Editor(pfp).resize((150, 150)).circle_image()

        montserrat = Font().montserrat(size = 40)
        montserrat_small = Font().montserrat(size = 30)

        ## ==> STYLING
        square = Editor(canvas=Canvas((500, 500), "#ff0000"))
        square.rotate(330, expand=True)

        bg.paste(square.image, (-350, -250))
        bg.paste(pfp.image, (30, 30))

        bg.text((200, 40), f"WELCOME {member.name}", font=montserrat, color="white")
        bg.rectangle((200, 100), width=350, height=2, fill="white")
        bg.text(
            (200,130),
            f"We Hope you enjoy your stay here!\n\nMember #{member.guild.member_count + 1}",
            font=montserrat_small,
            color="white"
        )

        return discord.File(fp=bg.image_bytes, filename="card.png")

    # =============================================================================================

    ## ==> USER JOIN
    # =============================================================================================

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:

        c = self.conn.cursor()

        ## ==> RUN A QUERY TO SEE IF WELCOMER IS ACTIVATED
        # ============================================

        c.execute(
            """
            SELECT * FROM "welcomer"
            WHERE guild_id = :guild_id
            """,
            {"guild_id": str(member.guild.id)}
        )

        # ============================================

        ## ==> CHECKS
        # ============================================

        if (fetches := c.fetchone()) is None: return

        elif fetches[4] == 0: return

        card = True if fetches[-1] == 1 else False
        channel = await self.bot.fetch_channel(int(fetches[3]))

        # ============================================

        # ==> SEND EMBED
        # ============================================

        if card:
            card = await self.card(member)
            await channel.send(
                fetches[1].replace("|user|", member.mention).replace("|guild|", str(member.guild)),
                file=card
            )
        else:
            await channel.send(
                fetches[1].replace("|user|", member.mention).replace("|guild|", str(member.guild)),
            )

        # ============================================

    # =============================================================================================

    ## ==> ON GUILD LEAVE
    # =============================================================================================

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        c = self.conn.cursor()

        ## ==> RUN A QUERY TO SEE IF WELCOMER IS ACTIVATED
        # ============================================

        c.execute(
            """
            SELECT * FROM "welcomer"
            WHERE guild_id = :guild_id
            """,
            {"guild_id": str(member.guild.id)}
        )

        # ============================================

        ## ==> CHECKS
        # ============================================

        if (fetches := c.fetchone()) is None: return

        elif fetches[4] == 0: return

        channel = await self.bot.fetch_channel(int(fetches[3]))

        # ============================================

        # ==> SEND EMBED
        # ============================================
        try:
            await channel.send(
                fetches[2].replace("|user|", str(member)).replace("|guild|", str(member.guild))
            )
        except Exception:
            return

        # ============================================

    # =============================================================================================

    ## ==> CONFIGURATION
    # =============================================================================================

    @commands.command(
        help="""
` `- **To configure Welcomer**
` `
` `- **Examples**:
`   `- ~p~welcomer welcome-message Hey |user|, welcome to |guild|
`   `- ~p~welcomer leave-message |user| left
`   `- ~p~welcomer channel #welcome
`   `- ~p~welcomer enable true
`   `- ~p~welcomer card true
"""
    )
    @commands.has_permissions(administrator=True)
    async def welcomer(self, ctx: commands.Context, thing: str = None, *, value = None) -> None:

        ## ==> CHECKS
        # =============================================================================================

        if ctx.author.bot: return

        if thing.lower() not in self.args:
            await ctx.send(
                embed=discord.Embed(
                    title="WELCOMER",
                    color=discord.Color.from_rgb(self.r, self.g, self.b),
                    description=f"""
                    {self.fail_emoji} Please use valid arguements

                    You can use the following Arguements:
                    ```
                    {", ".join(self.args)}
                    ```
                    """
                )
            )
            return

        # =============================================================================================

        c = self.conn.cursor()

        ## ==> WELCOME MESSAGE
        # =============================================================================================

        if thing.lower() in self.args[:3]:

            ## ==> CHECK IF VALUE CONTAINS |user| KEYWORD
            # ============================================

            if not value.__contains__("|user|"):

                ## ==> SEND EMBED
                await ctx.send(
                    embed=discord.Embed(
                        title="WELCOMER",
                        description=f"{self.fail_emoji} Please pass the `|user|` keyword",
                        color=discord.Color.from_rgb(self.r, self.g, self.b)
                    )
                )
                return

            # ============================================

            ## ==> UPDATE DATA
            # ============================================

            c.execute(
                """
                SELECT * FROM "welcomer"
                WHERE guild_id = :guild_id
                """,
                {"guild_id": str(ctx.guild.id)}
            )

            if c.fetchone() is not None:

                ## ==> UPDATE VALUE
                c.execute(
                    f"""
                    UPDATE "welcomer"
                    SET welcome = :welcome
                    WHERE guild_id = :guild_id
                    """,
                    {
                        "welcome": value,
                        "guild_id": str(ctx.guild.id)
                    }
                )
            else:
                c.execute(
                    """
                    INSERT INTO "welcomer" VALUES (
                        :guild_id,
                        :welcome,
                        :leave,
                        :channel,
                        :enabled,
                        :card
                    )
                    """,
                    {
                        "guild_id": str(ctx.guild.id),
                        "welcome": str(value),
                        "leave": None,
                        "channel": None,
                        "enabled": False,
                        "card": False
                    }
                )

            await ctx.send("Commiting the values")
            self.conn.commit()
            await ctx.send("Commited the values")
            c = self.conn.cursor()
            c.execute(
                "SELECT * FROM \"welcomer\""
            )
            await ctx.send(str(c.fetchall()))

            # ============================================

            await ctx.send(
                embed=discord.Embed(
                    title="WELCOMER",
                    color=discord.Color.from_rgb(self.r, self.g, self.b),
                    description=f"""
                    {self.success_emoji} Welcome Message Updated!

                    Example:
                    {value.replace('|user|', ctx.author.mention).replace('|guild|', str(ctx.guild))}
                    """
                )
            )

        # =============================================================================================

        ## ==> LEAVE MESSAGE
        # =============================================================================================

        elif thing.lower() in self.args[3:6]:

            ## ==> CHECK IF VALUE CONTAINS |user| KEYWORD
            # ============================================

            if not value.__contains__("|user|"):

                ## ==> SEND EMBED
                await ctx.send(
                    embed=discord.Embed(
                        title="WELCOMER",
                        description=f"{self.fail_emoji} Please pass the `|user|` keyword",
                        color=discord.Color.from_rgb(self.r, self.g, self.b)
                    )
                )
                return

            # ============================================

            ## ==> UPDATE VALUE
            # ============================================

            c.execute(
                """
                SELECT * FROM "welcomer"
                WHERE guild_id = :guild_id
                """,
                {"guild_id": str(ctx.guild.id)}
            )

            if c.fetchone() is not None:
                c.execute(
                    """
                    UPDATE "welcomer"
                    SET leave = :leave
                    WHERE guild_id = :guild_id
                    """,
                    {
                        "leave": value,
                        "guild_id": str(ctx.guild.id)
                    }
                )
            else:
                c.execute(
                    """
                    INSERT INTO "welcomer" VALUES (
                        :guild_id,
                        :welcome,
                        :leave,
                        :channel,
                        :enabled,
                        :card
                    )
                    """,
                    {
                        "guild_id": str(ctx.guild.id),
                        "welcome": None,
                        "leave": value,
                        "channel": None,
                        "enabled": False,
                        "card": False
                    }
                )

            self.conn.commit()

            # ============================================

            ## ==> SEND EMBED
            await ctx.send(
                embed=discord.Embed(
                    title="WELCOMER",
                    color=discord.Color.from_rgb(self.r, self.g, self.b),
                    description=f"""
                    {self.success_emoji} Leave Message Updated!

                    Example:
                    {value.replace('|user|', ctx.author.mention).replace('|guild|', str(ctx.guild))}
                    """
                )
            )

        # =============================================================================================

        ## ==> CHANNEL
        # =============================================================================================

        elif thing.lower() in self.args[6:9]:

            ## ==> CHANGE VALUE TO A discord.TextChannel OBJECT
            # ============================================

            try: channel = await commands.TextChannelConverter().convert(ctx, value)
            except commands.CommandError: return

            # ============================================

            ## ==> CHECK IF THE CHANNEL IS READABLE OR NOT
            # ============================================

            try:
                msg = await channel.send("""
**This is a test**

This is done to check if this channel is *readable* or not!
You can delete this message if you want!
                """)

            except discord.Forbidden:
                await ctx.send("I am having problems reading that channel :face_with_spiral_eyes:")
                return

            # ============================================

            ## ==> DELETE MESSAGE
            await msg.delete()

            ## ==> UPDATE DATA
            # ============================================

            c.execute(
                """
                SELECT * FROM "welcomer"
                WHERE guild_id = :guild_id
                """,
                {"guild_id": str(ctx.guild.id)}
            )

            if c.fetchone() is not None:
                c.execute(
                    """
                    UPDATE "welcomer"
                    SET channel = :channel
                    WHERE guild_id = :guild_id
                    """,
                    {"channel": str(channel.id), "guild_id": str(ctx.guild.id)}
                )
            else:
                c.execute(
                    """
                    INSERT INTO "welcomer" VALUES (
                        :guild_id,
                        :welcome,
                        :leave,
                        :channel,
                        :enable,
                        :card
                    )
                    """,
                    {
                        "guild_id": str(ctx.guild.id),
                        "welcome": None,
                        "leave": None,
                        "channel": str(channel.id),
                        "enable": False,
                        "card": False
                    }
                )

            self.conn.commit()

            # ============================================

            ## ==> SEND EMBED
            await ctx.send(
                embed=discord.Embed(
                    title="WELCOMER",
                    color=discord.Color.from_rgb(self.r, self.g, self.b),
                    description=f"{self.success_emoji} Welcome Channel updated!\n\nNew Channel: {channel.mention}"
                )
            )

        # =============================================================================================

        ## ==> ENABLE
        # =============================================================================================

        elif thing.lower() == self.args[9]:

            ## ==> CHECK IF VALUE IS BOOLEAN
            # ============================================

            if value.lower() not in (x := ["true", "1", "false", "0"]):
                await ctx.send(
                    embed=discord.Embed(
                        title="WELCOMER",
                        color=discord.Color.from_rgb(self.r, self.g, self.b),
                        description=f"{self.fail_emoji} **Please enter the correct values**\n\nUse the following values:\n```\n{', '.join(x)}\n```"
                    )
                )
                return

            # ============================================

            ## ==> GET DATA TO CHECK IF EVERYTHING IS CONFIGURED
            # ============================================

            c.execute(
                """
                SELECT * FROM "welcomer"
                WHERE guild_id = :guild_id
                """,
                {"guild_id": str(ctx.guild.id)}
            )

            # ============================================

            ## ==> CHECK IF GUILD EXISTS
            # ============================================

            if (fetches := c.fetchone()) is None:
                await ctx.send(
                    embed=discord.Embed(
                        title="WELCOMER",
                        color=discord.Color.from_rgb(self.r, self.g, self.b),
                        description=f"{self.fail_emoji} Please Configure Welcomer before enabling it!"
                    )
                )
                return

            # ============================================

            ## ==> CHECK IF ANY VALUE IS NOT CONFIGURED
            # ============================================

            _ = []
            for index, item in enumerate(fetches):
                if item is None:
                    if index == 1: x = "WELCOME_MESSAGE"
                    elif index == 2: x = "LEAVE_MESSAGE",
                    elif index == 3: x = "CHANNEL"

                    _.append(x)

            ## ==> NOTIFY USER
            if len(_) > 0:
                await ctx.send(
                    embed=discord.Embed(
                        title="WELCOMER",
                        color=discord.Color.from_rgb(self.r, self.g, self.b),
                        description=f"{self.fail_emoji} Please Configure Welcomer before enabling it!\n\nValue to be Configured:\n{', '.join(_)}"
                    )
                )
                return

            # ============================================

            c.execute(
                """
                UPDATE "welcomer"
                SET enable = :enable
                WHERE guild_id = :guild_id
                """,
                {
                    "enable": (enabled := True if value.lower() in ["true", '0'] else False),
                    "guild_id": str(ctx.guild.id)
                }
            )

            self.conn.commit()

            ## ==> NOTIFY USER
            await ctx.send(
                embed=discord.Embed(
                    title="WELCOMER",
                    color=discord.Color.from_rgb(self.r, self.g, self.b),
                    description=f"{self.success_emoji if enabled else self.fail_emoji} Welcomer has been {'Enabled!' if enabled else 'Disabled'}"
                )
            )

        # =============================================================================================

        elif thing.lower() in self.args[10:]:

            ## ==> CHECK IF VALUE IS BOOLEAN
            # ============================================

            if value.lower() not in (x := ["true", "1", "false", "0"]):
                await ctx.send(
                    embed=discord.Embed(
                        title="WELCOMER",
                        color=discord.Color.from_rgb(self.r, self.g, self.b),
                        description=f"{self.fail_emoji} **Please enter the correct values**\n\nUse the following values:\n```\n{', '.join(x)}\n```"
                    )
                )
                return

            # ============================================

            ## ==> GET DATA TO CHECK IF EVERYTHING IS CONFIGURED
            # ============================================

            c.execute(
                """
                SELECT * FROM "welcomer"
                WHERE guild_id = :guild_id
                """,
                {"guild_id": str(ctx.guild.id)}
            )

            if c.fetchone() is not None:
                c.execute(
                    """
                    UPDATE "welcomer"
                    SET card = :card
                    WHERE guild_id = :guild_id
                    """,
                    {
                        "card": (enabled := True if value.lower() in ["true", '0'] else False),
                        "guild_id": str(ctx.guild.id)
                    }
                )
            else:
                c.execute(
                    """
                    INSERT INTO "welcomer" VALUES (
                       :guild_id,
                       :welcome,
                       :leave,
                       :channel,
                       :enable,
                       :card
                    )
                    """,
                    {
                        "guild_id": str(ctx.guild.id),
                        "welcome": None,
                        "leave": None,
                        "channel": None,
                        "enable": False,
                        "card": (enabled := True if value.lower() in ["true", "0"] else False)
                    }
                )

            self.conn.commit()

            ## ==> NOTIFY USER
            await ctx.send(
                embed=discord.Embed(
                    title="WELCOMER",
                    color=discord.Color.from_rgb(self.r, self.g, self.b),
                    description=f"{self.success_emoji if enabled else self.fail_emoji} Welcome Cards have been {'Enabled' if enabled else 'Disabled'}"
                )
            )


    # =============================================================================================

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Welcomer(bot))
