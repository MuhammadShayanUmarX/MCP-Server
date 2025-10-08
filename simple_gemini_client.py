#!/usr/bin/env python3
"""
Simple Gemini Client for Todo Management
Direct integration without MCP complexity
"""

import os
import json
from pathlib import Path
import google.generativeai as genai
from database import get_todos, get_todo, create_todo, update_todo, delete_todo
from models import TodoCreate, TodoUpdate, TodoStatus

# Load .env file if it exists
def load_env_file():
    """Load .env file if it exists"""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

# Load environment variables
load_env_file()

class SimpleGeminiClient:
    def __init__(self):
        """Initialize the Simple Gemini Client"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key or self.api_key == 'your-api-key-here':
            raise ValueError("GEMINI_API_KEY not set. Please set it in .env file")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def process_natural_language(self, user_input: str) -> str:
        """Process natural language input using Gemini"""
        
        # Get current todos for context
        todos = get_todos()
        todos_context = ""
        if todos:
            todos_context = "Current todos:\n"
            for todo in todos:
                todos_context += f"- ID {todo.id}: {todo.title} ({todo.status})\n"
        else:
            todos_context = "No todos currently exist.\n"
        
        prompt = f"""
You are a helpful assistant that manages todos. 

{todos_context}

User request: "{user_input}"

Based on the user's request, determine what action to take and respond with a JSON object in this format:
{{
    "action": "action_name",
    "parameters": {{"param1": "value1", "param2": "value2"}}
}}

Available actions:
- list_todos: List all todos
- get_todo: Get specific todo (requires todo_id)
- create_todo: Create new todo (requires title, optional description, status)
- update_todo: Update existing todo (requires todo_id, optional title, description, status)
- delete_todo: Delete todo (requires todo_id)

Status values: pending, in_progress, completed

Only respond with the JSON object, no other text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Parse the JSON response
            action_data = json.loads(response_text)
            action = action_data.get("action")
            parameters = action_data.get("parameters", {})
            
            # Execute the action
            return self.execute_action(action, parameters)
            
        except json.JSONDecodeError as e:
            return f"Error parsing Gemini response: {e}"
        except Exception as e:
            return f"Error processing request: {e}"
    
    def execute_action(self, action: str, parameters: dict) -> str:
        """Execute the determined action"""
        
        try:
            if action == "list_todos":
                todos = get_todos()
                if not todos:
                    return "📝 No todos found"
                
                result = "📋 All Todos:\n"
                for todo in todos:
                    status_emoji = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}
                    emoji = status_emoji.get(todo.status, "📝")
                    result += f"{emoji} ID {todo.id}: {todo.title} ({todo.status})\n"
                    if todo.description:
                        result += f"   📄 {todo.description}\n"
                return result
            
            elif action == "get_todo":
                todo_id = parameters.get("todo_id")
                if not todo_id:
                    return "❌ Todo ID is required"
                
                todo = get_todo(todo_id)
                if not todo:
                    return f"❌ Todo with ID {todo_id} not found"
                
                status_emoji = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}
                emoji = status_emoji.get(todo.status, "📝")
                result = f"{emoji} Todo ID {todo.id}: {todo.title}\n"
                if todo.description:
                    result += f"📄 Description: {todo.description}\n"
                result += f"📊 Status: {todo.status}\n"
                result += f"📅 Created: {todo.created_at}\n"
                return result
            
            elif action == "create_todo":
                title = parameters.get("title")
                if not title:
                    return "❌ Title is required"
                
                description = parameters.get("description", "")
                status = parameters.get("status", "pending")
                
                try:
                    todo_data = TodoCreate(
                        title=title,
                        description=description,
                        status=TodoStatus(status)
                    )
                    todo = create_todo(todo_data)
                    return f"✅ Created todo: {todo.title} (ID: {todo.id})"
                except Exception as e:
                    return f"❌ Error creating todo: {e}"
            
            elif action == "update_todo":
                todo_id = parameters.get("todo_id")
                if not todo_id:
                    return "❌ Todo ID is required"
                
                update_data = {}
                if "title" in parameters:
                    update_data["title"] = parameters["title"]
                if "description" in parameters:
                    update_data["description"] = parameters["description"]
                if "status" in parameters:
                    update_data["status"] = TodoStatus(parameters["status"])
                
                todo_update = TodoUpdate(**update_data)
                updated_todo = update_todo(todo_id, todo_update)
                
                if not updated_todo:
                    return f"❌ Todo with ID {todo_id} not found"
                
                return f"✅ Updated todo: {updated_todo.title} (ID: {updated_todo.id})"
            
            elif action == "delete_todo":
                todo_id = parameters.get("todo_id")
                if not todo_id:
                    return "❌ Todo ID is required"
                
                success = delete_todo(todo_id)
                if success:
                    return f"🗑️ Todo with ID {todo_id} deleted successfully"
                else:
                    return f"❌ Todo with ID {todo_id} not found"
            
            else:
                return f"❌ Unknown action: {action}"
                
        except Exception as e:
            return f"❌ Error executing action: {e}"
    
    def interactive_mode(self):
        """Run interactive mode"""
        print("🤖 Gemini Todo Assistant")
        print("=" * 50)
        print("Available commands:")
        print("- 'list todos' or 'show todos' - List all todos")
        print("- 'create todo: [title]' - Create a new todo")
        print("- 'get todo [id]' - Get specific todo")
        print("- 'update todo [id]: [new title]' - Update todo")
        print("- 'delete todo [id]' - Delete todo")
        print("- 'help' - Show this help")
        print("- 'quit' or 'exit' - Exit the program")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n💬 Enter your request: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    print("\nAvailable commands:")
                    print("- 'list todos' or 'show todos' - List all todos")
                    print("- 'create todo: [title]' - Create a new todo")
                    print("- 'get todo [id]' - Get specific todo")
                    print("- 'update todo [id]: [new title]' - Update todo")
                    print("- 'delete todo [id]' - Delete todo")
                    print("- 'help' - Show this help")
                    print("- 'quit' or 'exit' - Exit the program")
                    continue
                
                if not user_input:
                    continue
                
                print("🔄 Processing...")
                result = self.process_natural_language(user_input)
                print(f"📋 Result:\n{result}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function"""
    try:
        client = SimpleGeminiClient()
        print("✅ Gemini Client initialized")
        client.interactive_mode()
    except ValueError as e:
        print(f"❌ {e}")
        print("\n💡 To fix:")
        print("1. Create .env file in project directory")
        print("2. Add: GEMINI_API_KEY=your-api-key-here")
        print("3. Get API key from: https://makersuite.google.com/app/apikey")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
