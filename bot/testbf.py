import bot.bf
from bot.models import *
import datetime
import os
import time


with open('info', 'r') as file:
    info = file.readline().split(":")
    username = info[0]
    password = info[1]
    appKey = info[2]


bf = bot.bf.Betfair(username, password, appKey=appKey)
bf.login()

print(datetime.datetime.now())
add_races(bf.get_catalogue())
add_prices(bf.get_markets(get_races()[:6]))
print(datetime.datetime.now())
