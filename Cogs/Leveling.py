import discord, json, sqlite3, random
from easy_pil import Canvas, Editor, Font, load_image_async
from discord.ext import commands


class Leveling(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        ## ==> GET EMOJIS AND OTHER STUFF FROM THE CFG FILE
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

        ## ==> SEE "on_message"
        self.CHANCE_LIST = [True for k in range(3)] + [False for k in range(7)]

        ## ==> DATABASE
        self.conn = sqlite3.Connection("Configuration/Leveling.db")

    ## ==> ON MESSAGE EVENT
    # =============================================================================================

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:

        ## ==> CHECKS
        if message.author.bot: return
        if not random.choice(self.CHANCE_LIST): return

        ## ==> CHOOSING A RANDOM NUMBER
        randNo = random.randint(5, 15)

        ## ==> CURSOR
        c = self.conn.cursor()

        ## ==> CHECK IF LEVELING IS ENABLED
        # ============================================

        c.execute(
            """
            SELECT * FROM "leveling_toggle"
            WHERE guild_id = :guild_id
            """,
            {"guild_id": str(message.guild.id)}
        )

        # ============================================

        if (fetches := c.fetchone()) is None: pass
        elif fetches[1] == 0: return

        ## ==> QUERYING TO SEE IF USER EXISTS IN DB
        # ============================================

        c.execute(
            "SELECT * FROM \"main_table\" WHERE guild_id = :guild_id AND id=:id",
            {"guild_id": str(message.guild.id), "id": str(message.author.id)}
        )

        # ============================================

        ## ==> IF GUILD AND AUTHOR ID DON'T EXIST IN THE DB
        # ============================================

        if (fetches := c.fetchone()) is None:

            ## ==> INSERTING VALUES INTO THE TABLE
            c.execute(
                f"INSERT INTO \"main_table\" VALUES (:id, :guild_id, :xp, :level, :totalxp, :username)",
                {
                    "guild_id": str(message.guild.id),
                    "id": str(message.author.id),
                    "xp": randNo,
                    "level": 0,
                    "totalxp": randNo,
                    "username": str(message.author)
                }
            )

        # ============================================

        ## ==> IF FETCHED VALUE'S XP IS == 0
        # ============================================

        elif fetches[3] == 0:

            ## ==> CHECK IF USER HAS A LEVEL UP
            # ============================================

            if fetches[2] + randNo >= 100:

                ## ==> NOTIFY USER
                await message.channel.send(
                    f"{self.stonks_emoji}, {message.author.mention}, You leveled up to Level 1"
                )

                ## ==> NEW XP
                newxp = fetches[2] + randNo - 100

                ## ==> UPDATE VALUES
                c.execute(
                    f"""
                    UPDATE \"main_table\"
                    SET xp = :newxp,
                        level = 1,
                        totalxp = :totalxp,
                        username = :username
                    WHERE id = :id AND guild_id = :guild_id
                    """,
                    {
                        "newxp": newxp,
                        "totalxp": fetches[4] + randNo,
                        "id": str(message.author.id),
                        "guild_id": str(message.guild.id),
                        "username": str(message.author)
                    }
                )

            # ============================================

            ## ==> IF USER DOESN'T HAVE A LEVEL UP
            # ============================================

            else:
                ## ==> UPDATE VALUES
                c.execute(
                    f"""
                    UPDATE \"main_table\"
                    SET xp = :newxp,
                        totalxp = :totalxp,
                        username = :username
                    WHERE id = :id AND guild_id = :guild_id
                    """,
                    {
                        "newxp": fetches[2] + randNo,
                        "totalxp": fetches[4] + randNo,
                        "id": str(message.author.id),
                        "guild_id": str(message.guild.id),
                        "username": str(message.author)
                    }
                )

            # ============================================

        # ============================================

        ## ==> IF FETCHED VALUE'S XP IS > 0
        # ============================================

        else:

            ## ==> IF USER HAS A LEVEL UP
            # ============================================

            if (int(fetches[2]) + randNo) >= int(fetches[3]) * 100:

                ## ==> NOTIFY USER
                await message.channel.send(
                    f"{self.stonks_emoji}, {message.author.mention}, You leveled up to Level {int(fetches[3]) + 1}"
                )

                ## ==> NEW XP
                newxp = fetches[2] + randNo - fetches[3] * 100

                ## ==> UPDATE VALUES
                c.execute(
                    f"""
                    UPDATE \"main_table\"
                    SET xp = :newxp,
                        level = :newlevel,
                        totalxp = :totalxp,
                        username = :username
                    WHERE id = :id AND guild_id = :guild_id
                    """,
                    {
                        "newxp": newxp,
                        "newlevel": fetches[3] + 1,
                        "totalxp": fetches[4] + randNo,
                        "id": str(message.author.id),
                        "guild_id": str(message.guild.id),
                        "username": str(message.author)
                    }
                )

            # ============================================

            ## ==> IF USER DOESN'T HAVE A LEVEL UP
            # ============================================

            else:

                ## ==> UPDATE VALUES
                c.execute(
                    f"""
                    UPDATE \"main_table\"
                    SET xp = :newxp,
                        totalxp = :totalxp,
                        username = :username
                    WHERE id = :id AND guild_id = :guild_id
                    """,
                    {
                        "newxp": fetches[2] + randNo,
                        "totalxp": fetches[4] + randNo,
                        "id": str(message.author.id),
                        "guild_id": str(message.guild.id),
                        "username": str(message.author)
                    }
                )

            # ============================================

        # ============================================

        ## ==> COMMIT CHANGES
        self.conn.commit()

        # ============================================

    # =============================================================================================

    ## ==> RANK COMMAND
    # =============================================================================================

    @commands.command(
        help="""
` `- **To get your rank card**
` `
` `- If you pass a user, that user's rank card will be given
"""
    )
    async def rank(self, ctx: commands.Context, *, member: commands.MemberConverter = None) -> None:

        ## ==> CHECKS
        if member is None: member = ctx.author
        if ctx.author.bot: return

        ## ==> CURSOR
        c = self.conn.cursor()

        ## ==> QUERY THE TOGGLE TABLE
        # ============================================

        c.execute(
            """
            SELECT * FROM "leveling_toggle"
            WHERE guild_id = :guild_id
            """,
            {"guild_id": str(ctx.guild.id)}
        )

        # ============================================

        ## ==> CHECK IF LEVELING IS ENABLED
        # ============================================

        if (fetches := c.fetchone()) is None:
            pass
        elif fetches[1] == 0:
            await ctx.send(
                embed=discord.Embed(
                    title="LEVELING",
                    description=f"{self.fail_emoji} Leveling is Disabled on your server",
                    color=discord.Color.from_rgb(self.r, self.g, self.b)
                )
            )
            return

        # ============================================

        ## ==> GET THE DATA OF MEMBER
        # ============================================

        c.execute(
            """
            SELECT * FROM "main_table" WHERE id = :id AND guild_id = :guild_id
            """,
            {"id": str(member.id), "guild_id": str(member.guild.id)}
        )

        # ============================================

        ## ==> CHECK IF MEMBER IS IN DB
        # ============================================
        if (fetches := c.fetchone()) is None:

            ## ==> SEND EMBED TO NOTIFY USER
            desc = f"{self.fail_emoji} {'''That user isn't''' if member.id != ctx.author.id else '''You aren't'''} Leveled"
            await ctx.send(
                embed=discord.Embed(
                    title="LEVELING",
                    color=discord.Color.from_rgb(self.r, self.g, self.b),
                    description=desc
                )
            )
            return

        # ============================================

        ## ==> QUERY TO GET THE DATA OF THE SERVER
        # ============================================

        c.execute(
            """
            SELECT * FROM \"main_table\"
            WHERE guild_id = :guild_id
            ORDER BY totalxp DESC
            """,
            {"guild_id": str(member.guild.id)}
        )
        fetches2 = c.fetchall()

        # ============================================

        ## ==> GET RANK OF MEMBER
        # ============================================

        rank = fetches2.index(
            (fetches[0], fetches[1], fetches[2], fetches[3], fetches[4], fetches[5])
        )

        # ============================================

        ## ==> LOAD ASSETS
        # ============================================

        background = Editor(canvas=Canvas((900, 300), "#000000"))
        profile = await load_image_async(str(member.avatar_url))
        profile = Editor(profile).resize((150, 150)).circle_image()

        montserrat = Font().montserrat(size = 40)
        montserrat_small = Font().montserrat(size = 30)

        # ============================================

        ## ==> STYLING
        # ============================================

        square = Canvas((500, 500), "#ff0000")
        square = Editor(canvas=square)
        square.rotate(30, expand=True)

        background.paste(square.image, (600, -250))
        background.paste(profile.image, (30, 30))

        # ============================================

        ## ==> PROGRESS BAR
        # ============================================

        background.rectangle(
            (30, 220),
            width=650,
            height=40,
            fill="white",
            radius=20
        )
        background.bar(
            (30, 220),
            max_width=650,
            height=40,
            percentage=fetches[2]/fetches[3] if fetches[3] != 0 else fetches[2],
            fill="orange",
            radius=20
        )

        # ============================================

        ## ==> WRITE DATA ON BG
        # ============================================

        background.text((200, 40), fetches[5], font=montserrat, color="white")

        background.rectangle((200, 100), width=350, height=2, fill="white")
        background.text(
            (200, 130),
            f"Level : {fetches[3]} | XP : {fetches[2]} / {(fetches[3]) * 100} | Rank : {rank+1}",
            font=montserrat_small,
            color="white"
        )

        # ============================================

        ## ==> SEND RANK CARD
        # ============================================

        file = discord.File(fp=background.image_bytes, filename="card.png")
        await ctx.send(file=file)

        # ============================================

    # =============================================================================================

    ## ==> LEADERBOARD
    # =============================================================================================

    @commands.command(
        aliases=["lb"],
        help="""
` `- To get this server's leaderboards
"""
    )
    async def leaderboard(self, ctx: commands.Context) -> None:

        ## ==> CHECKS
        if ctx.author.bot: return

        ## ==> CURSOR
        c = self.conn.cursor()

        ## ==> CHECK IF LEVELING IS ENABLED
        # ============================================

        c.execute(
            """
            SELECT * FROM "leveling_toggle"
            WHERE guild_id = :guild_id
            """,
            {"guild_id": str(ctx.guild.id)}
        )

        # ============================================

        ## ==> IF FETCHES IS DISABLED
        # ============================================

        if (fetches := c.fetchone()) is None:
            pass

        elif fetches[1] == 0:
            await ctx.send(
                embed=discord.Embed(
                    title="LEVELING",
                    description=f"{self.fail_emoji} Leveling is Disabled on your server",
                    color=discord.Color.from_rgb(self.r, self.g, self.b)
                )
            )
            return

        # ============================================

        ## ==> RUN A QUERY TO GET ALL RANKS FROM GUILD AND ORDER THEM IN DESCENDING ORDER
        # ============================================

        c.execute(
            """
            SELECT * FROM \"main_table\"
            WHERE guild_id = :guild_id
            ORDER BY totalxp DESC
            """,
            {"guild_id": str(ctx.guild.id)}
        )

        fetches = c.fetchall()

        # ============================================

        ## ==> PARENT IMAGE
        # ============================================

        canvas = Canvas((700, len(fetches)*100))
        bg = Editor(canvas = canvas)

        # ============================================

        ## ==> FONTS
        # ============================================

        montserrat = Font().montserrat(size = 25)
        montserrat_small = Font().montserrat(size = 20)

        # ============================================

        for index, item in enumerate(fetches if len(fetches) < 10 else fetches[:11]):

            ## ==> USER
            user = await self.bot.fetch_user(int(item[0]))

            ## ==> IMAGE
            background = Editor(canvas=Canvas((700, 100), color=(self.r, self.b, self.g)))

            ## ==> LOAD ASSETS
            # ============================================

            try:
                profile = await load_image_async(str(user.avatar_url))
            except Exception as e:
                print(e)
                profile = await load_image_async("https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Blue_question_mark_icon.svg/1200px-Blue_question_mark_icon.svg.png")
            profile = Editor(profile).resize((80, 80)).circle_image()

            background.paste(profile.image, (15,15))

            # ============================================

            ## ==> WRITE DATA ON BG
            # ============================================

            background.text((150, 25), fetches[index][5], font=montserrat, color="white")

            background.rectangle((150, 98), width=350, height=2, fill="white")
            background.text(
                (150, 55),
                f"Rank : {index+1}",
                font=montserrat_small,
                color="white"
            )

            # ============================================

            ## ==> PASTE IMAGE ON THE MAIN BG
            bg.paste(background.image, (0,100*index+1))

        await ctx.send(file=discord.File(fp=bg.image_bytes, filename="card.png"))

    # =============================================================================================

    ## ==> TOGGLE
    # =============================================================================================

    @commands.command(
        help="""
` `- **To Toggle (turn on or off) Leveling**
` `
` `- **Requires Administrator Permission**
"""
    )
    @commands.has_permissions(administrator=True)
    async def toggleLeveling(self, ctx: commands.Context) -> None:

        ## ==> CHECKS
        if ctx.author.bot: return

        c = self.conn.cursor()

        ## ==> QUERY TO CHECK IF GUILD IS IN DB
        # ============================================

        c.execute(
            """
            SELECT * FROM \"leveling_toggle\"
            WHERE guild_id = :guild_id
            """,
            {"guild_id": str(ctx.guild.id)}
        )

        # ============================================

        ## ==> IF IT DOESN'T EXIST
        # ============================================

        if (fetches := c.fetchone()) is None:

            ## ==> DISABLE IT
            c.execute(
                """
                INSERT INTO "leveling_toggle" VALUES(
                    :guild_id,
                    :enabled
                )
                """,
                {"guild_id": str(ctx.guild.id), "enabled": False}
            )
            enabled = False

        # ============================================

        ## ==> IF IT EXISTS
        # ============================================

        else:

            ## ==> UPDATE
            c.execute(
                """
                UPDATE "leveling_toggle"
                SET enabled = :enabled
                WHERE guild_id = :guild_id
                """,
                {"enabled": True if not fetches[1] else False, "guild_id":str(ctx.guild.id)}
            )

            enabled = True if not fetches[1] else False

        # ============================================

        ## ==> COMMIT CHANGES
        self.conn.commit()

        ## ==> SEND EMBED
        # ============================================

        await ctx.send(
            embed=discord.Embed(
                title="LEVELING",
                color = discord.Color.from_rgb(self.r, self.g, self.b),
                description=f"{self.success_emoji if enabled else self.fail_emoji} Leveling has been **{'Enabled' if enabled else 'Disabled'}**"
            )
        )

        # ============================================

    # =============================================================================================

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Leveling(bot))
