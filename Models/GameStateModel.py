from typing import List
from pydantic import BaseModel
from pymongo import MongoClient

from CustomTypes.PyObjectId import PyObjectId
from Models.DominoModel import DominoModel
from Models.GameModel import Hand, StatusEnum

class GameState(BaseModel):
    game_id: str
    game_name: str
    game_status: StatusEnum
    current_round_id: str
    round_number: int
    current_player_id: int
    arena: List[DominoModel]
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


def get_game_state(client: MongoClient, game_id: PyObjectId) -> GameState:
    db = client["ShootTheMoon"]
    games = db["games"]
    rounds = db["rounds"]
    hands_collection = db["hands"]

    game_doc = games.find_one({"_id": game_id})
    if not game_doc:
        raise ValueError(f"No game found with id {game_id}")

    game_name = game_doc.get("name")
    game_status = game_doc.get("status")
    score = game_doc.get("score", [0, 0])
    round_id = game_doc.get("currentRoundId")

    round_doc = rounds.find_one({"_id": round_id})
    if not round_doc:
        raise ValueError(f"No round found with id {round_id}")

    round_number = round_doc.get("round_number")
    turn_order = round_doc.get("turn_order")
    current_player_id = round_doc.get("current_player_id")
    dealer = round_doc.get("dealer")
    roundLeader = round_doc.get("roundLeader")
    spade = round_doc.get("spade")
    highestBid = round_doc.get("highestBid")
    winningBid = round_doc.get("winningBid")
    playerTurn = round_doc.get("playerTurn")

    # Arena is a list of DominoModel
    arena_data = round_doc.get("arena", [])
    arena = [DominoModel(**domino) for domino in arena_data]

    # Hands
    hand_docs = hands_collection.find({"round_id": round_id})
    hand_list = list(hand_docs)
    new_hands: List[Hand] = [[] for _ in range(len(hand_list))]

    for player_number, hand in enumerate(hand_list):
        for domino_data in hand.get("dominos", []):
            domino_data.pop("_id", None)
            new_hands[player_number].append(DominoModel(**domino_data))

    return GameState(
        game_id=str(game_id),
        game_name=game_name,
        game_status=game_status,
        current_round_id=str(round_id),
        round_number=round_number,
        current_player_id=current_player_id,
        arena=arena,
        turn_order=turn_order,
        hands=new_hands,
        game_complete=False,  # You might want to dynamically determine this
        score=score,
        dealer=dealer,
        roundLeader=roundLeader,
        spade=spade,
        highestBid=highestBid,
        winningBid=winningBid,
        playerTurn=playerTurn
    )
