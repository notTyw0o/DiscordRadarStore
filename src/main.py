from bot import startBot
from mongo import mongoConnect

if __name__ == "__main__":
    startBot()
    mongoConnect()