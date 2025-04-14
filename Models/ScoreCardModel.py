import os
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import MongoClient
from CustomTypes.PyObjectId import PyObjectId

class ScoreCardModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    teamScores: Optional[List[int]] = None

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True  # Required for ObjectId
        json_encoders = {ObjectId: str}

    def to_dict(self)->dict:
        return self.model_dump()

def create_initial_scorecard():
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    db = client.ShootTheMoon
    score_cards = db.scoreCards
    score_card = ScoreCardModel()
    score_card_id = score_cards.insert_one(score_card.to_dict()).inserted_id
    score_card_doc = score_cards.find_one({"_id": score_card_id})
    score_card = ScoreCardModel(**score_card_doc)
    return score_card
