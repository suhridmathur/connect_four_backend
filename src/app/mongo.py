from django.conf import settings

from pymongo.mongo_client import MongoClient

from rest_framework.exceptions import ValidationError


def connect_mongo():
    """
    Establishing connection with mongodb
    """
    database = settings.MONGO_SETTINGS["DB_NAME"]
    host = settings.MONGO_SETTINGS["HOST"]
    port = int(settings.MONGO_SETTINGS["PORT"])
    user = settings.MONGO_SETTINGS["USER"]
    password = settings.MONGO_SETTINGS["PASSWORD"]
    client = MongoClient(host, port)
    db = client[database]
    if bool(user):
        db.authenticate(user, password)
    return db


class MoveService:
    """
    Service used for dealing with moves of a particular game
    {
        "_id" : ObjectId(<object_id>),
        "token": "<token>",
        "player_one": [5, 1, 2, 9],
        "player_two": [5, 1, 2, 9],
    }
    """

    COLLECTION_NAME = "moves"

    def __init__(self):
        self._db = connect_mongo()
        self._collection = self._db[self.COLLECTION_NAME]

    def update(self, token, data_dict):
        self._collection.update({"token": token}, data_dict)

    def insert(self, data_dict):
        self._collection.insert_one(data_dict)

    def get_moves(self, token):
        moves = self._collection.find_one({"token": token})
        if moves:
            return dict(moves)
        raise ValidationError("Invalid Token")


class BoardService:
    """
    Service used for dealing with moves of a particular game
    {
        "_id" : ObjectId(<object_id>),
        "token": "<token>",
        "player_one": [5, 1, 2, 9],
        "player_two": [5, 1, 2, 9],
    }
    """

    COLLECTION_NAME = "game_board"

    def __init__(self):
        self._db = connect_mongo()
        self._collection = self._db[self.COLLECTION_NAME]

    def update(self, token, data_dict):
        self._collection.update({"token": token}, data_dict)

    def insert(self, data_dict):
        self._collection.insert_one(data_dict)

    def get_board(self, token):
        board = self._collection.find_one({"token": token})
        if board:
            return dict(self._collection.find_one({"token": token}))
        raise ValidationError("Invalid Token")
