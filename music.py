import discord
import os
import asyncio
import youtube_dl
from discord import *
from discord.ext import commands
from discord.ext.commands.context import Context

prefix = "?"
blocked_words = ["blocked words are here"]

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}

intents = discord.Intents.default()
Intents.message_content = True

client = discord.Client(intents=intents)


programmer_role = "987018590152699964"
            


@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")

@client.event
async def on_message(msg):
    if msg.author != client.user:
        if msg.content.lower().startswith(f"{prefix}info"):
            await msg.channel.send(f"Hi, Im musicbot Made By ijsbeertje!")

        for text in blocked_words:
            if text in str(msg.content.lower()):
                await msg.delete()
                await msg.channel.send("Hey, Dont Say That!")
                return
        if msg.content.startswith(f"{prefix}play"):

            try:
                voice_client = await msg.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            except:
                print("error")

            try:
                url = msg.content.split()[1]

                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

                song = data['url']
                player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable="C:\\ffmpeg\\ffmpeg.exe")

                voice_clients[msg.guild.id].play(player)

            except Exception as err:
                print(err)

        if msg.content.startswith(f"{prefix}pause"):
            try:
                voice_clients[msg.guild.id].pause()
            except Exception as err:
                print(err)

        if msg.content.startswith(f"{prefix}resume"):
            try:
                voice_clients[msg.guild.id].resume()
            except Exception as err:
                print(err)

        if msg.content.startswith(f"{prefix}stop"):
            try:
                voice_clients[msg.guild.id].stop()
                await voice_clients[msg.guild.id].disconnect()
            except Exception as err:
                print(err)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
if __name__ == "__main__":
    # Read the token from a file and strip newlines (Fixes issues when running the bot on linux)
    try:
        token = open(os.path.join(__location__, "token.txt"), "r").read().strip("\n")
    except FileNotFoundError:
        print("Please create a token.txt file and place your token in it!")
        quit()
    if token is None:
        print("Please create a token.txt file and place your token in it!")
        quit()
    # Run the bot instance
    client.run(token)
