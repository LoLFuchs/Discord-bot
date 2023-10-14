import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import os
import datetime
import time
import asyncio


load_dotenv()
token = "Token"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".",intents=intents)

time_window_milliseconds = 5000
max_msg_per_window = 5
author_msg_times = {}


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Syncro done")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="den Drachenlord"))
    print("Status done")
    print(f"Logged in as {bot.user.name}")

@bot.tree.command()
async def hello(ctx):
    await ctx.send("Hii There! I am Mannu And Welcome to the discord.py tutorial")

@bot.tree.command(name="avatar",description="Get user avatar")
async def avatar(interaction:discord.Interaction,member:discord.Member):
    await interaction.response.send_message(f"{member.mention} {member.display_avatar}")

@bot.tree.command(name="drachenlord",description="Erkläre was das ist")
async def slash_command(interaction:discord.Interaction):
    await interaction.response.send_message("Meddle, ich bin der Drachenlords größter Fan und unterstüze ihn wo es nur geht")

@bot.tree.command(name="haider",description="zu wie viel Prozent ist er ein Haider")
async def slash_command(interaction:discord.Interaction, user: discord.Member):
    prozent = random.randint(0, 100)
    if user.name == bot.user.name:
        await interaction.response.send_message("ICH BIN DOCH KEIN HAIDER DU LÜMMEL <:KekWait:1162778147436101705> ")
    elif user.name == "Drachenlord":
         await interaction.response.send_message("DER HEILIGE DRACHENLORD IST DOCH KEIN HAIDER, JETZT WERD NICHT FRECH, ER HAT 6 JAHRE LANG KAMPFSPORT GEMACHT")
    else:
        await interaction.response.send_message(f"{user.mention} ist zu {prozent}% ein Haider")

@bot.event
async def on_message(ctx):
    global author_msg_counts

    author_id = ctx.author.id
    # Get current epoch time in milliseconds
    curr_time = datetime.datetime.now().timestamp() * 1000

    # Make empty list for author id, if it does not exist
    if not author_msg_times.get(author_id, False):
        author_msg_times[author_id] = []

    # Append the time of this message to the users list of message times
    author_msg_times[author_id].append(curr_time)

    # Find the beginning of our time window.
    expr_time = curr_time - time_window_milliseconds

    # Find message times which occurred before the start of our window
    expired_msgs = [
        msg_time for msg_time in author_msg_times[author_id]
        if msg_time < expr_time
    ]

    # Remove all the expired messages times from our list
    for msg_time in expired_msgs:
        author_msg_times[author_id].remove(msg_time)
    # ^ note: we probably need to use a mutex here. Multiple threads
    # might be trying to update this at the same time. Not sure though.

    if len(author_msg_times[author_id]) > max_msg_per_window:
        await ctx.author.send("STOP SPAMMING")
        role = discord.utils.get(ctx.guild.roles, name="timeout")
        await ctx.author.add_roles(role)
        await ctx.channel.send(f"{ctx.author.mention} has been timed out for 2 minutes.")

        await asyncio.sleep(120)
        await ctx.author.remove_roles(role)
        await ctx.channel.send(f"{ctx.author.mention} has been un-timed out.")

bot.run(token)