from typing import List, Optional
from pydantic import BaseModel
import random
from bson import ObjectId

class Domino(BaseModel):
    sideA: int
    sideB: int

# Static list of all dominoes in a double-six set (highest to lowest)
ALL_DOMINOES: List[Domino] = [
    Domino(sideA=a, sideB=b)
    for a in range(6, -1, -1)
    for b in range(a, -1, -1)
]

Hand = List[Optional[Domino]]
Hands = List[Hand]


class Arena(BaseModel):
    slots: List[Optional[Domino]]  # Index 0 = Player One, 1 = Player Two, etc.

    def to_dict(self)->dict:
        return self.model_dump()


class ScoreCard(BaseModel):
    teamScores: List[int]  # [team1Score, team2Score]

class NewGame(BaseModel):
    name: str
    playerHands: Hands       # e.g. [ [d1, d2, ...], [d1, d2, ...] ]
    scoreCard: ScoreCard

    def to_dict(self)->dict:
        return self.model_dump()

def create_new_round(game_id: ObjectId):
    print('create_new_round: Start - game_id: ', game_id)
    new_round_doc = {}
    try:
        game_id = ObjectId(game_id)
        new_round_doc = {
            "gameId":game_id,
            "dealer":-1,
            "bid":-1,
            "winningBid":-1,
            "spade":-1,
            "arena":Arena(slots=[None, None, None, None]).to_dict()
        }

    except Exception as e:
        print(f"An error occurred: {e}")

    print('createcreate_new_round: Finish - game_id: ', game_id)
    return new_round_doc

class GameState(BaseModel):
    name: str
    dealer: int
    roundLeader: int
    spade: int
    bid: int
    biddingRound: bool
    bidWinner: int
    playerHands: Hands       # e.g. [ [d1, d2, ...], [d1, d2, ...] ]
    arena: Arena             # arena.slots[0] = player one’s domino
    scoreCard: ScoreCard
    playerTurn: int          # index of player whose turn it is


def create_empty_hand() -> Hand:
    return [Domino(sideA=0, sideB=0) for _ in range(7)]


def create_initial_game_state(name: str) -> NewGame:
    return NewGame(
        name=name,
        playerHands=create_shuffled_hands(),
        scoreCard=ScoreCard(teamScores=[0, 0]),
    )

def create_shuffled_hands() -> Hands:
    new_stack = ALL_DOMINOES[:]
    random.shuffle(new_stack)

    hands = [[] for _ in range(4)]

    for a in range(4):
        for b in range(7):
            hands[a].append(new_stack.pop())

    return hands
