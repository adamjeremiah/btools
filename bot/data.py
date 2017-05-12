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
    venue = CharField()
    countryCode = CharField()

    class Meta:
        database = db


class Horse(Model):
    race = ForeignKeyField(Race, related_name="horses")
    selectionId = IntegerField()
    runnerName = CharField()

    class Meta:
        database = db


class Market(Model):
    horse = ForeignKeyField(Horse, related_name="markets")
    time = DateTimeField()
    status = CharField()
    lastPriceTraded = FloatField()
    totalMatched = FloatField()

    class Meta:
        database = db


class AvailableToBack(Model):
    market = ForeignKeyField(Market, related_name="backs")
    price = FloatField()
    size = FloatField()

    class Meta:
        database = db


class AvailableToLay(Model):
    market = ForeignKeyField(Market, related_name="lays")
    price = FloatField()
    size = FloatField()

    class Meta:
        database = db


class TradedVolume(Model):
    market = ForeignKeyField(Market, related_name="volumes")
    price = FloatField()
    size = FloatField()

    class Meta:
        database = db


def add_races(catalogue):
    with db.atomic():
        for c in catalogue:
            try:
                r = Race(marketId=c.market_id,
                                eventId=c.event.id,
                                marketName=c.market_name,
                                marketStartTime=c.market_start_time + datetime.timedelta(hours=1),
                                countryCode=c.event.country_code,
                                venue=c.event.venue)
                r.save(force_insert=True)
            except IntegrityError as ie:
                pass
            try:
                for h in c.runners:
                    rc = Horse(race=r.marketId,
                               selectionId=h.selection_id,
                               runnerName=h.runner_name)

                    rc.save(force_insert=True)
            except IntegrityError as ie:
                pass


def add_prices(marketbook):
    time = datetime.datetime.now()
    with db.atomic():
        for m in marketbook:
            for r in m.runners:
                add = Market(horse=r.selection_id,
                             time=time,
                             status=r.status,
                             lastPriceTraded=r.last_price_traded or 0,
                             totalMatched=r.total_matched or 0)
                add.save()

                id = add.id
                with db.atomic():
                    for l in r.ex.available_to_back:
                        AvailableToBack.create(market=id, size=l.size, price=l.price)
                    for l in r.ex.available_to_back:
                        AvailableToLay.create(market=id, size=l.size, price=l.price)
                    for l in r.ex.available_to_back:
                        TradedVolume.create(market=id, size=l.size, price=l.price)

def get_races(less_than=datetime.timedelta(minutes=60)):
    now = datetime.datetime.now()
    return list(map(lambda x: x.marketId, Race.select().where(now < Race.marketStartTime)))



try:
    db.create_tables([Race, Horse, Market, AvailableToBack, AvailableToLay, TradedVolume])
except OperationalError:
    print("Tables Already setup")