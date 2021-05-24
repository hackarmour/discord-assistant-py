import discord
from discord.ext import commands

class Miscellaneous(commands.Cog):
    def __init__(self,bot: commands.Bot) -> None: 
        self.bot = bot
        
    ## ==> ERROR HANDLING
    #############################################################################################
    
    # @commands.Cog.listener()
    # async def on_command_error(self,ctx,error): await error.channel.send(embed=discord.Embed(title="Whoops",color=discord.Color.red(),description=f"An error occured while trying to run that command\n{error}"))
    
    #############################################################################################
    
    ## ==> HELP COMMAND
    #############################################################################################
    
    @commands.command()
    async def help(self, ctx: commands.Context) -> None:
        embed = discord.Embed(title="HELP",color=ctx.author.color)
        embed.set_footer(text="Developed By [ᴛʜᴇ ᴇᴍᴘᴇʀᴏʀ]")
        
        embed.add_field(
            name=":partying_face: **WELCOMER**",
            inline=False,
            value="""
**[ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀ ᴏɴʟʏ]**

:white_check_mark: `>toggle`:
    To Toggle Welcomer On or Off

:scroll: `>SetWelcomeMessage <message>`:
    To Set the Welcome Message
    Using `|user|` in message will replace it with a mention of the new user    -> Important
    Using `|guild|` in message will replace it with the name of the server
    
:dart: `>SetChannel <Channel>`:
    To Set the channel to send Welcome message in
    Mention channel as #<channel name>
"""
        )
        
        embed.add_field(
            name=":game_die: TIC TAC TOE",
            inline=False,
            value="""
--------------------------------------------------------------------------------------

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
        
        await ctx.send(embed=embed)
    
    #############################################################################################

## ==> ADDING THE COG TO BOT
#############################################################################################

def setup(bot:commands.Bot) -> None: bot.add_cog(Miscellaneous(bot))

#############################################################################################