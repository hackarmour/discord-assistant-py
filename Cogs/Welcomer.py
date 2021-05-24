import discord, json
from discord.ext import commands


class Welcomer(commands.Cog):
    def __init__(self,bot: commands.Bot) -> None:
        self.bot = bot
        ## ==> READING CONFIGURATION OF WELCOMER
        #############################################################################################
        
        with open("WelcomerConfig.json") as f:
            self.CONFIG = json.loads(f.read())
        
        #############################################################################################
        
            
    ## ==> TO WELCOME MEMBERS
    #############################################################################################
    
    @commands.Cog.listener()
    async def on_member_join(self,ctx) -> None:
        if str(ctx.guild.id) in self.CONFIG.keys():
            if self.CONFIG[str(ctx.guild.id)]["channel"] != None and self.CONFIG[str(ctx.guild.id)]["welcome_message"] != None and self.CONFIG[str(ctx.guild.id)]["leave_message"] != None and self.CONFIG[str(ctx.guild.id)]["active"]:
                channel = self.bot.get_channel(self.CONFIG[str(ctx.guild.id)]["channel"])
                await channel.send(self.CONFIG[str(ctx.guild.id)]["welcome_message"].replace("|user|",ctx.mention).replace("|guild|",str(ctx.guild)))
    
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
    async def toggle(self,ctx: commands.Context) -> None:
        if str(ctx.guild.id) not in self.CONFIG.keys():
            color = discord.Color.red()
            desc = "You have not Configured Welcomer In your server yet!\nPlease Config before toggling Welcomer"
        
        elif self.CONFIG[str(ctx.guild.id)]["active"]:
            color = discord.Color.red()
            desc = "Welcomer is Already Active On your server!"
            
        else:
            self.CONFIG[str(ctx.guild.id)]["active"] = True
            with open("WelcomerConfig.json",'w') as f: f.write(json.dumps(self.CONFIG))
            color = discord.Color.green()
            desc = "Welcomer has been activated on your server :partying_face:"
            
        await ctx.send(embed=discord.Embed(title="WELCOMER",description=desc, color=color))
        
    #############################################################################################
    
    ## ==> TO SET WELCOME MESSAGE
    #############################################################################################
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def SetWelcomeMessage(self,ctx: commands.Context,*, msg: str) -> None:
        print(msg)
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
            
            with open("WelcomerConfig.json",'w') as f: f.write(json.dumps(self.CONFIG))
            
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
            
            with open("WelcomerConfig.json",'w') as f: f.write(json.dumps(self.CONFIG))
            
            await ctx.send(embed=discord.Embed(color=discord.Color.green(),description=f":white_check_mark: Leave Message Updated!\nSet to: {msg.replace('|user|',ctx.author.mention).replace('|guild|', str(ctx.guild))}",title="WELCOMER"))

    #############################################################################################
               
    ## ==> TO SET CHANNEL TO SEND WELCOME MESSAGE
    #############################################################################################
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def SetChannel(self,ctx: commands.Context,channel: discord.TextChannel) -> None:
        if str(ctx.guild.id) not in self.CONFIG.keys():
            self.CONFIG[str(ctx.guild.id)] = {
                    "active": False,
                    "welcome_message": None,
                    "leave_message": None,
                    "channel": channel.id
                }
        else:
            self.CONFIG[str(ctx.guild.id)]["channel"] = channel.id
            
        with open("WelcomerConfig.json",'w') as f: f.write(json.dumps(self.CONFIG))
            
        await ctx.send(embed=discord.Embed(color=discord.Color.green(),description=f"The Channel to send welcome messages is now set to <#{channel.id}> !",title="WELCOMER"))
    
    #############################################################################################

def setup(bot: commands.Bot) -> None: bot.add_cog(Welcomer(bot))