from bot.models import *


#r = Race(marketName="WIN", marketStartTime="10pm", totalMatched=100.2, venue="Ling")
#r.save()

#race = Race.select().where(Race.venue == "Ling").get()

#create_tables()

for r in Race.select():
    print(r.marketId)