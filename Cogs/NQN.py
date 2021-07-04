import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from dpymenus import Page, PaginatedMenu
import json

class NQN(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(aliases=['nqn','n']) #Defining the command's aliases so that the command can be used with multiple names
    @commands.cooldown(1, 60,BucketType.user) #Setting a cooldown of 60seconds which means that a user can use this command only once in 60 seconds. This cooldown is to prevent spam
    async def _nqn(self, ctx:commands.Context,emojiName=None):
        if (emojiName==None): #Checking if a user specified an emoji name. If no emoji name is specified the bot sends the response below.
            await ctx.send("Please specify an emoji name. To get list of all emojis use `>nall` or `>nqnall`")
            return #Return statement so that if no emoji name is specified the bot should stop here.
        elif(emojiName!=None):
            with open('Configuration/emojis.json') as f:#Opening emojis.json file 
                allEmojis=json.load(f) #reading the content of the file
                emojisName=list(allEmojis.keys()) #getting all keys from json, The key is the name of emoji.
            if (emojiName in emojisName):#Checking if the emoji name is in the json file. If yes the command go on.
                emoji=allEmojis[emojiName]#Extracting emoji from json file
                webhook=await ctx.channel.create_webhook(name='Assistant') #Creating a wehook in that channel with the name "Assistant"
                if (ctx.author.nick==None):#Checking if the user has a nickname if yes..
                    name=ctx.author.name# ..setting the variable name with the user's nick name
                elif(ctx.author.nick!=None): #if user does not have any nickname..
                    name=ctx.author.nick #..setting the variable name with the user's name.
                await webhook.send(emoji,username=name,avatar_url=ctx.author.avatar_url) #Sending the wehook with content as emoji, username as the value of name variable and avatar_url as author's avatar_url
                await asyncio.sleep(20.0) #Waiting for 20seconds
                await webhook.delete() #deleting the webhook after 20 seconds so that the limit of webhook per channel which is 10 is not exceeded. This will just delete the webhook but not the message.
            elif(emojiName not in emojisName):
                await ctx.send("Sorry but this emoji doesn't exists.")
                return
            

    @commands.command(aliases=['nall','nqnall']) #Defining the command's aliases so that the command can be used with multiple names
    async def _all(self,ctx):
        with open('Configuration/emojis.json') as f: #Opening the json file
            allEmoji=json.load(f) #Reading the json file
            allEmoji=list(allEmoji.keys()) #Extracting all the keys from json file and typecasting them into list.
            nl='\n' #Declaring a new line character as a variable because newline character are not allowed in curly braces of the f string.

        '''Creating the three embeds with the emojis names'''
        emb1=Page(title='Emoji List',description=f'Page 1 out of 3\n{(nl).join(allEmoji[i] for i in range(19))}',color=ctx.author.color)
        emb2=Page(title='Emoji List',description=f'Page 2 out of 3\n{(nl).join(allEmoji[i] for i in range(19,37))}',color=ctx.author.color)
        emb3=Page(title='Emoji List',description=f'Page 3 out of 3\n{(nl).join(allEmoji[i] for i in range(38,len(allEmoji)))}',color=ctx.author.color)
        menu = PaginatedMenu(ctx) #Creating a reaction menu
        menu.add_pages([emb1, emb2, emb3]) #Adding pages into menu
        await menu.open() #sending the menu.

def setup(bot:commands.Bot):
    bot.add_cog(NQN(bot))