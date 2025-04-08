import json
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from os import getenv

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Models
class Domino(BaseModel):
    side_a: int
    side_b: int

    def to_dict(self):
        return {"side_a": self.side_a, "side_b": self.side_b}


class Hand(BaseModel):
    domino_one: Domino
    domino_two: Domino

    def to_dict(self):
        return {
            "domino_one": self.domino_one.to_dict(),
            "domino_two": self.domino_two.to_dict()
        }

class UpdateData(BaseModel):
    player: str
    score: int

class Item(BaseModel):
    id : str

class GameInfo(BaseModel):
    player_one_hand: Hand
    player_two_hand: Hand


# FastAPI app setup
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domain(s) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/")
def home():
    return {"message": "Domino game server running!"}

@app.get("/game_state/{item}")
def game_state(item: str):
    print('item: ', item)
    return item
    # example_state = {
    #     "d_one": {"side_a": 1, "side_b": 1},
    #     "d_two": {"side_a": 2, "side_b": 2}
    # }
    # return {
    #     "date": "2025-04-04",
    #     "temperatureC": 51,
    #     "temperatureF": 123,
    #     "summary": "Freezing",
    #     "domino": json.dumps(example_state)
    # }


@app.post("/create_game/")
async def create_game(domino: Domino):
    print("Received:", domino.side_a, domino.side_b)
    print(getenv("DATABASE_CONNECTION_STRING"))
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    post_id = 0
    try:
        client.admin.command('ping')
        db = client.BookStore
    #     collection = db.Books
    #     # post = {
    #     #     "author": "Mike",
    #     #     "text": "My first blog post!",
    #     #     "tags": ["mongodb", "python", "pymongo"],
    #     #     "date": datetime.datetime.now(tz=datetime.timezone.utc)
    #     # }
        posts = db.posts
    #     #str_result = str(GameInfo)
    #     #print("str_result" + str_result)
    #     #print("str_result: " + str_result)
        post_id = posts.insert_one(domino.to_dict()).inserted_id
    #     pprint.pprint(posts.find_one())
        print("post_id: ", post_id)
    except Exception as e:
        print(f"An error occurred: {e}")
    client.close()
    print("Client Closed successfully")

    #return {"received": str(post_id) if post_id else None}
    return str(post_id)

# Optional: If you want a placeholder for bad requests or form data testing
@app.post("/create_game_bad")
async def create_game_bad(request: Request):
    return {"message": "This route is not implemented yet"}

@app.put("/update_game/{game_id}")
def update_game(game_id: str, updated_data: UpdateData):
    return {"message": f"Game {game_id} updated", "data": updated_data}

@app.delete("/delete_game/{game_id}")
def delete_game(game_id: str):
    # Logic to delete the game using the game_id
    print(f"Deleting game with ID: {game_id}")
    return {"message": f"Game {game_id} updated"}

    # Example: Delete the game from the database or any other storage
    # try:
    #     client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    #     db = client.BookStore  # Use your actual database name
    #     posts = db.posts
    #     result = posts.delete_one({"_id": game_id})  # Assuming game_id is the _id in MongoDB
    #     if result.deleted_count > 0:
    #         return {"message": f"Game {game_id} deleted successfully."}
    #     else:
    #         return {"message": f"Game {game_id} not found."}
    # except Exception as e:
    #     print(f"Error deleting game: {e}")
    #     return {"message": "Error occurred while deleting the game."}
    # finally:
    #     client.close()

