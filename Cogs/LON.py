import asyncio
import discord
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import json
from dpymenus import PaginatedMenu, Page
import aiohttp
class LON(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    @commands.cooldown(1,60,BucketType.user)  #A cooldown so that this command can be used by individual once in minute to prevent spam.
    async def lon(self,ctx,emoji):
        if ctx.author.nick!=None: # checking if author has a nick name if yes, the webhook will use his/her nickname else username
            name=ctx.author.nick
        else:
            name=ctx.author.name
        with open('Configuration/emojis.json') as f: # opening emojis.json to check for emojis
            allEmojis=json.load(f) # loadig all the emojis
            emojiNames=list(allEmojis.keys()) # extracting all the custom names given to emojis
        if emoji.lower() not in emojiNames: # checking if emojiname exists in json file if it doesn't send the message and stop execution of command.
            await ctx.send("This emoji does not exist")
            return
        await ctx.message.delete()
        emoji=allEmojis[emoji.lower()] # getting emoji from json file
        allwebhooks=await ctx.channel.webhooks()  # getting all the webhooks of channel
        data=[]  # an empty list to add emoji's id
        for webhook in allwebhooks: # iterating through all the webhooks and adding webhook id in list
            data.append(webhook.id)
        with open('Configuration/webhooks.json') as f: # opening webhooks.json file to fetch webhook previously created by bot
            webhookdata=json.load(f)
        if str(ctx.channel.id) in list(webhookdata.keys()): # Checking if bot previously created a webhook 
            for webId in data: # Going through all the webhooks id's present in list
                if str(webId) in webhookdata[str(ctx.channel.id)]: # checking if the webhook previously created by bot still exists. then sending the emoji using webhook
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(webhookdata[str(ctx.channel.id)], adapter=AsyncWebhookAdapter(session))
                        await webhook.send(emoji, username=name,avatar_url=ctx.author.avatar_url)
                        return
        """If there is no webhook previously created by bot then creating a new webhook with the name assistant"""
        newWebhook=await ctx.channel.create_webhook(name="Assistant")
        webhookdata[str(ctx.channel.id)]=f"https://discord.com/api/webhooks/{newWebhook.id}/{newWebhook.token}" # making a complete url of new webhook
        with open('Configuration/webhooks.json','w') as f: # saving this url in json file for after use
            json.dump(webhookdata,f,indent=4)
        with open('Configuration/webhooks.json') as f: # opening json file again to get the url and send the webhook
            allWebhooks=json.load(f)
        async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(allWebhooks[str(ctx.channel.id)], adapter=AsyncWebhookAdapter(session))
                    await webhook.send(emoji, username=name,avatar_url=ctx.author.avatar_url)

    @commands.command()
    async def lonall(self,ctx):
        with open('Configuration/emojis.json') as f: #Opening Json file
            allEmojis=json.load(f)  #Extracting all the data from json file.
            allEmojis=list(allEmojis.keys())  #Extracting all the keys from json file.
            nl='\n'  #Declaring a newline character as new line/escape sequence characters are not allowed in curly braces of f string.
        menu=PaginatedMenu(ctx)  #Setting a menu with reactions to move back and forth between different embeds.

        # Creating three pages for the menu
        emb1=Page(title='Emojis',description=f'Page 1 out of 3.\n\n{(nl).join(allEmojis[i] for i in range(19))}',color=ctx.author.color)
        emb2=Page(title="Emojis",description=f'Page 2 out of 3.\n\n{(nl).join(allEmojis[i] for i in range(19,39))}',color=ctx.author.color)
        emb3=Page(title='Emojis',description=f'Page 3 out of 3.\n\n{(nl).join(allEmojis[i] for i in range(39,len(allEmojis)))}',color=ctx.author.color)
        menu.add_pages([emb1,emb2,emb3])  #Setting the three pages in the menu
        await menu.open()  #Sending the menu.


def setup(bot):
    bot.add_cog(LON(bot))
        
