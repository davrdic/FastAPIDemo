import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv

from Models.GameModel import create_new_game, get_game_state_old, update_current_round, get_game_state
from Models.HandRecord import create_hands
from MongoRepositories.DominoRepository import get_domino_deck
from gameService import deal_dominos
from gamestate import Domino
from Models.RoundModel import create_round

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

# @app.get("/game_state/{item}")
# def game_state(item: str):
#     print('game_state: ', item)
#     return item

@app.get("/find_game_by_name/{name}")
def find_game_by_name(name: str):
    print('find_game_by_name: ', name)
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    game = any
    game_state = any

    try:
        db = client["ShootTheMoon"]
        games = db["games"]
        game = games.find_one({"name": name})
        print("Game found: ", game)
    except Exception as e:
        print(f"An error occurred: {e}")
    game_id = game['_id']
    # if game and '_id' in game:
    #     game['id'] = str(game['_id'])
    #     del game['_id']
    # if game and 'currentRoundId' in game:
    #     game['currentRoundIdString'] = str(game['currentRoundId'])
    #     del game['currentRoundId']
    if game_id:
        game_state = get_game_state(client, game_id)
    client.close()
    print("Client Closed successfully")
    return game_state

@app.get("/find_all_game_names/")
def find_all_game_names():
    print('find_all_game_names')
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    names_list = []
    try:
        db = client["ShootTheMoon"]
        games_collection = db["games"]

        # Query to get only the "name" field from all game documents
        game_names = games_collection.find({}, {"_id": 0, "name": 1})

        # Convert cursor to a list of names
        names_list = [game["name"] for game in game_names]
    except Exception as e:
        print(f"An error occurred: {e}")
    client.close()
    print("Client Closed successfully")

    return names_list

@app.post("/create_game/")
async def create_game(domino: Domino):
    print("create_game:", domino.sideA, domino.sideB)
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

#Doc this one
@app.post("/create_game_by_name/{game_name}")
async def create_game_by_name(game_name: str):
    print("Start POST create_game_by_name: ", game_name)
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    deck = get_domino_deck(0, 28)
    game_id = create_new_game(game_name)
    print("game_id: ", game_id)
    round_id = create_round(client, game_id)
    print("round_id: ", round_id)
    hand_ids = deal_dominos(deck, game_id, round_id)
    #hand_ids = create_hands(client, game_id, round_id, hands)
    #print("hand_ids: ", hand_ids)
    round_result = update_current_round(client, game_id, round_id)
    game = {"game_id": str(game_id), "round_id": str(round_id), "hand_ids": str(hand_ids), "round_result": str(round_result)}
    game_state = get_game_state(client, game_id)
    # client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    # post_id = 0
    # game = create_initial_game_state(game_name)
    # print("game: ", game)
    # #print("all dominos: ", ALL_DOMINOES)
    try:
        print("try block start create_game_by_name: ", game_name)
        # db = client.ShootTheMoon
        # games = db.games
        # post_id = games.insert_one(game.to_dict()).inserted_id
        # game = games.find_one({'_id': post_id})
        # print("post_id: ", post_id)
        # new_round_doc = create_new_round(post_id)
        # round_id = db.rounds.insert_one(new_round_doc).inserted_id
        # print('round_id: ', round_id)
        # update_data = {
        #     "currentRoundId": round_id
        # }
        # result = db.games.update_one({"_id": post_id}, {"$set": update_data})
        # print("after update: ", result)
        # #game = games.find_one({'_id': post_id})
        print("try block end create_game_by_name: ", game_name)
    except Exception as e:
        print(f"An error occurred: {e}")
    client.close()
    # if game and '_id' in game:
    #     game['id'] = str(game['_id'])
    #     del game['_id']
    # if game and 'currentRoundId' in game:
    #     game['currentRoundIdString'] = str(game['currentRoundId'])
    #     del game['currentRoundId']
    print("End POST create_game_by_name: ", game_name)
    return game_state

# @app.put("/update_game/{game_id}")
# def update_game(game_id: str, updated_data: UpdateData):
#     print(f"update_game: {game_id} {UpdateData}")
#     return {f"update_game: {game_id} {updated_data}"}

@app.delete("/delete_game/{game_id}")
def delete_game(game_id: str):
    # Logic to delete the game using the game_id
    print(f"delete_game: {game_id}")
    return {f"delete_game: {game_id}"}

