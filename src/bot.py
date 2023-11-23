import discord
from discord.ext import commands
import client_data
import mongo
import discordembed

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

if client_data.SECRET_KEY == 'fc8af3e8ecf73bbd83597682037925d7':
    bot.load_extension('cogs.commands_admin')
    bot.load_extension('cogs.commands_user')
else:
    bot.load_extension('cogs.commands_user')
    try:
        bot.load_extension(f'cogs.{client_data.SECRET_KEY}')
    except:
        pass

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=client_data.PRESENCE))
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    invalid_prefixes = ['.', ',', '!', '>', '/']

    # Check if the message starts with any of the invalid prefixes
    if message.content.startswith(tuple(invalid_prefixes)):
        assets = await mongo.getassets()
        arrow = assets['assets']['sticker_1']
        embed = await discordembed.textembed('Command error, please use (/) slash commands!')
        await message.channel.send(embed=embed)

    await bot.process_commands(message)

def startBot():
    bot.run(client_data.TOKEN)
