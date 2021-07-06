import discord, asyncio
from discord.ext import commands

class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # The two following variables are to store the data 
        self.MEMBER_DATA = {}
        self.BOARDS = {}
        
        self.DEFAULT_BOARD = [
            ":white_large_square:",":white_large_square:",":white_large_square:",
            ":white_large_square:",":white_large_square:",":white_large_square:",
            ":white_large_square:",":white_large_square:",":white_large_square:"
        ]
    
    # Invite a member to a game
    @commands.command()
    async def ttt(self, ctx: commands.Context, p2: commands.MemberConverter) -> None:
       
        # Some checks
        if ctx.author.id == p2.id:
            await ctx.send("You can't invite yourself!")
            return
        
        if ctx.author.bot:
            return
        
        if p2.bot:
            await ctx.send("That member is a bot")
            return
        
        # Check if the inviter is already in, asking or requested for a game
        if ctx.author.id in self.MEMBER_DATA.keys():
            if self.MEMBER_DATA[ctx.author.id]["inGame"]:
                await ctx.send("You're already in a Game")
                return
            elif self.MEMBER_DATA[ctx.author.id]["askingGame"]:
                await ctx.send("You're already asking for a Game")
                return
            elif self.MEMBER_DATA[ctx.author.id]["requestedToPlay"]:
                await ctx.send("You're already requesting someone else to play")
            else:
                self.MEMBER_DATA[ctx.author.id] = {"askingGame":p2.id,"askingGameTo":p2.id,"inGame":False,"inGameWith":None,"requestedToPlay":False,"requestedToPlayBy":None,"TIMEUP":False}
        else:
            self.MEMBER_DATA[ctx.author.id] = {"askingGame":p2.id,"askingGameTo":p2.id,"inGame":False,"inGameWith":None,"requestedToPlay":False,"requestedToPlayBy":None,"TIMEUP":False}
        
        # Same checks for player 2
        if p2.id in self.MEMBER_DATA.keys():
            if self.MEMBER_DATA[p2.id]["inGame"]:
                await ctx.send(f"That user is already in a Game")
                self.MEMBER_DATA[ctx.author.id] = {"askingGame":False,"askingGameTo":None,"inGame":False,"inGameWith":None,"requestedToPlay":True,"requestedToPlayBy":ctx.author.id}
                return
            elif self.MEMBER_DATA[p2.id]["askingGame"]:
                await ctx.send("That user is asking for a game to someone else")
                self.MEMBER_DATA[ctx.author.id] = {"askingGame":False,"askingGameTo":None,"inGame":False,"inGameWith":None,"requestedToPlay":True,"requestedToPlayBy":ctx.author.id}
                return
        else:
            self.MEMBER_DATA[p2.id] = {"askingGame":False,"askingGameTo":None,"inGame":False,"inGameWith":None,"requestedToPlay":True,"requestedToPlayBy":ctx.author.id}

        # Embed to request a game
        DESC = f""""
{p2.mention}, {ctx.author.mention} invites you to a game of Tic Tac Toe!

Use `>accept @{ctx.author}` to accept the invite
Use `>unaccept @{ctx.author}` to unaccept the invite
"""
        embed_ = discord.Embed(title = "TIC TAC TOE",description = DESC,color=discord.Color.green())
        embed_.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed_)

        # Timeout if player 2 did not accept
        await asyncio.sleep(15)
        try:
            if self.MEMBER_DATA[ctx.author.id]["inGame"]: return
            else:
                await ctx.send("Request Timed Out")
                del self.MEMBER_DATA[ctx.author.id], self.MEMBER_DATA[p2.id]
        except KeyError: pass
        
    # Accept a game
    @commands.command()
    async def accept(self, ctx: commands.Context, p1: commands.MemberConverter) -> None:
        
        # Check if player 2 is 
        ## available to play 
        ## or asked for game        
        if p1.id in self.MEMBER_DATA.keys():
            if self.MEMBER_DATA[p1.id]["askingGameTo"] != ctx.author.id:
                await ctx.send(f"{p1.mention} isn't asking you to play")
                del self.MEMBER_DATA[ctx.author.id]
                return
                
            elif self.MEMBER_DATA[p1.id]["inGame"]:
                await ctx.send(f"You're already in a Game")
                del self.MEMBER_DATA[ctx.author.id]
                return
            elif self.MEMBER_DATA[p1.id]["requestedToPlay"]:
                await ctx.send(f"You're asked by someone else to play: <@{self.MEMBER_DATA[ctx.author.id]['requestedToPlayBy']}>")
                del self.MEMBER_DATA[ctx.author.id]
                return
        else:
            await ctx.send("You're not requested by anyone to play")
            return

        # Embed to notify the players to play
        DESC = f"""
The Game Has begun, {ctx.author.mention} and {p1.mention}
Bring it On!
"""

        embed_ = discord.Embed(description=DESC,title="TIC TAC TOE",color=discord.Color.green())
        embed_.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed_)
        
        # Change the data in the variables        
        self.MEMBER_DATA[p1.id] = {"askingGame":False,"askingGameTo":None,"inGame":True,"inGameWith":ctx.author.id,"requestedToPlay":False,"requestedToPlayBy":None}
        self.MEMBER_DATA[ctx.author.id] = {"askingGame":False,"askingGameTo":None,"inGame":True,"inGameWith":p1.id,"requestedToPlay":False,"requestedToPlayBy":None}
        
        self.BOARDS[ctx.author.id] = {"BOARD":self.DEFAULT_BOARD.copy(),"OPPONENT":p1.id,"MARK":"x","IN_TURN":True,"POS":1,"EXIT":False}
        self.BOARDS[p1.id] = {"BOARD":self.DEFAULT_BOARD.copy(),"OPPONENT":ctx.author.id,"MARK":"o","IN_TURN":False,"POS":1,"EXIT":False}
        
    # Exit the game
    @commands.command(aliases=["quit"])
    async def exit(self,ctx: commands.Context,p2:commands.MemberConverter) -> None:
        
        # Checks
        if ctx.author.id not in self.MEMBER_DATA.keys():
            await ctx.send("You're not playing")
            return
        else:
            if self.MEMBER_DATA[ctx.author.id]["inGame"] and self.MEMBER_DATA[ctx.author.id]["inGameWith"]!= p2.id:
                await ctx.send("That user is not the one you want to quit playing with")
                return
            elif self.MEMBER_DATA[ctx.author.id]["inGame"] and self.MEMBER_DATA[ctx.author.id]["inGameWith"] == p2.id: pass        
            else:
                await ctx.send("You're not playing")
                return
          
        if p2.id not in self.MEMBER_DATA.keys():
            await ctx.send("You're not playing")
            return
        else:
            if self.MEMBER_DATA[p2.id]["inGame"] and self.MEMBER_DATA[p2.id]["inGameWith"]!= ctx.author.id:
                await ctx.send("That user is not playing with you")
                return
            elif self.MEMBER_DATA[p2.id]["inGame"] and self.MEMBER_DATA[p2.id]["inGameWith"] == ctx.author.id: pass
            else:
                await ctx.send("You're not playing")
                return
            
        # Change set exit vote true for author
        self.BOARDS[ctx.author.id]["EXIT"] = True
        
        # Check if player 2 has voted to exit too        
        if self.BOARDS[p2.id]["EXIT"]:
            DESC = f"""
    The match between {p2.mention} and {ctx.author.mention} has been exited
    """
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[p2.id],self.BOARDS[ctx.author.id], self.BOARDS[p2.id]
        else:
            DESC = f"""
{p2.mention}, {ctx.author.mention} wants to end the match
Use `>exit` to exit or ignore this message to continue
""" 
        embed_ = discord.Embed(title="TIC TAC TOE",description=DESC,color=discord.Color.red())

        await ctx.send(embed=embed_)

    # Declined invitation
    @commands.command(aliases=["decline"])
    async def unaccept(self, ctx: commands.Context, p1: commands.MemberConverter) -> None:
        
        # Check if player 2 isavailable to play
        if p1.id in self.MEMBER_DATA.keys():
            if self.MEMBER_DATA[p1.id]["askingGameTo"] != ctx.author.id:
                await ctx.send(f"{p1.mention} isn't asking you to play")
                del self.MEMBER_DATA[ctx.author.id]
                return
            elif self.MEMBER_DATA[p1.id]["inGame"]:
                await ctx.send(f"You're already in a Game")
                del self.MEMBER_DATA[ctx.author.id]
                return
            elif self.MEMBER_DATA[p1.id]["requestedToPlay"]:
                await ctx.send(f"You're asked by someone else to play: <@{self.MEMBER_DATA[ctx.author.id]['requestedToPlayBy']}>")
                del self.MEMBER_DATA[ctx.author.id]
                return
        else:
            await ctx.send("You're not requested by anyone to play")
            return
        
        del self.MEMBER_DATA[p1.id], self.MEMBER_DATA[ctx.author.id]
        
        DESC = f"""
{p1.mention}, {ctx.author.mention} has unaccepted your invite
Why not try someone else?        
"""
        
        embed_ = discord.Embed(description=DESC,title="TIC TAC TOE",color=discord.Color.red())
        embed_.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed_)
    
    # Place
    @commands.command(aliases=["set"])
    async def place(self, ctx: commands.Context, no: int):
        
        # Checks
        if ctx.author.id in self.BOARDS.keys(): pass
        else:
            await ctx.send("You are not playing")
            return
        
           
        if no not in [1,2,3,4,5,6,7,8,9]:
            await ctx.send("That is an invalid number")
            return
        
        if self.BOARDS[ctx.author.id]["IN_TURN"]:pass
        else:
            await ctx.send("It isn't your turn")
            return

        if self.BOARDS[ctx.author.id]["BOARD"][no-1] != ":white_large_square:":
            await ctx.send("That place is already occupied")
            return
      
        # Opponent
        
        OtherP = self.BOARDS[ctx.author.id]["OPPONENT"]

        # Change value on board
        self.BOARDS[ctx.author.id]["BOARD"][no-1] = f":regional_indicator_{self.BOARDS[ctx.author.id]['MARK']}:"
        self.BOARDS[OtherP]["BOARD"][no-1] = f":regional_indicator_{self.BOARDS[ctx.author.id]['MARK']}:"

        # Change to opponent's turn
        self.BOARDS[ctx.author.id]["IN_TURN"] = False
        self.BOARDS[OtherP]["IN_TURN"] = True
        
        # The current board
        board_temp = [
            self.BOARDS[ctx.author.id]['BOARD'][0],self.BOARDS[ctx.author.id]['BOARD'][1],self.BOARDS[ctx.author.id]['BOARD'][2],
            self.BOARDS[ctx.author.id]['BOARD'][3],self.BOARDS[ctx.author.id]['BOARD'][4],self.BOARDS[ctx.author.id]['BOARD'][5],
            self.BOARDS[ctx.author.id]['BOARD'][6],self.BOARDS[ctx.author.id]['BOARD'][7],self.BOARDS[ctx.author.id]['BOARD'][8]
        ]
        
        # Board for sending in channel
        boardprint = f"""
{self.BOARDS[ctx.author.id]['BOARD'][0]} {self.BOARDS[ctx.author.id]['BOARD'][1]} {self.BOARDS[ctx.author.id]['BOARD'][2]}
{self.BOARDS[ctx.author.id]['BOARD'][3]} {self.BOARDS[ctx.author.id]['BOARD'][4]} {self.BOARDS[ctx.author.id]['BOARD'][5]}  
{self.BOARDS[ctx.author.id]['BOARD'][6]} {self.BOARDS[ctx.author.id]['BOARD'][7]} {self.BOARDS[ctx.author.id]['BOARD'][8]} 
"""
        await ctx.send(boardprint)
        x = ":regional_indicator_x:"
        o = ":regional_indicator_o:"
        
        # Check winner

        ## X - vertical
        if board_temp[0] == x and board_temp[1] == x and board_temp[2] == x:
            await ctx.send("X is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
            return
            
        elif board_temp[3] == x and board_temp[4] == x and board_temp[5] == x:
            await ctx.send("X is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
            return
            
        elif board_temp[6] == x and board_temp[7] == x and board_temp[8] == x:
            await ctx.send("X is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
            return
        
        ## X - horizontal
        elif board_temp[0] == x and board_temp[3] == x and board_temp[6] == x:
            await ctx.send("X is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
            return
            
        elif board_temp[1] == x and board_temp[4] == x and board_temp[7] == x:
            await ctx.send("X is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
            return
            
        elif board_temp[2] == x and board_temp[5] == x and board_temp[8] == x:
            await ctx.send("X is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
            return    
        
        # X - diagonal
        elif board_temp[0] == x and board_temp[4] == x and board_temp[8] == x:
            await ctx.send("X is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
            return
            
        elif board_temp[2] == x and board_temp[4] == x and board_temp[6] == x:
            await ctx.send("X is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]  
            return  
            
        # O - vertical
        if board_temp[0] == o and board_temp[1] == o and board_temp[2] == o:
            await ctx.send("O is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
            return
            
        elif board_temp[3] == o and board_temp[4] == o and board_temp[5] == o:
            await ctx.send("O is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
            return
            
        elif board_temp[6] == o and board_temp[7] == o and board_temp[8] == o:
            await ctx.send("O is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
            return
        
        ## O - horizontal
        elif board_temp[0] == o and board_temp[3] == o and board_temp[6] == o:
            await ctx.send("O is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
            return
            
        elif board_temp[1] == o and board_temp[4] == o and board_temp[7] == o:
            await ctx.send("O is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
            return
            
        elif board_temp[2] == o and board_temp[5] == o and board_temp[8] == o:
            await ctx.send("O is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP] 
            return   
        
        ## O - diagonal
        elif board_temp[0] == o and board_temp[4] == o and board_temp[8] == o:
            await ctx.send("O is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
            return
            
        elif board_temp[2] == o and board_temp[4] == o and board_temp[6] == o:
            await ctx.send("O is the WINNER")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
            return
        
        if self.BOARDS[ctx.author.id]["POS"] == 9:
            await ctx.send("Match Draw")
            del self.MEMBER_DATA[ctx.author.id],self.MEMBER_DATA[OtherP]
            del self.BOARDS[ctx.author.id],self.BOARDS[OtherP]
        
        try:
            self.BOARDS[ctx.author.id]["POS"] += 1
            self.BOARDS[OtherP]["POS"] += 1
        except KeyError: pass

        del board_temp
        
def setup(bot):
    bot.add_cog(TicTacToe(bot))
