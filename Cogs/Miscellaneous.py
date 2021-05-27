import discord, sys, datetime, requests, json
from discord.ext import commands
from random import choice
from time import time
from os import listdir

class Miscellaneous(commands.Cog):
    def __init__(self,bot: commands.Bot) -> None: 
        self.bot = bot
        with open("Configuration/config.json") as f:
            self.STARTTIME = json.loads(f.read())["starttime"]
        
        self.EIGHT_BALL_ANSWERS = [
            "Yeah", "Yes", "Ofcourse", "Ofc", "Ah Yes", "I see in the Prophecy: TRUE!"
            "Nah", "No", 'Nope', 'Never', "I don't think so",
            "idk", "Maybe", "ig", "I'm bored", "You're annoying"
        ]
        
    ## ==> ERROR HANDLING
    #############################################################################################
    
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error): await ctx.send(embed=discord.Embed(title="Whoops",color=discord.Color.red(),description=f"An error occured while trying to run that command\n{error}"))
    
    #############################################################################################
    
    ## ==> HELP COMMAND
    #############################################################################################
    
    @commands.command()
    async def help(self, ctx: commands.Context,*,thing=None) -> None:
        embed = discord.Embed(title="HELP",color=ctx.author.color)
        embed.set_footer(text="Developed By [ᴛʜᴇ ᴇᴍᴘᴇʀᴏʀ] and PHÄÑTÖM KÑÏGHT")
        
        if thing == None:
            embed.add_field(
                name="What do you want help with?",
                value="Type any of the commands below to get help:",
                inline=False
            )
            embed.add_field(name="`>help Welcomer`",value="To Get Help with Welcomer Commands")
            embed.add_field(name="`>help Moderation`",value="To Get Help with Moderation Commands")
            embed.add_field(name="`>help Tic Tac Toe`",value="To Get Help with Tic Tac Toe Commands")
            embed.add_field(name="`>help Fun`",value="To Get Help with Fun Commands")
        
        elif thing.lower() == "welcomer":
            embed.add_field(
                name="**WELCOMER**",
                inline=False,
                value="""          
:white_check_mark: `>toggleWelcomer`:
    To Toggle Welcomer On or Off

:scroll: `>SetWelcomeMessage <message>`:
    To Set the Welcome Message
    Using `|user|` in message will replace it with a mention of the new user    -> Important
    Using `|guild|` in message will replace it with the name of the server

:scroll: `>SetLeaveMessage <message>`:
    To Set the Leave Message
    Using `|user|` in message will replace it with User's Name                  -> Important
    Using `|guild|` in message will replace it with Server's Name
    
:dart: `>setWelcomeChannel <Channel>`:
    To Set the channel to send Welcome message in
    Mention channel as #<channel name>
    """
            )
        
        elif thing.lower() == "tic tac toe":
            embed.add_field(
                name="TIC TAC TOE",
                inline=False,
                value="""
:video_game: `>ttt <user>`:
    To Start a game of Tic Tac Toe with <user>
    Other Aliases of this command: `>TTT`, `>TicTacToe`
    
:thumbsup: `>accept <user>`:
    To Accept an invitation for Tic Tac Toe with <user>
    Other Aliases: `>Accept`

:thumbsdown: `>unaccept <user>`:
    To Unaccept an invitation for Tic Tac Toe with <user>
    Other Aliases: `>Unaccept`, `>decline`
    
:negative_squared_cross_mark: `>exit <user>`:
    To Force Exit a match between author and <user> [Requires both players to run the command]
    Other Aliases: `>Exit`, `>quit`
    
:white_check_mark: `>place <number>`
    To Place an X or O on <number> on the board
    Other Aliases: `>Place`, `>set`
"""
            )
        
        elif thing.lower() == "moderation":
            embed.add_field(
                name="MODERATION",
                value="""
:x: `>ban <user>`
    To Ban <user>
    
:negative_squared_cross_mark: `>kick <user>`
    To Kick <user>
    
:white_check_mark: `>unban <username>#<discriminator>`
    To Unban the user passed in the function
            
:ninja: `>setLogChannel <channel>`
    To Set the Log Channel on the server
    It will not send logs until this is not set
    
:white_check_mark: `>toggleLog`
    To Toggle Logs
    It will not send logs until this is not done
    
:x: `>purge <number>`
    It will clear <number> amount of messages
    Other aliases: `>clear`, `>delete`
""",
                inline=False
            )
        elif thing.lower() == "fun":
            embed.add_field(
                name="FUN",
                inline=False,
                value="""
:thinking_face: `>8ball <question>`
    Give a random answer for <question>
    
:joy: `>meme`
    Sends a meme from Reddit!
    
:rofl: `>memes <number>`
    Sends <number> amount of memes!!
"""
            )
        
        else:
            embed.add_field(name="I can't Understand what do you mean", value="Use just `>help` without any arguements")
        
        await ctx.send(embed=embed)
    
    #############################################################################################

    ## ==> 8BALL
    #############################################################################################
    
    @commands.command(aliases=["8ball"])
    async def eightBall(self, ctx: commands.Context, *, question) -> None:
        embed = discord.Embed(color=ctx.author.color, title="8BALL", description=f"Question - {question}?\nAnswer - {choice(self.EIGHT_BALL_ANSWERS)}")
        embed.set_author(name=str(ctx.author)[:-5], icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    #############################################################################################

    ## ==> STATS
    #############################################################################################
    
    @commands.command()
    async def stats(self,ctx: commands.Context) -> None:
        pyver = str(sys.version[:6])
        embed_ = discord.Embed(title="STATS",color=ctx.author.color,inline=False)
        embed_.add_field(inline=False,name="Uptime",value=str(datetime.timedelta(seconds=int(round(time() - self.STARTTIME)))))
        embed_.add_field(inline=False,name="Ping",value=f"{round(self.bot.latency * 1000)}ms")
        embed_.add_field(inline=False,name="Discord.py version",value=discord.__version__)
        embed_.add_field(inline=False,name="Python Version",value=pyver)
        embed_.add_field(inline=False,name="Server",value=ctx.guild)
        embed_.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed = embed_)

    #############################################################################################
    
    ## ==> MEMES
    #############################################################################################
    
    @commands.command(aliases=["MEME","Meme","MEme","MEMe"])
    async def meme(self,ctx: commands.Context) -> None:
        r = requests.get("https://memes.blademaker.tv/api?lang=en")
        res = r.json()
        embed_ = discord.Embed(title=res['title'],color=discord.Color.blue())
        embed_.set_image(url = res["image"])
        embed_.set_author(name = ctx.author,icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed_)

    @commands.command(aliases=["MEMES","Memes","MEmes","MEMes","MEMEs"])
    async def memes(self,ctx: commands.Context,number:int) -> None:
        if number < 21:
            for i in range(number):
                r = requests.get("https://memes.blademaker.tv/api?lang=en")
                res = r.json()
                embed_ = discord.Embed(title=res['title'],color=discord.Color.blue())
                embed_.set_image(url = res["image"])
                embed_.set_author(name = ctx.author,icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed_)
                
    #############################################################################################
        
## ==> ADDING THE COG TO BOT
#############################################################################################

def setup(bot:commands.Bot) -> None: bot.add_cog(Miscellaneous(bot))

#############################################################################################