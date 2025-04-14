import os
import random

from pymongo import MongoClient

from CustomTypes.PyObjectId import PyObjectId
from Models.DominoRecord import DominoRecord
from typing import List

from Models.HandRecord import HandRecord

Hand = List[DominoRecord]
Hands = List[HandRecord]

def deal_dominos(deck: List[DominoRecord], game_id: PyObjectId, round_id: PyObjectId):
    random.shuffle(deck)
    hands: List[HandRecord] = [HandRecord(game_id=game_id, round_id=round_id, dominos=[]) for _ in range(4)]
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    db = client.ShootTheMoon
    hands_collection = db.hands
    hand_ids: List[int] = []

    for a in range(4):
        asdf: List[DominoRecord] = []
        for b in range(7):
            what = deck.pop()
            what.to_dict()
            #what.id = str(what.id)
            #print("what: ", what)
            hands[a].append(what)
            asdf.append(what)
        hand = HandRecord(game_id=game_id, round_id=round_id, dominos=hands[a].dominos)
        hand_doc = hand.to_dict()
        if hand_doc.get("_id") is None:
            del hand_doc["_id"]
        hand_id = hands_collection.insert_one(hand_doc).inserted_id
        #hands[a].id=str(hand_id)
        hands[a].id = hand_id
        hand_ids.append(hand_id)
    return hand_ids