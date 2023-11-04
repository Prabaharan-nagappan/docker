from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()

# Define your MongoDB client here.
mongo_client = MongoClient("mongodb://my_fastapi_app-mongo-1:27017/")

class Item(BaseModel):
    name: str
    description: str

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    # Access the "mydatabase" database from the MongoDB client.
    db = mongo_client["mydatabase"]

    # Access the "items" collection in the database.
    items_collection = db["items"]

    # Insert the item data into the collection.
    inserted_item = items_collection.insert_one(item.dict())

    # Return the inserted item.
    return {
        "name": item.name,
        "description": item.description,
        "_id": str(inserted_item.inserted_id)  # Convert ObjectId to string
    }
