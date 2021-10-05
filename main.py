# =============================================================================================
# Copyright (C) 2021 HackArmour

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# =============================================================================================

import discord, json, os, traceback
from discord.ext import commands
from time import time
from discord_components import DiscordComponents

# READING TOKEN
TOKEN = input("Enter The Token of your bot: ")

## ==> CREATING A BOT INSTANCE
# ============================================

bot = commands.Bot(
    command_prefix=">",
    intents=discord.Intents.all(),
    case_insensitive=True,
    owner_ids=[754894159403286531, 510480545160101898, 628575263818514444, 706839448620498965]
)

# ============================================

## ==> READ CONFIGURATIONS
# ============================================

with open("Configuration/config.json") as f:
    cfg = json.load(f)
    fail = cfg["fail_emoji"]
    success = cfg["success_emoji"]
    embed_color = cfg["embed_color"]
    r = embed_color[0]
    g = embed_color[1]
    b = embed_color[2]

# ============================================

## ==> IMPORT COGS
# ============================================

for i in os.listdir("Cogs"):
    if i.endswith(".py"):
        bot.load_extension(f"Cogs.{i[:-3]}")


# ============================================

## ==> ON READY
# ============================================

@bot.event
async def on_ready() -> None:

    ## ==> DUMP THE STARTTIME
    cfg["starttime"] = time()
    with open("Configuration/config.json", 'w') as f:
        json.dump(cfg, f, indent=4)

    DiscordComponents(bot)
    print("I've Woken Up")

# ============================================


## ==> RELOAD COGS COMMAND
# =============================================================================================

@bot.command()
async def reload(ctx: commands.Context, cog: str) -> None:

    ## ==> CHECK
    if ctx.author.id not in bot.owner_ids: return

    ## ==> RUNS IF ASKED TO RELOAD ALL COGS
    if cog.lower() == "all":
        for i in os.listdir("Cogs"):
            if i.endswith(".py"):
                try:
                    bot.unload_extension(f"Cogs.{i[:-3]}")
                    bot.load_extension(f"Cogs.{i[:-3]}")
                except Exception:
                    await ctx.send(
                        embed=discord.Embed(
                            title='COGS',
                            color=discord.Color.from_rgb(r, g, b),
                            description=f"{fail} **Error Occured While Loading `{i}`**\n```\n{traceback.format_exc()}\n```"
                        )
                    )
        print(f"{'#'*25} Reloaded All Cogs {'#'*25}")
        await ctx.send(
            embed=discord.Embed(
                title="COGS",
                description=f"{success} **Reloaded** all Cogs",
                color=discord.Color.from_rgb(r, g, b)
            )
        )

    ## ==> ELSE TRIES TO RELOAD THE COG TOLD TO
    else:
        try:
            bot.unload_extension(f"Cogs.{cog}")
            bot.load_extension(f"Cogs.{cog}")
            await ctx.send(
                embed=discord.Embed(
                    title='COGS',
                    color=discord.Color.from_rgb(r, g, b),
                    description=f"{success} **Reloaded** Cog `{cog}`"
                )
            )
            print(f"{'#' * 25} Reloaded {cog} {'#' * 25}")
        except Exception:
            await ctx.send(
                embed=discord.Embed(
                    title='COGS',
                    color=discord.Color.from_rgb(r, g, b),
                    description=f"{fail} **Error Occured While Reloading `{cog}`**\n```\n{traceback.format_exc()}\n```"
                )
            )

# =============================================================================================

## ==> LOAD COGS COMMAND
# =============================================================================================


@bot.command()
async def load(ctx: commands.Context, cog: str) -> None:

    ## ==> CHECK
    if ctx.author.id not in bot.owner_ids: return

    ## ==> LOAD COG
    try:
        bot.load_extension(f"Cogs.{cog}")
        await ctx.send(
            embed=discord.Embed(
                title='COGS',
                color=discord.Color.from_rgb(r, g, b),
                description=f"{success} **Loaded** Cog `{cog}`"
            )
        )
    except Exception:
        await ctx.send(
            embed=discord.Embed(
                title='COGS',
                color=discord.Color.from_rgb(r, g, b),
                description=f"{fail} **Error Occured While Loading `{cog}`**\n```\n{traceback.format_exc()}\n```"
            )
        )

# =============================================================================================

## ==> UNLOAD COGS COMMAND
# =============================================================================================

@bot.command()
async def unload(ctx: commands.Context, cog: str) -> None:

    ## ==> CHECKS
    if ctx.author.id not in bot.owner_ids: return

    ## ==> UNLOAD COG
    try:
        bot.unload_extension(f"Cogs.{cog}")
        await ctx.send(
            embed=discord.Embed(
                title='COGS',
                color=discord.Color.from_rgb(r, g, b),
                description=f"{success} **Unloaded** Cog `{cog}`"
            )
        )
    except Exception:
        await ctx.send(
            embed=discord.Embed(
                title='COGS',
                color=discord.Color.from_rgb(r, g, b),
                description=f"{fail} **Error Occured While Unloading `{cog}`**\n```\n{traceback.format_exc()}\n```"
            )
        )

# =============================================================================================

## ==> CHANGE PRESENCE
# ============================================

@bot.command()
async def change_presence(ctx: commands.Context, *, presence: str) -> None:
    if ctx.author.id in bot.owner_ids:
        await bot.change_presence(activity=discord.Game(presence))


# ============================================

## ==> RUN THE BOT
if __name__ == "__main__":
    bot.run(TOKEN)
