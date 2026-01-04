import chromadb
import uuid
from typing import List, Dict, Any, Optional
from app.services.llm_provider import LLMProvider

class MemoryService:
    def __init__(self, persist_directory: str = "chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="user_memories")

    async def add_memory(self, text: str, provider: LLMProvider, metadata: Dict[str, Any] = None) -> bool:
        """
        Adds a new memory to the vector store.
        """
        print(f"DEBUG: Attempting to add memory: '{text}'")
        if not text:
            print("DEBUG: Memory text is empty.")
            return

        # Generate embedding
        embedding = await provider.get_embedding(text)
        if not embedding:
            print("DEBUG: Failed to generate embedding for memory.")
            return False

        # Generate hash for deduplication
        import hashlib
        text_hash = hashlib.sha256(text.encode()).hexdigest()

        # Check for duplicates using metadata
        try:
            existing = self.collection.get(where={"text_hash": text_hash})
            if existing and existing['ids']:
                print(f"DEBUG: Memory already exists (hash match): {text}")
                return True
        except Exception as e:
            print(f"DEBUG: Error checking for duplicates: {e}")

        # Add to ChromaDB
        try:
            print(f"DEBUG: Adding to ChromaDB collection: {self.collection.name}")
            
            # Ensure metadata is not empty (ChromaDB requires non-empty dict if provided)
            final_metadata = metadata or {}
            if not final_metadata:
                final_metadata = {"type": "memory"}
            
            # Add hash to metadata
            final_metadata["text_hash"] = text_hash
                
            self.collection.add(
                documents=[text],
                embeddings=[embedding],
                metadatas=[final_metadata],
                ids=[str(uuid.uuid4())]
            )
            print(f"DEBUG: Memory added successfully: {text}")
            print(f"DEBUG: Current collection count: {self.collection.count()}")
            return True
        except Exception as e:
            print(f"DEBUG: Failed to add memory to ChromaDB: {e}")
            return False

    async def search_memory(self, query: str, provider: LLMProvider, limit: int = 3) -> List[str]:
        """
        Searches for relevant memories.
        """
        if not query:
            return []

        print(f"DEBUG: Searching memory for query: '{query}'")

        # Generate embedding for query
        embedding = await provider.get_embedding(query)
        if not embedding:
            print("DEBUG: Failed to generate embedding for query.")
            return []

        # Query ChromaDB
        try:
            results = self.collection.query(
                query_embeddings=[embedding],
                n_results=limit
            )
            print(f"DEBUG: ChromaDB results: {results}")

            if results and results['documents']:
                return results['documents'][0]
        except Exception as e:
            print(f"DEBUG: Error querying ChromaDB: {e}")
        
        return []

    def get_all_memories(self) -> List[str]:
        """
        Returns all stored memories (for debugging/viewing).
        """
        # ChromaDB doesn't have a cheap "get all" without limit, but we can peek
        count = self.collection.count()
        if count == 0:
            return []
        results = self.collection.get(limit=count)
        return results['documents'] if results else []

    def clear_memories(self):
        """
        Clears all memories.
        """
        self.client.delete_collection("user_memories")
        self.collection = self.client.get_or_create_collection(name="user_memories")
