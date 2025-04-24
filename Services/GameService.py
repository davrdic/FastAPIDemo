import os
import random

from typing import List
from pymongo import MongoClient
from pymongo.collection import Collection

from CustomTypes.PyObjectId import PyObjectId
from Models.DominoModel import DominoModel
from Models.HandModel import HandModel

def deal_dominos(deck: List[DominoModel], game_id: PyObjectId, round_id: PyObjectId) -> List[PyObjectId]:
    random.shuffle(deck)

    hands: List[HandModel] = [HandModel(game_id=game_id, round_id=round_id, dominos=[]) for _ in range(4)]
    hand_ids: List[PyObjectId] = []

    connection_string = os.getenv("DATABASE_CONNECTION_STRING")
    if not connection_string:
        raise EnvironmentError("Missing DATABASE_CONNECTION_STRING")

    client = MongoClient(connection_string)
    db = client["ShootTheMoon"]
    hands_collection: Collection = db["hands"]

    try:
        for i in range(4):
            # Draw 7 dominos per hand
            for _ in range(7):
                domino = deck.pop()
                hands[i].append(domino)

            hand_doc = hands[i].to_dict()
            hand_doc.pop("_id", None)  # Remove _id if it's None

            inserted_id = hands_collection.insert_one(hand_doc).inserted_id
            hands[i].id = inserted_id
            hand_ids.append(inserted_id)

    except Exception as e:
        print(f"[deal_dominos] Error: {e}")

    finally:
        client.close()

    return hand_ids