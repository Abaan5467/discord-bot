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

load_dotenv(dotenv_path='discord-bot\\vars.env')

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

quotes = {
    'Azaan (Hamish Chor)':'Enjoy ur life an live in nature with ur family',
    'Abaan':'Do ando ka omelette banta hai bacha nahi',
    'Azaan (Hamish chor)': 'Jab apna aage nahi badhta toh durson ka kaatna padta hai',
          }

coins = 0
player_health = 100
player_inventory = {}
game_situations = {
                    'kaalwatul':'*You see a kalwatul.*',
                    'chaand':'*You see chaand.*',
                    'nothing':'*You see nothing.*'
                   
                   }
character_drops = {
    'kaalwatul':['N-word pass'],
    'chaand':['PW band'],
    'hamish chor':['Protien'],
}
outcomes = {
            'kaalwatul':{
                            'attack':{
                                            '***You killed kaalwatul and found the guy who asked. You Win***': [500,500,False],
                                            '*Kalwatul is dead lmao*' : [10,0,True],  #[coins, health]
                                            '*Kalwatul used his cake and beat you. Ouch. That hurt a lot*': [-10,-50,False],
                                            '*Kalwatul got scared and ran away lmaoo*': [5,0,True]
                                    },
                            'run':{
                                        '***You ran away and found the guy who asked. You Win***': [500,500,False],
                                        '*You ran away*': [10,0,False],
                                        '*Kalwatul caught you and beat you*': [-10,-50,False],
                                        '*You ran away and found a first-aid kit and a wallet*': [5,10,False]
                                    }
                        },
            'chaand':{
                            'talk':{
                                    '***You talked to her and she lead you to the guy who asked. You Win***': [500,500,False],
                                    '*You talked to chaand and she gave you PW band* 😭': [100,100,True],
                                    '*She left you in 2 days*': [-100,-50,False],
                                    '*She said \" aura +100000 \" *': [60,5,True]
                                    },
                            'run':{
                                    '***You ran away and found the guy who asked. You Win***': [500,500,False],
                                    '*You ran away*': [20,0,False],
                                    '*She caught you and beat you*': [-10,-50,False],
                                    '*You ran away and found a first-aid kit and a wallet*': [5,5,False]
                                    }
                        },

            'hamish chor':{

                            'talk':{
                                '***You talked to him and he lead you to the guy who asked. You Win***': [500,500,False],
                                '*You talked to him and he said a legendary quote*': [0,0,False],
                                '*He stole your wallet and ran away*': [-100,-5,True],
                                '*You talked to him and you both went to do chori*':[100,0,True]

                            },
                            'run':{
                                '***You ran away and found the guy who asked. You Win***': [500,500,False],
                                '*You ran away*': [10,0,False],
                                '*He caught you and stole your wallet*': [-50,-10,False],
                                '*His dada caught you and used his fireball ability*': [-100,-100,False]

                            }
                            
                        },
            'nothing':{
                            'wait':{
                                    '***You waited and the guy who asked showed up. You Win***': [500,500,False],
                                    '*You waited and nothing happened*': [0,0,False],
                                    '*You waited and a treasure fell from the sky*': [100,0,False],
                                    '*You waited and kaalwatul came and beat you*': [-10,-50,False]
                                    },
                            'walk':{
                                    '***You walked and reached the house of the guy who asked. You Win***': [500,500,False],
                                    '*You walked and nothing happened*': [0,0,False],
                                    '*You walked and fell in a hole*': [-10,-10,False],
                                    '*You walked and found a treasure*': [100,0,False]
                                    }
                        }
}
outcome_weights = [0.05,0.32,0.32,0.31]  

shuffled_keys = random.sample(elements.keys(), len(elements))
string_time = datetime.now().strftime('%I:%M %p')

defIntents = discord.Intents.default()
defIntents.members = True
defIntents.message_content = True

bot = commands.Bot(command_prefix='.',intents=defIntents)



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

@bot.command(help='Sends a random legendary quote')
async def quote(ctx):
    quote_artist = random.choice(list(quotes.keys()))
    await ctx.send(f'Once {quote_artist} said:\n **\"{quotes[quote_artist]}\"**')

@bot.command(help='Starts a text-based adventure game')
async def game(ctx):
    global player_health
    global coins
    defeted_in_a_row = 0
    item = ''
    await ctx.send('Game started.')
    await ctx.send('**Objective: Find the guy who asked**')
    await asyncio.sleep(1)
    await ctx.send(f'**Current stats: {ctx.author}\nHealth: {player_health}\nCoins: {coins}**')
    await asyncio.sleep(1)
    
    def check(m):
        return m.author == ctx.author
    
    while player_health > 0:
        character = random.choice(list(game_situations.keys()))
        await ctx.send(game_situations[character])

        prompt = ' / '.join(list(outcomes[character].keys()))
        await asyncio.sleep(1)
        await ctx.send(f'*What will you do? ({prompt}): *')
        try:
            action = await bot.wait_for('message', check=check, timeout=20.0)
        except asyncio.TimeoutError:
            await ctx.send('**Time out. Run command again**')
            break
        try:
            outcome = random.choices(list(outcomes[character][action.content].keys()),weights=outcome_weights,k=1)[0]
        except (KeyError, ValueError):
            await ctx.send('**Invalid action. Try again**')
            try:
                action = await bot.wait_for('message', check=check, timeout=20.0)
            except asyncio.TimeoutError:
                await ctx.send('**Time out. Run command again**')
            continue
        await asyncio.sleep(1)
        await ctx.send(outcome)


        if random.choice([True,False]) and outcomes[character][action.content][outcome][-1]:
            item = random.choice(character_drops[character])
            await ctx.send(f'***{character.capitalize()} dropped {item}***')
            player_inventory[item] = player_inventory.get(item,0) + 1
            

        if outcomes[character][action.content][outcome][0:-1] == [500,500]:
            defeted_in_a_row = 0
            break
        elif outcomes[character][action.content][outcome][0:-1] == [-100,-100]:
            await asyncio.sleep(1)
            defeted_in_a_row += 1
            await ctx.send('***You died. Game over***')
            break
        coins += outcomes[character][action.content][outcome][0]
        player_health += outcomes[character][action.content][outcome][1]

        if player_health > 100:
            player_health = 100
        if coins < 0:
            coins = 0

        if player_health <= 0:
            await asyncio.sleep(1)
            defeted_in_a_row += 1
            await ctx.send('***You died. Game over***')
            break
        await asyncio.sleep(1)
        await ctx.send(f' **Coins : {outcomes[character][action.content][outcome][0]:+d} | Health : {outcomes[character][action.content][outcome][1]:+d}** | Inventory: {player_inventory}')
        await ctx.send(f'**Current stats: {ctx.author}\nHealth: {player_health}\nCoins: {coins}**')
        if defeted_in_a_row >=5:
            await ctx.send(f'**You lost {defeted_in_a_row} times in a row lmao. Skill issue fr** 💀')
            break
    player_health = 100
    coins = 0
bot.run(TOKEN)