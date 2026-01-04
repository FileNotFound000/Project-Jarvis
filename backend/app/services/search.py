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
