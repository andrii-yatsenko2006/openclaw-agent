import ollama
from typing import List, Dict

class Brain:
    """
    Handles communication with the local Ollama LLM.
    """
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Sends a conversation history to the model and returns the text response.
        """
        try:
            # Call local Ollama instance
            response = ollama.chat(
                model=self.model_name,
                messages=messages,
            )
            return response.get('message', {}).get('content', '')

        except Exception as e:
            # Log error and return a safe fallback message
            print(f"Brain Error: {e}")
            return "Error: Could not reach the local LLM. Is Ollama running?"

    def check_connection(self) -> bool:
        """
        Verifies if the specified model is pulled and available locally.
        """
        try:
            models_info = ollama.list()
            available_models = [m.get('name', '') for m in models_info.get('models', [])]

            # Match base name (e.g., 'llama3' matches 'llama3:latest')
            return any(self.model_name in  model for model in available_models)

        except Exception:
            return False