import requests
from dotenv import load_dotenv
load_dotenv()
import os

import requests

# URL where you want to send the POST request
url = os.getenv("BASE_URL") + '/data'

# JSON data to be sent in the POST request
data = {
    'key1': 'value1',
    'key2': 'value2'
}

# Make the POST request with JSON data
response = requests.post(url, json=data)

# Check the response status
if response.status_code == 200:  # 200 means success
    print("POST request successful")
    print("Response:", response.json())  # Print the JSON response content
else:
    print("POST request failed")
