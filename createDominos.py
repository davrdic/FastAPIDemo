from pymongo import MongoClient
from typing import List
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Models.DominoModel import DominoModel

ALL_DOMINOES: List[DominoModel] = [
    DominoModel(shortId="standard_" + str(a) + "_" + str(b), highValue=a, lowValue=b, doublet=a == b)
    for a in range(0, 7, 1)
    for b in range(0, a+1, 1)
]
print("ALL_DOMINOES :", ALL_DOMINOES)
client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
domino_id = 0

try:
    db = client.ShootTheMoon
    dominos = db.dominos
    domino_dicts = [d.to_dict() for d in ALL_DOMINOES]
    domino_ids = dominos.insert_many(domino_dicts).inserted_ids
    print("domino_ids: ", domino_ids)
except Exception as e:
    print(f"An error occurred: {e}")
client.close()
print("Client Closed successfully")