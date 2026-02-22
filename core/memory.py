import os
import chromadb
from typing import List, Dict, Any

class Memory:
    """
    Manages the Long-Term Memory of the agent using ChromaDB (Vector Store).
    """
    def __init__(self, db_path: str = os.getenv("CHROMA_DB_PATH", "./data/chroma_db"), collection_name: str = "agent_memory"):
        # Initialize the local ChromaDB client. Data is saved to the db_path folder.
        self.client = chromadb.PersistentClient(path=db_path)

        # Get or create a collection
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_memory(self, text: str, metadata: Dict[str, Any] = None) -> None:
        """
        Saves a new memory (fact, preference, etc.) into the vector database.
        """
        if metadata is None:
            metadata = {}

        # Generate a simple unique ID based on the current item count
        memory_id = f"mem_{self.collection.count() + 1}"

        # ChromaDB automatically handles embedding (converting text to vectors)
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[memory_id],
        )

    def search_memory(self, query: str, n_results: int = 3) -> List[str]:
        """
        Searches the database for memories most relevant to the user's query.
        """
        # If the database is empty, return an empty list immediately
        if self.collection.count() == 0:
            return []

        # Perform a similarity search
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, self.collection.count()),
        )

        # Extract and return the matching text documents
        if results and results.get('documents'):
            return results['documents'][0]
        return []

    def get_all_memories(self) -> Dict[str, Any]:
        """
        Retrieves all stored memories.
        Useful for the 'Under the Hood' UI page to show what the bot knows.
        """
        return self.collection.get()