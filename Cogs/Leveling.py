## ==> IMPORTS
#############################################################################################

import discord, os, json
import pandas as pd
import numpy as np
from discord.ext import commands
from random import randint, choice
from disrank.generator import Generator

#############################################################################################

class LevelingPD(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        with open("Configuration/Leveling.json") as f:
            self.CONFIG = json.load(f)
        
            
    def position(self, userid, guildid):
        
        ## ==> OPEN FILE
        df = pd.read_csv(f"Configuration/Leveling.csv")
        df = df.astype({"xp": np.int64, "Level": np.int64, "TotalXP": np.int64})
            
            
        ## ==> FILTER DATA AND GET THE RANK
        df_filt = df[df["ID"].str.endswith(str(guildid))]
        df_filt.sort_values("TotalXP",ascending=False ,inplace=True)
        df_filt.reset_index(inplace=True)
        df_filt = df_filt[df_filt["ID"].str.startswith(str(userid))]
        
        ## ==> RETURN THE RANK
        return None if df_filt.index.values[0] == np.NaN else df_filt.index.values[0] + 1
        

    ## ==> INCREMENT XP
    #########################################################################################
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        
        if message.author.bot: return
        if message.author.guild is None: return
                
        if str(message.guild.id) in self.CONFIG.keys():
            if self.CONFIG[str(message.guild.id)]:
                return
                
        if not choice([True, True, True, False, False, False, False, False, False, False]):
            return
        
                
        ## ==> CHOOSE A RANDOM VALUE FOR XP        
        _randNo = randint(5,15)
        
        ## ==> READ THE FILE
        #####################################################################################
        
        if "Leveling.csv" in os.listdir("Configuration"):
            df = pd.read_csv(f"Configuration/Leveling.csv")
            df = df.astype({"xp": np.int64, "Level": np.int64, "TotalXP": np.int64})
        else: 
            df = pd.DataFrame({"ID": [], "xp": [], "Level": [], "TotalXP": []})
            df = df.astype({"xp": np.int64, "Level": np.int64, "TotalXP": np.int64})
        
        #####################################################################################
                
        ## ==> FILTER THE VALUE
        df_filt = df[df['ID'] == f"{message.author.id} & {message.author.guild.id}"]
                
        ## ==> CHECK IF THE USER ALREADY EXISTS OR NOT
        #####################################################################################
        
        if df_filt.shape[0] != 0:
            
            ## ==> CHANGE INDEX
            df.set_index("ID", inplace = True)
            
            ## ==> INCREMENT VALUES
            #################################################################################
            
            if df.loc[f"{message.author.id} & {message.author.guild.id}", 'Level'] != 0:
                
                ## ==> CHECK IF USER HAS A LEVEL UP
                #############################################################################
                
                if (df.loc[f"{message.author.id} & {message.author.guild.id}", 'xp'] + _randNo) >= (df.loc[f"{message.author.id} & {message.author.guild.id}", 'Level'] * 100):
                    df.loc[f"{message.author.id} & {message.author.guild.id}", 'xp'] += _randNo - (df.loc[f"{message.author.id} & {message.author.guild.id}", 'Level'] * 100)
                
                    df.loc[f"{message.author.id} & {message.author.guild.id}", 'Level'] += 1
                    level = df.loc[f"{message.author.id} & {message.author.guild.id}", 'Level']
                    await message.channel.send(f"Congrats, {message.author.mention}, You've Leveled Up to Level {level}!")
                
                #################################################################################
                
                else: 
                    df.loc[f"{message.author.id} & {message.author.guild.id}", 'xp'] += _randNo
                    
            else:
                # here 100 is added and not multiplied because 0 * 100 = 0
                if (df.loc[f"{message.author.id} & {message.author.guild.id}", 'xp'] + _randNo) >= (df.loc[f"{message.author.id} & {message.author.guild.id}", 'Level'] + 100):
                    df.loc[f"{message.author.id} & {message.author.guild.id}", 'xp'] += _randNo - (df.loc[f"{message.author.id} & {message.author.guild.id}", 'Level'] + 100)
                    df.loc[f"{message.author.id} & {message.author.guild.id}", 'Level'] += 1
                    await message.channel.send(f"Congrats, {message.author.mention}, You've Leveled Up to Level 1!")
                else: 
                    df.loc[f"{message.author.id} & {message.author.guild.id}", 'xp'] += _randNo
            
            ## ==> INCREMENT TOTAL XP
            df.loc[f"{message.author.id} & {message.author.guild.id}", "TotalXP"] += _randNo
            
            #################################################################################
            
        
        #####################################################################################
        
        ## ==> ADD THE USER IF THEY DON'T EXIST
        elif df_filt.shape[0] == 0:
            
            if message.author.id == message.author.guild.id:
                return
                        
            df = df.append({"ID": f"{message.author.id} & {message.author.guild.id}", "xp": _randNo, "Level": 0, "TotalXP": _randNo}, ignore_index=True, sort=False)
            df.set_index("ID", inplace=True)
        
        
        ## ==> EXPORT THE DATAFRAME        
        df.to_csv(f"Configuration/Leveling.csv", index=True)

    #########################################################################################

    @commands.command()
    async def rank(self, ctx: commands.Context,*, user: commands.MemberConverter = None) -> None:
        
        ## ==> CHECKS
        #####################################################################################
        
        if user is None: user = ctx.author
        if user.bot: return
        
        #####################################################################################
        
        ## ==> READ FILE
        #####################################################################################
        
        df = pd.read_csv("Configuration/Leveling.csv")
        df = df.astype({"xp": np.int64, "Level": np.int64, "TotalXP": np.int64})
        
        #####################################################################################
        
        ## ==> CHECK IF THE USER IS LEVELED OR NOT
        #####################################################################################
        
        df_filt = df[df['ID'] == f"{user.id} & {user.guild.id}"]
        if df_filt.shape[0] == 0:
            await ctx.send(f"{'''You're''' if user.id == ctx.author.id else f'''{str(user.name)} is'''} not ranked Yet")
            return
        
        #####################################################################################
        
        ## ==> CHANGE INDEX        
        df.set_index("ID", inplace=True)

        ## ==> GET RANK
        rank = self.position(user.id, user.guild.id)
        
        ## ==> ARGUEMENTS FOR DISRANK
        args = {
            'profile_image': user.avatar_url,
            'bg_image': "https://th.bing.com/th/id/R.a1f53543c06c76bcf5ac0279cce89c97?rik=mcsHKpPSRIfsEw&riu=http%3a%2f%2fwww.crossfire-radio.com%2ftest%2fimages%2fimage16x9.png&ehk=7cDpJsoT4ug4YJEm2bETVl%2fT21RzWDORKMCmxjPKPB0%3d&risl=&pid=ImgRaw",
            'level': df.loc[f"{user.id} & {user.guild.id}"]["Level"],
            'user_xp': df.loc[f"{user.id} & {user.guild.id}"]['xp'],
            'next_xp': (df.loc[f"{user.id} & {user.guild.id}"]['Level'] * 100) if df.loc[f"{user.id} & {user.guild.id}"]['Level'] != 0 else (df.loc[f"{user.id} & {user.guild.id}"]['Level'] + 100),
            'user_position': rank,
            'user_name': str(user),
            'user_status': str(user.status)
        }
        
        ## ==> GENERATE RANK CARD
        image = Generator().generate_profile(**args)
        
        ## ==> SEND FILE
        file = discord.File(fp=image, filename=f'image.png')
        await ctx.send(file=file)
        del args, image, file, rank
    
    ## ==> LEADERBOARD
    #########################################################################################
    
    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx: commands.Context) -> None:
        
        ## ==> READ FILE
        df = pd.read_csv(f"Configuration/Leveling.csv")
        df = df.astype({"xp": np.int64, "Level": np.int64, "TotalXP": np.int64})
        
        ## ==> FILTER THE FILE
        df_filt = df[df["ID"].str.endswith(str(ctx.author.guild.id))]
        df_filt.sort_values("TotalXP",ascending=False ,inplace=True)
        df_filt.reset_index(inplace=True)
        _ = []
        
        ## ==> GET LEADERBOARD
        if df_filt.shape[0] >= 9:
            for i in range(9): _.append(df_filt.loc[i, "ID"][:19])
        else:
            for i in range(df_filt.shape[0]): _.append(df_filt.loc[i, "ID"][:18])
            
            
        lb = "\n\n".join([f"{index+1}.  {self.bot.get_user(int(item))}" for index, item in enumerate(_)])
        await ctx.send(embed=discord.Embed(title="LEADERBOARD", color=ctx.author.color, description=f"```\n{lb}\n```"))

    #########################################################################################
    
    ## ==> TOGGLE LEVELING
    #########################################################################################
    
    @commands.command()
    async def ToggleLeveling(self, ctx: commands.Context) -> None:
        if str(ctx.author.guild.id) in self.CONFIG.keys():
            self.CONFIG[str(ctx.author.guild.id)] = True if not self.CONFIG[str(ctx.author.guild.id)] else False
        else:
            self.CONFIG[str(ctx.author.guild.id)] = True
            
        with open("Configuration/Leveling.json", 'w') as f:
            json.dump(self.CONFIG, f, indent=4)
    
        enabledordisabled = "Disabled" if self.CONFIG[str(ctx.author.guild.id)] else "Enabled"
    
        await ctx.send(
            embed=discord.Embed(
                title="LEVELING",
                description=f"Leveling has been {enabledordisabled}",
                color = discord.Color.green() if enabledordisabled == "Enabled" else discord.Color.red()
            )
        )
    
    #########################################################################################

def setup(bot:commands.Bot):
    bot.add_cog(LevelingPD(bot))