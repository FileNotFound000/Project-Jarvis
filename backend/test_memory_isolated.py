import asyncio
import os
from app.services.agent import AgentService
from app.services.memory import MemoryService

async def test_embedding():
    print("\n--- Testing Embedding ---", flush=True)
    from dotenv import load_dotenv
    load_dotenv()
    print(f"GEMINI_API_KEY env: {os.getenv('GEMINI_API_KEY')}", flush=True)
    
    agent = AgentService()
    await asyncio.sleep(1) # Wait for async configure
    print(f"Agent Provider: {type(agent.provider).__name__}", flush=True)
    if hasattr(agent.provider, 'api_key'):
        print(f"Provider API Key: {agent.provider.api_key}", flush=True)

    text = "Hello world"
    print(f"Generating embedding for: '{text}'", flush=True)
    try:
        embedding = await agent.provider.get_embedding(text)
        print(f"Embedding length: {len(embedding)}", flush=True)
        return embedding
    except Exception as e:
        print(f"Embedding failed: {e}", flush=True)
        return None

def test_chroma(embedding):
    print("\n--- Testing ChromaDB ---", flush=True)
    if not embedding:
        print("Skipping Chroma test due to missing embedding.", flush=True)
        # Use dummy embedding
        embedding = [0.1] * 768 
        print("Using dummy embedding.", flush=True)

    try:
        ms = MemoryService(persist_directory="test_chroma_db")
        ms.collection.add(
            documents=["Test document"],
            embeddings=[embedding],
            ids=["test_id"]
        )
        print("Added to ChromaDB.", flush=True)
        
        results = ms.collection.query(
            query_embeddings=[embedding],
            n_results=1
        )
        print(f"Query results: {results}", flush=True)
    except Exception as e:
        print(f"ChromaDB failed: {e}", flush=True)

async def main():
    emb = await test_embedding()
    test_chroma(emb)

if __name__ == "__main__":
    asyncio.run(main())
