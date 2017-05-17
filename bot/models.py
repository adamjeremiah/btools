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
    selectionId = IntegerField(primary_key=True)
    runnerName = CharField()

    class Meta:
        database = db
        #primary_key = CompositeKey('race', 'selectionId')
        indexes = ((('race', 'selectionId'), True),)


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
        primary_key = False


class AvailableToLay(Model):
    market = ForeignKeyField(Market, related_name="lays")
    price = FloatField()
    size = FloatField()

    class Meta:
        database = db
        primary_key = False


class TradedVolume(Model):
    market = ForeignKeyField(Market, related_name="volumes")
    price = FloatField()
    size = FloatField()

    class Meta:
        database = db
        primary_key = False


def add_prices(marketbook):
    backs = []
    lays = []
    volumes = []
    now = datetime.datetime.now()
    for d in marketbook:
        with db.atomic():
            for h in d.runners:
                market = Market.create(horse=h.selection_id,
                                       time=now,
                                       status=h.status,
                                       lastPriceTraded=h.last_price_traded or 0.0,
                                       totalMatched=h.total_matched or 0.0)
                market.save()
                for back in h.ex.available_to_back:
                    backs.append({'market': market,
                                  'price': back.price,
                                  'size': back.size})
                for lay in h.ex.available_to_lay:
                    lays.append({'market': market,

                                 'price': lay.price,
                                 'size': lay.size})
                for volume in h.ex.traded_volume:
                    volumes.append({'market': market,
                                    'price': volume.price,
                                    'size': volume.size})

    with db.atomic():
        for bs in range(0, len(backs), 100):
            AvailableToBack.insert_many(backs[bs:bs + 100]).execute()
        for ls in range(0, len(lays), 100):
            AvailableToLay.insert_many(lays[ls:ls + 100]).execute()
        for vs in range(0, len(volumes), 100):
            TradedVolume.insert_many(volumes[vs:vs + 100]).execute()


def get_races(less_than=datetime.timedelta(minutes=60)):
    now = datetime.datetime.now()
    return list(map(lambda x: x.marketId, Race.select().where(now < Race.marketStartTime)))


try:
    db.create_tables([Race, Horse, Market, AvailableToBack, AvailableToLay, TradedVolume])
except OperationalError:
    print("Tables Already setup")


def add_races(catalogue):
    races = []
    horses = []
    for m in catalogue:
        races.append({'marketId': m.market_id,
                      'eventId': m.event.id,
                      'marketName': m.market_name,
                      'marketStartTime': m.market_start_time,
                      'venue': m.event.venue,
                      'countryCode': m.event.country_code})
        for h in m.runners:
            horses.append({'race': m.market_id,
                           'selectionId': h.selection_id,
                           'runnerName': h.runner_name})

    with db.atomic():
        Race.insert_many(races).on_conflict(action='IGNORE').execute()
        for hrs in range(0, len(horses), 100):
            Horse.insert_many(horses[hrs:hrs + 100]).on_conflict(action='IGNORE').execute()
