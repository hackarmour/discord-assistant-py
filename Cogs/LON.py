import discord, asyncio, json
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from dpymenus import PaginatedMenu, Page


class LON(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        
        ## ==> READ VALUES
        with open("Configuration/config.json") as f:
            cfg = json.load(f)
            self.fail_emoji = cfg["fail_emoji"]
            self.success_emoji = cfg["success_emoji"]
            embed_color = cfg["embed_color"]
            self.r = embed_color[0]
            self.g = embed_color[1]
            self.b = embed_color[2]

    @commands.command(
        help="""
` `- **Sends a webhook with the Emoji passed in the command**
"""
    )
    @commands.cooldown(1,60,BucketType.user)  
    async def lon(self, ctx: commands.Context, emojiName: str) -> None:
        
        ## ==> LOADING CONFIG
        with open('Configuration/emojis.json') as f:  
            allEmojis=json.load(f)  
            allJsonKeys=list(allEmojis.keys())
    
        ## ==> IF EMOJI EXISTS IN FILE
        if emojiName in allJsonKeys:
            
            ## ==> GET EMOJI
            emoji = allEmojis[emojiName]
            
            ## ==> DELETE MESSAGE
            await ctx.message.delete()
            
            ## ==> CREATE WEBHOOK
            webhook = await ctx.channel.create_webhook(name='Assistant')
            
            ## ==> CONFIGURE WEBHOOK
            if (ctx.author.nick==None):
                name = ctx.author.name
            else:
                name = ctx.author.nick
                
            ## ==> SEND WEBHOOK
            await webhook.send(emoji,username=name,avatar_url=ctx.author.avatar_url)
            await asyncio.sleep(20.0)
            
            ## Timer of 20 seconds so that the webhook can be removed after 20 seconds for 2 reasons.
            ## 1. Not to exceed the limit of 10 webhooks per channel.
            ## 2. To prevent rate limit as immediate deletion can use bot to be rate limited by the discord to prevent spam.
            
            ## ==> DELETING THE WEBHOOK
            await webhook.delete()
            
            
        elif (emojiName not in allJsonKeys):
            await ctx.send(F" {self.fail_emoji}Sorry, this emoji doesn't exist.")


    @commands.command(
        help="""
` `- **To get all the emojis available**
"""
    )
    async def lonall(self,ctx):
        
        ## ==> OPEN CONFIGURATION
        with open('Configuration/emojis.json') as f: 
            allEmojis = json.load(f)
            allEmojis = list(allEmojis.keys())
            nl='\n'

        ## ==> PAGINATED MENU
        menu = PaginatedMenu(ctx)

        ## ==> CREATING 3 PAGES FOR MENU
        emb1 = Page(
            title='Emojis',
            description=f'Page 1 out of 3.\n\n{(nl).join(allEmojis[:19])}',
            color=discord.Color.from_rgb(self.r, self.g, self.b)
        )
        emb2 = Page(
            title="Emojis",
            description=f'Page 2 out of 3.\n\n{(nl).join(allEmojis[19:39])}',
            color=discord.Color.from_rgb(self.r, self.g, self.b)
        )
        emb3 = Page(
            title='Emojis',
            description=f'Page 3 out of 3.\n\n{(nl).join(allEmojis[39:])}',
            color=discord.Color.from_rgb(self.r, self.g, self.b)
        )
        
        ## ==> SETTING UP THE PAGES
        menu.add_pages([emb1,emb2,emb3]) 
        
        ## ==> SENDING THE MENU
        await menu.open()


def setup(bot):
    bot.add_cog(LON(bot))
        
