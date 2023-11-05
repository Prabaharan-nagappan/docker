import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from bson import ObjectId
from pymongo import MongoClient

app = FastAPI()


# Get the MongoDB connection URL from an environment variable
mongo_url = os.getenv("MONGO_URL")

# MongoDB connection
mongo_client = MongoClient(mongo_url)
db = mongo_client["mydatabase"]
items_collection = db["items"]

class Item(BaseModel):
    ID: str
    name: str
    description: str
    

@app.get("/")
def root():
    return {"message": "Use /docs for FastAPI CRUD operations"}

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    # Insert the item data into the collection.
    inserted_item = items_collection.insert_one(item.dict())

    return {
        "name": item.name,
        "description": item.description,
        "_id": str(inserted_item.inserted_id)  # Convert ObjectId to string
    }

@app.get("/items/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 10):
    # Retrieve items from the collection with pagination.
    items = items_collection.find().skip(skip).limit(limit)
    items_list = []
    for item in items:
        item["ID"] = str(item["_id"])  # Update "ID" field
        items_list.append(item)
    return items_list

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    item = items_collection.find_one({"_id": ObjectId(item_id)})
    if item:
        item["ID"] = str(item["_id"])  # Update "ID" field
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, updated_item: Item):
    # Update the item by its ID.
    result = items_collection.update_one({"_id": ObjectId(item_id)},
                                        {"$set": updated_item.dict()})

    if result.matched_count > 0:
        return updated_item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", response_model=Dict[str, str])
async def delete_item(item_id: str):
    # Delete the item by its ID.
    result = items_collection.delete_one({"_id": ObjectId(item_id)})

    if result.deleted_count > 0:
        return {"message": "Item deleted"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
