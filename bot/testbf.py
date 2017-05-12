import bot.bf
from bot.data import *
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


# Get catalogue for the day
bfc = bf.get_catalogue()
# Add markets and horses to DB
add_races(bfc)

#ids = Race.select().where((Race.marketStartTime - datetime.datetime.now()) < 30)
#for i in ids:
#    print(i.marketStartTime)


#add_prices(markets)

now = datetime.datetime.now()
then = datetime.datetime.now() + datetime.timedelta(seconds=5)
while True:
    add_prices(bf.get_markets(get_races()[:6]))
    now = datetime.datetime.now()


## instead of polling and sending to db to add every time.
## poll many times, then do bulk insert every few seconds?



#markets = bf.get_markets(get_races()[:6])
#for m in markets:
#    print(m.json())

#print(get_races())
#store as json instead?

