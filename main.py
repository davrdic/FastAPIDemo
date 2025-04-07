import json
import os
import datetime
import pprint

from fastapi.encoders import jsonable_encoder
#import python_multipart

#from python_multipart import parse_form
from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Union
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware


# class Domino:
#     def __init__(self, sida_a, side_b):
#         self.side_a = sida_a
#         self.side_b = side_b

#domino = Domino(1, 2)



class Domino(BaseModel):
    side_a : int
    side_b : int
    def to_dict(self):
        return {"side_a": self.side_a, "side_b": self.side_b}


class Hand(Domino):
    domino_one : Domino
    domino_two : Domino
    def to_dict(self):
        return {self.domino_one.to_dict(), self.domino_two.to_dict()}

class GameInfo(BaseModel):
    player_one_hand : Hand
    player_two_hand : Hand

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {'data': 'Hello world'}

@app.get("/game_state")
def game_state():
    # myDomino = Domino
    # print("myDomino: " + (myDomino.side_a))
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

@app.post("/create_game_bad")
async def create_game_bad(request: Request):
    #print(json.dumps(request))
    # print(data)
    return
    #print("Data: " + json.loads(data))
    # client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    # try:
    #     db = client.BookStore
    #     posts = db.posts
    #     post_id = posts.insert_one(data).inserted_id
    #     print(post_id)
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #return

class Item(BaseModel):
    key1: str
    key2: str

@app.post("/create_game/")
async def create_game(domino: Domino):
    print("hello")
    print("Received move: ", domino.side_b)
    return {"received": domino}
    #data = await request.json()
    # print(data)
    # client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    #
    # try:
    #     client.admin.command('ping')
    #     db = client.BookStore
    #     collection = db.Books
    #     # post = {
    #     #     "author": "Mike",
    #     #     "text": "My first blog post!",
    #     #     "tags": ["mongodb", "python", "pymongo"],
    #     #     "date": datetime.datetime.now(tz=datetime.timezone.utc)
    #     # }
    #     posts = db.posts
    #     #str_result = str(GameInfo)
    #     #print("str_result" + str_result)
    #     #print("str_result: " + str_result)
    #     #post_id = posts.insert_one(game_info.to_dict()).inserted_id
    #     pprint.pprint(posts.find_one())
    #     print("Connected to MongoDB successfully!")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #
    # client.close()
    # print("Post Success")