from peewee import *

db = SqliteDatabase('outsera_test.db')


class BaseModel(Model):
    class Meta:
        database = db


class Producer(BaseModel):
    name = CharField(max_length=200, unique=True, null=False)


class Studio(BaseModel):
    name = CharField(max_length=200, unique=True, null=False)


class Movie(BaseModel):
    movie_name = CharField(max_length=200, null=False)
    year = IntegerField(null=False)
    bool_winner = BooleanField(null=False)

    class Meta:
        indexes = (
            (('movie_name', 'year'), True),
        )


class MovieProducer(BaseModel):
    movie = ForeignKeyField(Movie, null=False, backref='film_award_producer')
    producer = ForeignKeyField(Producer, null=False, backref='film_award_producer')


class MovieStudio(BaseModel):
    movie = ForeignKeyField(Movie, null=False, backref='film_award_studio')
    studio = ForeignKeyField(Studio, null=False, backref='film_award_studio')


db.connect()
db.create_tables([Producer, Studio, Movie, MovieProducer, MovieStudio])
