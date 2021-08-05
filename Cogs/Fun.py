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
    
    
    ## ==> ROCK PAPER SCISSORS
    #############################################################################################
    
    @commands.command()
    @commands.guild_only()
    async def rps(self, ctx: commands.Context, p2: commands.MemberConverter) -> None:
        
        ## ==> CHECKS
        #############################################################################################
        
        if ctx.author.bot: return
        if p2.bot: 
            await ctx.send("You can't play against a bot!")
            return
        if ctx.author.id == p2.id:
            await ctx.send("You can't invite yourself!")
            return
        
        #############################################################################################
        
        ## ==> CREATING BUTTONS
        #############################################################################################
        
        p1Buttons = [
            Button(label="Rock", style=ButtonStyle.blue, id="p1r", emoji = '🪨'),
            Button(label="Paper", style=ButtonStyle.blue, id="p1p", emoji = '📄'),
            Button(label="Scissors", style=ButtonStyle.blue, id="p1s", emoji = '✂')
        ]
        
        p2Buttons = [
            Button(label="Rock", style=ButtonStyle.red, id="p2r", emoji = '🪨'),
            Button(label="Paper", style=ButtonStyle.red, id="p2p", emoji = '📄'),
            Button(label="Scissors", style=ButtonStyle.red, id="p2s", emoji = '✂')
        ]
        
        buttons = [p1Buttons, p2Buttons]
        
        #############################################################################################
        
        ## ==> CREATE EMBED
        embed = discord.Embed(
                title="ROCK PAPER SCISSORS",
                description=f"{ctx.author.mention} - Blue\n{p2.mention} - Red",
                color=discord.Color.from_rgb(46,49,54)
        )
        
        ## ==> SEND MESSAGE
        message = await ctx.send(
            embed=embed,
            components=buttons
        )
        
        ## ==> DECLARE VARIABLES
        p1choice, p2choice = None, None
        
        ## ==> MAIN LOOP
        #############################################################################################
        
        while True:
            ## ==> GET REACTION
            #########################################################################################
            
            try:
                reaction = await self.bot.wait_for(
                    "button_click",
                    timeout=25.0,
                    check=lambda res: res.user == ctx.author or res.user == p2
                )
            except asyncio.TimeoutError:
                await message.edit(
                    "Either of you guys didn't click on time, so I ended the game",
                    components=[[]]
                )
                return
                
            #############################################################################################      
            
            ## ==> CHECK IF REACTION WAS FROM P1
            #############################################################################################
            
            if reaction.component.id in ['p1r', 'p1p','p1s'] and reaction.user == ctx.author:
                
                ## ==> DISABLE ALL THE BUTTONS FOR P1
                for i in p1Buttons: i._disabled = True
                
                ## ==> TO CHECK IF THIS IS THE LAST REACTION
                if i == 1: 
                    desc = "*Processing...*"
                else: 
                    desc = f"{ctx.author.mention} has got a choice!\n{p2.mention}, choose your quick!"
                ## ==> RESPOND TO REACTION
                await reaction.respond(
                    type=InteractionType.UpdateMessage,
                    embed=discord.Embed(
                        title="ROCK PAPER SCISSORS",
                        description=desc,
                        color=discord.Color.from_rgb(46,49,54)
                    ),
                    components=[p1Buttons, p2Buttons]
                )
                p1choice = reaction.component.label
            
            #############################################################################################
            
            ## ==> TO CHECK IF REACTION WAS FROM P2
            #############################################################################################
            
            elif reaction.component.id in ['p2r', 'p2p', 'p2s'] and reaction.user == p2:
                
                ## ==> DISABLE ALL THE BUTTONS FOR P2
                for i in p2Buttons: i._disabled = True
                
                ## ==> TO CHECK IF THIS IS THE LAST REACTION
                if i == 1: 
                    desc = "*Processing...*"
                else:
                    desc = f"{p2.mention} has got a choice!\n{ctx.author.mention}, choose your quick!"
                    
                ## ==> RESPOND TO REACTION
                await reaction.respond(
                    type=InteractionType.UpdateMessage,
                    embed=discord.Embed(
                        title="ROCK PAPER SCISSORS",
                        description=desc,
                        color=discord.Color.from_rgb(46,49,54)
                    ),
                    components=[p1Buttons, p2Buttons]
                )
                p2choice = reaction.component.label
        
            #############################################################################################
        
            ## ==> CHECK IF BOTH PlAYERS HAVE RESPONDED
            if p1choice is not None and p2choice is not None: break
            
        #############################################################################################
        
        await asyncio.sleep(2.0)
        
        ## ==> CHECK FOR WINNER
        #############################################################################################
        
        ## ==> P1
        #############################################################################################
        if (p1choice.lower(), p2choice.lower()) in [
            ("paper", "rock"),
            ("rock", "scissors"),
            ("scissors", "paper")
        ]:
            await message.edit(
                embed=discord.Embed(
                    title="ROCK PAPER SCISSOR",
                    description=f"""
{ctx.author.mention} chose {p1choice}
{p2.mention} chose {p2choice}
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**{ctx.author.mention} has won!**
""",
                    color=discord.Color.from_rgb(46,49,54)
                ),
                components=[]
            )
        
        #############################################################################################
        
        ## ==> P2
        #############################################################################################
        
        elif (p2choice.lower(), p1choice.lower()) in [("paper", "rock"), ("rock", "scissors"), ("scissors", "paper")]:
            await message.edit(
                embed=discord.Embed(
                    title="ROCK PAPER SCISSOR",
                    description=f"""
{ctx.author.mention} chose {p1choice}
{p2.mention} chose {p2choice}
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**{p2.mention} has won!**
""",
                    color=discord.Color.from_rgb(46,49,54)
                ),
                components=[]
            )
            
        #############################################################################################
        
        ## ==> DRAWED GAME
        else:
            await message.edit(
                embed=discord.Embed(
                    title="ROCK PAPER SCISSOR",
                    description="Both of you chose the same Button, so the game is drawed",
                    color=discord.Color.from_rgb(46,49,54)
                ),
                components=[]
            )
        
        #############################################################################################

    
    #############################################################################################
        
    ## ==> TIC TAC TOE
    #############################################################################################
    
    @commands.command()
    @commands.guild_only()
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
        embed = discord.Embed(
            title="TIC TAC TOE",
            description=f"{p2.mention},{ctx.author.mention} invites you to a game of Tic Tac Toe!",
            color=discord.Color.from_rgb(46,49,54)
        )
        message = await ctx.send(
            embed=embed,
            components=[[accept, decline]]
        )
        
        ## ==> CHECK IF USER RESPONDED
        try:
            res = await self.bot.wait_for("button_click", timeout=25.0, check=lambda res: res.user == p2)
        except asyncio.TimeoutError:
            await message.edit(
                embed=discord.Embed(
                    title="TIC TAC TOE",
                    description=f"Oh no! {p2.name} didn't click any button on time",
                    color=discord.Color.from_rgb(46,49,54)
                    ),
                components=[]
            )
            return
        
        if res.component.label == "Accept":
            await res.respond(
                type = InteractionType.UpdateMessage,
                embed=discord.Embed(
                    title=f"Game between {ctx.author.name} and {p2.name}",
                    description="Please wait for the bot to respond with all emojis",
                    color=discord.Color.from_rgb(46,49,54)
                ),
                components = []
            )
            await asyncio.sleep(2.0)
        elif res.component.label == "Decline":
            await res.respond(
                type = InteractionType.UpdateMessage,
                embed=discord.Embed(
                    title=f"Game between {ctx.author.name} and {p2.name}",
                    description="Match Declined",
                    color=discord.Color.from_rgb(46,49,54)
                ),
                components = []
            )
            return
        
        ##############################################################################################
        
        ## ==> EDIT THE EMBED TO SET THE GRID
        ##############################################################################################
        
        embed = discord.Embed(
            title=f"Game Between {ctx.author.name} and {p2.name}", 
            description="".join(self._board_template), 
            color=discord.Color.from_rgb(46,49,54)
        )
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
                await message.edit(
                    embed=discord.Embed(
                        color=discord.Color.from_rgb(46,49,54),
                        title=f"Game Between {ctx.author.name} and {p2.name}",
                        description=f"{ctx.author.name if _turn == p2 else p2.name} has won the game since {p2.name if _turn == p2 else ctx.author.name} didn't respond in time!"
                    )
                )
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
                await message.edit(
                    embed=discord.Embed(
                        title=f"Game Between {ctx.author.name} and {p2.name}",
                        color=discord.Color.from_rgb(46,49,54),
                        description=f"{_turn} has won the Game!"
                    )
                )
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[3], _current_board[4], _current_board[5]) == (":x:", ":x:", ":x:\n") or (_current_board[3], _current_board[4], _current_board[5]) == (":o:", ":o:", ":o:\n"): 
                await message.clear_reactions()
                await message.edit(
                    embed=discord.Embed(
                        title=f"Game Between {ctx.author.name} and {p2.name}",
                        color=discord.Color.from_rgb(46,49,54),
                        description=f"{_turn} has won the Game!"
                    )
                )
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[6], _current_board[7], _current_board[8]) == (":x:", ":x:", ":x:") or (_current_board[6], _current_board[7], _current_board[8]) == (":o:", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(
                    embed=discord.Embed(
                        title=f"Game Between {ctx.author.name} and {p2.name}",
                        color=discord.Color.from_rgb(46,49,54),
                        description=f"{_turn} has won the Game!"
                    )
                )
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[0], _current_board[3], _current_board[6]) == (":x:", ":x:", ":x:") or (_current_board[0], _current_board[3], _current_board[6]) == (":o:", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(
                    embed=discord.Embed(
                        title=f"Game Between {ctx.author.name} and {p2.name}",
                        color=discord.Color.from_rgb(46,49,54),
                        description=f"{_turn} has won the Game!"
                    )
                )
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[1], _current_board[4], _current_board[7]) == (":x:", ":x:", ":x:") or (_current_board[1], _current_board[4], _current_board[7]) == (":o:", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(
                    embed=discord.Embed(
                        title=f"Game Between {ctx.author.name} and {p2.name}",
                        color=discord.Color.from_rgb(46,49,54),
                        description=f"{_turn} has won the Game!"
                    )
                )
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[2], _current_board[5], _current_board[8]) == (":x:\n", ":x:\n", ":x:") or (_current_board[2], _current_board[5], _current_board[8]) == (":o:\n", ":o:\n", ":o:"): 
                await message.clear_reactions()
                await message.edit(
                    embed=discord.Embed(
                        title=f"Game Between {ctx.author.name} and {p2.name}",
                        color=discord.Color.from_rgb(46,49,54),
                        description=f"{_turn} has won the Game!"
                    )
                )
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[0], _current_board[4], _current_board[8]) == (":x:", ":x:", ":x:") or (_current_board[0], _current_board[4], _current_board[8]) == (":o:", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(
                    embed=discord.Embed(
                        title=f"Game Between {ctx.author.name} and {p2.name}",
                        color=discord.Color.from_rgb(46,49,54),
                        description=f"{_turn} has won the Game!"
                    )
                )
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[2], _current_board[4], _current_board[6]) == (":x:\n", ":x:", ":x:") or (_current_board[2], _current_board[4], _current_board[6]) == (":o:\n", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(
                    embed=discord.Embed(
                        title=f"Game Between {ctx.author.name} and {p2.name}",
                        color=discord.Color.from_rgb(46,49,54),
                        description=f"{_turn} has won the Game!"
                    )
                )
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
            
            embed = discord.Embed(
                title=f"Game Between {ctx.author.name} and {p2.name}",
                color=discord.Color.from_rgb(46,49,54),
                description="".join(_current_board)
            )
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
                await message.edit(
                    embed=discord.Embed(
                        title=f"Game Between {ctx.author.name} and {p2.name}",
                        color=discord.Color.from_rgb(46,49,54),
                        description="Game Draw!"
                    )
                )
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            
            self.data[f"{ctx.author.id} & {p2.id}"]["TURN_NO"] += 1
            
            ##############################################################################################
        
        await ctx.send(
            embed = discord.Embed(
                title=f"Game Between {ctx.author.name} and {p2.name}",
                description=f"Final Board:\n{''.join(_current_board)}",
                color=discord.Color.from_rgb(46,49,54)
            )            
        )
        
        ##############################################################################################
    
    #############################################################################################
    
    ## ==> COIN FLIP
    #############################################################################################
    
    @commands.command()
    async def coin(self, ctx: commands.Context) -> None:
        await ctx.send(
            embed=discord.Embed(
                title="COIN FLIP",
                description=f"Coin has been Tossed: {choice(['Heads', 'Tails'])}",
                color=discord.Color.from_rgb(46,49,54)
            )
        )

    #############################################################################################
    
    ## ==> press f to pay respect
    #############################################################################################
    
    @commands.command()
    async def f(self, ctx: commands.Context, *, reason: str = None) -> None:
        if reason is not None:
            if any(k in reason for k in ["https://", "http://", "discord.com", "discord.gg"]):
                await ctx.send("That reason contains a website D:")
                return
            elif reason.__contains__("<@"):
                await ctx.send("There are pings in the reason")
                return
            else:
                await ctx.send(
                    f"{ctx.author.name} has pressed f to pay respect for reason: {reason.replace('@everyone', 'everyone').replace('@here', 'here')}"
                )
        else:
            await ctx.send(f"{ctx.author.name} has pressed f to pay respect")
    
    #############################################################################################
    
    ## ==> 8BALL
    #############################################################################################

    @commands.command(aliases=['8ball'])
    async def eightBall(self, ctx: commands.Context, *, question) -> None:
        embed = discord.Embed(
            color=discord.Color.from_rgb(46,49,54),
            title="8BALL",
            description=f"Question - {question}?\nAnswer - {choice(self.EIGHT_BALL_ANSWERS)}"
        )
        embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    #############################################################################################

    ## ==> MEMES
    #############################################################################################

    @commands.command()
    async def meme(self,ctx: commands.Context) -> None:
        while True:
            r = requests.get("https://memes.blademaker.tv/api?lang=en")
            res = r.json()
            if res["nsfw"]:
                continue
            embed_ = discord.Embed(title=res['title'],color=discord.Color.from_rgb(46,49,54))
            embed_.set_image(url = res["image"])
            embed_.set_author(name = ctx.author,icon_url = ctx.author.avatar_url)
            embed_.set_footer(text=f"👍 {res['ups']} **|** 👎 {res['downs']}")
            await ctx.send(embed = embed_)
            break

    #############################################################################################

def setup(bot:commands.Bot):
    bot.add_cog(Fun(bot))
