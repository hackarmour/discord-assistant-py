import discord, json
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        ## ==> GET VALUES
        with open("Configuration/config.json") as f:
            cfg = json.load(f)
            self.fail_emoji = cfg["fail_emoji"]
            self.success_emoji = cfg["success_emoji"]
            embed_color = cfg["embed_color"]
            self.r = embed_color[0]
            self.g = embed_color[1]
            self.b = embed_color[2]
    
    
    ## ==> ERROR HANDLING
    ###############################################################################################
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        
        ## ==> IF ARGUEMENTS AREN'T PASSED
        if isinstance(error, commands.MissingRequiredArgument): 
            return
        
        ## ==> IF COMMAND COULDN'T BE RESOLVED
        elif isinstance(error, commands.CommandNotFound): 
            return
        
        ## ==> IF COMMAND IS ON COOLDOWN
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                embed=discord.Embed(
                    title="ERROR", 
                    description=f"{self.fail_emoji} {str(ctx.command)} Command is on Cooldown",
                    color=discord.Color.from_rgb(self.r, self.g, self.b)
                )
            )
        
        ## ==> IF CHANNEL ISN'T FOUND
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send(
                embed=discord.Embed(
                    title="ERROR", 
                    description=f"{self.fail_emoji} That channel can not be found",
                    color=discord.Color.from_rgb(self.r, self.g, self.b)
                )
            )
            
        ## ==> IF CHANNEL ISN'T READABLE
        elif isinstance(error, commands.ChannelNotReadable):
            await ctx.send(
                embed=discord.Embed(
                    title="ERROR", 
                    description=f"{self.fail_emoji} Can not read that channel",
                    color=discord.Color.from_rgb(self.r, self.g, self.b)
                )
            )
        
        ## ==> IF IT ISN'T ANY OF THE ABOVE
        else:
            
            ## ==> IF BOT IS MISSING PERMS OR MISSING ACCESS
            if str(error).endswith("Missing Permissions") or str(error).endswith("Missing Access"): 
                return
            
            ## ==> EMBED WITH INFORMATION
            embed = discord.Embed(
                    title='ERROR',
                    description=f"{self.fail_emoji} Error message:\n**{error}**\n\nCommand: **{ctx.command}**",
                    color=discord.Color.from_rgb(self.r, self.g, self.b)
                )
            
            ## ==> CHANGE AUTHOR
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            
            await self.bot.get_channel(872818862742204487).send(embed=embed)
        
    ###############################################################################################
        
def setup(bot: commands.Bot) -> None:
    bot.add_cog(ErrorHandler(bot))