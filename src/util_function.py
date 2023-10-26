import discord
from discord.ext import commands
import locale
import datetime

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
    
async def timenow():
    current_time = datetime.datetime.now()
    return current_time.strftime("%Y/%m/%d at %I:%M %p")

def rupiah_format(angka, with_prefix=False, desimal=2):
    locale.setlocale(locale.LC_NUMERIC, 'IND')
    rupiah = locale.format("%.*f", (desimal, angka), True)
    if with_prefix:
        return "Rp. {}".format(rupiah)
    return rupiah