from pymongo import MongoClient
from typing import List
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from Models.DominoRecord import DominoRecord

# domino = Domino(
#     shortId=00,
#     lowValue=0,
#     highValue=0,
#     doublet=True,
# )

# Hand = List[Domino]
# hand = [domino, domino]

# print("create_hand:", hand)
# client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
# hand_id = 0
# try:
#     db = client.ShootTheMoon
#     hands = db.hands
#     hand_dicts = [d.model_dump() for d in hand]
#     hand_id = hands.insert_one({"dominos": hand_dicts}).inserted_id
#     print("hand_id: ", hand_id)
# except Exception as e:
#     print(f"An error occurred: {e}")
# client.close()
# print("Client Closed successfully")

ALL_DOMINOES: List[DominoRecord] = [
    DominoRecord(shortId="standard_" + str(a) + "_" + str(b), highValue=a, lowValue=b, doublet=a == b)
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