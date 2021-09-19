import discord, json, sqlite3
from discord.ext import commands


class Logs(commands.Cog):
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

        self.args = [
            "channel", "logs-channel", "logs_channel",
            "enable"
        ]

        self.conn = sqlite3.Connection("Configuration/Moderation.db")

    ## ==> SEND LOGS
    # =============================================================================================

    ## ==> MESSAGE EDIT
    # =============================================================================================

    @commands.Cog.listener()
    async def on_message_edit(self, msg_before: discord.Message, msg_after: discord.Message) -> None:

        ## ==> CURSOR
        c = self.conn.cursor()

        ## ==> RUN QUERY TO CHECK IF LOGS ARE ENABLED
        # ============================================

        c.execute(
            """
            SELECT * FROM "moderation" WHERE guild_id = :guild_id
            """,
            {"guild_id": str(msg_after.guild.id)}
        )

        # ============================================

        if (fetches := c.fetchone()) is None:
            return

        channel = await self.bot.fetch_channel(int(fetches[1]))

        ## ==> EMBED
        embed = discord.Embed(
            title=f'Message Edited in {msg_after.channel}',
            color=discord.Color.from_rgb(self.r, self.g, self.b)
        )

        ## ==> ADD FIELDS AND AUTHOR
        embed.set_author(name=msg_after.author,icon_url=msg_after.author.avatar_url)
        embed.add_field(name='Old message',value=msg_before.content)
        embed.add_field(name='Edited Message',value=msg_after.content)

        try:
            await channel.send(embed=embed)
        except discord.HTTPException:
            return

    # =============================================================================================

    ## ==> MESSAGE DELETE
    # =============================================================================================

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:

        ## ==> CURSOR
        c = self.conn.cursor()

        ## ==> RUN QUERY TO CHECK IF LOGS ARE ENABLED
        # ============================================

        c.execute(
            """
            SELECT * FROM "moderation" WHERE guild_id = :guild_id
            """,
            {"guild_id": str(message.guild.id)}
        )

        # ============================================

        if (fetches := c.fetchone()) is None:
            return

        channel = await self.bot.fetch_channel(int(fetches[1]))

        ## ==> EMBED
        embed = discord.Embed(
            title=f'Message Deleted in {message.channel}',
            color=discord.Color.from_rgb(self.r, self.g, self.b)
        )

        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        embed.add_field(name='Message', value=message.content)

        embed.timestamp = message.created_at

        try:
            await channel.send(embed=embed)
        except discord.HTTPException:
            return

    # =============================================================================================

    ## ==> LOGS CONFIG COMMAND
    # =============================================================================================

    @commands.command(
        help="""
` `- **To Configure Logs on this server**
` `
` `  **Examples**:
`  ` ~p~logs channel #logs
`  ` ~p~logs enable true
`  ` ~p~logs enable false
"""
    )
    @commands.has_permissions(administrator=True)
    async def logs(self, ctx: commands.Context, thing: str, *, value: str) -> None:

        ## ==> CHECKS
        # ============================================

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

        # ============================================

        c = self.conn.cursor()

        ## ==> IF USER WANTS TO CONFIGURE LOGS CHANNEL
        # ============================================

        if thing.lower() in self.args[:3]:

            ## ==> CONVERT TO discord.ext.commands.TextChannelConverter
            # ============================================
            try:
                channel = await commands.TextChannelConverter().convert(ctx, value)
            except commands.CommandError:
                return

            # ============================================

            ## ==> CHECK IF CHANNEL IS READABLE
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

            await msg.delete()

            # ============================================

            ## ==> QUERY TO SEE IF GUILD EXISTS IN DB
            # ============================================

            c.execute(
                "SELECT * FROM \"moderation\" WHERE guild_id = :guild_id",
                {"guild_id": str(ctx.guild.id)}
            )

            # ============================================

            ## ==> IF GUILD NOT IN DB
            # ============================================

            if c.fetchone() is None:

                ## ==> ADD DATA
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
                        "logs_channel": str(channel.id),
                        "logs_enabled": False,
                        "automod": False
                    }
                )

            # ============================================

            ## ==> IF DATA IS IN DB
            # ============================================

            else:

                ## ==> UPDATE DATA
                c.execute(
                    """
                    UPDATE "moderation"
                    SET logs_channel = :logs_channel
                    WHERE guild_id = :guild_id
                    """,
                    {
                        "logs_channel": str(channel.id),
                        "guild_id": str(ctx.guild.id)
                    }
                )

            # ============================================

            ## ==> SEND EMBED
            await ctx.send(
                embed=discord.Embed(
                    title="LOGS",
                    description=f"{self.success_emoji} Logs channel has been changed to {channel.mention}",
                    color=discord.Color.from_rgb(self.r, self.g, self.b)
                )
            )

        # ============================================

        elif thing.lower() in self.args[-1]:

            ## ==> CHECK IF IS BOOLEAN
            # ============================================

            if value.lower() not in (x := ["true", "1", "false", "0"]):

                ## ==> SEND EMBED
                await ctx.send(
                    embed=discord.Embed(
                        title="LOGS",
                        description=f"""
                        {self.fail_emoji} Please use valid arguements

                        You can use the following arguements:
                        ```
                        {', '.join(x)}
                        ```
                        """,
                        color=discord.Color.from_rgb(self.r, self.g, self.b)
                    )
                )
                return

            # ============================================

            ## ==> QUERY TO SEE IF GUILD EXISTS IN DB
            # ============================================

            c.execute(
                "SELECT * FROM \"moderation\" WHERE guild_id = :guild_id",
                {"guild_id": str(ctx.guild.id)}
            )

            # ============================================

            ## ==> IF GUILD NOT IN DB
            # ============================================

            if (fetches := c.fetchone()) is None:

                ## ==> SEND EMBED
                await ctx.send(
                    embed=discord.Embed(
                        title="LOGS",
                        description=f"{self.fail_emoji} Please set the Channel where I should send logs before enabling it!",
                        color = discord.Color.from_rgb(self.r, self.g, self.b)
                    )
                )
                return

            # ============================================

            ## ==> IF CHANNEL NOT CONFIGURED
            # ============================================

            elif fetches[1] is None:

                ## ==> SEND EMBED
                await ctx.send(
                    embed=discord.Embed(
                        title="LOGS",
                        description=f"{self.fail_emoji} Please set the Channel where I should send logs before enabling it!",
                        color = discord.Color.from_rgb(self.r, self.g, self.b)
                    )
                )
                return

            # ============================================

            ## ==> CHANGE DATA
            # ============================================

            c.execute(
                """
                UPDATE "moderation"
                SET logs_enabled = :logs_enabled
                WHERE guild_id = :guild_id
                """,
                {
                    "logs_enabled": (x := True if fetches[2] == 0 else False),
                    "guild_id": str(ctx.guild.id)
                }
            )

            await ctx.send(
                embed=discord.Embed(
                    title="LOGS",
                    description=f"{self.success_emoji} Logs have been {'Enabled!' if x else 'Disabled'}",
                    color = discord.Color.from_rgb(self.r, self.g, self.b)
                )
            )

            # ============================================

        ## ==> COMMIT CHANGES
        self.conn.commit()

    # =============================================================================================

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Logs(bot))
