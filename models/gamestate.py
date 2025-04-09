from typing import List, Optional
from pydantic import BaseModel


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
    hands = [
        [ALL_DOMINOES[0], ALL_DOMINOES[1], ALL_DOMINOES[2], ALL_DOMINOES[3], ALL_DOMINOES[4], ALL_DOMINOES[5], ALL_DOMINOES[6]],
        [ALL_DOMINOES[7], ALL_DOMINOES[8], ALL_DOMINOES[9], ALL_DOMINOES[10], ALL_DOMINOES[11], ALL_DOMINOES[12], ALL_DOMINOES[13]],
        [ALL_DOMINOES[14], ALL_DOMINOES[15], ALL_DOMINOES[16], ALL_DOMINOES[17], ALL_DOMINOES[18], ALL_DOMINOES[19], ALL_DOMINOES[20]],
        [ALL_DOMINOES[21], ALL_DOMINOES[22], ALL_DOMINOES[23], ALL_DOMINOES[24], ALL_DOMINOES[25], ALL_DOMINOES[26], ALL_DOMINOES[27]]
    ]
    return hands
