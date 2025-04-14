import os
import pprint
from typing import List
from pymongo import MongoClient
from Models.DominoRecord import DominoRecord

def get_domino_deck(start: int, count: int) -> List[DominoRecord]:
    book_store_client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    deck = []
    try:
        shoot_the_moon_db = book_store_client.ShootTheMoon
        dominos_collection = shoot_the_moon_db.dominos
        dominos_collection.find()
        cursor = dominos_collection.find().skip(start).limit(count)
        deck = [DominoRecord(**doc) for doc in cursor]
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        book_store_client.close()
        return deck