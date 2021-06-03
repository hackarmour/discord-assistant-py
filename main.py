#############################################################################################
#
# This is an open source Discord Bot which is obviously written in Python   
# enter the Token in the file "config.json"
# The Functionalities:
# Welcomer
# Tic Tac Toe
# Moderation
#
#  Happy Codings,
#   ~ TheEmperor342 and PhantomKnight287
# 
#############################################################################################

## ==> IMPORTING NECESSARY MODULES
#############################################################################################

import discord, json, os
from discord.ext import commands
import datetime, time

#############################################################################################

## ==> READING TOKEN OUT FROM THE CONFIGURATION FILE
#############################################################################################

with open("Configuration/config.json") as f:
    TOKEN = json.loads(f.read())["token"]

#############################################################################################

## ==> CREATING BOT AND IMPORTING COGS
#############################################################################################

bot = commands.Bot(command_prefix=">", intents=discord.Intents.all(),case_insensitive=True)
bot.remove_command("help")



@bot.event
async def on_ready(): 
    print("The Bot is Ready")
    with open("Configuration/config.json") as f:
        config = json.loads(f.read())
        config["starttime"] = time.time()
        
    with open("Configuration/config.json", 'w') as f:
        f.write(json.dumps(config))
        
for i in os.listdir("Cogs"):
    if i.endswith(".py"):
        bot.load_extension(F"Cogs.{i[:-3]}")   

@bot.command()
async def reload(ctx,cog):
    if ctx.author.id in [754894159403286531, 510480545160101898]:
        if cog.lower() == "all":
            for i in os.listdir("Cogs"):
                if i.endswith(".py"):
                    bot.unload_extension(F"Cogs.{i[:-3]}")
                    bot.load_extension(F"Cogs.{i[:-3]}")
        await ctx.send("Reloaded all Cogs")
    else:
        bot.unload_extension(F"Cogs.{cog}")
        bot.load_extension(F"Cogs.{cog}")

#############################################################################################

## ==> RUNNING THE BOT
#############################################################################################

bot.run(TOKEN)

#############################################################################################