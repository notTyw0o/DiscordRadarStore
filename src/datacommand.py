from discord.ext import commands
from discord.commands import Option
import mongo
import util_function
import client_data
import discordembed


COMMAND = [
     {
          'name': 'Register',
          'function': mongo.register
     }
]