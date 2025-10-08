#!/usr/bin/env python3
"""
Clean Todo App with Gemini AI
Simple and clean implementation
"""

import os
import json
from datetime import datetime
from typing import List, Optional
from pathlib import Path
import google.generativeai as genai

# Load .env file if it exists
def load_env():
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env()

class Todo:
    def __init__(self, id: int, title: str, description: str = "", status: str = "pending"):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

class TodoApp:
    def __init__(self):
        self.todos: List[Todo] = []
        self.next_id = 1
        self.gemini_model = None
        
        # Initialize Gemini if API key is available
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key and api_key != 'your-api-key-here':
            try:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                print("✅ Gemini AI enabled")
            except:
                print("⚠️ Gemini AI not available")
    
    def add_todo(self, title: str, description: str = "", status: str = "pending") -> Todo:
        """Add a new todo"""
        todo = Todo(self.next_id, title, description, status)
        self.todos.append(todo)
        self.next_id += 1
        return todo
    
    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """Get a specific todo"""
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None
    
    def update_todo(self, todo_id: int, title: str = None, description: str = None, status: str = None) -> bool:
        """Update a todo"""
        todo = self.get_todo(todo_id)
        if not todo:
            return False
        
        if title:
            todo.title = title
        if description is not None:
            todo.description = description
        if status:
            todo.status = status
        
        todo.updated_at = datetime.now()
        return True
    
    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo"""
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                self.todos.pop(i)
                return True
        return False
    
    def list_todos(self) -> List[Todo]:
        """Get all todos"""
        return self.todos
    
    def process_ai_command(self, user_input: str) -> str:
        """Process natural language command with Gemini"""
        if not self.gemini_model:
            return "❌ Gemini AI not available. Set GEMINI_API_KEY in .env file"
        
        # Create context
        todos_context = ""
        if self.todos:
            todos_context = "Current todos:\n"
            for todo in self.todos:
                todos_context += f"- ID {todo.id}: {todo.title} ({todo.status})\n"
        else:
            todos_context = "No todos currently exist.\n"
        
        prompt = f"""
You are a helpful todo assistant. 

{todos_context}

User request: "{user_input}"

Respond with a JSON object in this format:
{{
    "action": "action_name",
    "parameters": {{"param1": "value1"}}
}}

Available actions:
- list: List all todos
- get: Get specific todo (requires id)
- create: Create new todo (requires title, optional description, status)
- update: Update todo (requires id, optional title, description, status)
- delete: Delete todo (requires id)

Status values: pending, in_progress, completed

Only respond with JSON, no other text.
"""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            action_data = json.loads(response.text.strip())
            
            action = action_data.get("action")
            params = action_data.get("parameters", {})
            
            return self.execute_action(action, params)
            
        except Exception as e:
            return f"❌ Error: {e}"
    
    def execute_action(self, action: str, params: dict) -> str:
        """Execute the determined action"""
        try:
            if action == "list":
                if not self.todos:
                    return "📝 No todos found"
                
                result = "📋 All Todos:\n"
                for todo in self.todos:
                    emoji = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(todo.status, "📝")
                    result += f"{emoji} ID {todo.id}: {todo.title} ({todo.status})\n"
                    if todo.description:
                        result += f"   📄 {todo.description}\n"
                return result
            
            elif action == "get":
                todo_id = params.get("id")
                if not todo_id:
                    return "❌ Todo ID required"
                
                todo = self.get_todo(todo_id)
                if not todo:
                    return f"❌ Todo {todo_id} not found"
                
                emoji = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(todo.status, "📝")
                result = f"{emoji} Todo {todo.id}: {todo.title}\n"
                if todo.description:
                    result += f"📄 {todo.description}\n"
                result += f"📊 Status: {todo.status}\n"
                result += f"📅 Created: {todo.created_at.strftime('%Y-%m-%d %H:%M')}\n"
                return result
            
            elif action == "create":
                title = params.get("title")
                if not title:
                    return "❌ Title required"
                
                description = params.get("description", "")
                status = params.get("status", "pending")
                
                todo = self.add_todo(title, description, status)
                return f"✅ Created: {todo.title} (ID: {todo.id})"
            
            elif action == "update":
                todo_id = params.get("id")
                if not todo_id:
                    return "❌ Todo ID required"
                
                success = self.update_todo(
                    todo_id,
                    params.get("title"),
                    params.get("description"),
                    params.get("status")
                )
                
                if success:
                    return f"✅ Updated todo {todo_id}"
                else:
                    return f"❌ Todo {todo_id} not found"
            
            elif action == "delete":
                todo_id = params.get("id")
                if not todo_id:
                    return "❌ Todo ID required"
                
                success = self.delete_todo(todo_id)
                if success:
                    return f"🗑️ Deleted todo {todo_id}"
                else:
                    return f"❌ Todo {todo_id} not found"
            
            else:
                return f"❌ Unknown action: {action}"
                
        except Exception as e:
            return f"❌ Error: {e}"
    
    def run(self):
        """Run the todo app"""
        print("📝 Clean Todo App with Gemini AI")
        print("=" * 40)
        
        if self.gemini_model:
            print("🤖 AI Mode: Use natural language commands")
            print("Examples:")
            print("- 'Create a todo called Learn Python'")
            print("- 'List all my todos'")
            print("- 'Update todo 1 to completed'")
        else:
            print("📋 Manual Mode: Use direct commands")
            print("Commands: list, create <title>, get <id>, update <id> <title>, delete <id>")
        
        print("\nType 'help' for commands, 'quit' to exit")
        print("=" * 40)
        
        while True:
            try:
                user_input = input("\n💬 Enter command: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    print("\n📋 Available Commands:")
                    if self.gemini_model:
                        print("🤖 AI Commands (Natural Language):")
                        print("- 'Create a todo called [title]'")
                        print("- 'List all my todos'")
                        print("- 'Update todo [id] to [status]'")
                        print("- 'Delete todo [id]'")
                        print("- 'Get details of todo [id]'")
                    else:
                        print("📝 Manual Commands:")
                        print("- list")
                        print("- create <title>")
                        print("- get <id>")
                        print("- update <id> <new_title>")
                        print("- delete <id>")
                    continue
                
                if not user_input:
                    continue
                
                if self.gemini_model:
                    # Use AI processing
                    print("🔄 Processing with AI...")
                    result = self.process_ai_command(user_input)
                else:
                    # Manual command processing
                    parts = user_input.split()
                    command = parts[0].lower()
                    
                    if command == 'list':
                        if not self.todos:
                            result = "📝 No todos found"
                        else:
                            result = "📋 All Todos:\n"
                            for todo in self.todos:
                                emoji = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(todo.status, "📝")
                                result += f"{emoji} ID {todo.id}: {todo.title} ({todo.status})\n"
                    
                    elif command == 'create':
                        if len(parts) < 2:
                            result = "❌ Usage: create <title>"
                        else:
                            title = ' '.join(parts[1:])
                            todo = self.add_todo(title)
                            result = f"✅ Created: {todo.title} (ID: {todo.id})"
                    
                    elif command == 'get':
                        if len(parts) < 2:
                            result = "❌ Usage: get <id>"
                        else:
                            try:
                                todo_id = int(parts[1])
                                todo = self.get_todo(todo_id)
                                if todo:
                                    emoji = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(todo.status, "📝")
                                    result = f"{emoji} Todo {todo.id}: {todo.title} ({todo.status})"
                                else:
                                    result = f"❌ Todo {todo_id} not found"
                            except ValueError:
                                result = "❌ Invalid ID"
                    
                    elif command == 'update':
                        if len(parts) < 3:
                            result = "❌ Usage: update <id> <new_title>"
                        else:
                            try:
                                todo_id = int(parts[1])
                                new_title = ' '.join(parts[2:])
                                if self.update_todo(todo_id, title=new_title):
                                    result = f"✅ Updated todo {todo_id}"
                                else:
                                    result = f"❌ Todo {todo_id} not found"
                            except ValueError:
                                result = "❌ Invalid ID"
                    
                    elif command == 'delete':
                        if len(parts) < 2:
                            result = "❌ Usage: delete <id>"
                        else:
                            try:
                                todo_id = int(parts[1])
                                if self.delete_todo(todo_id):
                                    result = f"🗑️ Deleted todo {todo_id}"
                                else:
                                    result = f"❌ Todo {todo_id} not found"
                            except ValueError:
                                result = "❌ Invalid ID"
                    
                    else:
                        result = "❌ Unknown command. Type 'help' for available commands."
                
                print(f"📋 {result}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function"""
    app = TodoApp()
    app.run()

if __name__ == "__main__":
    main()

