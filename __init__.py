# __init__.py // @toblobs

# standard library imports
import asyncio
from datetime import datetime, timezone
import sqlite3

# third party library imports
import numpy as np
import disnake

# constants and settings
__version__ = '1.0'
__stampdate__ = '.2'

LED_DIMENSIONS = (7, 5)

BOT_TOKEN = open('token.txt', 'r').read().strip()
GUILD = 1138065389163659314
CHANNEL = 1225736218910785586

PYTHONASYNCIODEBUG = 1
DATABASE_FILE = 'data.db'