import discord, json
from discord.ext import commands


class Welcomer(commands.Cog):
    def __init__(self,bot: commands.Bot) -> None:
        self.bot = bot
        ## ==> READING CONFIGURATION OF WELCOMER
        #############################################################################################
        
        with open("Configuration/WelcomerConfig.json") as f:
            self.CONFIG = json.loads(f.read())
        
        #############################################################################################
        
            
    ## ==> TO WELCOME MEMBERS
    #############################################################################################
    
    @commands.Cog.listener()
    async def on_member_join(self,ctx) -> None:
        if str(ctx.guild.id) in self.CONFIG.keys():
            if self.CONFIG[str(ctx.guild.id)]["channel"] != None and self.CONFIG[str(ctx.guild.id)]["welcome_message"] != None and self.CONFIG[str(ctx.guild.id)]["leave_message"] != None and self.CONFIG[str(ctx.guild.id)]["active"]:
                channel = self.bot.get_channel(self.CONFIG[str(ctx.guild.id)]["channel"])
                await channel.send(self.CONFIG[str(ctx.guild.id)]["welcome_message"].replace("|user|", ctx.mention).replace("|guild|",str(ctx.guild)))
    
    @commands.Cog.listener()
    async def on_member_remove(self,ctx) -> None:
        if str(ctx.guild.id) in self.CONFIG.keys():
            if self.CONFIG[str(ctx.guild.id)]["channel"] != None and self.CONFIG[str(ctx.guild.id)]["welcome_message"] != None and self.CONFIG[str(ctx.guild.id)]["leave_message"] != None and self.CONFIG[str(ctx.guild.id)]["active"]:
                channel = self.bot.get_channel(self.CONFIG[str(ctx.guild.id)]["channel"])
                await channel.send(self.CONFIG[str(ctx.guild.id)]["leave_message"].replace("|user|",str(ctx)).replace("|guild|",str(ctx.guild)))
                
    #############################################################################################
        
    ## ==> TO TOGGLE WELCOMER
    #############################################################################################
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def toggleWelcomer(self,ctx: commands.Context) -> None:
        if str(ctx.guild.id) not in self.CONFIG.keys():
            color = discord.Color.red()
            desc = "You have not Configured Welcomer In your server yet!\nPlease Configure Welcomer!"
        
        elif self.CONFIG[str(ctx.guild.id)]["channel"] == None:
            color = discord.Color.red()
            desc = "You havent set the channel"
        
        else:
            self.CONFIG[str(ctx.guild.id)]["active"] = True if not self.CONFIG[str(ctx.guild.id)]["active"] else False
            with open("Configuration/WelcomerConfig.json",'w') as f: json.dump(self.CONFIG,f, indent=4)
            color = (discord.Color.green()) if self.CONFIG[str(ctx.guild.id)]["active"] else (discord.Color.red())
            desc = f"Welcomer has been {'Activated' if self.CONFIG[str(ctx.guild.id)]['active'] else 'Deactivated'} on your server {':partying_face:' if self.CONFIG[str(ctx.guild.id)]['active'] else ''}"
            
        await ctx.send(embed=discord.Embed(title="WELCOMER",description=desc, color=color))
        
    #############################################################################################
    
    ## ==> TO SET WELCOME MESSAGE
    #############################################################################################
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def SetWelcomeMessage(self,ctx: commands.Context,*, msg: str) -> None:
        if not msg.lower().__contains__("|user|"):
            await ctx.send("Please enter `|user|` keyword in your message")
            return
        else:
            if str(ctx.guild.id) not in self.CONFIG.keys():
                self.CONFIG[str(ctx.guild.id)] = {
                    "active": False,
                    "welcome_message": msg,
                    "leave_message": None,
                    "channel": None
                }
            else: self.CONFIG[str(ctx.guild.id)]["welcome_message"] = msg
            with open("Configuration/WelcomerConfig.json",'w') as f: json.dump(self.CONFIG, f, indent=4)
            
            await ctx.send(embed=discord.Embed(color=discord.Color.green(),description=f":white_check_mark: Welcome Message Updated!\nSet to: {msg.replace('|user|',ctx.author.mention).replace('|guild|', str(ctx.guild))}",title="WELCOMER"))
            
    #############################################################################################
    
    ## ==> TO SET LEAVE MESSAGE
    #############################################################################################
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def SetLeaveMessage(self,ctx: commands.Context,*, msg: str) -> None:
        if not msg.lower().__contains__("|user|"):
            await ctx.send("Please enter `|user|` keyword in your message")
            return
        else:
            if str(ctx.guild.id) not in self.CONFIG.keys():
                self.CONFIG[str(ctx.guild.id)] = {
                    "active": False,
                    "welcome_message": None,
                    "leave_message": msg,
                    "channel": None
                }
            else: self.CONFIG[str(ctx.guild.id)]["leave_message"] = msg
            
            with open("Configuration/WelcomerConfig.json",'w') as f: json.dump(self.CONFIG,f, indent=4)
            
            await ctx.send(embed=discord.Embed(color=discord.Color.green(),description=f":white_check_mark: Leave Message Updated!\nSet to: {msg.replace('|user|',ctx.author.mention).replace('|guild|', str(ctx.guild))}",title="WELCOMER"))

    #############################################################################################
               
    ## ==> TO SET CHANNEL TO SEND WELCOME MESSAGE
    #############################################################################################
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setWelcomeChannel(self,ctx: commands.Context,channel: discord.TextChannel) -> None:
        if channel in ctx.guild.channels:
            if str(ctx.guild.id) not in self.CONFIG.keys():
                self.CONFIG[str(ctx.guild.id)] = {
                        "active": False,
                        "welcome_message": None,
                        "leave_message": None,
                        "channel": channel.id
                    }
            else:
                self.CONFIG[str(ctx.guild.id)]["channel"] = channel.id
            
            with open("Configuration/WelcomerConfig.json",'w') as f: json.dump(self.CONFIG,f, indent=4)
            
            await ctx.send(embed=discord.Embed(color=discord.Color.green(),description=f"The Channel to send welcome messages is now set to <#{channel.id}> !",title="WELCOMER"))
    
    #############################################################################################

def setup(bot: commands.Bot) -> None: bot.add_cog(Welcomer(bot))