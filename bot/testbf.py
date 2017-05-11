import bot.bf
from bot.data import *
import os


with open('info', 'r') as file:
    info = file.readline().split(":")
    username = info[0]
    password = info[1]
    appKey = info[2]


bf = bot.bf.Betfair(username, password, appKey=appKey)
bf.login()



bfc = bf.get_catalogue()


add_races(bfc)

i=0
while (i < 10):
    m = bf.get_markets(['1.131576043', '1.131576048', '1.131576053', '1.131597957'])
    add_prices(m)
    i += 1

