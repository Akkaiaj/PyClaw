import os
from dotenv import load_dotenv

load_dotenv()

# Core API Keys
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Plugin API Keys (optional)
MOLTBOOK_API_KEY = os.getenv('MOLTBOOK_API_KEY')
MOLTBOOK_API_URL = os.getenv('MOLTBOOK_API_URL', 'https://api.moltbook.com')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
SERPER_API_KEY = os.getenv('SERPER_API_KEY')  # For web search

# Bot Settings
DATABASE_FILE = os.getenv('DATABASE_FILE', 'pyclaw.db')
MAX_CONVERSATION_HISTORY = int(os.getenv('MAX_CONVERSATION_HISTORY', '10'))
DEFAULT_AGENT = os.getenv('DEFAULT_AGENT', 'friendly')

# Feature Flags
ENABLE_MODERATION = os.getenv('ENABLE_MODERATION', 'true').lower() == 'true'
ENABLE_WEATHER = os.getenv('ENABLE_WEATHER', 'true').lower() == 'true'
ENABLE_NEWS = os.getenv('ENABLE_NEWS', 'true').lower() == 'true'
ENABLE_SEARCH = os.getenv('ENABLE_SEARCH', 'true').lower() == 'true'
ENABLE_GAMES = os.getenv('ENABLE_GAMES', 'true').lower() == 'true'
ENABLE_MOLTBOOK = os.getenv('ENABLE_MOLTBOOK', 'true').lower() == 'true'
