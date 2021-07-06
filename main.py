# Import the necessary modules
import discord, json, os
from discord.ext import commands
from time import time

# Read the token
TOKEN = input("Enter The Token of your bot: ")

# Initialize the bot instance
bot = commands.Bot(command_prefix=">", intents=discord.Intents.all(),case_insensitive=True)
bot.remove_command("help")

for i in os.listdir("Cogs"):
    if i.endswith(".py"):
        bot.load_extension(F"Cogs.{i[:-3]}")

@bot.event
async def on_ready():
    print("The Bot is Ready")
    with open("Configuration/config.json") as f:
        config = json.loads(f.read())
        config["starttime"] = float(time())

    with open("Configuration/config.json", 'w') as f:
        f.write(json.dumps(config))

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

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
