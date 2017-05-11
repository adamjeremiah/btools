from peewee import *
import os
import datetime


db = SqliteDatabase('testData.db')
db.connect()


class Race(Model):
    marketId = FloatField(primary_key=True)
    eventId = IntegerField()
    marketName = CharField()
    marketStartTime = DateTimeField()
    # totalMatched = FloatField() # Don't need as I'll capture this when checking prices
    venue = CharField()
    countryCode = CharField()

    class Meta:
        database = db


class Market(Model):
    race = ForeignKeyField(Race, related_name="markets")
    time = DateTimeField()
    status = CharField()
    numberOfRunners = IntegerField()
    lastMatchTime = DateTimeField()
    totalMatched = FloatField()
    totalAvailable = FloatField()

    class Meta:
        database = db


class Horse(Model):
    race = ForeignKeyField(Race, related_name="horses")
    selectionId = IntegerField(primary_key=True)
    runnerName = CharField()

    class Meta:
        database = db


class Price(Model):
    horse = ForeignKeyField(Horse, related_name="prices")
    timeStamp = TimeField()
    lastPriceTraded = FloatField()
    totalMatched = FloatField

    class Meta:
        database = db


def add_races(catalogue):
    for c in catalogue:
        try:
            r=Race.create(marketId=c.market_id,
                        eventId=c.event.id,
                        marketName=c.market_name,
                        marketStartTime=c.market_start_time,
                        countryCode=c.event.country_code,
                        venue=c.event.venue)
        except IntegrityError:
            pass

        for h in c.runners:
            try:
                Horse.create(race_id=c.market_id,
                             selectionId=h.selection_id,
                             runnerName=h.runner_name)
            except IntegrityError:
                pass

def add_prices(marketbook):
    for m in marketbook:
        Market.create(race_id=m.market_id,
                      time=datetime.datetime.now(),
                      status=m.status,
                      numberOfRunners=m.number_of_active_runners,
                      lastMatchTime=m.last_match_time,
                      totalMatched=m.total_matched,
                      totalAvailable=m.total_available)

try:
    db.create_tables([Race, Horse, Market, Price])
except OperationalError:
    print("Tables Already setup")