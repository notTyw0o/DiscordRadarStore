import discord
from discord.ext import commands
import locale
from datetime import datetime, timedelta

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
    current_time = datetime.now()
    return current_time.strftime("%Y/%m/%d at %I:%M %p")

def rupiah_format(angka, with_prefix=False, desimal=2):
    try:
        # Change the locale setting to a supported one (for example, 'en_US.UTF-8')
        locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')

        rupiah = locale.format("%.*f", (desimal, angka), True)
        if with_prefix:
            return "Rp. {}".format(rupiah)
        return rupiah
    except locale.Error as e:
        print(f"Error occurred: {e}")
        return "Error: Unsupported locale setting"

def expired(date_string):
    # Convert the given date string to a datetime object
    given_date = datetime.strptime(date_string, '%d-%m-%Y')

    # Get the current date
    current_date = datetime.now()

    # Compare the given date with the current date
    if current_date > given_date:
        return True  # The given date has passed
    else:
        return False  # The given date has not passed
