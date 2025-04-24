from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import MongoClient

from CustomTypes.PyObjectId import PyObjectId
from Models.DominoModel import DominoModel

class RoundModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    game_id: PyObjectId
    round_number: int = 1
    arena: List[DominoModel] = Field(default_factory=list)
    turn_order: List[int] = Field(default_factory=lambda: [0, 1, 2, 3])
    current_player_id: int = 0
    dealer: int = 0
    roundLeader: int = -1
    spade: int = -1
    highestBid: int = 0
    winningBid: int = 0
    playerTurn: int = 0

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True)

    def append_to_arena(self, domino: DominoModel):
        self.arena.append(domino)


def create_round(client: MongoClient, game_id: PyObjectId) -> PyObjectId:
    db = client["ShootTheMoon"]
    collection = db["rounds"]
    round_record = RoundModel(game_id=game_id)
    round_doc = round_record.to_dict()

    round_doc.pop("_id", None)  # Safely remove if present

    round_id = collection.insert_one(round_doc).inserted_id
    print("Created round:", round_id)
    return round_id