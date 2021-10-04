import discord, requests, asyncio, json
from discord.ext import commands
from random import choice
from discord_components import Button, ButtonStyle, InteractionType


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        ## ==> READ VALUES
        with open("Configuration/config.json") as f:
            cfg = json.load(f)
            self.fail_emoji = cfg["fail_emoji"]
            self.success_emoji = cfg["success_emoji"]
            embed_color = cfg["embed_color"]
            self.r = embed_color[0]
            self.g = embed_color[1]
            self.b = embed_color[2]
            
            
        self.EIGHT_BALL_ANSWERS = [
            "Yeah", "Yes", "Ofcourse", "Ofc", "Ah Yes", "I see in the Prophecy: TRUE!"
            "Nah", "No", 'Nope', 'Never', "I don't think so",
            "idk", "Maybe", "ig", "I'm bored", "You're annoying"
        ]
        
    
    
    ## ==> ROCK PAPER SCISSORS
    #############################################################################################
    
    @commands.command(
        help="""
` `- **To Play Rock Paper Scissors With <p2>**
"""
    )
    @commands.guild_only()
    async def rps(self, ctx: commands.Context, p2: commands.MemberConverter) -> None:
        
        ## ==> CHECKS
        #############################################################################################
        
        if ctx.author.bot: return
        if p2.bot: 
            await ctx.send(f"{self.fail_emoji} You can't play against a bot!")
            return
        if ctx.author.id == p2.id:
            await ctx.send(f"{self.fail_emoji} You can't invite yourself!")
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
                color=discord.Color.from_rgb(self.r, self.g, self.b)
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
                for i in p1Buttons: i.disabled = True
                
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
                        color=discord.Color.from_rgb(self.r, self.g, self.b)
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
                        color=discord.Color.from_rgb(self.r, self.g, self.b)
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
                    color=discord.Color.from_rgb(self.r, self.g, self.b)
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
                    color=discord.Color.from_rgb(self.r, self.g, self.b)
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
    
    @commands.command(
        help="""
` `- **To Play Tic Tac Toe With <p2>**
"""
    )
    async def ttt(self, ctx: commands.Context, p2: commands.MemberConverter) -> None:
        
        if ctx.author.bot: return
        if p2.bot: 
            await ctx.send(f"{self.fail_emoji} You can't play against a bot!")
            return
        if ctx.author == p2:
            await ctx.send(f"{self.fail_emoji} You can't invite yourself!")
            return
        
        
        ## ==> BUTTONS
        accept = Button(label="Accept", style=ButtonStyle.green)
        decline = Button(label="Decline", style=ButtonStyle.red)
        
        ## ==> SEND THE MESSAGES
        embed = discord.Embed(
            title="TIC TAC TOE",
            description=f"{p2.mention},{ctx.author.mention} invites you to a game of Tic Tac Toe!",
            color=discord.Color.from_rgb(self.r, self.g, self.b)
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
                    description=f"{self.fail_emoji} Oh no! {p2.name} didn't click any button on time",
                    color=discord.Color.from_rgb(self.r, self.g, self.b)
                    ),
                components=[]
            )
            return
        
        ## ==> CONTINUE THE GAME IF THE USER CLICKED ACCEPT BUTTON
        if res.component.label == "Accept":
            await res.respond(
                type = InteractionType.UpdateMessage,
                embed=discord.Embed(
                    title=f"Game between {ctx.author.name} and {p2.name}",
                    description="Get ready to play!",
                    color=discord.Color.from_rgb(self.r, self.g, self.b)
                ),
                components = []
            )
            await asyncio.sleep(2.0)
            
        ## ==> STOP THE GAME IF USER PRESSED DECLINE BUTTON
        elif res.component.label == "Decline":
            await res.respond(
                type = InteractionType.UpdateMessage,
                embed=discord.Embed(
                    title=f"Game between {ctx.author.name} and {p2.name}",
                    description="Match Declined",
                    color=discord.Color.from_rgb(self.r, self.g, self.b)
                ),
                components = []
            )
            return
        
        ## ==> START GAME
        ##############################################################################################
        
        ## ==> BOARD
        board = [
            [Button(label = " ", style=ButtonStyle.green, id="0"), Button(label = " ", style=ButtonStyle.green, id="1"), Button(label = " ", style=ButtonStyle.green, id="2")],
            [Button(label = " ", style=ButtonStyle.green, id="3"), Button(label = " ", style=ButtonStyle.green, id="4"), Button(label = " ", style=ButtonStyle.green, id="5")],
            [Button(label = " ", style=ButtonStyle.green, id="6"), Button(label = " ", style=ButtonStyle.green, id="7"), Button(label = " ", style=ButtonStyle.green, id="8")]
        ]
        
        ## ==> VARIABLES
        i, _turn = 0, ctx.author
        
        ## ==> EDIT THE MESSAGE TO START GAME
        await message.edit(
            embed=discord.Embed(
                title="TIC TAC TOE",
                color=discord.Color.from_rgb(self.r, self.g, self.b),
                description=f"{_turn.mention}'s turn"
            ),
            components=board
        )
        
        ## ==> MAIN LOOP
        ##############################################################################################
        xyz = 0
        while i < 9:
            
            ## ==> GET INTERACTION
            try:
                interaction = await self.bot.wait_for(
                    "button_click",
                    timeout=25,
                    check=lambda i: i.user == _turn
                )
                
            ## ==> THIS IS RAN ONLY WHEN THERE IS A TIMEOUT
            except asyncio.TimeoutError:
                oppositeTurn = ctx.author.mention if _turn == p2 else p2.mention
                
                ## ==> DISABLE ALL THE BUTTONS
                for j in board: 
                    for k in j: k.disabled = True
                    
                ## ==> EDIT MESSAGE AND DECLARE WINNER
                await message.edit(
                    embed=discord.Embed(
                        title="TIC TAC TOE",
                        color=discord.Color.from_rgb(self.r, self.g, self.b),
                        description=f"{oppositeTurn} has **won** the game since {_turn.mention} didn't click on any buttons in time!"
                    ),
                    components=board
                )
                
                return
            
            
            ## ==> CHECK IF THE BUTTON PRESSED IS OCCUPIED
            if str(interaction.component.id).startswith("occupied"):
                await interaction.respond(
                    InteractionType = InteractionType.ChannelMessageWithSource,
                    content="That Place is occupied"
                )
                continue

            ## ==> EMPTY LIST
            indexes = []
            
            ## ==> GET THE INDEXES OF THE BUTTON PRESSED
            for index, item in enumerate(board):
                for index2, item2 in enumerate(item):
                    if item2.id == interaction.component.id:
                        indexes.append(index)
                        indexes.append(index2)
            
            ## ==> CHANGE THE MARK AND ID
            board[indexes[0]][indexes[1]].style = ButtonStyle.red if _turn == ctx.author else ButtonStyle.blue
            board[indexes[0]][indexes[1]].id = f"occupied{xyz}"
            xyz += 1
            
            ## ==> CHANGE TURN
            _turn = ctx.author if _turn == p2 else p2

            
            ## ==> CHECK IF ANYONE WON
            winCondition = (
                (board[0][0].style, board[1][0].style, board[2][0].style) == (ButtonStyle.red, ButtonStyle.red, ButtonStyle.red) 
                or
                (board[0][1].style, board[1][1].style, board[2][1].style) == (ButtonStyle.red, ButtonStyle.red, ButtonStyle.red)
                or
                (board[0][2].style, board[1][2].style, board[2][2].style) == (ButtonStyle.red, ButtonStyle.red, ButtonStyle.red)
                or 
                (board[0][0].style, board[1][1].style, board[2][2].style) == (ButtonStyle.red, ButtonStyle.red, ButtonStyle.red)
                or
                (board[0][2].style, board[1][1].style, board[2][0].style) == (ButtonStyle.red, ButtonStyle.red, ButtonStyle.red)
                or
                (board[0][0].style, board[0][1].style, board[0][2].style) == (ButtonStyle.red, ButtonStyle.red, ButtonStyle.red)
                or
                (board[1][0].style, board[1][1].style, board[1][2].style) == (ButtonStyle.red, ButtonStyle.red, ButtonStyle.red)
                or
                (board[2][0].style, board[2][1].style, board[2][2].style) == (ButtonStyle.red, ButtonStyle.red, ButtonStyle.red)
            
                or
                
                (board[0][0].style, board[1][0].style, board[2][0].style) == (ButtonStyle.blue, ButtonStyle.blue, ButtonStyle.blue) 
                or
                (board[0][1].style, board[1][1].style, board[2][1].style) == (ButtonStyle.blue, ButtonStyle.blue, ButtonStyle.blue)
                or
                (board[0][2].style, board[1][2].style, board[2][2].style) == (ButtonStyle.blue, ButtonStyle.blue, ButtonStyle.blue)
                or 
                (board[0][0].style, board[1][1].style, board[2][2].style) == (ButtonStyle.blue, ButtonStyle.blue, ButtonStyle.blue)
                or
                (board[0][2].style, board[1][1].style, board[2][0].style) == (ButtonStyle.blue, ButtonStyle.blue, ButtonStyle.blue)
                or
                (board[0][0].style, board[0][1].style, board[0][2].style) == (ButtonStyle.blue, ButtonStyle.blue, ButtonStyle.blue)
                or
                (board[1][0].style, board[1][1].style, board[1][2].style) == (ButtonStyle.blue, ButtonStyle.blue, ButtonStyle.blue)
                or
                (board[2][0].style, board[2][1].style, board[2][2].style) == (ButtonStyle.blue, ButtonStyle.blue, ButtonStyle.blue)
            )

            ## ==> RAN IF ANYONE WON
            if winCondition:
                
                ## ==> DISABLE BUTTONS
                for j in board: 
                    for k in j: k.disabled = True
                    
                ## ==> ANNOUNCE WINNER
                await interaction.respond(
                    type=InteractionType.UpdateMessage,
                    embed=discord.Embed(
                        title="TIC TAC TOE",
                        color = discord.Color.from_rgb(self.r, self.g, self.b),
                        description=f"{p2.mention if _turn == ctx.author else ctx.author.mention} **has won!**"
                    ),
                    components=board
                )
                return
            
            ## ==> RAN IF ANYONE DIDN'T WIN
            else:
                
                ## ==> UPDATE MESSAGE
                await interaction.respond(
                    type = InteractionType.UpdateMessage,
                    embed=discord.Embed(
                        title=f"Game between {ctx.author.name} and {p2.name}",
                        color = discord.Color.from_rgb(self.r, self.g, self.b),
                        description=f"{_turn.mention}'s turn"
                    ),
                    components = board
                )
                
            ## ==> INCREMENT i
            i += 1
            
        ##############################################################################################
        
        ## ==> RAN IF THE WHILE LOOP'S CONDITION IS FALSE, IE, WHEN THE GAME IS DRAWED
        else:
            
            ## ==> DISABLE BUTTONS
            for i in board: 
                for j in i: j.disabled = True
                
            ## ==> ANNOUNCE GAME DRAW
            await message.edit(
                embed=discord.Embed(
                    title="TIC TAC TOE",
                    color = discord.Color.from_rgb(self.r, self.g, self.b),
                    description=f"Game Draw!"
                ),
                components=board
            )
        
        ##############################################################################################
    
    ## ==> COIN FLIP
    #############################################################################################
    
    @commands.command(
        help="""
` `- **To Flip a Coin**
"""
    )
    async def coin(self, ctx: commands.Context) -> None:
        await ctx.send(
            embed=discord.Embed(
                title="COIN FLIP",
                description=f"Coin has been Tossed: {choice(['Heads', 'Tails'])}",
                color=discord.Color.from_rgb(self.r, self.g, self.b)
            )
        )

    #############################################################################################
    
    ## ==> press f to pay respect
    #############################################################################################
    
    @commands.command(
        help="""
` `- **To Press :regional_indicator_f: to Pay respect**
"""
    )
    async def f(self, ctx: commands.Context, *, reason: str = None) -> None:
        if reason is not None:
            if any(k in reason for k in ["https://", "http://", "discord.com", "discord.gg"]):
                await ctx.send(f"{self.fail_emoji} That reason contains a website")
                return
            elif reason.__contains__("<@"):
                await ctx.send(f"{self.fail_emoji} There are pings in the reason")
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

    @commands.command(
        aliases=['8ball'],
        help="""
` `- **8Ball**

` `- **Aliases**:
`   `8ball
"""
    )
    async def eightBall(self, ctx: commands.Context, *, question) -> None:
        embed = discord.Embed(
            color=discord.Color.from_rgb(self.r, self.g, self.b),
            title="8BALL",
            description=f"Question - {question}?\nAnswer - {choice(self.EIGHT_BALL_ANSWERS)}"
        )
        embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    #############################################################################################

    ## ==> MEMES
    #############################################################################################

    @commands.command(
        help="""
` `- **To get a meme**
"""
    )
    async def meme(self,ctx: commands.Context) -> None:
        while True:
            r = requests.get("https://memes.blademaker.tv/api?lang=en")
            res = r.json()
            if res["nsfw"]:
                continue
            embed_ = discord.Embed(title=res['title'],color=discord.Color.from_rgb(self.r, self.g, self.b))
            embed_.set_image(url = res["image"])
            embed_.set_author(name = ctx.author,icon_url = ctx.author.avatar_url)
            embed_.set_footer(text=f"👍 {res['ups']}")
            await ctx.send(embed = embed_)
            break

    #############################################################################################

def setup(bot:commands.Bot):
    bot.add_cog(Fun(bot))
