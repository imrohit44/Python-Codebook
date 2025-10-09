'''
# Simple REST API with FastAPI

This program creates a high-performance REST API using FastAPI. It provides endpoints to create and retrieve "to-do" items. FastAPI automatically generates interactive API documentation (using Swagger UI), which is one of its best features.

Concepts: API development, data validation (Pydantic), asynchronous web frameworks.

**How to Run**

**1. Save the code and execute it:**

```
python Program_7.py
```
'''

# Save as api_server.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

# --- Data Model Definition using Pydantic ---
# This provides data validation and serialization
class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False

# --- In-memory "Database" ---
# A simple dictionary to store our data
db: Dict[int, TodoItem] = {}
next_id = 1

# --- FastAPI Application Instance ---
app = FastAPI(
    title="Simple Todo API",
    description="A basic API for managing a to-do list.",
    version="1.0.0",
)

# --- API Endpoints ---
@app.post("/todos/", response_model=TodoItem, status_code=201)
async def create_todo(item: TodoItem):
    """
    Create a new to-do item. The ID will be assigned automatically.
    """
    global next_id
    item.id = next_id
    db[next_id] = item
    next_id += 1
    return item

@app.get("/todos/", response_model=List[TodoItem])
async def get_all_todos():
    """
    Retrieve a list of all to-do items.
    """
    return list(db.values())

@app.get("/todos/{todo_id}", response_model=TodoItem)
async def get_todo_by_id(todo_id: int):
    """
    Retrieve a single to-do item by its ID.
    """
    if todo_id not in db:
        return {"error": "Todo not found"}
    return db[todo_id]

# To run this app, use the command: uvicorn api_server:app --reload