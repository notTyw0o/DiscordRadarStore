import discord
from discord.ext import commands
import client_data
import mongo

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

if client_data.SECRET_KEY == 'fc8af3e8ecf73bbd83597682037925d7':
    bot.load_extension('cogs.commands_admin')
    bot.load_extension('cogs.commands_user')
else:
    bot.load_extension('cogs.commands_user')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=client_data.PRESENCE))
    print(f'Logged in as {bot.user.name}')

def startBot():
    bot.run(client_data.TOKEN)
