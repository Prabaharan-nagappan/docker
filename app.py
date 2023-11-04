# app.py
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

client = AsyncIOMotorClient("mongodb://localhost:27017")
database = client["mydatabase"]
collection = database["mycollection"]

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

@app.post("/items/", response_model=None)
async def create_item(item: Item):
    document = {
        "name": item.name,
        "description": item.description
    }
    result = await collection.insert_one(document)
    item_id = str(result.inserted_id)
    return {"item_id": item_id, **document}

@app.get("/items/")
async def read_items():
    items = []
    async for item in collection.find():
        items.append(item)
    return items
