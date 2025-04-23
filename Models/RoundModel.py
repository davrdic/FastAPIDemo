from email.policy import default
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import MongoClient

from CustomTypes.PyObjectId import PyObjectId
from Models.DominoRecord import DominoRecord

class RoundModel(BaseModel):
    id: str | Optional[PyObjectId] = Field(alias="_id", default=None)
    game_id: str | PyObjectId
    round_number: int = Field(default=1)
    arena: List[DominoRecord] = Field(default=[])
    turn_order: List[int] = Field(default=[0, 1, 2, 3])
    current_player_id: int = Field(default=0)
    dealer: int = Field(default=0)
    roundLeader: int = Field(default=-1)
    spade: int = Field(default=-1)
    highestBid: int = Field(default=0)
    winningBid: int = Field(default=0)
    playerTurn: int = Field(default=0)

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True  # Required for ObjectId
        json_encoders = {ObjectId: str}

    def to_dict(self)->dict:
        return self.model_dump(by_alias=True)

    def append(self, item):
        return self.dominos.append(item)

def create_round(client: MongoClient, game_id: PyObjectId):
    shoot_the_moon_db = client.ShootTheMoon
    rounds_collection = shoot_the_moon_db.rounds
    round_record = RoundModel(game_id=game_id)
    round_doc = round_record.to_dict()
    print("round_doc: ", round_doc)
    if round_doc.get("_id") is None:
        del round_doc["_id"]
    round_id = rounds_collection.insert_one(round_doc).inserted_id
    print("round_id ", round_id)
    return round_id