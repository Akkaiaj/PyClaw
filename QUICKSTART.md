# 🚀 PyClaw Supercharged - Quick Start

## ⚡ Get Running in 5 Minutes

### Step 1: Get API Keys (2 minutes)

1. **Telegram Bot Token:**
   - Open Telegram, search `@BotFather`
   - Send `/newbot`, follow prompts
   - Copy the token

2. **Anthropic API Key:**
   - Visit [console.anthropic.com](https://console.anthropic.com)
   - Sign up/login
   - Go to API Keys → Create Key
   - Copy the key

### Step 2: Setup (2 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
nano .env  # or use any text editor

# Add your keys:
TELEGRAM_BOT_TOKEN=paste_your_telegram_token_here
ANTHROPIC_API_KEY=paste_your_anthropic_key_here
```

### Step 3: Run (1 minute)

```bash
python bot.py
```

That's it! 🎉

### Step 4: Test

1. Open Telegram
2. Search for your bot (name you gave BotFather)
3. Send `/start`
4. Chat with your AI!

---

## 🌐 Deploy to Cloud (5 minutes)

### Railway (Easiest)

1. Push this code to GitHub
2. Go to [railway.app](https://railway.app)
3. New Project → Deploy from GitHub
4. Add environment variables (copy from `.env`)
5. Done! ✅

### Render

1. Push to GitHub
2. [render.com](https://render.com) → New Web Service
3. Connect repo
4. Build: `pip install -r requirements.txt`
5. Start: `python bot.py`
6. Add env vars
7. Deploy! ✅

---

## 🎮 First Steps

Try these commands in your bot:

```
/start          - See all features
/friendly       - Switch to friendly mode
/remember name My name is John
/recall name    - Bot remembers!
/trivia         - Play a game
/weather Tokyo  - Get weather (needs API key)
```

---

## ❓ Troubleshooting

**Bot doesn't start?**
- Check Python version: `python --version` (need 3.9+)
- Check API keys in `.env`
- Look at error messages

**Bot doesn't respond?**
- Did you send `/start` to bot in Telegram?
- Check bot is running (terminal should show logs)
- Verify token is correct

**Need help?**
- Read full `README.md`
- Check the code comments
- Open GitHub issue

---

## 🎯 Next Steps

1. **Try all agents** - `/friendly`, `/expert`, `/researcher`, `/creative`
2. **Build knowledge base** - Use `/remember` for important facts
3. **Add optional plugins** - Get API keys for weather, news, search
4. **Deploy to cloud** - Make it 24/7 available
5. **Customize** - Edit agents in `agents/` directory

---

**Happy botting! 🤖**
