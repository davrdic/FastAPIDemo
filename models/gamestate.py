from pydantic import BaseModel

# Models
class Domino(BaseModel):
    side_a: int
    side_b: int

    def to_dict(self):
        return {"side_a": self.side_a, "side_b": self.side_b}


class Hand(BaseModel):
    domino_one: Domino
    domino_two: Domino

    def to_dict(self):
        return {
            "domino_one": self.domino_one.to_dict(),
            "domino_two": self.domino_two.to_dict()
        }

class UpdateData(BaseModel):
    player: str
    score: int

class Item(BaseModel):
    id : str

class NewGame(BaseModel):
    name: str

    def to_dict(self):
        return {
            "name": self.name
        }

class Game(BaseModel):
    id : int
    newGame : NewGame