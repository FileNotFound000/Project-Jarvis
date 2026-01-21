from duckduckgo_search import DDGS

def search_web(query: str, max_results: int = 3) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return "No results found."
            
            formatted_results = []
            for r in results:
                formatted_results.append(f"Title: {r['title']}\nLink: {r['href']}\nSnippet: {r['body']}")
            
            return "\n\n".join(formatted_results)
    except Exception as e:
        print(f"Search error: {e}")
        return f"Error performing search: {str(e)}"

def get_first_youtube_video(query: str) -> str:
    """
    Find the first YouTube video URL for a query.
    """
    try:
        with DDGS() as ddgs:
            # Search for videos
            results = list(ddgs.videos(query, max_results=1))
            if results:
                return results[0]['content'] # 'content' is the URL in DDGS video results
            return None
    except Exception as e:
        print(f"YouTube search error: {e}")
        return None
