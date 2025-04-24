import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv

from Models.GameModel import create_new_game, update_current_round
from Models.RoundModel import create_round
from Models.GameStateModel import get_game_state
from MongoRepositories.DominoRepository import get_domino_deck
from Services.GameService import deal_dominos

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Domino game server running!"}

@app.get("/find_game_by_name/{name}")
def find_game_by_name(name: str):
    """Finds a game by its name and returns the full game state."""
    print('find_game_by_name:', name)
    game_state = None
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))

    try:
        db = client["ShootTheMoon"]
        game = db["games"].find_one({"name": name})
        if game:
            game_id = game.get('_id')
            if game_id:
                game_state = get_game_state(client, game_id)
    except Exception as e:
        print(f"[find_game_by_name] Error: {e}")
    finally:
        client.close()
        print("Client closed successfully")

    return game_state

@app.get("/find_all_game_names/")
def find_all_game_names():
    """Returns a list of all game names in the database."""
    print('find_all_game_names')
    names_list = []
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))

    try:
        db = client["ShootTheMoon"]
        game_names = db["games"].find({}, {"_id": 0, "name": 1})
        names_list = [game["name"] for game in game_names]
    except Exception as e:
        print(f"[find_all_game_names] Error: {e}")
    finally:
        client.close()
        print("Client closed successfully")

    return names_list

@app.post("/create_game_by_name/{game_name}")
async def create_game_by_name(game_name: str):
    """Creates a new game by name, sets up round and hands, and returns initial game state."""
    print("Start POST create_game_by_name:", game_name)
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))

    try:
        deck = get_domino_deck(0, 28)
        game_id = create_new_game(game_name)
        round_id = create_round(client, game_id)
        deal_dominos(deck, game_id, round_id)
        update_current_round(client, game_id, round_id)
        game_state = get_game_state(client, game_id)
        return game_state
    except Exception as e:
        print(f"[create_game_by_name] Error: {e}")
        return {"error": str(e)}
    finally:
        client.close()
        print("End POST create_game_by_name:", game_name)