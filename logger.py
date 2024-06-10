# logger.py
from config import DEBUG

def log(message):
    if DEBUG:
        print(message)
