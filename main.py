import discord
from discord.ext import commands
from datetime import datetime
from datetime import date
import random
import asyncio
import random
import os
import re
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['TOKEN']

elements = {
    'Hydrogen': 'h',
    'Helium': 'he',
    'Lithium': 'li',
    'Beryllium': 'be',
    'Boron': 'b',
    'Carbon': 'c',
    'Nitrogen': 'n',
    'Oxygen': 'o',
    'Fluorine': 'f',
    'Neon': 'ne',
    'Sodium': 'na',
    'Magnesium': 'mg',
    'Aluminum': 'al',
    'Silicon': 'si',
    'Phosphorus': 'p',
    'Sulfur': 's',
    'Chlorine': 'cl',
    'Argon': 'ar',
    'Potassium': 'k',
    'Calcium': 'ca'
}

outcome_weights = [0.05,0.32,0.32,0.31]  

shuffled_keys = random.sample(elements.keys(), len(elements))
string_time = datetime.now().strftime('%I:%M %p')

defIntents = discord.Intents.default()
defIntents.members = True
defIntents.message_content = True

bot = commands.Bot(command_prefix='.',intents=defIntents)      #change this to the command prefix you want



@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with your feelings"))
    print(f'Logged in as {bot.user}')
    for server in bot.guilds:
        for channel in server.text_channels:
            if channel.name == 'general':   #change this to the channel you want the bot to send the message in
                await channel.send('Cheetah')
                break
          
@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    try:
        with open("discord-bot\\text files\\logs.txt", "a") as myfile:  
            myfile.write(f'{message.author} : {message.content}\t at {date.today()}  {string_time} in server: {message.guild}\n')
    except UnicodeEncodeError:
        pass

    await bot.process_commands(message)

@bot.command(help='Starts a quiz about elements and their atomic numbers and symbols')
async def chem(ctx):
    score = 0
    incorrect_answer_keys = []
    await ctx.send("**Welcome to the chemistry quiz. Write the symbols and the atomic numbers of the following elements within 15 seconds each. Type 'quit' to end the quiz.**")
    await asyncio.sleep(1.5)

    for question in shuffled_keys:
        await ctx.send(f' What is the symbol and atomic number of {question}?')

        def check(m):
            return m.author == ctx.author
        try:
            answer = await bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.send(f'Sorry, you took too long to answer. The correct answer was {elements[question]} and atomic number was {list(elements.keys()).index(question)+1}')
            continue
        if answer.content.lower().split(' ')[0] == elements[question] and answer.content.lower().split(' ')[1] == str(list(elements.keys()).index(question)+1):
            await ctx.send('Correct!')
            score += 1
        elif answer.content.lower() == 'quit':
            await ctx.send(f'Quiz ended by {ctx.author}')
            return
        else:
            await ctx.send(f'Incorrect! The answer was {elements[question]} and atomic number was {list(elements.keys()).index(question)+1}')
            incorrect_answer_keys.append(question)
    await ctx.send(f'You got {score} out of {len(elements)} questions correct!')
    await ctx.send(f'You got the following elements wrong: {", ".join(incorrect_answer_keys)}')
    await ctx.send(f'Accuracy: {score/len(elements)*100}%')

@bot.command(help='Solves math equations')
async def math(ctx,*equ):
    equation = ' '.join(equ)
    try:
        await ctx.send(f'Answer = {eval(equation)}')
    except ZeroDivisionError:
        await ctx.send('Cannot divide by zero')
    except:
        await ctx.send('Invalid equation')

@bot.command(help='Makes the bot join a VC')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

@bot.command(help='Makes the bot leave the VC')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel.")

@bot.command(help='Plays music from a file')
async def play(ctx, *, filename):
    ffmpeg_executable = os.environ['FFMPEG_PATH']
    voice_client = ctx.guild.voice_client

    if not voice_client:
        await ctx.send("I need to be in a voice channel to play music.")
        return

   

    voice_client.play(discord.FFmpegPCMAudio(executable=ffmpeg_executable, source=filename))
    


    await ctx.send(f'Now playing: {filename}')

@bot.command(help='Pauses the music')
async def pause(ctx):
    voice_client = ctx.guild.voice_client

    if not voice_client or not voice_client.is_playing():
        await ctx.send("I'm not playing anything right now.")
        return

    voice_client.pause()
    await ctx.send("Playback paused.")

@bot.command(help='Resumes the music')
async def resume(ctx):
    voice_client = ctx.guild.voice_client

    if not voice_client or not voice_client.is_paused():
        await ctx.send("Playback is not paused.")
        return

    voice_client.resume()
    await ctx.send("Playback resumed.")

@bot.command(help='Stops the music')
async def stop(ctx):
    voice_client = ctx.guild.voice_client

    if not voice_client or not voice_client.is_playing():
        await ctx.send("I'm not playing anything right now.")
        return

    voice_client.stop()
    await ctx.send("Playback stopped.")

@bot.command(help='Clears a specified number of messages')
async def purge(ctx,num):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.message.delete()  
        await ctx.channel.purge(limit=int(num)+1)
    else: 
        await ctx.send('You do not have the required permissions')

@bot.command(help='Pings a website')
async def ping(ctx,website):
    response = os.system("ping " + website)
    if response == 0:
        await ctx.send(f'{website} is up')
    else:
        await ctx.send(f'{website} is down')

@bot.command(help='Sends our memes')
async def memes(ctx):
    prompts = ['**Loading...**','**Fetching meme...**','**Looking in the cosmos..**','**Searching in the void....**','**Searching in the void of my broken heart...**']
    memes = [a for a in os.listdir(os.environ['MEMES_FOLDER'])]
    memes = sorted(memes, key=lambda x: int(re.match(r'(\d+)', x).group(1)))

    def check(m):
        return m.author == ctx.author

    await ctx.send('**Note: This feature takes time to load, won\'t show memes immediatley, wait or kys**')
    await ctx.send('**Meme IDs:**')
    await asyncio.sleep(0.5)

    await ctx.send('\n'.join(memes).replace('.mp4',''))

    await ctx.send('**Enter ID: **')
    try:
        answer = await bot.wait_for('message', check=check, timeout=20.0)
        await ctx.send(random.choice(prompts))
    except asyncio.TimeoutError:
        await ctx.send('**Time out. Run command again**')
    try:
        file = discord.File(f'{os.environ['MEMES_FOLDER']} {memes[int(answer.content)-1]}')
        await ctx.send(file=file)
    except (IndexError, ValueError):
        await ctx.send('Invalid meme number')
bot.run(TOKEN)