from peewee import *
import datetime

db = SqliteDatabase('games.db')

class BaseModel(Model):
    class Meta:
        database = db
    date_created = DateTimeField(default=datetime.datetime.now)
    id = PrimaryKeyField()

class Player(BaseModel):
    name = CharField()
    room_id = IntegerField(null=True)
    order_in_room = IntegerField(default=0)
    score = IntegerField(default=0)
    has_voted = BooleanField(default=False)
    is_leader = BooleanField(default=False)

class Room(BaseModel):
    code = CharField(unique=True)
    owner = ForeignKeyField(Player, related_name='owner_of')
    leader = ForeignKeyField(Player, related_name='leader_of', null=True)
    num_players = IntegerField(default=0)
    round_num = IntegerField(default=0)
    prompt = CharField(null=True)
    votes = IntegerField(default=0)

class Submission(BaseModel):
    text = CharField()
    author = ForeignKeyField(Player)
    room = ForeignKeyField(Room)
    show_auth = BooleanField(default=False)
    randomizer = FloatField()
    votes = IntegerField(default=0)
    round_num = IntegerField()

class Vote(BaseModel):
    room = ForeignKeyField(Room)
    voter = ForeignKeyField(Player, related_name='voted_for')
    submission = ForeignKeyField(Submission, related_name='voted_for_by')
    round_num = IntegerField()

def initialize_db():
    db.connect()
    db.create_tables([Player, Room, Submission, Vote], safe=True)