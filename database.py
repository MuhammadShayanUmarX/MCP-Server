from typing import List, Optional
from models import Todo, TodoCreate, TodoUpdate, TodoStatus
from datetime import datetime

# In-memory storage for simplicity
todos_db: List[Todo] = []
next_id = 1

def get_todos() -> List[Todo]:
    return todos_db

def get_todo(todo_id: int) -> Optional[Todo]:
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    return None

def create_todo(todo_data: TodoCreate) -> Todo:
    global next_id
    now = datetime.now()
    todo = Todo(
        id=next_id,
        title=todo_data.title,
        description=todo_data.description,
        status=todo_data.status,
        created_at=now,
        updated_at=now
    )
    todos_db.append(todo)
    next_id += 1
    return todo

def update_todo(todo_id: int, todo_data: TodoUpdate) -> Optional[Todo]:
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            update_data = todo_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(todo, field, value)
            todo.updated_at = datetime.now()
            todos_db[i] = todo
            return todo
    return None

def delete_todo(todo_id: int) -> bool:
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            todos_db.pop(i)
            return True
    return False
