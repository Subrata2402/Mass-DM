import discord
from discord.ext import commands
from discord.ext.commands import bot

token = "ODEzODM2MjA2NjM4NzU5OTQ3.YDVGCA.Vn4C5Qolwk1Q2zdYxrnkCbNESUc"

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
                print(f"DM sent to: {member.name}#{member.discriminator}")
                
            except:
                print(f"DM couldn't send  to: {member.name}#{member.discriminator}")
                
    else:
        await ctx.channel.send("You didn't provide any message.")


client.run(token)
