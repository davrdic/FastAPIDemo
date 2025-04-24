import os
from typing import List
from pymongo import MongoClient
from pymongo.collection import Collection
from Models.DominoModel import DominoModel

def get_domino_deck(start: int, count: int) -> List[DominoModel]:
    connection_string = os.getenv("DATABASE_CONNECTION_STRING")
    if not connection_string:
        raise EnvironmentError("Missing DATABASE_CONNECTION_STRING environment variable")

    client = MongoClient(connection_string)
    deck: List[DominoModel] = []

    try:
        db = client["ShootTheMoon"]
        collection: Collection = db["dominos"]
        cursor = collection.find().skip(start).limit(count)
        result = [DominoModel(**doc) for doc in cursor]
        deck.extend(result)
    except Exception as e:
        print(f"[get_domino_deck] Error: {e}")
    finally:
        client.close()

    return deck