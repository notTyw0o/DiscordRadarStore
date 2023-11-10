import discord
from discord.ext import commands
import hashlib
import locale
from datetime import datetime, timedelta
import random
import string
import os
import subprocess
import mongo

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

def generatemd5(input_string):
    encoded_string = input_string.encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(encoded_string)
    hashed_string = md5_hash.hexdigest()

    return hashed_string

def getonemonth():
    current_date = datetime.now()

    # Add one month to the current date
    one_month_later = current_date + timedelta(days=30)  # Adds 30 days for simplicity

    # Format the date as "date-month-year"
    formatted_date = one_month_later.strftime('%d-%m-%Y')

    return formatted_date

def addonemonth(timenow):
    current_date = datetime.strptime(timenow, '%d-%m-%Y')

    # Add one month to the current date
    one_month_later = current_date + timedelta(days=30)  # Adds 30 days for simplicity

    # Format the date as "date-month-year"
    formatted_date = one_month_later.strftime('%d-%m-%Y')

    return formatted_date

def generate_random_string(length):
    # Define the characters you want to include in the random string
    characters = string.ascii_letters + string.digits  # Includes both uppercase and lowercase letters, and digits

    # Generate a random string of specified length
    random_string = ''.join(random.choice(characters) for i in range(length))

    return random_string

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

async def startbot(secretkey: str):
    check = await mongo.checksecret(secretkey)
    if check['status'] == 200:
        directory_path = "/root/Project/DiscordRadarStore/src"
        os.chdir(directory_path)

        command = f"pm2 start main.py --interpreter=python3 --name {secretkey} -- {secretkey}"
        subprocess.run(command, shell=True, check=True)

        return {'status': 200, 'message': 'Success, try checking your bot now!'}
    else:
        return {'status': 400, 'message': check['message']}
    
async def offbot(secretkey: str):
    check = await mongo.checksecret(secretkey)
    if check['status'] == 200:
        command = f"pm2 delete {secretkey}"
        subprocess.run(f"{command}", shell=True)
        return {'status': 200, 'message': 'Success, try check your bot now!'}
    else:
        return {'status': 400, 'message': check['message']}
    
async def restartbot(secretkey: str):
    check = await mongo.checksecret(secretkey)
    if check['status'] == 200:
        command = f"pm2 restart {secretkey}"
        subprocess.run(f"{command}", shell=True)
        return {'status': 200, 'message': 'Success, try check your bot now!'}
    else:
        return {'status': 400, 'message': check['message']}