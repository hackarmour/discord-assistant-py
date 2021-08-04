import discord, json, asyncio
from discord.ext import commands
from discord_components import InteractionType, Select, SelectOption


class Config(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        with open("Configuration/ModConfig.json") as f:
            self.MODCONFIG = json.load(f)
        with open("Configuration/WelcomerConfig.json") as f:
            self.WELCOMERCONFIG = json.load(f)
        with open("Configuration/Leveling.json") as f:
            self.LEVELINGCONFIG = json.load(f)
    
    ## ==> CONFIG COMMAND
    #############################################################################################
    
    @commands.command()
    async def config(self, ctx: commands.Context) -> None:
        
        ## ==> CHECKS
        #########################################################################################
        
        if ctx.author.bot: return
        if ctx.author.guild is None: return
        
        #########################################################################################
        
        ## ==> MAIN EMBED
        #########################################################################################
        
        embed = discord.Embed(
            title="CONFIGURATION",
            description = """
:gear: What do you want to Configure?

```
Legends:
⇨: A brief description
→: A breif decription of the brief description
```
""",
            color=ctx.author.color
        )
        
        #########################################################################################
        
        ## ==> SELECT
        #########################################################################################
        
        select = Select(
            placeholder="Choose what you want to configure!",
            options=[
                SelectOption(
                    label="Welcomer",
                    value="welcomer",
                    description="To Configure Welcomer",
                    emoji="👋"
                ),
                SelectOption(
                    label="Moderation",
                    value="mod",
                    description="To Configure Moderation",
                    emoji="🧐"
                ),
                SelectOption(
                    label="Leveling",
                    value="level",
                    description="To Configure Leveling",
                    emoji="📈"
                )
            ]
        )
        
        #########################################################################################
        
        ## ==> SEND MESSAGE
        #########################################################################################
        
        await ctx.send(
            embed = embed,
            components = [select]
        )
        
        ## ==> CHECK FOR REACTION
        #########################################################################################
        
        while True:
            try:
                ## ==> GET REACTION
                reaction = await self.bot.wait_for(
                    "select_option",
                    timeout = 60.0,
                    check = lambda i: i.user == ctx.author
                )
            except asyncio.TimeoutError:
                select._disabled = True
                return
            
            ## ==> WELCOMER
            #########################################################################################
            
            if reaction.component[0].value == "welcomer":
                embed = discord.Embed(
                    title = "WELCOMER CONFIGURATION",
                    description = """
Here are the Configuration commands for Welcomer:

```
SetWelcomerChannel #<channel>
⇨ I should be able to read and write the channel!

SetWelcomeMessage <message>
⇨ Needs arguement "|user|" in <message> 
→ This arguement is replaced with the mention of the new user
⇨ Optional arguement "|guild|" 
→ This arguement is replaced with the name of this server

SetLeaveMessage <message>
⇨ Has the same arguements as "SetWelcomeMessage"

ToggleWelcomer
⇨ Turns Welcomer on or off
```
""",
                    color = discord.Color.random()
                )
                
                embed.set_author(name=f"{self.bot.user.name} Configuration", icon_url=self.bot.user.avatar_url)
                try:
                    await reaction.respond(
                        type = InteractionType.UpdateMessage,
                        embed = embed,
                        components=[select]
                    )
                except discord.NotFound: pass
            
            #########################################################################################
            
            ## ==> MODERATION
            #########################################################################################
            
            elif reaction.component[0].value == "mod":
                embed = discord.Embed(
                    title = "MODERATION CONFIGURATION",
                    color = discord.Color.random(),
                    description = """
Here are the Configuration commands for Moderation:
```
SetLogsChannel #<channel>
⇨ I should be able to read the channel!

ToggleMod
⇨ Turns AutoMod on or off

ToggleLog
⇨ Turns Logs on or off
```
"""
                )
                embed.set_author(name=f"{self.bot.user.name} Configuration", icon_url=self.bot.user.avatar_url)
                
                try:
                    await reaction.respond(
                        type = InteractionType.UpdateMessage,
                        embed = embed,
                        components=[select]
                    )
                except discord.NotFound: pass

            #########################################################################################

            ## ==> LEVELING
            #########################################################################################
            
            elif reaction.component[0].value == "level":
                embed = discord.Embed(
                    title="LEVELING CONFIGURATION",
                    color = discord.Color.random(),
                    description = """
Here is the Configuration command for Leveling:
```
ToggleLeveling
⇨ Turns Leveling on or off
```
"""
                )
                
                embed.set_author(name=f"{self.bot.user.name} Configuration", icon_url=self.bot.user.avatar_url)
                
                try:
                    await reaction.respond(
                        type = InteractionType.UpdateMessage,
                        embed = embed,
                        components=[select]
                    )
                except discord.NotFound: pass
            
            #########################################################################################
                
        #########################################################################################
            
    #############################################################################################
            
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Config(bot))
        