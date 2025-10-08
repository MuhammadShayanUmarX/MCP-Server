from fastapi import FastAPI, HTTPException
from typing import List
from models import Todo, TodoCreate, TodoUpdate
from database import get_todos, get_todo, create_todo, update_todo, delete_todo

app = FastAPI(title="Todo API", description="A simple todo management API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Welcome to Todo API"}

@app.get("/todos", response_model=List[Todo])
async def read_todos():
    """Get all todos"""
    return get_todos()

@app.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int):
    """Get a specific todo by ID"""
    todo = get_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/todos", response_model=Todo)
async def create_todo_endpoint(todo: TodoCreate):
    """Create a new todo"""
    return create_todo(todo)

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo_endpoint(todo_id: int, todo: TodoUpdate):
    """Update an existing todo"""
    updated_todo = update_todo(todo_id, todo)
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@app.delete("/todos/{todo_id}")
async def delete_todo_endpoint(todo_id: int):
    """Delete a todo"""
    if not delete_todo(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
