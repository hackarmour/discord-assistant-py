import discord,asyncio,json
from discord.ext import commands

## Configuration by TheEmperor342

class Logs(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        with open("Configuration/ModConfig.json") as f: self.CONFIG = json.loads(f.read())
        self.illegal_words=['Nigger','Nigga','N1gg3r','N1gger','Nigg3r','N1gga','N1gg@','Dick','Fuck','F U C K','f u c k','gandu','gaandu','gaamdu','fuck','nigger','nigga','n1gg3r','n1gga','n1gg@','dick']
        
    ## ==> THIS FUNCTION BANS CERTAIN WORDS. IF YOU WANT TO BAN SOME MORE WORDS, ADD THEM TO THE LIST ABOVE
    #############################################################################################
    
    @commands.Cog.listener()
    async def on_message(self,message: discord.Message) -> None:
        if message.author.bot:
            return
        if str(message.author.guild.id) in self.CONFIG.keys():
            if self.CONFIG[str(message.author.guild.id)]["ModEnabled"]:
                if any(word in message.content for word in self.illegal_words):
                    user=message.author
                    await message.delete() #This command deletes the messages if it contains those words
                    await user.send('Your message was deleted due to use of profane and illegal words and you are temporarily muted for 10 minutes.')#This line sends a dm to user
                    role = discord.utils.get(message.guild.roles,name='Muted') #This command gives the user a muted role, you can change the muted role with any role you want to give but the name is case sensitive
                    
                    if role is None:
                        role = await message.author.guild.create_role(name="Muted")

                        for channel in message.author.guild.channels:
                            await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        
                    
                    await message.author.add_roles(role)
                    await asyncio.sleep(600.0) #this is  a timer of 10 mins, after 10 mins the role gets removed automatically.
                    try: await message.author.remove_roles(role)
                    except Exception: pass
                    
            
        elif (str(message.author.id)=='849673169278468116' and str(message.channel.id)=='839650841522339860'):
            await message.add_reaction('🔥')
            await message.add_reaction('<:dorime:839708454876741652>')
            await message.add_reaction('<:prayge:846337069022445568>')
            
        elif (self.bot.user in message.mentions):
            await message.channel.send(embed=discord.Embed(title=f"Hi! I'm {str(self.bot.user)[:-5]}", description="You can use `>help` to get help with my commands",color=message.author.color))
        
    
    #############################################################################################
        
    ## ==>  THIS FUNCTION SENDS LOGS IN A SPECIFIC CHANNEL IF A MESSAGE IS EDITED
    #############################################################################################
    
    @commands.Cog.listener()
    async def on_message_edit(self,message_before,message_after):
        if str(message_before.guild.id) in self.CONFIG.keys():
            try:
                if self.CONFIG[str(message_before.guild.id)]["toggled"] and self.CONFIG[str(message_before.guild.id)]["channel"] != None:        
                    emb=discord.Embed(title=f'Message Edited in {message_after.channel}',description='',color=discord.Color.red())
                    emb.set_author(name=message_after.author,icon_url=message_after.author.avatar_url)
                    emb.add_field(name='Old message',value=message_before.content)
                    emb.add_field(name='Edited Message',value=message_after.content)
                    try: await self.bot.get_channel(self.CONFIG[str(message_before.guild.id)]["channel"]).send(embed=emb)
                    except KeyError: pass
            except KeyError:
                emb=discord.Embed(title=f'Message Edited in {message_after.channel}',description='',color=discord.Color.red())
                emb.set_author(name=message_after.author,icon_url=message_after.author.avatar_url)
                emb.add_field(name='Old message',value=message_before.content)
                emb.add_field(name='Edited Message',value=message_after.content)
                try: await self.bot.get_channel(self.CONFIG[str(message_before.guild.id)]["channel"]).send(embed=emb)
                except KeyError: pass
            
    #############################################################################################
        
    ## ==> THIS FUNCTION SENDS LOG WHEN A MESSAGE GETS DELETED
    #############################################################################################
    
    @commands.Cog.listener()
    async def on_message_delete(self,message):
        if str(message.guild.id) in self.CONFIG.keys():
            try:
                if self.CONFIG[str(message.guild.id)]["toggled"] and self.CONFIG[str(message.guild.id)]["channel"] != None:
                    emb=discord.Embed(title='Deleted Message', description=f'Message in {message.channel.mention} sent by {message.author} is deleted.',color=discord.Color.red())
                    emb.set_author(name=message.author,icon_url=message.author.avatar_url)
                    emb.add_field(name='Message',value=message.content)
                    emb.timestamp=message.created_at
                    try: await self.bot.get_channel(self.CONFIG[str(message.guild.id)]["channel"]).send(embed=emb)
                    except KeyError: pass
            except KeyError:
                emb=discord.Embed(title='Deleted Message', description=f'Message in {message.channel.mention} sent by {message.author} is deleted.',color=discord.Color.red())
                emb.set_author(name=message.author,icon_url=message.author.avatar_url)
                emb.add_field(name='Message',value=message.content)
                emb.timestamp=message.created_at
                try: await self.bot.get_channel(self.CONFIG[str(message.guild.id)]["channel"]).send(embed=emb)
                except KeyError: pass
        
    #############################################################################################
    
    ## ==> CONFIGURATION
    #############################################################################################
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def togglemod(self, ctx: commands.Context) -> None:
        if str(ctx.guild.id) in self.CONFIG.keys():
            self.CONFIG[str(ctx.guild.id)]["ModEnabled"] = True if not self.CONFIG[str(ctx.guild.id)]["ModEnabled"] else False
        else:
            self.CONFIG[str(ctx.guild.id)] = {"ModEnabled":True}
        with open("Configuration/ModConfig.json",'w') as f: json.dump(self.CONFIG, f, indent=4)
        enabledordisabled = 'enabled' if self.CONFIG[str(ctx.guild.id)]["ModEnabled"] else 'disabled'
        await ctx.send(embed=discord.Embed(title="MODERATION", description=f"The AutoMod Feature has been {enabledordisabled}!", color = ctx.author.color))
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def toggleLog(self, ctx: commands.Context) -> None:
        if str(ctx.guild.id) in self.CONFIG.keys():
            self.CONFIG[str(ctx.guild.id)]["toggled"] = True if not self.CONFIG[str(ctx.guild.id)]["toggled"] else False
        else:
            self.CONFIG[str(ctx.guild.id)] = {"channel": None, "toggled": True}
            
        with open("Configuration/ModConfig.json",'w') as f: json.dump(self.CONFIG, f, indent=4)
        await ctx.send(embed=discord.Embed(color=ctx.author.color, title="MODERATION", description="Logs Have Been Toggled"))
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setLogChannel(self,ctx: commands.Context, channel: discord.TextChannel):
        if channel in ctx.guild.channels:
            if str(ctx.guild.id) not in self.CONFIG.keys(): self.CONFIG[str(ctx.guild.id)] = {"channel": channel.id, "toggled":False}
            else: self.CONFIG[str(ctx.guild.id)]["channel"] = channel.id
            
            with open("Configuration/ModConfig.json",'w') as f: json.dump(self.CONFIG, f, indent=4)
            embed = discord.Embed(title="MODERATION",description=f"Logs set to <#{channel.id}> !", color=ctx.author.color)
            await ctx.send(embed=embed)
        else: return
        
    #############################################################################################

    ## ==> KICK
    #############################################################################################
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, user:commands.MemberConverter, *, reason=None) -> None:
        if user is None: await ctx.send('Please specify a user')
        else:
            await user.kick(reason=reason)
            await ctx.send(f'{user} has been kicked from your server')
        
    #############################################################################################

    ## ==> BAN
    #############################################################################################
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context , user: commands.MemberConverter, *, reason=None) -> None:
        if user == ctx.author:
            await ctx.send("You can't ban yourself!")
            return
        if user==None:
            await ctx.send('Please specify a user')
            return
        await user.ban(reason=reason)
        await ctx.send(f'{user} has been banned from your server.')
        
    #############################################################################################
    
    ## ==> UNBAN
    #############################################################################################

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context,* , member) -> None:
        banned_users = await ctx.guild.bans()
        if member.isdigit():
            member = await self.bot.fetch_user(member)
            if member in banned_users:
                await ctx.send(f"{member.name} is not banned!")
            else:
                await ctx.guild.unban(member)
                await ctx.send(f"Unbanned {member.name}")
        else:
            member_name,member_disc=member.split('#')#This command will split the member name and its discriminator
            for banned_entry in banned_users:
                user = banned_entry.user
                if (user.name,user.discriminator) == (member_name,member_disc):#This line checks if the given user is in banned users list if yes the next line unban them.
                    await ctx.guild.unban(user)
                    await ctx.send(f'{user.name} has been unbanned')
                    return
            await ctx.send(member+'was not found')#and if the given user is not in banned users list it just send this message.
    
    #############################################################################################
    
    @commands.command()
    @commands.has_guild_permissions(mute_members=True)
    async def mute(self, ctx, user:commands.MemberConverter=None, time=None, *, reason=None):
        if user == None:
            await ctx.send("You must mention a member to mute!")
            return
        elif time == None:
            await ctx.send("Please mention a time!")
            return

        count = 0
        for i in time:
            if i.isalpha():
                count += 1
        if count > 1:
            await ctx.send("Please mention a valid time!")
        elif user == ctx.author:
            await ctx.send("You can't mute yourself!")
        else:
            if reason == None:
                reason = "Unspecified"
            
            digits = time[:-1]
            duration = time[-1]
            if duration == 's':
                seconds = digits
            elif duration == 'm':
                seconds = int(digits) * 60
            elif duration == 'h':
                seconds = int(digits) * 3600
            elif duration == 'd':
                seconds = int(digits) * 86400
            elif duration == 'w':
                seconds = int(digits) * 604800
            else:
                await ctx.send("Invalid duration input")
                return
            
            Muted = discord.utils.get(ctx.guild.roles, name="Muted")
            if Muted == None:
                Muted = await ctx.guild.create_role(name="Muted")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(Muted, speak=False, send_messages=False)
            
            if Muted not in user.roles:
                await user.add_roles(Muted)
                await ctx.send(f"{str(user)[:-5]} has been muted for {time}.")
                await user.send(f"You are muted from the server for {time}\nReason: {reason}")
                await asyncio.sleep(int(seconds))  
            else:
                await ctx.send("Member is already muted")
                return

            if Muted in user.roles:
                await user.remove_roles(Muted)
                await ctx.send(f"{str(user)[:-5]} has been unmuted after {time}.")
                await user.send(f"You have been unmuted from {ctx.guild.name}")
            return

    @commands.command()
    @commands.has_guild_permissions(mute_members=True)
    async def unmute(self, ctx, user:commands.MemberConverter=None):

        if user == None:
            await ctx.send("Please provide a user!")
            return

        Muted = discord.utils.get(ctx.guild.roles, name="Muted")
        if Muted in user.roles:
            await user.remove_roles(Muted)
            await ctx.send(f"{str(user)[:-5]} has been unmuted.")
            await user.send(f"You have been unmuted from {ctx.guild.name}")
        else:
            await ctx.send("Member is not muted!")

    @commands.command(aliases=['purge'])#This is a purge commands,the aliases in paranthese means that you can call this command with the folllowing names.
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount=5) -> None:
        """This command takes only two parameters,that is amount to messages to delete, if no amount is supplied it deletes 5 messages."""
        await ctx.channel.purge(limit=amount+1)#This line is responsible for deleting messages.
        msg = await ctx.send(f'Successfully deleted {amount} messages.')#This line sends a message that n number of messages are deleted.
        await asyncio.sleep(3.0)#Timer of 3 seconds.
        await msg.delete()#This line will delete the message saying n number of messages are deleted.
        
    #############################################################################################

def setup(bot):
    bot.add_cog(Logs(bot))
