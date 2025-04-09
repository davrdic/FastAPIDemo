import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv
from models.gamestate import Domino, UpdateData, NewGame

# Load environment variables from .env file
load_dotenv()

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

@app.get("/find_game_by_name/{name}")
def find_game_by_name(name: str):
    print('find_game_by_name: ', name)
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    game = any

    try:
        db = client["ShootTheMoon"]
        games = db["games"]
        game = games.find_one({"name": name})
        print("Game found: ", game)
    except Exception as e:
        print(f"An error occurred: {e}")
    client.close()
    print("Client Closed successfully")

    if game and '_id' in game:
        game['id'] = str(game['_id'])
        del game['_id']

    return game

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

@app.post("/create_game_by_name/{game_name}")
async def create_game_by_name(game_name: str):
    print(" POST create_game_by_name: ", game_name)
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    post_id = 0
    game = NewGame(name=game_name)
    try:
        db = client.ShootTheMoon
        games = db.games
        post_id = games.insert_one(game.to_dict()).inserted_id
        print("post_id: ", post_id)
    except Exception as e:
        print(f"An error occurred: {e}")
    client.close()
    return str(f"POST COMPLETE create_game_by_name: {post_id}")

@app.put("/update_game/{game_id}")
def update_game(game_id: str, updated_data: UpdateData):
    print(f"update_game: {game_id} {UpdateData}")
    return {f"update_game: {game_id} {updated_data}"}

@app.delete("/delete_game/{game_id}")
def delete_game(game_id: str):
    # Logic to delete the game using the game_id
    print(f"delete_game: {game_id}")
    return {f"delete_game: {game_id}"}

