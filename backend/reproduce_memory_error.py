import asyncio
import os
from dotenv import load_dotenv
from app.services.memory import MemoryService
from app.providers.gemini import GeminiProvider

# Load environment variables
load_dotenv()

async def reproduce():
    print("Initializing services...")
    
    # Check API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment.")
        return

    try:
        # Initialize Provider
        provider = GeminiProvider()
        await provider.configure({"api_key": api_key})
        print("GeminiProvider initialized.")

        # Initialize Memory Service
        memory_service = MemoryService()
        print("MemoryService initialized.")

        # Test Data
        text = "Test memory: The sky is blue."
        
        # Attempt to add memory
        print(f"Attempting to add memory: '{text}'")
        success = await memory_service.add_memory(text, provider)
        
        if success:
            print("SUCCESS: Memory added successfully.")
        else:
            print("FAILURE: Failed to add memory.")

    except Exception as e:
        print(f"EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(reproduce())
