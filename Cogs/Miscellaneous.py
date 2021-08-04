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
        print(type(error))
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            if (str(ctx.command) == "ban" or str(ctx.command) == "kick") and isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(embed=discord.Embed(title="Whoops", description=f"Tell me the user you want to {str(ctx.command)} too!", color=discord.Color.red()))
            elif str(ctx.command) == "unban" and isinstance(error, commands.MemberNotFound):
                await ctx.send(embed=discord.Embed(title="Whoops", description=f"Pass Either the ID of the user or `name#discriminator` for me to identify them", color=discord.Color.red()))
            elif str(ctx.command) == "SetWelcomeMessage":
                await ctx.send(embed=discord.Embed(title="Whoops", description=f"Enter the Message for me to welcome users with!", color=discord.Color.red()))
            elif str(ctx.command) == "SetLeaveMessage":
                await ctx.send(embed=discord.Embed(title="Whoops", description=f"Enter the Message for me to send if someone leaves!", color=discord.Color.red()))
            elif str(ctx.command) == "setWelcomeChannel":
                await ctx.send(embed=discord.Embed(title="Whoops", description=f"Mention the channel where I will welcome users", color=discord.Color.red()))
            elif str(ctx.command) == "ttt":
                await ctx.send(embed=discord.Embed(title="Whoops", description="Please pass the user with whom you want to play TicTacToe too!", color = discord.Color.red()))
            elif str(ctx.command) == "Embed":
                await ctx.send(embed=discord.Embed(title="Whoops", description="Please mention the channel you want to send embed to", color=discord.Color.red()))
            else:
                await ctx.send(embed=discord.Embed(title="Whoops", description="Please pass all the arguements for that command", color = discord.Color.red()))
            
        elif str(ctx.command) == "setWelcomerChannel" and isinstance(error, commands.ChannelNotFound):
            await ctx.send(embed=discord.Embed(title="Whoops", description=f"That channel doesn't Exist!", color=discord.Color.red()))
        elif str(ctx.command) == "setWelcomerChannel" and isinstance(error, commands.ChannelNotReadable):
            await ctx.send(embed=discord.Embed(title="Whoops", description=f"I cannot read that channel!", color=discord.Color.red()))
        elif isinstance(error, commands.ChannelNotReadable): 
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=discord.Embed(title="Whoops", description=f"{str(ctx.command).capitalize()} Command is on Cooldown!", color=discord.Color.red()))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Whoops", description="You are missing Permissions to do that!", color=discord.Color.red()))
        else:
            await ctx.send(embed=discord.Embed(title="Whoops", description=f"An Unexpected Error has popped out of nowhere: {error}", color = discord.Color.red()))

            
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
                    label="Moderation",
                    value="Moderation",
                    description="Get help with Moderation",
                    emoji="🧐"
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
                    label="Configuration",
                    value="Configuration",
                    description="Get help with Configuration",
                    emoji="⚙"
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
            "Moderation": discord.Embed(
                title="MODERATION",
                color=ctx.author.color,
                description="""
**Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**
    
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
            "Fun": discord.Embed(
                title="FUN",
                color=ctx.author.color,
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
                color=ctx.author.color,
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
"""
            ),
            "Music": discord.Embed(
                title="MUSIC",
                color=ctx.author.color,
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
                color=ctx.author.color,
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
            "Configuration": discord.Embed(
                title="CONFIGURATION",
                color=ctx.author.color,
                description="""
**Arguements surrounded by `()` are optional whereas arguements surrounded by `[]` are necessary!**

• :gear: `config`
```
To configure the bot in your server
```
"""
            ),
            "Miscellaneous": discord.Embed(
                title="MISCELLANEOUS",
                color=ctx.author.color,
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

• :moneybag: `donate`
```
Get the patreon link of HackArmour
```
"""
            )
        }
        
        #########################################################################################
        
        ## ==> SEND MESSAGE
        #########################################################################################
        
        await ctx.send(
            embed=discord.Embed(
                title="HELP",
                color=discord.Color.random(),
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
                    timeout=60.0,
                    check=lambda i: i.user == ctx.author
                )
            except asyncio.TimeoutError:
                select._disabled = True
                break
            try:
                await reaction.respond(
                    type=InteractionType.UpdateMessage,
                    embed = embeds[reaction.component[0].label]
                )
            except discord.NotFound: ...
            
        #########################################################################################

    #############################################################################################

    ## ==> STATS
    #############################################################################################

    @commands.command()
    async def stats(self,ctx: commands.Context) -> None:
        pyver = str(sys.version[:6])
        embed = discord.Embed(title="STATS",color=ctx.author.color,inline=False)
        embed.add_field(inline=True,name="UPTIME",value=f"```\n{str(datetime.timedelta(seconds=int(round(time() - self.STARTTIME))))}\n```")
        embed.add_field(inline=True,name="PING",value=f"```\n{round(self.bot.latency * 1000)}ms\n```")
        embed.add_field(inline=True,name="DISCORD.PY VERSION",value=f"```\n{discord.__version__}\n```")
        embed.add_field(inline=True,name="PYTHON VERSION",value=f"```\n{pyver}\n```")
        embed.add_field(inline=True,name="SERVER",value=f"```\n{ctx.guild}\n```")
        embed.add_field(inline=True,name='TOTAL SERVERS',value=f'```\n{str(len(self.bot.guilds))}\n```')
        embed.set_thumbnail(url=ctx.guild.icon_url)
<<<<<<< HEAD
        embed.set_image(url="https://cdn.discordapp.com/attachments/616315208251605005/616319462349602816/Tw.gif")
        await ctx.send(embed = embed, components=[[Button(label="Invite Me", style=ButtonStyle.URL, url="https://assistant.hackarmour.tech", emoji = '🔗')]])
=======
        await ctx.send(embed = embed, components=[[Button(label="Invite Me", style=ButtonStyle.URL, url="https://discord.com/api/oauth2/authorize?client_id=845154524997877770&permissions=8&scope=bot")]])
>>>>>>> f58be3d1c5c7758052424365742d09aa31f26f44

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
        embed = discord.Embed(title="Support Us",color=ctx.author.color)
        embed.add_field(name='Please support the development by becoming a patron!',value="Click the Button below to go our Patreon page.")
        embed.set_image(url="https://cdn.discordapp.com/attachments/616315208251605005/616319462349602816/Tw.gif")
        await ctx.send(components=[[btn]], embed=embed)

    ############################################################################################
    
## ==> ADDING THE COG TO BOT
#############################################################################################

def setup(bot:commands.Bot) -> None: bot.add_cog(Miscellaneous(bot))

#############################################################################################
