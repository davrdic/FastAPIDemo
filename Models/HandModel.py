from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field

from CustomTypes.PyObjectId import PyObjectId
from Models.DominoModel import DominoModel


class HandModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    game_id: PyObjectId
    round_id: PyObjectId
    dominos: List[DominoModel]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True)

    def append(self, item: DominoModel):
        self.dominos.append(item)