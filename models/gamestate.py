from typing import List, Optional
from pydantic import BaseModel
import random


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


class ScoreCard(BaseModel):
    teamScores: List[int]  # [team1Score, team2Score]


class NewGame(BaseModel):
    name: str
    playerHands: Hands       # e.g. [ [d1, d2, ...], [d1, d2, ...] ]
    arena: Arena             # arena.slots[0] = player one’s domino
    scoreCard: ScoreCard
    playerTurn: int          # index of player whose turn it is

    def to_dict(self)->dict:
        return self.model_dump()

class Game(BaseModel):
    id: int
    name: str
    playerHands: Hands       # e.g. [ [d1, d2, ...], [d1, d2, ...] ]
    arena: Arena             # arena.slots[0] = player one’s domino
    scoreCard: ScoreCard
    playerTurn: int          # index of player whose turn it is


def create_empty_hand() -> Hand:
    return [Domino(sideA=0, sideB=0) for _ in range(7)]


def create_initial_game_state(name: str) -> NewGame:
    return NewGame(
        name=name,
        #playerHands=[create_empty_hand() for _ in range(4)],
        playerHands=create_shuffled_hands(),
        arena=Arena(slots=[None, None, None, None]),
        scoreCard=ScoreCard(teamScores=[0, 0]),
        playerTurn=0
    )

def create_shuffled_hands() -> Hands:
    new_stack = ALL_DOMINOES[:]
    random.shuffle(new_stack)

    hands = [[] for _ in range(4)]

    for a in range(4):
        for b in range(7):
            hands[a].append(new_stack.pop())

    return hands
