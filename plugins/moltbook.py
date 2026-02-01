import requests
import os
from typing import Optional

class MoltbookPlugin:
    def __init__(self):
        self.api_key = os.getenv('MOLTBOOK_API_KEY')
        self.api_url = os.getenv('MOLTBOOK_API_URL', 'https://api.moltbook.com')
    
    async def post_message(self, content: str, user_id: str = None) -> tuple:
        if not self.api_key:
            return False, "❌ Moltbook API key not configured"
        
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        payload = {'content': content, 'source': 'pyclaw_bot'}
        if user_id:
            payload['user_id'] = user_id
        
        try:
            response = requests.post(f'{self.api_url}/posts', json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                return True, "✅ Posted to Moltbook!"
            else:
                return False, f"❌ Moltbook error: {response.status_code}"
        except Exception as e:
            return False, f"❌ Moltbook error: {str(e)}"
    
    async def get_feed(self, limit: int = 10) -> Optional[str]:
        if not self.api_key:
            return "❌ Moltbook API key not configured"
        
        headers = {'Authorization': f'Bearer {self.api_key}'}
        try:
            response = requests.get(f'{self.api_url}/posts?limit={limit}', headers=headers, timeout=10)
            if response.status_code == 200:
                posts = response.json()
                feed_text = "📱 **Moltbook Feed**\n\n"
                for post in posts:
                    author = post.get('author', 'Unknown')
                    content = post.get('content', '')[:100]
                    feed_text += f"**{author}:** {content}...\n\n"
                return feed_text.strip()
            else:
                return "❌ Failed to fetch feed"
        except Exception as e:
            return f"❌ Feed error: {str(e)}"
