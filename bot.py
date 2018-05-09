#Example Bot by Ryan Mason
#20180509

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

bot = commands.Bot(command_prefix="#")

@bot.event
async def on_ready():
    print("Squads are about to be scheduled")
    print("My bot name is " + bot.user.name)

bot.run("NDQzODg2NDQwMzA1MzkzNjg2.DdUBng.x06sGMDze57xOFTxTgdFu1cg2Tc")