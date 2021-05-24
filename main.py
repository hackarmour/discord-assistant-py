#############################################################################################
#
# This is an open source Discord Bot which is obviously written in Python   
# enter the Token in the file "config.json"
#
#  Happy Codings,
#   ~ TheEmperor342 and PhantomKnight287
# 
#############################################################################################

## ==> IMPORTING NECESSARY MODULES
#############################################################################################

import discord, json, os
from discord.ext import commands

#############################################################################################

## ==> READING TOKEN OUT FROM THE CONFIGURATION FILE
#############################################################################################

with open("config.json") as f:
    TOKEN = json.loads(f.read())["token"]

#############################################################################################

## ==> CREATING BOT AND IMPORTING COGS
#############################################################################################

bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())
bot.remove_command("help")

for i in os.listdir("Cogs"):
    if i.endswith(".py"):
        bot.load_extension(F"Cogs.{i[:-3]}")

@bot.event
async def on_ready(): print("The Bot is Ready")

## You can uncomment this function and put all the id's of users whom you want which will be able to reload cogs
# @bot.command()
# async def reload(ctx,cog):
#     if ctx.author.id in [Uncomment and put your id here if you want to use this function]: # list example -> [<id in integer form>, <another id>]
#         if cog.lower() == "all":
#             for i in os.listdir("Cogs"):
#                 if i.endswith(".py"):
#                     bot.unload_extension(F"Cogs.{i[:-3]}")
#                     bot.load_extension(F"Cogs.{i[:-3]}")
#         await ctx.send("Reloaded all Cogs")
#     else:
#         bot.unload_extension(F"Cogs.{cog}")
#         bot.load_extension(F"Cogs.{cog}")

#############################################################################################

## ==> RUNNING THE BOT
#############################################################################################

bot.run(TOKEN)

#############################################################################################