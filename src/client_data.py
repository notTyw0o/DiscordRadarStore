from dotenv import load_dotenv
load_dotenv()
import os
import requests
import sys

url = os.getenv("BASE_URL") + '/data'

# JSON data to be sent in the POST request
data = {
    'secretkey': sys.argv[1]
}

response = requests.post(url, json=data)

# Check the response status
try:
    data = response.json()
    SECRET_KEY = data['data']['secretkey']
    TOKEN = data['data']['discordtoken']
    OWNER_ID = data['data']['discordid']
    PRESENCE = data['data']['presence']
    if sys.argv[1] == '1d9e40aecbb863188240a3ea08089c6d':
        HOTMAIL_API = os.getenv('KUNGSAW_HOTMAIL')
    else:
        HOTMAIL_API = os.getenv('HOTMAIL_API')
except:
    print(response.json())
    sys.exit()
    



