import requests
from bs4 import BeautifulSoup
import os

class SearchPlugin:
    def __init__(self):
        self.api_key = os.getenv('SERPER_API_KEY')
        self.base_url = "https://google.serper.dev/search"
    
    async def search(self, query: str) -> str:
        """Search the web and return summarized results"""
        if not self.api_key:
            return await self._duckduckgo_search(query)
        
        try:
            headers = {
                'X-API-KEY': self.api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {'q': query}
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('organic', [])[:5]
                
                search_text = f"🔍 **Search results for '{query}'**\n\n"
                
                for i, result in enumerate(results, 1):
                    title = result.get('title', 'No title')
                    snippet = result.get('snippet', 'No description')
                    search_text += f"{i}. **{title}**\n   {snippet}\n\n"
                
                return search_text.strip()
            else:
                return "❌ Search failed"
        except Exception as e:
            return f"❌ Search error: {str(e)}"
    
    async def _duckduckgo_search(self, query: str) -> str:
        """Fallback DuckDuckGo search (no API key)"""
        try:
            url = f"https://html.duckduckgo.com/html/?q={query}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='result', limit=5)
            
            search_text = f"🔍 **Search results for '{query}'**\n\n"
            
            for i, result in enumerate(results, 1):
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem and snippet_elem:
                    title = title_elem.get_text(strip=True)
                    snippet = snippet_elem.get_text(strip=True)
                    search_text += f"{i}. **{title}**\n   {snippet}\n\n"
            
            return search_text.strip() if len(results) > 0 else "❌ No results found"
        except Exception as e:
            return f"❌ Search error: {str(e)}"
