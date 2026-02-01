import requests
import os
from datetime import datetime

class NewsPlugin:
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2/top-headlines"
    
    async def get_news(self, topic: str = None, country: str = 'us', limit: int = 5) -> str:
        """Get latest news headlines"""
        if not self.api_key:
            return "❌ News API key not configured. Add NEWS_API_KEY to .env"
        
        try:
            params = {
                'apiKey': self.api_key,
                'country': country,
                'pageSize': limit
            }
            
            if topic:
                params['q'] = topic
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                if not articles:
                    return f"📰 No news found for '{topic}'" if topic else "📰 No news available"
                
                news_text = f"📰 **Latest News{' about ' + topic if topic else ''}**\n\n"
                
                for i, article in enumerate(articles[:limit], 1):
                    title = article['title']
                    source = article['source']['name']
                    news_text += f"{i}. **{title}**\n   _{source}_\n\n"
                
                return news_text.strip()
            else:
                return "❌ Failed to fetch news"
        except Exception as e:
            return f"❌ News error: {str(e)}"
