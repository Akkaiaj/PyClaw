# 🚀 PyClaw Supercharged

The ultimate Python Telegram AI bot with persistent memory, multi-agent personalities, and powerful plugins.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production--Ready-success.svg)

## ✨ Features

### 🧠 Advanced Intelligence
- **Persistent Knowledge Base** - SQLite-powered storage for facts and information
- **Multi-Agent System** - 4 distinct AI personalities with unique behaviors
- **Conversation Memory** - Remembers context across sessions
- **Context Enhancement** - Automatically includes relevant stored knowledge

### 🎭 AI Agents
1. **😊 Friendly Claude** - Warm, casual, and supportive conversations
2. **🎓 Expert Claude** - Technical precision and deep knowledge
3. **🔬 Research Assistant** - Analytical, thorough investigations
4. **🎨 Creative Claude** - Imaginative and artistic responses

### 🔌 Powerful Plugins
- **🌤️ Weather** - Real-time weather data (OpenWeather API)
- **📰 News** - Latest headlines and news search (News API)
- **🔍 Web Search** - DuckDuckGo search with no API key required
- **🎮 Games** - Interactive trivia, riddles, and math challenges
- **📱 Moltbook** - Social media integration with auto-posting
- **🛡️ Moderation** - Content filtering and spam detection

### 🔒 Safety & Security
- Automated content moderation
- Spam pattern detection
- Logging system for review
- Privacy-focused design

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.9 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Anthropic API Key (from [console.anthropic.com](https://console.anthropic.com))

### Local Installation

1. **Clone or download this repository**
   ```bash
   cd pyclaw-supercharged
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_token
   ANTHROPIC_API_KEY=your_anthropic_key
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

That's it! Your bot is now running locally. 🎉

---

## ☁️ Cloud Deployment

### Option 1: Railway (Recommended - Free Tier Available)

1. **Fork this repository** to your GitHub account

2. **Go to [Railway.app](https://railway.app)** and sign in

3. **Create New Project** → **Deploy from GitHub**

4. **Select your forked repository**

5. **Add environment variables:**
   - Click on your service
   - Go to "Variables" tab
   - Add all variables from `.env.example`

6. **Deploy!**
   - Railway will automatically detect the `Procfile`
   - Your bot will be live in ~2 minutes

**Railway Free Tier:**
- $5 free credit monthly
- Great for testing and personal use
- Sleeps after 500 hours/month

### Option 2: Render

1. **Fork this repository**

2. **Go to [Render.com](https://render.com)** and sign in

3. **New → Web Service**

4. **Connect your repository**

5. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
   
6. **Add environment variables** from `.env.example`

7. **Create Web Service**

**Render Pricing:**
- Free tier available (with limitations)
- Paid tier: $7/month for always-on service

### Option 3: VPS (DigitalOcean, Linode, Vultr)

1. **Create Ubuntu 22.04 droplet** ($5-6/month)

2. **SSH into your server**
   ```bash
   ssh root@your_server_ip
   ```

3. **Install dependencies**
   ```bash
   apt update && apt upgrade -y
   apt install python3-pip git -y
   ```

4. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/pyclaw-supercharged.git
   cd pyclaw-supercharged
   ```

5. **Install Python packages**
   ```bash
   pip3 install -r requirements.txt
   ```

6. **Configure environment**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your API keys
   ```

7. **Run with PM2** (keeps bot alive)
   ```bash
   npm install -g pm2
   pm2 start bot.py --interpreter python3 --name pyclaw
   pm2 save
   pm2 startup  # Follow the instructions
   ```

8. **Check status**
   ```bash
   pm2 status
   pm2 logs pyclaw
   ```

---

## 🎮 Bot Commands

### Basic Commands
| Command | Description |
|---------|-------------|
| `/start` | Welcome message with full feature list |
| `/help` | Show all available commands |
| `/settings` | Open settings menu with inline buttons |
| `/clear` | Clear conversation history |

### Agent Management
| Command | Description |
|---------|-------------|
| `/agents` | Show agent selection menu |
| `/friendly` | Switch to Friendly Claude |
| `/expert` | Switch to Expert Claude |
| `/researcher` | Switch to Research Assistant |
| `/creative` | Switch to Creative Claude |

### Knowledge Base
| Command | Description | Example |
|---------|-------------|---------|
| `/remember <topic> <info>` | Store a fact | `/remember birthday June 15th` |
| `/recall <topic>` | Retrieve stored info | `/recall birthday` |
| `/forget <topic>` | Delete stored fact | `/forget birthday` |
| `/knowledge` | List all stored topics | - |

### Plugins
| Command | Description | Example |
|---------|-------------|---------|
| `/weather <city>` | Get current weather | `/weather Tokyo` |
| `/news [topic]` | Latest news headlines | `/news technology` |
| `/search <query>` | Web search | `/search Python tutorials` |
| `/trivia` | Play trivia game | - |
| `/riddle` | Get a riddle | - |
| `/math` | Math challenge | - |

### Moltbook Integration
| Command | Description |
|---------|-------------|
| `/post` | Post last AI response to Moltbook |
| `/auto_post <on/off>` | Toggle automatic posting |
| `/feed` | View recent Moltbook posts |

---

## 🔑 API Keys Setup

### Required Keys

#### 1. Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow instructions
3. Copy the token provided
4. Add to `.env` as `TELEGRAM_BOT_TOKEN`

#### 2. Anthropic API Key
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key
5. Add to `.env` as `ANTHROPIC_API_KEY`

### Optional Plugin Keys

#### OpenWeather API (Weather Plugin)
- Get free key: [openweathermap.org/api](https://openweathermap.org/api)
- Free tier: 1,000 calls/day
- Add as `OPENWEATHER_API_KEY`

#### News API (News Plugin)
- Get free key: [newsapi.org](https://newsapi.org)
- Free tier: 100 requests/day
- Add as `NEWS_API_KEY`

#### Serper API (Web Search Plugin)
- Get key: [serper.dev](https://serper.dev)
- Optional: Falls back to DuckDuckGo if not provided
- Add as `SERPER_API_KEY`

#### Moltbook API
- Contact Moltbook for API credentials
- Add as `MOLTBOOK_API_KEY` and `MOLTBOOK_API_URL`

---

## ⚙️ Configuration

### Feature Flags

Disable features you don't need by editing `.env`:

```env
ENABLE_MODERATION=false   # Disable content moderation
ENABLE_WEATHER=false      # Disable weather plugin
ENABLE_NEWS=false         # Disable news plugin
ENABLE_SEARCH=true        # Keep search enabled
ENABLE_GAMES=true         # Keep games enabled
ENABLE_MOLTBOOK=false     # Disable Moltbook integration
```

### Bot Settings

```env
MAX_CONVERSATION_HISTORY=10  # Number of messages to remember
DEFAULT_AGENT=friendly        # Default agent on startup
DATABASE_FILE=pyclaw.db       # SQLite database location
```

---

## 🏗️ Project Structure

```
pyclaw-supercharged/
├── bot.py                  # Main bot orchestrator
├── config.py               # Configuration loader
├── database.py             # SQLite database manager
├── schema.sql              # Database schema
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
├── .gitignore             # Git ignore rules
├── Procfile               # Deployment configuration
├── README.md              # This file
├── agents/                # AI personality agents
│   ├── __init__.py
│   ├── base_agent.py      # Base agent class
│   ├── friendly.py        # Friendly personality
│   ├── expert.py          # Expert personality
│   ├── researcher.py      # Research personality
│   └── creative.py        # Creative personality
├── plugins/               # Feature plugins
│   ├── __init__.py
│   ├── plugin_manager.py  # Plugin system
│   ├── weather.py         # Weather integration
│   ├── news.py            # News integration
│   ├── search.py          # Web search
│   ├── games.py           # Interactive games
│   ├── moltbook.py        # Moltbook integration
│   └── moderation.py      # Content moderation
└── utils/                 # Utility functions
    ├── __init__.py
    ├── keyboards.py       # Telegram inline keyboards
    └── formatting.py      # Text formatting helpers
```

---

## 🗄️ Database Schema

### Tables

**knowledge** - User-specific facts
- `id`, `user_id`, `topic`, `content`, `created_at`

**conversations** - Chat history
- `id`, `user_id`, `role`, `content`, `agent`, `created_at`

**user_settings** - User preferences
- `user_id`, `active_agent`, `auto_post_moltbook`, `language`, `created_at`

**moderation_log** - Safety logs
- `id`, `user_id`, `message`, `flagged_reason`, `created_at`

The database automatically:
- Creates tables on first run
- Manages indexes for performance
- Limits conversation history per user
- Persists across deployments

---

## 🛠️ Development

### Adding a New Agent

1. Create `agents/your_agent.py`:
```python
from agents.base_agent import BaseAgent

class YourAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Your Agent",
            emoji="🤖",
            description="Your description"
        )
    
    def get_system_prompt(self) -> str:
        return "Your system prompt here..."
```

2. Register in `agents/__init__.py`:
```python
from agents.your_agent import YourAgent

AGENTS = {
    # ... existing agents
    'youragent': YourAgent()
}
```

3. Add command handler in `bot.py`

### Adding a New Plugin

1. Create `plugins/your_plugin.py`:
```python
class YourPlugin:
    async def your_method(self, param: str) -> str:
        # Your plugin logic
        return result
```

2. Register in `bot.py`:
```python
from plugins.your_plugin import YourPlugin

if ENABLE_YOUR_FEATURE:
    plugin_manager.register_plugin('yourplugin', YourPlugin)
```

3. Add command handler

---

## 📊 Performance & Limits

### Database
- SQLite handles thousands of users
- Automatic cleanup of old conversations
- Efficient indexing for fast queries

### API Rate Limits
- **Anthropic**: Depends on your plan
- **OpenWeather**: 1,000 calls/day (free)
- **News API**: 100 requests/day (free)
- **Telegram**: 30 messages/second

### Resource Usage
- RAM: ~50-100MB idle
- CPU: <5% during normal operation
- Storage: ~1MB per 1,000 messages

---

## 🐛 Troubleshooting

### Bot doesn't respond
1. Check if bot is running: `pm2 status` (VPS) or check Railway/Render logs
2. Verify `TELEGRAM_BOT_TOKEN` is correct
3. Ensure bot has been started in Telegram (send `/start`)

### Database errors
1. Check file permissions: `chmod 644 pyclaw.db`
2. Ensure `schema.sql` exists
3. Delete database and restart to recreate

### Plugin errors
1. Verify API keys in `.env`
2. Check feature flags are enabled
3. Review logs for specific error messages

### Deployment issues
- **Railway**: Check build logs, ensure all env vars are set
- **Render**: Verify build/start commands match `Procfile`
- **VPS**: Check PM2 logs with `pm2 logs pyclaw`

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore` already
2. **Rotate API keys regularly** - Especially if exposed
3. **Enable moderation** - Keeps content safe
4. **Monitor logs** - Check for unusual activity
5. **Update dependencies** - Run `pip install --upgrade -r requirements.txt` periodically

---

## 📝 License

MIT License - Feel free to fork, modify, and use for personal or commercial projects.

---

## 🤝 Contributing

Contributions welcome! Here's how:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 💬 Support

### Issues
Found a bug? Have a suggestion? [Open an issue on GitHub](https://github.com/yourusername/pyclaw-supercharged/issues)

### Questions
- Check this README first
- Review the code comments
- Ask in GitHub Discussions

---

## 🎯 Roadmap

**Planned Features:**
- [ ] Voice message support
- [ ] Image generation integration
- [ ] Scheduled reminders
- [ ] Multi-language support
- [ ] Web dashboard for management
- [ ] Advanced analytics
- [ ] Custom plugin marketplace

---

## 📚 Resources

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [Anthropic API Documentation](https://docs.anthropic.com)
- [Python Telegram Bot Library](https://python-telegram-bot.org)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

## 🌟 Acknowledgments

Built with:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot framework
- [Anthropic Claude](https://www.anthropic.com/claude) - AI engine
- [SQLite](https://www.sqlite.org/) - Database
- Inspired by OpenClaw

---

## 📞 Contact

**Project Maintainer:** Your Name  
**GitHub:** [@yourusername](https://github.com/yourusername)  
**Project Link:** [github.com/yourusername/pyclaw-supercharged](https://github.com/yourusername/pyclaw-supercharged)

---

**Built with ❤️ using Python, Telegram, and Claude AI**

*Last Updated: February 2026*
