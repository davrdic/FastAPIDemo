import os
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import MongoClient
from CustomTypes.PyObjectId import PyObjectId
from Models.HandRecord import HandRecord
from Models.ScoreCardModel import ScoreCardModel
from gamestate import create_initial_game_state, Domino

Hands = List[HandRecord]

class Game(BaseModel):
    id: str | Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    currentRoundId: Optional[PyObjectId] = Field(default=None)


    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True  # Required for ObjectId
        json_encoders = {ObjectId: str}

    def to_dict(self)->dict:
        return self.model_dump(by_alias=True)

def create_new_game(game_name: str):
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    db = client.ShootTheMoon
    games = db.games
    game = Game(name=game_name)
    game_doc = game.to_dict()
    if game_doc.get("_id") is None:
        del game_doc["_id"]
    game_id = games.insert_one(game_doc).inserted_id
    game_doc = games.find_one({"_id": game_id})
    game = Game(**game_doc)
    print("This is the game ", game)
    return game_id

def get_game_state(game_id: ObjectId):
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    db = client.ShootTheMoon
    games = db.games
    game_doc = games.find_one({"_id": game_id})
    game = Game(**game_doc)
    return

def update_current_round(client: MongoClient, game_id: PyObjectId, round_id: PyObjectId):
    update_data = {
        "currentRoundId": round_id
    }
    shoot_the_moon_db = client.ShootTheMoon
    games = shoot_the_moon_db.games
    result = games.update_one({"_id": game_id}, {"$set": update_data})
    return result

class GameState(BaseModel):
    gameId: str
    gameName: str
    gameComplete: bool