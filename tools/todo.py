import json
import os
from typing import List, Dict, Any

class TodoManager:
    """
    Manages a persistent To-Do list for the agent using a JSON file.
    """
    def __init__(self, file_path: str = None):
        # Fetch path from environment variable or use default
        self.file_path = file_path or os.getenv("TODO_FILE_PATH", "./data/todo.json")
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """
        Creates the JSON file with an empty list if it doesn't exist.
        """
        if not os.path.exists(self.file_path):
            # Create the 'data' directory if it's missing
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w", encoding='utf-8') as f:
                json.dump([], f)

    def add_task(self, task_name: str) -> str:
        """
        Adds a new pending task to the list.
        Returns a status message for the agent's observation.
        """
        tasks = self.get_tasks()

        new_task = {
            "id": len(tasks) + 1,
            "task": task_name,
            "status": "pending",
        }

        tasks.append(new_task)
        self._save_tasks(tasks)

        return f"Task '{task_name}' added successfully with ID {new_task['id']}."

    def mark_done(self, task_id: int) -> str:
        """
        Marks a specific task as done using its ID.
        """
        tasks = self.get_tasks()

        for t in tasks:
            if t["id"] == task_id:
                if t["status"] == "done":
                    return f"Task {task_id} is already marked as done."

                t["status"] = "done"
                self._save_tasks(tasks)
                return f"Task {task_id} marked as done."

        return f"Error: Task with ID {task_id} not found."

    def get_tasks(self) -> List[Dict[str, Any]]:
        """
        Returns the list of all tasks.
        """
        try:
            with open(self.file_path, "r", encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _save_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """
        Internal method to save the updated tasks list back to the file.
        """
        with open(self.file_path, "w", encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)