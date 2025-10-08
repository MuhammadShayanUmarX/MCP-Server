
# Gemini CLI Usage Guide for MCP Todo Server

## Setup Steps:

1. Set your Gemini API Key:
   export GEMINI_API_KEY="your-api-key-here"

2. Run the Gemini MCP Client:
   python gemini_mcp_client.py

3. Or use direct CLI:
   python direct_todo_cli.py

## Available Commands:

### Natural Language Examples:
- "Create a todo called Learn MCP"
- "List all my todos" 
- "Update todo 1 to completed"
- "Delete todo 2"
- "Get details of todo 1"

### Direct MCP Tools:
- list_todos
- get_todo (with todo_id)
- create_todo (with title, description, status)
- update_todo (with todo_id and updates)
- delete_todo (with todo_id)

## Testing:
python test_demo.py
