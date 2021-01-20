import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
import datetime
import time
import colorsys
import random



client = commands.Bot(command_prefix = "+")


@client.event
async def on_ready():
    print(client.user.name)
    print('====================')
    print('Developed by Subrata#3297')
    print('====================')
    print('Connected to discord')
    print('====================')
    print(client.user.id)
    print('Bot is ready for DM')


@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

@client.command()
async def dm(ctx, *, args=None):
    if args != None:
        members = ctx.guild.members
        for member in members:
            try:
                await member.send(f"{member.mention} {args}")
                print(f"DM sent to: {member.name}#{member.discriminator}")
                
            except:
                print(f"DM couldn't send  to: {member.name}#{member.discriminator}")
                
    else:
        await ctx.channel.send("You didn't provide any message.")


client.run("Nzc4NDc0NDE5ODQwMDkwMTIy.X7SgzQ.Rd-BE2Qgi0FpSY0Eu-UaWdWH2Jc", bot=True)
