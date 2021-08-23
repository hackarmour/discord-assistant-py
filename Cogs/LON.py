import asyncio
import discord
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import json
from discord_components import SelectOption,Select,InteractionType
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
        with open('Configuration/emojis.json') as f:
            emojis=json.load(f)
            emojis=list(emojis.keys())
            nl='\n'
        page1=discord.Embed(title="Emojis",description=f'Page 1 out of 9.\n{nl.join(emojis[i] for i in range(19))}',color=ctx.author.color)
        page2=discord.Embed(title='Emojis',description=f'Page 2 out of 9.\n{nl.join(emojis[i] for i in range(19,37))}',color=ctx.author.color)
        page3=discord.Embed(title='Emojis',description=f'Page 3 out of 9.\n{nl.join(emojis[i] for i in range(37,57))}',color=ctx.author.color)
        page4=discord.Embed(title='Emojis',description=f'Page 4 out of 9.\n {(nl).join(emojis[i] for i in range(57,76))}',color=ctx.author.color)
        page5=discord.Embed(title='Emojis',description=f'Page 5 out of 9.\n{(nl).join(emojis[i] for i in range(76,95))}',color=ctx.author.color)
        page6=discord.Embed(title='Emojis',description=f'Page 6 out of 9.\n {(nl).join(emojis[i] for i in range(95,114))}',color=ctx.author.color)
        page7=discord.Embed(title='Emojis',description=f'Page 7 out of 9.\n {(nl).join(emojis[i] for i in range(114,133))}',color=ctx.author.color)
        page8=discord.Embed(title='Emojis',description=f'Page 8 out of 9.\n {(nl).join(emojis[i] for i in range(133,155))}',color=ctx.author.color)
        page9=discord.Embed(title="Emojis",description=f"Page 9 out of 9.\n {(nl).join(emojis[i] for i in range(155,len(emojis)))}",color=ctx.author.color)

        for embed in [page1,page2,page3,page4,page5,page6,page7,page8,page9]:
            embed.set_footer(text="""To use these emojis '>lon {emojiName}'""")

        select=Select(
            placeholder="Please select a Page Number!",
            options=[
                SelectOption(
                    label="Page 1",
                    value="page1"
                    ),
                SelectOption(
                    label="Page 2",
                    value="page2"
                    ),
                SelectOption(
                    label="Page 3",
                    value="page3"
                    ),
                SelectOption(
                    label="Page 4",
                    value="page4"
                    ),
                SelectOption(
                    label="Page 5",
                    value="page5"
                    ),
                SelectOption(
                    label="Page 6",
                    value="page6"
                    ),
                SelectOption(
                    label="Page 7",
                    value="page7"
                    ),
                SelectOption(
                    label="Page 8",
                    value="page8"
                    ),
                SelectOption(
                    label="Page 9",
                    value="page9"
                    )
                ]
            )
        embeds={
            "page1":page1,
            "page2":page2,
            "page3":page3,
            "page4":page4,
            "page5":page5,
            "page6":page6,
            "page7":page7,
            "page8":page8,
            "page9":page9
        }
        msg=await ctx.send(embed=page1,components=[select])
        while True:
            try:
                reaction = await self.bot.wait_for('select_option',timeout=30.0)
            except asyncio.TimeoutError:
                select.disabled = True
                await msg.edit(components=[select])
                break
            except discord.HTTPException:
                pass
            if(reaction.author!=ctx.author):
                await reaction.respond(
                    type=4,
                    content="This menu is not for you",
                    empherel=True
                )
                continue
            try:
                await reaction.respond(
                    type=InteractionType.UpdateMessage,
                    embed = embeds[reaction.component[0].value]
                    )
            except discord.NotFound: pass
            except discord.HTTPException:
                pass


def setup(bot):
    bot.add_cog(LON(bot))
