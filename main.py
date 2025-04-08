import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
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
    print('game_state: ', item)
    return item

@app.post("/create_game/")
async def create_game(domino: Domino):
    print("create_game:", domino.side_a, domino.side_b)
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    post_id = 0
    try:
        db = client.BookStore
        posts = db.posts
        post_id = posts.insert_one(domino.to_dict()).inserted_id
        print("post_id: ", post_id)
    except Exception as e:
        print(f"An error occurred: {e}")
    client.close()
    print("Client Closed successfully")

    #return {"received": str(post_id) if post_id else None}
    return str(f"create_game: {post_id}")

@app.put("/update_game/{game_id}")
def update_game(game_id: str, updated_data: UpdateData):
    print(f"update_game: {game_id} {UpdateData}")
    return {f"update_game: {game_id} {updated_data}"}

@app.delete("/delete_game/{game_id}")
def delete_game(game_id: str):
    # Logic to delete the game using the game_id
    print(f"delete_game: {game_id}")
    return {f"delete_game: {game_id}"}

