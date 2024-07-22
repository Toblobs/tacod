# __init__.py // @toblobs


# third party library imports
import numpy as np
import asyncio
import disnake
from datetime import datetime, timezone
PYTHONASYNCIODEBUG = 1


# constants and settings
__version__ = '1.0'
__stampdate__ = '.0'
LED_DIMENSIONS = (7, 5)
COMPLETED_CAPTCHAS_COUNTER = 0
BOT_TOKEN = open('token.txt', 'r').read().strip()
GUILD = 1138065389163659314