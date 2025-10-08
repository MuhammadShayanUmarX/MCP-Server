# Todo App - FastAPI to MCP Conversion

This project demonstrates how to create a FastAPI todo application and convert it to an MCP (Model Context Protocol) server.

## Project Structure

```
├── main.py              # FastAPI application
├── models.py            # Pydantic models for data validation
├── database.py          # In-memory database operations
├── mcp_server.py        # MCP server implementation
├── mcp_config.json     # MCP server configuration
├── test_mcp.py         # Test script for MCP server
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Features

### FastAPI Application
- RESTful API endpoints for todo management
- CRUD operations (Create, Read, Update, Delete)
- Data validation with Pydantic models
- In-memory storage for simplicity

### MCP Server
- Converts FastAPI functionality to MCP tools
- 5 available tools: list_todos, get_todo, create_todo, update_todo, delete_todo
- Compatible with MCP clients and AI assistants

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the FastAPI Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

API Endpoints:
- `GET /` - Welcome message
- `GET /todos` - List all todos
- `GET /todos/{id}` - Get specific todo
- `POST /todos` - Create new todo
- `PUT /todos/{id}` - Update todo
- `DELETE /todos/{id}` - Delete todo

### Running the MCP Server

```bash
python mcp_server.py
```

The MCP server provides these tools:
- `list_todos` - Get all todos
- `get_todo` - Get specific todo by ID
- `create_todo` - Create new todo
- `update_todo` - Update existing todo
- `delete_todo` - Delete todo

### Testing the MCP Server

```bash
python test_mcp.py
```

This will run a comprehensive test of all MCP server functionality.

## API Examples

### FastAPI Examples

Create a todo:
```bash
curl -X POST "http://localhost:8000/todos" \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn MCP", "description": "Study Model Context Protocol", "status": "pending"}'
```

Get all todos:
```bash
curl "http://localhost:8000/todos"
```

### MCP Tool Examples

The MCP server can be used with MCP-compatible clients. The tools accept JSON arguments and return structured responses.

## Data Models

### Todo Model
- `id`: Integer (auto-generated)
- `title`: String (required)
- `description`: String (optional)
- `status`: Enum (pending, in_progress, completed)
- `created_at`: DateTime (auto-generated)
- `updated_at`: DateTime (auto-updated)

## Status Values
- `pending`: Todo is not started
- `in_progress`: Todo is being worked on
- `completed`: Todo is finished

## Development

The project uses:
- **FastAPI** for the REST API
- **Pydantic** for data validation
- **MCP** for the protocol server
- **asyncio** for asynchronous operations

## Notes

- The database is in-memory and will reset when the application restarts
- The MCP server runs in stdio mode for easy integration
- Both the FastAPI app and MCP server share the same data models and business logic
# MCP-Server
