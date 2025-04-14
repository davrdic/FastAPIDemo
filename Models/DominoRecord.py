from typing import Optional, Annotated, List
from bson import ObjectId
from pydantic import BaseModel, Field, BeforeValidator
from CustomTypes.PyObjectId import PyObjectId

class DominoRecord(BaseModel):
    id: str | Optional[PyObjectId] = Field(alias="_id", default=None)
    shortId: str
    highValue: int
    lowValue: int
    doublet: bool

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True  # Required for ObjectId
        json_encoders = {ObjectId: str}

    def to_dict(self)->dict:
        return self.model_dump()

    def pop_to_dict(self):
        self.to_dict()
        return self.pop()