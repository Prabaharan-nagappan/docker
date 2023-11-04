# app.py
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

client = AsyncIOMotorClient("mongodb://mongo:27017")
database = client["mydatabase"]
collection = database["mycollection"]

@app.post("/items/")
async def create_item(item: dict):
    await collection.insert_one(item)
    return item

@app.get("/items/")
async def read_items():
    items = []
    async for item in collection.find():
        items.append(item)
    return items
