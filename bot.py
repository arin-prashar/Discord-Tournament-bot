import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
from dotenv import load_dotenv
import os

point_tally=dict()
load_dotenv()
TOKEN = os.getenv('bt_Token')
client = commands.Bot(command_prefix='!',intents=discord.Intents.all())
client.remove_command('help')

with open("Bot/Ranks.txt", "w") as f:
    f.write("")
@client.event
async def on_ready():
    print('Bot is ready!! ')

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="List of commands", color=0xeee657)
    embed.add_field(name="!ping", value="Returns bot latency", inline=False)
    embed.add_field(name="!addusr", value="Adds a user to the list --** Mention all users to add to list **", inline=False)
    embed.add_field(name="!win", value="Adds a point to the user --** Requires Mention **", inline=False)
    embed.add_field(name="!loss", value="Subtracts a point from the user --** Requires Mention **", inline=False)
    embed.add_field(name="!ranks", value="Displays the ranks", inline=False)
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    bot_lat=client.latency*1000
    print("pinged")
    await ctx.send("%.2f ms  Pong!"%bot_lat)

@client.command()
async def win(ctx, name):
    # Get the Member object for the user
    try:
        user_id = int(name[2:-1])
        member = ctx.guild.get_member(user_id)
    
    except:
        await ctx.send("Please mention the user")
        return
    dname=member.display_name
    
    # add a point to the user in the dictionary and update the file
    point_tally[dname]+=1
    
    with open("Bot/Ranks.txt", "r") as f:
        lines = f.readlines()
        
        for i in lines:
            x=i.split()
            if x[0]==dname:
                lines[lines.index(i)]=f"{dname} -- {point_tally[dname]} \n"
                
    f.close()
    with open("Bot/Ranks.txt", "w") as f:
        # update the file
        f.writelines(lines)
    f.close()
    await ctx.send(f"{dname} has {point_tally[dname]} points")


@client.command()
async def addusr(ctx,*,names):
    l=names.split()
    for name in l:
        try:
            user_id = int(name[2:-1])
            member = ctx.guild.get_member(user_id)           
            dname=member.display_name
            with open("Bot/Ranks.txt", "a") as f:
                point_tally[dname]=0
                f.write(f"{dname} -- {point_tally[dname]} \n")
        except:
            await ctx.send("Please mention the user")
            return
    await ctx.send("Users added to the list")

@client.command()
async def ranks(ctx):
    # open the file and display the ranks
    embed = discord.Embed(title="Ranks", description="List of ranks", color=0xeee657)
    with open ("Bot/Ranks.txt", "r") as f:
        lines = f.readlines()
        f.close()
    for i,j in point_tally.items():
        embed.add_field(name=i, value=j, inline=False)
    await ctx.send(embed=embed)

@client.command()
async def loss(ctx, name):
    # Get the Member object for the user
    try:
        user_id = int(name[2:-1])
        member = ctx.guild.get_member(user_id)
    
    except:
        await ctx.send("Please mention the user")
        return
    dname=member.display_name
    
    # add a point to the user in the dictionary and update the file
    point_tally[dname]-=1
    
    with open("Bot/Ranks.txt", "r") as f:
        lines = f.readlines()
        
        for i in lines:
            x=i.split()
            if x[0]==dname:
                lines[lines.index(i)]=f"{dname} -- {point_tally[dname]} \n"
                
    f.close()
    with open("Bot/Ranks.txt", "w") as f:
        # update the file
        f.writelines(lines)
    f.close()
    await ctx.send(f"{dname} has {point_tally[dname]} points.")

client.run(TOKEN)