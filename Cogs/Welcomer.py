from gc import collect
import discord, asyncio, json
from discord.ext import commands


class Welcomer(commands.Cog):
    def __init__(self,bot: commands.Bot) -> None:
        self.bot = bot
        ## ==> READING CONFIGURATION OF WELCOMER
        #############################################################################################
        
        with open("Configuration/WelcomerConfig.json") as f:
            self.CONFIG = json.loads(f.read())
        
        #############################################################################################
        
        self.args = [
            "welcomemessage", "welcome-message", "welcome_message",
            "leavemessage", "leave-message", "leave_message",
            "channel", "welcomer_channel", "welcomer-channel",
            "enable"
        ]
        
    def rewrite(self) -> None:
        with open("Configuration/WelcomerConfig.json",'w') as f: json.dump(self.CONFIG,f, indent=4)
    
    ## ==> TO WELCOME MEMBERS
    #############################################################################################
    
    @commands.Cog.listener()
    async def on_member_join(self,ctx) -> None:
        if str(ctx.guild.id) in self.CONFIG.keys():
            if self.CONFIG[str(ctx.guild.id)]["channel"] != None and self.CONFIG[str(ctx.guild.id)]["welcome_message"] != None and self.CONFIG[str(ctx.guild.id)]["leave_message"] != None and self.CONFIG[str(ctx.guild.id)]["active"]:
                channel = self.bot.get_channel(self.CONFIG[str(ctx.guild.id)]["channel"])
                try:
                    await channel.send(self.CONFIG[str(ctx.guild.id)]["welcome_message"].replace("|user|", ctx.mention).replace("|guild|",str(ctx.guild)))
                except discord.Forbidden:
                    pass
    
    @commands.Cog.listener()
    async def on_member_remove(self,ctx) -> None:
        if str(ctx.guild.id) in self.CONFIG.keys():
            if self.CONFIG[str(ctx.guild.id)]["channel"] != None and self.CONFIG[str(ctx.guild.id)]["welcome_message"] != None and self.CONFIG[str(ctx.guild.id)]["leave_message"] != None and self.CONFIG[str(ctx.guild.id)]["active"]:
                channel = self.bot.get_channel(self.CONFIG[str(ctx.guild.id)]["channel"])
                try:
                    await channel.send(self.CONFIG[str(ctx.guild.id)]["leave_message"].replace("|user|",str(ctx)).replace("|guild|",str(ctx.guild)))
                except discord.Forbidden:
                    pass
                
    #############################################################################################
        
    ## ==> CONFIGURATION
    #############################################################################################
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def welcomer(self, ctx: commands.Context, var: str = None, *, _:str = None) -> None:
        
        ## ==> CHECK IF VAR IS NOT PASSED
        if var is None:
            await ctx.send(
                embed = discord.Embed(
                    title="WELCOMER",
                    description="Please pass the arguements\n\nYou can use the following arguements:\n```\n{}\n```".format(", ".join(self.args)),
                    color = discord.Color.from_rgb(46,49,54)
                )
            )
            return
        
        ## ==> CHECK IF THERE IS A BAD ARGUEMENT
        elif var.lower() not in self.args:
            await ctx.send(
                embed = discord.Embed(
                    title="WELCOMER",
                    description="I don't understand what you mean by that\n\nYou can use the following arguements:\n```\n{}\n```".format(", ".join(self.args)),
                    color = discord.Color.from_rgb(46,49,54)
                )
            )
            return
        
        ## ==> WELCOME MESSAGE
        #########################################################################################
        
        elif var.lower() in self.args[:3]:
            
            ## ==> CHECK IF |user| KEYWORD IS IN _ OR NOT
            if "|user|" not in _:
                await ctx.send("Please enter the `|user|` keyword!")
                return

            ## ==> CHECK IF GUILD ID IS IN FILE
            if str(ctx.guild.id) in self.CONFIG.keys():
                
                ## ==> CHANGE WELCOME MESSAGE TO _
                self.CONFIG[str(ctx.guild.id)]["welcome_message"] = _
                
                
            ## ==> GUILD ID IS NOT IN THE FILE
            else:
                
                ## ==> CREATE CONFIG FOR GUILD
                self.CONFIG[str(ctx.guild.id)] = {
                    "active": False,
                    "welcome_message": _,
                    "leave_message": None,
                    "channel": None
                }
                
            ## ==> SEND EMBED
            new_message = _.replace('|user|',ctx.author.mention).replace('|guild|', str(ctx.guild))
            await ctx.send(
                embed=discord.Embed(
                    title = "WELCOMER",
                    description=f":white_check_mark: Welcome Message Updated!\nSet to: {new_message}",
                    color = discord.Color.from_rgb(46,49,54)
                )
            )
        
        #########################################################################################
        
        ## ==> LEAVE MESSAGE
        #########################################################################################
        
        elif var.lower() in self.args[3:6]:
            
            ## ==> CHECK IF |user| KEYWORD IS IN _
            if "|user|" not in _:
                await ctx.send("Please enter the `|user|` keyword!")
                return

            ## ==> IF GUILD ID IS IN FILE
            if str(ctx.guild.id) in self.CONFIG.keys():
                
                ## ==> CHANGE LEAVE MESSAGE
                self.CONFIG[str(ctx.guild.id)]["leave_message"] = _
                
            
            ## ==> GUILD ID NOT IN FILE
            else:
                
                ## ==> CREATE CONFIG FOR GUILD
                self.CONFIG[str(ctx.guild.id)] = {
                    "active": False,
                    "welcome_message": None,
                    "leave_message": _,
                    "channel": None
                }
                
            ## ==> SEND EMBED
            new_message = _.replace('|user|',ctx.author.mention).replace('|guild|', str(ctx.guild))
            await ctx.send(
                embed=discord.Embed(
                    title = "WELCOMER",
                    description=f":white_check_mark: Leave Message Updated!\nSet to: {new_message}",
                    color = discord.Color.from_rgb(46,49,54)
                )
            )
        
        #########################################################################################
        
        ## ==> CHANNEL
        #########################################################################################
        
        elif var.lower() in self.args[6:9]:
            
            ## ==> CHANGE _ TO A discord.TextChannel OBJECT
            try: channel = await commands.TextChannelConverter().convert(ctx, _)
            except commands.CommandError: return
            
            ## ==> CHECK IF THE CHANNEL IS READABLE OR NOT            
            try:
                msg = await channel.send("""
**This is a test**

This is done to check if this channel is *readable* or not!
You can delete this message if you want!
            """)
            except discord.Forbidden:
                await ctx.send("I am having problems reading that channel :face_with_spiral_eyes:")
                return
            
            
            ## ==> DELETE THE MESSAGE
            await msg.delete()
            
            ## ==> IF GUILD ID IS IN CONFIG
            if str(ctx.guild.id) in self.CONFIG.keys():
                self.CONFIG[str(ctx.guild.id)]["channel"] = channel.id
            
            ## ==> IF GUILD ID IS NOT IN CONFIG
            else:
                self.CONFIG[str(ctx.guild.id)] = {
                    "active": False,
                    "welcome_message": None,
                    "leave_message": None,
                    "channel": channel.id
                }
            
            ## ==> SEND EMBED
            await ctx.send(
                embed = discord.Embed(
                    title="WELCOMER",
                    description=":white_check_mark: Welcomer channel changed!",
                    color = discord.Color.from_rgb(46,49,54)
                )
            )
            
        #########################################################################################
        
        ## ==> TOGGLE
        #########################################################################################
        
        elif var.lower() in self.args[-1]:
            
            ## ==> CHECK IF IT IS A BAD ARGUEMENT
            if _.lower() not in ["true", "false"]:
                await ctx.send("**Bad arguement**\n\nPlease pass either `true` or `false`")
                return
            
            ## ==> CHECK IF GUILD ID IS IN CONFIGURATION
            if str(ctx.guild.id) not in self.CONFIG.keys():
                await ctx.send("You have to Configure welcomer before this!")
                return
            
            ## ==> INITIALIZE EMPTY LIST
            __ = []
            
            ## ==> CHECK IF ANY VALUE IS NONE
            for i in self.CONFIG[str(ctx.guild.id)].keys():
                if self.CONFIG[str(ctx.guild.id)][i] is None:
                    __.append(i.upper())
            
            ## ==> IF LENGTH OF __ ISN'T 0, SOME VALUES ARE NOT CONFIGURED
            if len(__) != 0:
                await ctx.send(
                    embed=discord.Embed(
                        title="WELCOMER",
                        description=f"Following values are not configured!\n\n{', '.join(__)}",
                        color=discord.Color.from_rgb(46,49,54)
                    )
                )
                return
            
            ## ==> IF THIS IS RAN, ALL VALUES ARE CONFIGURED
            elif len(__) == 0:
                
                ## ==> CHANGE _ TO BOOLEAN
                _ = True if _.lower() == "true" else False
                
                ## ==> CHANGE VALUES IN CONFIGURATION
                self.CONFIG[str(ctx.guild.id)]["active"] = _
                
                ## ==> SEND EMBED
                await ctx.send(
                    embed=discord.Embed(
                        title="WELCOMER",
                        description=f"{':x: ' if not _ else ':white_check_mark:'} Welcomer has been {'Enabled!' if _ else 'Disabled'}",
                        color = discord.Color.from_rgb(46,49,54)
                    )
                )

        #########################################################################################    
            
        ## ==> REWRITE CONFIGURATION
        self.rewrite()

    #############################################################################################

def setup(bot: commands.Bot) -> None: bot.add_cog(Welcomer(bot))