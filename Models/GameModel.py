import os
from enum import Enum
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import MongoClient
from CustomTypes.PyObjectId import PyObjectId
from Models.DominoRecord import DominoRecord
from Models.HandRecord import HandRecord
from Models.RoundModel import RoundModel
from Models.ScoreCardModel import ScoreCardModel
from gamestate import create_initial_game_state, Domino

Hand = List[DominoRecord]
Hands = List[HandRecord]

class StatusEnum(str, Enum):
    bidding = 'bidding'
    playing = 'playing'
    complete = 'complete'

class Game(BaseModel):
    id: str | Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    currentRoundId: Optional[PyObjectId] = Field(default=None)
    status: StatusEnum
    score: List[int] = Field(default=[0,0])


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
    game = Game(name=game_name, status=StatusEnum.bidding)
    game_doc = game.to_dict()
    if game_doc.get("_id") is None:
        del game_doc["_id"]
    game_id = games.insert_one(game_doc).inserted_id
    game_doc = games.find_one({"_id": game_id})
    game = Game(**game_doc)
    print("This is the game ", game)
    return game_id

def get_game_state_old(game_id: ObjectId):
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

def get_game_state(client: MongoClient, game_id: PyObjectId):
    shoot_the_moon_db = client.ShootTheMoon
    games = shoot_the_moon_db.games
    rounds = shoot_the_moon_db.rounds
    hands_collection =shoot_the_moon_db.hands
    game_doc = games.find_one({"_id": game_id})
    game_name = game_doc.get("name")
    game_status = game_doc.get("status")
    score = game_doc.get("score")
    round_id = game_doc.get("currentRoundId")
    round_doc = rounds.find_one({"_id": round_id})
    round_number = round_doc.get("round_number")
    turn_order = round_doc.get("turn_order")
    current_player_id = round_doc.get("current_player_id")
    dealer = round_doc.get("dealer")
    roundLeader = round_doc.get("roundLeader")
    spade = round_doc.get("spade")
    highestBid = round_doc.get("highestBid")
    winningBid = round_doc.get("winningBid")
    playerTurn = round_doc.get("playerTurn")
    hand_docs = hands_collection.find({"round_id": round_id})
    hand_list = list(hand_docs)
    new_hands: List[Hand] = [[] for _ in range(len(hand_list))]

    for player_number, hand in enumerate(hand_list):
        for domino in hand['dominos']:
            domino.pop('_id', None)  # Safely remove '_id' if it exists
            new_hands[player_number].append(domino)

    print("hand_list: ", hand_list)
    dominos: List[DominoRecord] = []
    print("Dominos: ", str(dominos))
    game_complete = False
    game_state = GameState(
        game_id=str(game_id),
        game_name = game_name,
        game_status = game_status,
        current_round_id=str(round_id),
        current_player_id=current_player_id,
        round_number=round_number,
        arena=dominos,
        turn_order=turn_order,
        hands=new_hands,
        game_complete=game_complete,
        score=score,
        dealer=dealer,
        roundLeader=roundLeader,
        spade=spade,
        highestBid=highestBid,
        winningBid=winningBid,
        playerTurn=playerTurn
    )
    print("game_state: ", game_state)
    return game_state

class GameState(BaseModel):
    game_id: str
    game_name: str
    game_status: StatusEnum
    current_round_id: str
    round_number: int
    current_player_id: int
    arena: List[DominoRecord]
    turn_order: List[int]
    hands: List[Hand]
    game_complete: bool
    score: List[int]
    dealer: int
    roundLeader: int
    spade: int
    highestBid: int
    winningBid: int
    playerTurn: int
