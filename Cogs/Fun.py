import discord, requests, asyncio
from discord.ext import commands
from random import choice
from discord_components import Button, ButtonStyle, InteractionType


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        self.EIGHT_BALL_ANSWERS = [
            "Yeah", "Yes", "Ofcourse", "Ofc", "Ah Yes", "I see in the Prophecy: TRUE!"
            "Nah", "No", 'Nope', 'Never', "I don't think so",
            "idk", "Maybe", "ig", "I'm bored", "You're annoying"
        ]
        
        self._board_template = [
            ":white_large_square:",":white_large_square:",":white_large_square:\n",
            ":white_large_square:",":white_large_square:",":white_large_square:\n",
            ":white_large_square:",":white_large_square:",":white_large_square:"
        ]
        self._emoji_template = ['↖', '⬆', '↗', '⬅', '⏹', '➡', '↙', '⬇', '↘']
        self.data = {}
    
    
    @commands.command()
    async def ttt(self, ctx: commands.Context, p2: commands.MemberConverter) -> None:
        
        ## ==> CHECKS
        ##############################################################################################
        
        if ctx.author.bot: return
        if p2.bot: 
            await ctx.send("You can't play against a bot!")
            return
        if ctx.author.id == p2.id:
            await ctx.send("You can't invite yourself!")
            return
        
        ##############################################################################################
        
        ## ==> ASK FOR A GAME
        #############################################################################################
        
        ## ==> BUTTONS
        accept = Button(label="Accept", style=ButtonStyle.green)
        decline = Button(label="Decline", style=ButtonStyle.red)
        
        ## ==> SEND THE MESSAGES
        embed = discord.Embed(title="TIC TAC TOE", description=f"{p2.mention}, {ctx.author.mention} invites you to a game of Tic Tac Toe!")
        message = await ctx.send(
            embed=embed,
            components=[[accept, decline]]
        )
        
        ## ==> CHECK IF USER RESPONDED
        try:
            res = await self.bot.wait_for("button_click", timeout=25.0, check=lambda res: res.user == p2)
        except asyncio.TimeoutError:
            await message.edit(embed=discord.Embed(title="TIC TAC TOE", description=f"Oh no! {p2.name} didn't click any button on time.", color=discord.Color.red()), components=[])
            return
        
        if res.component.label == "Accept":
            await res.respond(type = InteractionType.UpdateMessage, embed=discord.Embed(title=f"Game between {ctx.author.name} and {p2.name}", description="Please wait for the bot to respond with all emojis", color=discord.Color.green()), components = [])
            await asyncio.sleep(2.0)
        elif res.component.label == "Decline":
            await res.respond(type = InteractionType.UpdateMessage, embed=discord.Embed(title=f"Game between {ctx.author.name} and {p2.name}", description="Match Declined",color=discord.Color.red()), components = [])
            return
        
        ##############################################################################################
        
        ## ==> EDIT THE EMBED TO SET THE GRID
        ##############################################################################################
        
        embed = discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", description="".join(self._board_template), color=ctx.author.color)
        embed.set_footer(text=f"{ctx.author.name}'s Turn")
        await message.edit(embed = embed)
                
        ##############################################################################################
        
        ## ==> VARIABLES
        ##############################################################################################
        
        _turn = ctx.author
        _current_board = self._board_template.copy()
        self.data[f"{ctx.author.id} & {p2.id}"] = {"CUR_REACTION": None, "TURN_NO": 1}
        
        ##############################################################################################
        
        ## ==> ADD REACTIONS
        ##############################################################################################
        
        for i in self._emoji_template: await message.add_reaction(i)
        
        ##############################################################################################
        
        ## ==> CHECK FOR `wait_for`
        ##############################################################################################
        
        def check(reaction, user):
            if user == _turn:
                self.data[F"{ctx.author.id} & {p2.id}"]["CUR_REACTION"] = str(reaction.emoji)
            return user == _turn
        
        ##############################################################################################        
           
        ## ==> MAIN LOOP
        ##############################################################################################
        
        while True:
            
            ## ==> TO CHECK IF WHAT THE USER REACTED WITH IS VALID OR NOT
            ##############################################################################################
            
            x = []
            for index, item in enumerate(_current_board):
                if item == ":white_large_square:" or item == ":white_large_square:\n":
                    if index == 0:
                        x.append(self._emoji_template[0])
                    if index == 1:
                        x.append(self._emoji_template[1])
                    if index == 2:
                        x.append(self._emoji_template[2])
                    if index == 3:
                        x.append(self._emoji_template[3])
                    if index == 4:
                        x.append(self._emoji_template[4])
                    if index == 5:
                        x.append(self._emoji_template[5])
                    if index == 6:
                        x.append(self._emoji_template[6])
                    if index == 7:
                        x.append(self._emoji_template[7])
                    if index == 8:
                        x.append(self._emoji_template[8])
            
            ##############################################################################################
            
            ## ==> WAIT FOR PLAYER TO REACT
            ##############################################################################################
            
            try: await self.bot.wait_for("reaction_add", timeout=25.0, check=check)
            except asyncio.TimeoutError:
                await message.edit(embed=discord.Embed(color=discord.Color.green(), title=f"Game Between {ctx.author.name} and {p2.name}", description=f"{ctx.author.name if _turn == p2 else p2.name} has won the game since {p2.name if _turn == p2 else ctx.author.name} didn't respond in time!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
                
            ##############################################################################################
            
            ## ==> CHECK IF REACTION WAS VALID OR NOT
            ##############################################################################################
            
            if self.data[f"{ctx.author.id} & {p2.id}"]["CUR_REACTION"] not in x:
                await message.remove_reaction(self.data[f"{ctx.author.id} & {p2.id}"]["CUR_REACTION"], _turn)
                continue
            
            ##############################################################################################
            
            ## ==> PUT THE MARK ON THE BOARD
            ##############################################################################################
            
            index = f"{ctx.author.id} & {p2.id}"
                
            mark = ":x:" if _turn == ctx.author else ":o:"
                
            if self.data[index]["CUR_REACTION"] == self._emoji_template[0]:
                _current_board[0] = mark
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[1]:
                _current_board[1] = mark
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[2]:
                _current_board[2] = f"{mark}\n"
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[3]:
                _current_board[3] = mark
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[4]:
                _current_board[4] = mark
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[5]:
                _current_board[5] = f"{mark}\n"
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[6]:
                _current_board[6] = mark
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[7]:
                _current_board[7] = mark
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[8]:
                _current_board[8] = mark
            
            ##############################################################################################
            
            ## ==> CHECK FOR WINNER
            ##############################################################################################
            
            if (_current_board[0], _current_board[1], _current_board[2]) == (":x:", ":x:", ":x:\n") or (_current_board[0], _current_board[1], _current_board[2]) == (":o:", ":o:", ":o:\n"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[3], _current_board[4], _current_board[5]) == (":x:", ":x:", ":x:\n") or (_current_board[3], _current_board[4], _current_board[5]) == (":o:", ":o:", ":o:\n"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[6], _current_board[7], _current_board[8]) == (":x:", ":x:", ":x:") or (_current_board[6], _current_board[7], _current_board[8]) == (":o:", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[0], _current_board[3], _current_board[6]) == (":x:", ":x:", ":x:") or (_current_board[0], _current_board[3], _current_board[6]) == (":o:", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[1], _current_board[4], _current_board[7]) == (":x:", ":x:", ":x:") or (_current_board[1], _current_board[4], _current_board[7]) == (":o:", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[2], _current_board[5], _current_board[8]) == (":x:\n", ":x:\n", ":x:") or (_current_board[2], _current_board[5], _current_board[8]) == (":o:\n", ":o:\n", ":o:"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[0], _current_board[4], _current_board[8]) == (":x:", ":x:", ":x:") or (_current_board[0], _current_board[4], _current_board[8]) == (":o:", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[2], _current_board[4], _current_board[6]) == (":x:\n", ":x:", ":x:") or (_current_board[2], _current_board[4], _current_board[6]) == (":o:\n", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            
            ##############################################################################################
            
            ## ==> CHANGE THE TURN TO THE OTHER PLAYER
            ##############################################################################################
            
            _turn = p2 if _turn == ctx.author else ctx.author
            
            ##############################################################################################            
            
            ## ==> RESET X FOR THE BOT TO REACT TO THE EMBED
            ##############################################################################################
            
            x = []
            for index, item in enumerate(_current_board):
                if item == ":white_large_square:" or item == ":white_large_square:\n":
                    if index == 0:
                        x.append(self._emoji_template[0])
                    if index == 1:
                        x.append(self._emoji_template[1])
                    if index == 2:
                        x.append(self._emoji_template[2])
                    if index == 3:
                        x.append(self._emoji_template[3])
                    if index == 4:
                        x.append(self._emoji_template[4])
                    if index == 5:
                        x.append(self._emoji_template[5])
                    if index == 6:
                        x.append(self._emoji_template[6])
                    if index == 7:
                        x.append(self._emoji_template[7])
                    if index == 8:
                        x.append(self._emoji_template[8])
            
            ##############################################################################################
            
            ## ==> UPDATE THE EMBED
            ##############################################################################################
            
            embed = discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description="".join(_current_board))
            embed.set_footer(text=f"{_turn.name}'s Turn")
            await message.edit(embed=embed)
            await message.clear_reactions()
            for i in x: await message.add_reaction(i)
            del x
            
            ##############################################################################################
            
            ## ==> UPDATE TURN NUMBER
            ##############################################################################################
            
            # IF TURN NUMBER = 9, GAME IS OVER
            
            if self.data[f"{ctx.author.id} & {p2.id}"]["TURN_NO"] == 9:
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=discord.Color.green(), description="Game Draw!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            
            self.data[f"{ctx.author.id} & {p2.id}"]["TURN_NO"] += 1
            
            ##############################################################################################
        
        await ctx.send(embed = discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", description=f"Final Board:\n{''.join(_current_board)}", color=ctx.author.color))
        
        ##############################################################################################
    
    
    ## ==> COIN FLIP
    #############################################################################################
    
    @commands.command()
    async def coin(self, ctx: commands.Context) -> None:
        await ctx.send(embed=discord.Embed(title="COIN FLIP", description=f"Coin has been Tossed: {choice(['Heads', 'Tails'])}", color=discord.Color.green()))

    #############################################################################################
    
    ## ==> press f to pay respect
    #############################################################################################
    
    @commands.command()
    async def f(self, ctx: commands.Context, *, reason: str = None) -> None:
        if reason is not None:
            if reason.__contains__("https://"):
                await ctx.send("That reason contains a website D:")
                return
            elif reason.__contains__("<@"):
                await ctx.send("There are pings in the reason")
                return
            else:
                await ctx.send(f"{ctx.author.name} has pressed f to pay respect for reason: {reason.replace('@everyone', 'everyone').replace('@here', 'here')}" if reason is not None else f"{ctx.author.name} has pressed f to pay respect")
        else:
            await ctx.send(f"{ctx.author.name} has pressed f to pay respect for reason: {reason.replace('@everyone', 'everyone').replace('@here', 'here')}" if reason is not None else f"{ctx.author.name} has pressed f to pay respect")
    
    #############################################################################################
    
    ## ==> 8BALL
    #############################################################################################

    @commands.command(aliases=['8ball'])
    async def eightBall(self, ctx: commands.Context, *, question) -> None:
        embed = discord.Embed(color=ctx.author.color, title="8BALL", description=f"Question - {question}?\nAnswer - {choice(self.EIGHT_BALL_ANSWERS)}")
        embed.set_author(name=str(ctx.author)[:-5], icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    #############################################################################################

    ## ==> MEMES
    #############################################################################################

    @commands.command()
    async def meme(self,ctx: commands.Context) -> None:
        r = requests.get("https://memes.blademaker.tv/api?lang=en")
        res = r.json()
        embed_ = discord.Embed(title=res['title'],color=discord.Color.blue())
        embed_.set_image(url = res["image"])
        embed_.set_author(name = ctx.author,icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed_)

    @commands.command()
    async def memes(self, ctx: commands.Context, number: int = 3) -> None:
        if number <= 3:
            for i in range(number):
                r = requests.get("https://memes.blademaker.tv/api?lang=en")
                res = r.json()
                embed_ = discord.Embed(title=res['title'], color=discord.Color.blue())
                embed_.set_image(url = res["image"])
                embed_.set_author(name = ctx.author,icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed_)

    #############################################################################################

def setup(bot:commands.Bot):
    bot.add_cog(Fun(bot))
