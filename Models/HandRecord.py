from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import MongoClient

from CustomTypes.PyObjectId import PyObjectId
from Models.DominoRecord import DominoRecord

class HandRecord(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    game_id: PyObjectId
    round_id: PyObjectId
    dominos: List[DominoRecord]

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True  # Required for ObjectId
        json_encoders = {ObjectId: str}

    def to_dict(self)->dict:
        return self.model_dump(by_alias=True)

    def append(self, item):
        return self.dominos.append(item)

def create_hands(client: MongoClient, game_id: PyObjectId, hand_id: PyObjectId, hands: List[HandRecord]):
    hand_id = 0
    shoot_the_moon_db = client.ShootTheMoon
    hands_collection = shoot_the_moon_db.rounds
    #hand_record = HandRecord(dominos=hands[0])
    hand_doc = hands[0].to_dict()
    print("hands[0].to_dict(): ", hands[0])
    #print("hand_doc: ", hand_doc)
    # if hand_doc.get("_id") is None:
    #     del hand_doc["_id"]
    # hand_id = hands_collection.insert_one(hand_doc).inserted_id
    # print("hand_id ", hand_id)
    return hand_id