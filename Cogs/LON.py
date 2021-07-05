import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import json
from dpymenus import PaginatedMenu, Page
class LON(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    @commands.cooldown(1,60,BucketType.user)  #A cooldown so that this command can be used by individual once in minute to prevent spam.
    async def lon(self,ctx,emojiName):
        with open('Configuration/emojis.json') as f:  #Opening json file to read all the data
            allEmojis=json.load(f)  # Reading all the data of json file
            allJsonKeys=list(allEmojis.keys())  #Extracting keys from json file to perform check

        if (emojiName in allJsonKeys):  #Checking if emoji name is in file if yes...
            emoji=allEmojis[emojiName] ##..Extracting emoji from the json file
            await ctx.message.delete()  #Deleting the message.
            webhook=await ctx.channel.create_webhook(name='Assistant')  #Creating a webhook with name "Assistant"
            if (ctx.author.nick==None): ##Checking if the author has nickname if no name variable is set to author's name
                name=ctx.author.name
            elif (ctx.author.nick!=None):  #Else name variable is set to author's nickname
                name=ctx.author.nick
            await webhook.send(emoji,username=name,avatar_url=ctx.author.avatar_url)  #Sending webhook with content as emoji, username as name variable and avatar as author's avatar
            await asyncio.sleep(20.0)
            '''Timer of 20seconds so that the webhook can be removed after 20seconds for 2 reasons.
            1. Not to exceed the limit of 10 webhooks per channel.
            2. To prevent rate limit as immediate deletion can use bot to be rate limited by the discord to prevent spam.'''
            await webhook.delete()  #Deleting the webhook, This will only delete webhook but not the message.
        elif (emojiName not in allJsonKeys): #..If emoji name is not in list then sending the message written below.
            await ctx.send("Sorry, this emoji doesn't exist.")


    @commands.command()
    async def lonall(self,ctx):
        with open('Configuration/emojis.json') as f: #Opening Json file
            allEmojis=json.load(f)  #Extracting all the data from json file.
            allEmojis=list(allEmojis.keys())  #Extracting all the keys from json file.
            nl='\n'  #Declaring a newline character as new line/escape sequence characters are not allowed in curly braces of f string.
        menu=PaginatedMenu(ctx)  #Setting a menu with reactions to move back and forth between different embeds.

        '''Creating three pages for the menu'''
        emb1=Page(title='Emojis',description=f'Page 1 out of 3.\n\n{(nl).join(allEmojis[i] for i in range(19))}',color=ctx.author.color)
        emb2=Page(title="Emojis",description=f'Page 2 out of 3.\n\n{(nl).join(allEmojis[i] for i in range(19,39))}',color=ctx.author.color)
        emb3=Page(title='Emojis',description=f'Page 3 out of 3.\n\n{(nl).join(allEmojis[i] for i in range(39,len(allEmojis)))}',color=ctx.author.color)
        menu.add_pages([emb1,emb2,emb3])  #Setting the three pages in the menu
        await menu.open()  #Sending the menu.


def setup(bot):
    bot.add_cog(LON(bot))
        
