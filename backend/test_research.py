import asyncio
from app.services.research import search_and_scrape

async def main():
    print("Testing search_and_scrape...")
    result = await search_and_scrape("history of internet")
    print("\n--- RESULT ---\n")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
