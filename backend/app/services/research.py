import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from app.services.agent import AgentService
import asyncio

async def search_and_scrape(query: str, max_results: int = 5) -> str:
    """Searches the web and scrapes content from top results."""
    print(f"Searching for: {query}")
    results = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Simple query first to test
    search_query = query
    
    try:
        with DDGS() as ddgs:
            ddgs_results = list(ddgs.text(search_query, max_results=max_results))
            print(f"DEBUG: Found {len(ddgs_results)} results for '{search_query}'")
            
            for r in ddgs_results:
                url = r['href']
                title = r['title']
                snippet = r.get('body', '')
                
                # Double check filtering
                if "researchgate.net" in url:
                    continue
                    
                print(f"Scraping: {url}")
                
                content_to_add = ""
                try:
                    # Timeout to prevent hanging
                    response = requests.get(url, headers=headers, timeout=5)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Extract text from paragraphs
                        paragraphs = soup.find_all('p')
                        text_content = "\n".join([p.get_text() for p in paragraphs])
                        
                        # Check for "blocked" content
                        if "access to this paper is restricted" in text_content.lower() or "please login" in text_content.lower():
                             print(f"Content restricted for {url}, using snippet.")
                             content_to_add = snippet
                        elif len(text_content) > 200:
                            # Truncate to avoid token limits
                            content_to_add = text_content[:2000]
                        else:
                            print(f"Content too short for {url}, using snippet.")
                            content_to_add = snippet
                    else:
                        print(f"Failed to fetch {url} (Status {response.status_code}), using snippet.")
                        content_to_add = snippet
                        
                except Exception as e:
                    print(f"Failed to scrape {url}: {e}, using snippet.")
                    content_to_add = snippet
                
                results.append(f"Source: {title} ({url})\nContent:\n{content_to_add}\n---")
                    
    except Exception as e:
        return f"Error during research: {str(e)}"

    if not results:
        return "No useful information found."

    return "\n\n".join(results)

async def generate_research_report(topic: str, llm_service: AgentService, session_id: str):
    """Generates a research report by searching, scraping, and summarizing."""
    
    # 1. Search and Scrape
    yield {"text": f"🔍 **Researching:** '{topic}'...\n\n"}
    
    raw_data = await search_and_scrape(topic)
    
    yield {"text": f"📚 **Reading** gathered materials...\n\n"}
    
    # 2. Summarize with LLM
    prompt = f"""
    You are an expert research analyst. 
    Topic: {topic}
    
    Below is raw data gathered from the web:
    {raw_data}
    
    Please write a comprehensive research report on the topic based ONLY on the provided data.
    - Use Markdown formatting.
    - Cite sources where possible.
    - Be objective and detailed.
    """
    
    async for chunk in llm_service.generate_response_stream(prompt, session_id=session_id, save_user_message=False):
        if "text" in chunk:
            yield chunk
