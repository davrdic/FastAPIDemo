from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

from CustomTypes.PyObjectId import PyObjectId

class DominoModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    shortId: str
    highValue: int
    lowValue: int
    doublet: bool

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True  # allows both `id` and `_id` usage

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True)

    def pop_to_dict(self) -> dict:
        data = self.to_dict()
        data.pop("_id", None)
        return data
