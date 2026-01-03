# CRUD operations (Create, Read, Update, Delete)
# Input validation with Pydantic
# Error handling with HTTPException
# Automatic API documentation
# In-memory database (can be replaced with a real DB later)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

# Create FastAPI instance
app = FastAPI(
    title="Sample FastAPI REST API",
    description="A simple REST API built with FastAPI",
    version="1.0.0"
)

# Data model for request/response validation
class Item(BaseModel):
    id: int = Field(..., gt=0, description="Unique ID of the item (must be > 0)")
    name: str = Field(..., min_length=1, max_length=50, description="Name of the item")
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    description: Optional[str] = Field(None, max_length=200)

# In-memory "database"
items_db: List[Item] = []

# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the FastAPI REST API!"}

# Create item
@app.post("/items", response_model=Item, status_code=201, tags=["Items"])
def create_item(item: Item):
    # Check for duplicate ID
    if any(existing_item.id == item.id for existing_item in items_db):
        raise HTTPException(status_code=400, detail="Item with this ID already exists.")
    items_db.append(item)
    return item

# Get all items
@app.get("/items", response_model=List[Item], tags=["Items"])
def get_items():
    return items_db

# Get item by ID
@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found.")

# Update item
@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
def update_item(item_id: int, updated_item: Item):
    for index, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            items_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found.")

# Delete item
@app.delete("/items/{item_id}", status_code=204, tags=["Items"])
def delete_item(item_id: int):
    for index, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            del items_db[index]
            return
    raise HTTPException(status_code=404, detail="Item not found.")

# Run the app
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)