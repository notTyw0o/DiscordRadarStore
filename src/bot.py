import discord
from discord.ext import commands
import client_data
import mongo

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

# Load the math_cogs.py module as an extension
bot.load_extension('cogs.commands_list')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=client_data.PRESENCE))
    print(f'Logged in as {bot.user.name}')

def startBot():
    bot.run(client_data.TOKEN)
