from peewee import *


class Data:
    db = SqliteDatabase('testData.db')

    def __init__(self):
        self.db.connect()

    class Race(Model):
        marketId = PrimaryKeyField()
        markedName = CharField()
        marketStartTime = CharField()
        totalMatched = FloatField()
        venue = CharField()

        class Meta:
            database = Data.db

    class Horse(Model):
        marketId = ForeignKeyField(Data.Race, related_name="horses")
        selectionID = PrimaryKeyField()
        runnerName = CharField()

        class Meta:
            database = Data.db

    class Price(Model):
        selectionID = ForeignKeyField(Data.Horse, related_name="prices")
        timeStamp = TimeField()
        lastPriceTraded = FloatField()
        totalMatched = FloatField



    class Market(Model):
        marketID = ForeignKeyField(Data.Race, related_name="markets")
        totalMatched = FloatField()
        timeStamp = TimeField()
        lastMatchTime = CharField()
        totalAvailable = FloatField()
