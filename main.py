import json
import os

from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Union
from pydantic import BaseModel

client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))

try:
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"An error occurred: {e}")

client.close()

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {'data': 'Hello world'}

@app.get("/game_state")
def game_state():
    x = {
      "sideA": 1,
      "sideB": 1
    }
    xstring = json.dumps(x)
    return (

            {"date": "2025-04-04", "temperatureC": 51, "temperatureF": 123, "summary": "Freezing", "domino": xstring}

    )