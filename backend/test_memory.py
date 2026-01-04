import asyncio
from app.services.memory import MemoryService
from app.providers.gemini import GeminiProvider
from app.services.settings import SettingsService
from dotenv import load_dotenv

async def test_memory():
    load_dotenv()
    
    print("Initializing services...")
    settings_service = SettingsService()
    settings = settings_service.load_settings()
    
    provider = GeminiProvider()
    await provider.configure(settings)
    
    memory_service = MemoryService()
    
    print("Adding memory...")
    await memory_service.add_memory("My favorite color is green.", provider)
    
    print("Searching memory...")
    results = await memory_service.search_memory("What is my favorite color?", provider)
    print(f"Results: {results}")
    
    # Clean up (optional, or just leave it)
    # memory_service.clear_memories()

if __name__ == "__main__":
    asyncio.run(test_memory())
