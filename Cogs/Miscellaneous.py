import discord, sys, datetime, json, asyncio
from discord.ext import commands
from time import time
from discord_components import Button, ButtonStyle, Select, SelectOption, InteractionType

class Miscellaneous(commands.Cog):
    def __init__(self,bot: commands.Bot) -> None:
        self.bot = bot
        with open("Configuration/config.json") as f:
            self.STARTTIME = json.loads(f.read())["starttime"]
        
        with open("Configuration/Help.json") as f:
            self.CONFIG = json.load(f)

    ## ==> ERROR HANDLING
    #############################################################################################

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            pass
        elif str(ctx.command) == "setWelcomerChannel" and isinstance(error, commands.ChannelNotFound):
            await ctx.send(embed=discord.Embed(title="Whoops", description=f"<a:aFail:848315264491192320> That channel doesn't Exist!", color=discord.Color.red()))
        elif str(ctx.command) == "setWelcomerChannel" and isinstance(error, commands.ChannelNotReadable):
            await ctx.send(embed=discord.Embed(title="Whoops", description=f"<a:aFail:848315264491192320> I cannot read that channel!", color=discord.Color.red()))
        elif isinstance(error, commands.ChannelNotReadable): 
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=discord.Embed(title="Whoops", description=f"<a:aFail:848315264491192320> {str(ctx.command).capitalize()} Command is on Cooldown!", color=discord.Color.red()))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Whoops", description="<a:aFail:848315264491192320> You are missing Permissions to do that!", color=discord.Color.red()))
        else:
            if str(error).endswith("Missing Permissions"): return
            embed = discord.Embed(
                    title='ERROR',
                    description=f"<a:aFail:848315264491192320> Error message:\n**{error}**\n\nCommand: **{ctx.command}**",
                    color=discord.Color.from_rgb(46,49,54)
                )
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await self.bot.get_channel(877408123344789515).send(embed=embed)
            
    ##############################################################################################

    ## ==> AVATAR
    #############################################################################################

    @commands.command(aliases=['av'])
    async def avatar(self, ctx: commands.Context, user: commands.MemberConverter = None) -> None:
        if user == None: user = ctx.author
        embed = discord.Embed(color=user.color,title="AVATAR")
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    #############################################################################################

    ## ==> HELP COMMAND
    ##############################################################################################
    
    @commands.command()
    async def help(self, ctx: commands.Context) -> None:
        
        ## ==> SELECT WIDGET
        #########################################################################################
        
        select = Select(
            placeholder="Choose what you want help with!",
            options = [
                SelectOption(
                    label="Welcomer",
                    value="Welcomer",
                    description="Get help with Welcomer",
                    emoji="👋"
                ),
                SelectOption(
                    label="Moderation",
                    value="Moderation",
                    description="Get help with Moderation",
                    emoji="🧐"
                ),
                SelectOption(
                    label="Logs",
                    value="Logs",
                    description="Get help with Logs",
                    emoji="🔍"
                ),
                SelectOption(
                    label="Fun",
                    value="Fun",
                    description="Get help with Fun",
                    emoji="😄"
                ),
                SelectOption(
                    label="Leveling",
                    value="Leveling",
                    description="Get help with Leveling",
                    emoji="📈"
                ),
                SelectOption(
                    label="Music",
                    value="Music",
                    description="Get help with Music",
                    emoji="🎶"
                ),
                SelectOption(
                    label="LON",
                    value="LON",
                    description="Get help with LON",
                    emoji="😃"
                ),
                SelectOption(
                    label="Miscellaneous",
                    value="Miscellaneous",
                    description="Get help with Other Commands",
                    emoji="⚪"
                ),
            ]
        )
        
        #########################################################################################
        
        ## ==> EMBEDS DICTIONARY
        #########################################################################################

        embeds = {
            "Welcomer": discord.Embed(
                title="WELCOMER",
                color=discord.Color.from_rgb(46,49,54),
                description=f"""
**Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**

• <a:gearSpinning:873882264134643712> `welcomer [configuration] [value]`
```
To Configure Welcomer

Examples:
{self.bot.command_prefix}welcomer welcome-message Hey |user|, Welcome to |guild|^
{self.bot.command_prefix}welcomer leave-message |user| left |guild|^
{self.bot.command_prefix}welcomer channel #welcomer
{self.bot.command_prefix}welcomer enable true
{self.bot.command_prefix}welcomer enable false
```
"""
            ).set_footer(text="^ \"|user|\" and \"|guild|\" are keywords and are required in these configurations"),
            "Moderation": discord.Embed(
                title="MODERATION",
                color=discord.Color.from_rgb(46,49,54),
                description="""
**Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**

• :face_with_symbols_over_mouth: `ToggleAutoMod`
```
To Toggle AutoMod
```

• :x: `ban [member] (reason)`
```
To Ban a member
```

• :rage: `kick [member] (reason)`
```
To Kick a member
```

• :white_check_mark: `unban [[username#discriminator] OR [UserID]]`
```
To Unban a member
```

• :mute: `mute [member] [time] (reason)`
```
To Mute a member 

time:
s, m, h, d, w
```

• :loud_sound: `unmute [member]`
```
To Unmute a member
```

• :x: `purge (number)`
```
To clear number amount of messages

default is 5
```
"""
            ),
            "Logs": discord.Embed(
                title="LOGS",
                color=discord.Color.from_rgb(46,49,54),
                description=f"""
**Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**

• <a:gearSpinning:873882264134643712> `logs [configuration] [value]`
```
To Configure Logs

Examples:
{self.bot.command_prefix}logs channel #logs
{self.bot.command_prefix}logs enable true
{self.bot.command_prefix}logs enable false
```
"""  
            ),
            "Fun": discord.Embed(
                title="FUN",
                color=discord.Color.from_rgb(46,49,54),
                description="""
**Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**

• :rock: `rps [member]`
```
To play Rock-Paper-Scissors with a member
```

• :o:`ttt [member]`
```
To play Tic-Tac-Toe with a member
```

• :question: `8ball [question]`
```
Get a random answer of your question
```

• :coin: `coin`
```
Tosses an imaginary coin
```

• :regional_indicator_f: `f (reason)`
```
press F to pay respect
```

• :joy: `meme`
```
I will meme for you
```
"""
            ),
            "Leveling": discord.Embed(
                title="LEVELING",
                color=discord.Color.from_rgb(46,49,54),
                description="""
**Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**

• :chart_with_upwards_trend: `rank (member)`
```
To get the rank card of a member

Defaults to the member who ran the command
```

• :chart_with_upwards_trend: `lb`
```
To get the leaderboards of your server
```

• :bar_chart: `ToggleLeveling`
```
To Toggle Leveling
```
"""
            ),
                        
            "Music": discord.Embed(
                title="MUSIC",
                color=discord.Color.from_rgb(46,49,54),
                description="""
**Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**

• :notes: `p [Music Name]`
```
To Play Music

You need to be connected to a VC before running this
``` 

• :notepad_spiral: `q`
```
To get the current queue
```

• :arrow_right: `skip`
```
To Skip the current song
```

• :pause_button: `pause`
```
To pause the playback of music
```

• :arrow_forward: `resume`
```
To resume the playback of music
```

• :no_entry_sign: `disconnect`
```
To stop the music and disconnect from your VC
```
"""
            ),
            "LON": discord.Embed(
                title="**L**ACK **O**F **N**ITRO",
                color=discord.Color.from_rgb(46,49,54),
                description="""
**Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**

• :smile: `LON [emoji name]`
```
To send a webhook with emoji
```

• :smile: `LONall`
```
To send all available emojis
```
"""
            ),
            "Miscellaneous": discord.Embed(
                title="MISCELLANEOUS",
                color=discord.Color.from_rgb(46,49,54),
                description="""
**Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**

• :sunglasses: `avatar (member)`
```
To get the avatar of a member

Defaults to the person who ran this command
```

• :diamond_shape_with_a_dot_inside: `help`
```
This command
```

• :grey_question: `about (member)`
```
To get the Info about a member

Defaults to the person who ran this command
```

• :grey_exclamation: `stats`
```
To get my stats
```

• <:ha:873879461634924614> `donate`
```
Get the patreon link of HackArmour
```
"""
            )
        }
        
        #########################################################################################
        
        ## ==> SEND MESSAGE
        #########################################################################################
        
        msg = await ctx.send(
            embed=discord.Embed(
                title="HELP",
                color=discord.Color.from_rgb(46,49,54),
                description="What do you want help with?"
            ),
            components=[select]
        )
        
        #########################################################################################
        
        ## ==> CHECK FOR REACTION AND EDIT THE EMBED
        #########################################################################################
        
        while True:
            try:
                reaction = await self.bot.wait_for(
                    "select_option",
                    timeout=60.0
                )
                if(reaction.author!=ctx.author):
                    await reaction.respond(
                        type=4,
                        content="This menu is not for you",
                        empherel=True
                    )
                    continue
            except asyncio.TimeoutError:
                select.disabled = True
                await msg.edit(components=[select])
                break
            except discord.HTTPException:
                pass
            try:
                await reaction.respond(
                    type=InteractionType.UpdateMessage,
                    embed = embeds[reaction.component[0].label]
                )
            except discord.NotFound: pass
            except discord.HTTPException:
                pass
            
        #########################################################################################

    #############################################################################################

    ## ==> STATS
    #############################################################################################

    @commands.command()
    async def stats(self,ctx: commands.Context) -> None:
        embed = discord.Embed(title="STATS",color=discord.Color.from_rgb(46,49,54),inline=False)
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
        await ctx.send(embed = embed, components=[[Button(label="Invite Me", style=ButtonStyle.URL, url="https://discord.com/oauth2/authorize?client_id=845154524997877770&permissions=-9&scope=bot", emoji = '🔗')]])

    #############################################################################################

    ## ==> USER INFO
    #############################################################################################

    @commands.command(aliases=['abt'])
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

    #############################################################################################
    
    ## ==> DONATE COMMAND
    ############################################################################################

    @commands.command()
    async def donate(self,ctx: commands.Context) -> None:
        btn = Button(label="Patreon - Hack Armour", style=ButtonStyle.URL, url = "https://www.patreon.com/hackarmour", id = "embed", emoji = "🔗")
        embed = discord.Embed(title="Support Us",color=discord.Color.from_rgb(46,49,54))
        embed.add_field(name='Please support the development by becoming a patreon!',value="Click the Button below to go our Patreon page.")
        embed.set_image(url="https://cdn.discordapp.com/attachments/616315208251605005/616319462349602816/Tw.gif")
        await ctx.send(components=[[btn]], embed=embed)

    ############################################################################################
    
## ==> ADDING THE COG TO BOT
#############################################################################################

def setup(bot:commands.Bot) -> None: bot.add_cog(Miscellaneous(bot))

#############################################################################################
