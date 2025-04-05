import json
import os
import datetime
import pprint

from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Union
from pydantic import BaseModel
from starlette.requests import Request


class Domino:
    def __init__(self, sida_a, side_b):
        self.side_a = sida_a
        self.side_b = side_b

domino = Domino(1, 2)

class GameInfo(BaseModel):
    player_one_hand : str

# client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
#
# try:
#     client.admin.command('ping')
#     db = client.BookStore
#     collection = db.Books
#     post = {
#         "author": "Mike",
#         "text": "My first blog post!",
#         "tags": ["mongodb", "python", "pymongo"],
#         "date": datetime.datetime.now(tz=datetime.timezone.utc)
#     }
#     posts = db.posts
#     post_id = posts.insert_one(post).inserted_id
#     pprint.pprint(posts.find_one())
#     print("Connected to MongoDB successfully!")
# except Exception as e:
#     print(f"An error occurred: {e}")
#
# client.close()

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {'data': 'Hello world'}

@app.get("/game_state")
def game_state():
    x = {
        'd_one': {
            "side_a": 1,
            "side_b": 1
        },
        'd_two': {
            "side_a": 2,
            "side_b": 2
        }
    }
    #anotherx = '{"d_one": {"side_a": 1, "side_b": 1}, "d_two": {"side_a": 2, "side_b": 2}}'
    xstring = json.dumps(x)
    #print("xstring: " + xstring)
    return (

            {"date": "2025-04-04", "temperatureC": 51, "temperatureF": 123, "summary": "Freezing", "domino": xstring}
    )

@app.post("/create_game")
async def create_game(request: Request):
    print("Success")
    data = await request.json()
    print(data)
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    try:
        db = client.BookStore
        posts = db.posts
        post_id = posts.insert_one(data).inserted_id
        print(post_id)
    except Exception as e:
        print(f"An error occurred: {e}")
    return

@app.post("/create_game_bad")
def create_game_bad(game_info : GameInfo):
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))

    try:
        client.admin.command('ping')
        db = client.BookStore
        collection = db.Books
        # post = {
        #     "author": "Mike",
        #     "text": "My first blog post!",
        #     "tags": ["mongodb", "python", "pymongo"],
        #     "date": datetime.datetime.now(tz=datetime.timezone.utc)
        # }
        posts = db.posts
        #str_result = str(GameInfo)
        #print("str_result" + str_result)
        #print("str_result: " + str_result)
        #post_id = posts.insert_one(str(GameInfo)).inserted_id
        #pprint.pprint(posts.find_one())
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

    client.close()
    return game_info