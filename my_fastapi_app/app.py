from fastapi import FastAPI
from pydantic import BaseModel
import pymongo

app = FastAPI()

# Define your MongoDB connection parameters
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["mydatabase"]

class Item(BaseModel):
    name: str
    description: str

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    # Insert the item into the MongoDB collection
    item_data = item.dict()
    result = db.items.insert_one(item_data)
    item_id = str(result.inserted_id)
    
    return {"item_id": item_id, **item.dict()}
