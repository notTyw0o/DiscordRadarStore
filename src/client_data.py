from dotenv import load_dotenv
load_dotenv()
import os
import hashlib

SECRET = os.getenv("OWNER_ID") + os.getenv("OWNER_PASSWORD")
hash_object = hashlib.md5()
hash_object.update(SECRET.encode('utf-8'))

SECRET_KEY = hash_object.hexdigest()
TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
