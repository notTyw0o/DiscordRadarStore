from dotenv import load_dotenv
load_dotenv()
import os
import requests
import sys

url = os.getenv("BASE_URL") + '/data'

# JSON data to be sent in the POST request
data = {
    'secretkey': os.getenv('SECRET_KEY')
}

response = requests.post(url, json=data)

# Check the response status
try:
    data = response.json()
    SECRET_KEY = data['data']['secretkey']
    TOKEN = data['data']['discordtoken']
    OWNER_ID = data['data']['discordid']
    PRESENCE = data['data']['presence']
except:
    print(data['message'])
    sys.exit(1)
    



