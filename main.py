import discord
from discord.ext import commands
from discord.ext.commands import bot

token = "BOT_TOKEN"

intents = discord.Intents.all()
client = commands.Bot(command_prefix = "+", intents=intents)


@client.event
async def on_ready():
    print(client.user.name)
    print('====================')
    print('Bot is ready for DM')

@client.command()
async def send(ctx, *, args=None):
    if args != None:
        members = ctx.guild.members
        for member in members:
            try:
                await member.send(f"{member.mention} {args}")
                print(f"DM sent to: {member}")
                
            except:
                print(f"DM couldn't send  to: {member}")
                
    else:
        await ctx.channel.send("You didn't provide any message.")


client.run(token)
