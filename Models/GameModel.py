import os

from enum import Enum
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import MongoClient

from CustomTypes.PyObjectId import PyObjectId
from Models.DominoModel import DominoModel
from Models.HandModel import HandModel

Hand = List[DominoModel]
Hands = List[HandModel]


class StatusEnum(str, Enum):
    bidding = "bidding"
    playing = "playing"
    complete = "complete"


class Game(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    currentRoundId: Optional[PyObjectId] = None
    status: StatusEnum
    score: List[int] = Field(default_factory=lambda: [0, 0])

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True)


def create_new_game(game_name: str) -> PyObjectId:
    connection_string = os.getenv("DATABASE_CONNECTION_STRING")
    if not connection_string:
        raise EnvironmentError("Missing DATABASE_CONNECTION_STRING")

    client = MongoClient(connection_string)
    db = client["ShootTheMoon"]
    games = db["games"]

    try:
        game = Game(name=game_name, status=StatusEnum.bidding)
        game_doc = game.to_dict()
        game_doc.pop("_id", None)
        game_id = games.insert_one(game_doc).inserted_id

        game_doc = games.find_one({"_id": game_id})
        game = Game(**game_doc)
        print("Created game:", game)
        return game_id
    finally:
        client.close()


def update_current_round(client: MongoClient, game_id: PyObjectId, round_id: PyObjectId):
    db = client["ShootTheMoon"]
    games = db["games"]
    result = games.update_one({"_id": game_id}, {"$set": {"currentRoundId": round_id}})
    return result