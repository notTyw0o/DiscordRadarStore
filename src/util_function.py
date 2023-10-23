import discord
from discord.ext import commands

async def isAuthor(received_id: str, owner_id: str):
    if str(received_id) == owner_id:
        response = {
            'status': 200,
            'message': 'Authorized!'
        }
        return response
    else:
        response = {
            'status': 400,
            'message': 'Unauthorized!'
        }
        return response