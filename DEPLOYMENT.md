# 🚢 Deployment Guide

Complete deployment guide for PyClaw Supercharged on various platforms.

---

## 📋 Pre-Deployment Checklist

- [ ] Tested locally
- [ ] All API keys obtained
- [ ] `.env` configured
- [ ] Code pushed to GitHub (for cloud deployment)
- [ ] README.md reviewed

---

## 1️⃣ Railway Deployment (Recommended)

**Why Railway?**
- ✅ Free $5/month credit
- ✅ Auto-deploys from GitHub
- ✅ Easy environment variables
- ✅ Built-in logging

### Steps:

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your-repo-url
   git push -u origin main
   ```

2. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

3. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your pyclaw-supercharged repo

4. **Add Environment Variables**
   - Click on your service
   - Go to "Variables" tab
   - Add each variable from `.env.example`:
     ```
     TELEGRAM_BOT_TOKEN=your_token
     ANTHROPIC_API_KEY=your_key
     # ... add all others
     ```

5. **Deploy**
   - Railway auto-detects `Procfile`
   - Deployment starts automatically
   - Check "Deployments" tab for status

6. **View Logs**
   - Click "View Logs" to see bot output
   - Should see "🚀 PyClaw Supercharged starting..."

7. **Test**
   - Open Telegram
   - Send `/start` to your bot
   - Should respond immediately

### Railway Tips:

- **Free tier limits:** 500 hours/month, $5 credit
- **Database:** SQLite persists with Railway volumes
- **Updates:** Push to GitHub → auto-redeploys
- **Logs:** View in real-time from dashboard

---

## 2️⃣ Render Deployment

**Why Render?**
- ✅ Free tier available
- ✅ Simple setup
- ✅ Good documentation

### Steps:

1. **Push to GitHub** (same as Railway step 1)

2. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

3. **New Web Service**
   - Dashboard → "New +"
   - Select "Web Service"

4. **Connect Repository**
   - Choose your pyclaw-supercharged repo
   - Give it a name

5. **Configure Build**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Instance Type:** Free

6. **Environment Variables**
   - Scroll to "Environment Variables"
   - Click "Add Environment Variable"
   - Add all from `.env.example`

7. **Create Web Service**
   - Click "Create Web Service"
   - Wait for build (~2-3 minutes)

8. **Check Logs**
   - View logs from dashboard
   - Should see bot starting

### Render Tips:

- **Free tier:** Service sleeps after 15 min inactivity
- **Upgrade:** $7/month for always-on
- **Database:** Persists on paid tier
- **Manual redeploy:** Use dashboard button

---

## 3️⃣ VPS Deployment (DigitalOcean, Linode, Vultr)

**Why VPS?**
- ✅ Full control
- ✅ Always on
- ✅ More resources
- ❌ Requires server management

### Recommended: DigitalOcean

**Cost:** $6/month for basic droplet

### Steps:

1. **Create Droplet**
   - Go to [digitalocean.com](https://digitalocean.com)
   - Create → Droplets
   - **Image:** Ubuntu 22.04 LTS
   - **Plan:** Basic ($6/mo)
   - **Location:** Closest to you
   - **Authentication:** SSH key or password
   - Create Droplet

2. **Connect to Server**
   ```bash
   ssh root@your_droplet_ip
   ```

3. **Update System**
   ```bash
   apt update && apt upgrade -y
   ```

4. **Install Dependencies**
   ```bash
   # Python and pip
   apt install python3-pip python3-venv git -y
   
   # Node.js (for PM2)
   curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
   apt install -y nodejs
   
   # PM2 (process manager)
   npm install -g pm2
   ```

5. **Clone Repository**
   ```bash
   cd /opt
   git clone https://github.com/yourusername/pyclaw-supercharged.git
   cd pyclaw-supercharged
   ```

6. **Setup Virtual Environment** (optional but recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

7. **Install Python Packages**
   ```bash
   pip install -r requirements.txt
   ```

8. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env
   ```
   - Add all your API keys
   - Save: Ctrl+X, Y, Enter

9. **Test Run**
   ```bash
   python3 bot.py
   ```
   - Check for errors
   - Press Ctrl+C to stop

10. **Run with PM2**
    ```bash
    pm2 start bot.py --interpreter python3 --name pyclaw
    pm2 save
    pm2 startup
    ```
    - Follow the instruction from `pm2 startup`

11. **Verify Running**
    ```bash
    pm2 status
    pm2 logs pyclaw
    ```

12. **Setup Auto-Restart**
    - PM2 already handles this
    - Bot restarts on crash
    - Survives server reboot

### VPS Management Commands:

```bash
# View logs
pm2 logs pyclaw

# Restart bot
pm2 restart pyclaw

# Stop bot
pm2 stop pyclaw

# Update code
cd /opt/pyclaw-supercharged
git pull
pm2 restart pyclaw

# Monitor resources
pm2 monit
```

### VPS Security Tips:

1. **Setup Firewall**
   ```bash
   ufw allow ssh
   ufw enable
   ```

2. **Create Non-Root User**
   ```bash
   adduser botuser
   usermod -aG sudo botuser
   ```

3. **Use SSH Keys** (not passwords)

4. **Keep Updated**
   ```bash
   apt update && apt upgrade -y
   ```

---

## 4️⃣ Heroku Deployment (Alternative)

**Note:** Heroku removed free tier, but paid tier is $7/month

### Steps:

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login**
   ```bash
   heroku login
   ```

3. **Create App**
   ```bash
   cd pyclaw-supercharged
   heroku create your-bot-name
   ```

4. **Add Environment Variables**
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=your_token
   heroku config:set ANTHROPIC_API_KEY=your_key
   # ... add all others
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **View Logs**
   ```bash
   heroku logs --tail
   ```

---

## 🔍 Post-Deployment Checklist

After deploying, verify:

- [ ] Bot responds to `/start`
- [ ] All commands work
- [ ] Database persists (test with `/remember` → restart → `/recall`)
- [ ] Logs show no errors
- [ ] Agent switching works
- [ ] Optional plugins work (if configured)

---

## 📊 Monitoring

### Railway
- Dashboard → View Logs
- Check "Metrics" for resource usage

### Render
- Dashboard → Logs tab
- Metrics available on paid tier

### VPS
```bash
# PM2 monitoring
pm2 monit

# Check disk space
df -h

# Check memory
free -h

# View process
top
```

---

## 🐛 Common Deployment Issues

### 1. Bot doesn't start

**Check:**
- Environment variables set correctly
- Python version (must be 3.9+)
- All dependencies installed
- View logs for specific error

**Fix:**
- Railway/Render: Check environment variables tab
- VPS: `pm2 logs pyclaw --err`

### 2. Database errors

**Symptoms:** Can't remember/recall facts

**Fix:**
- Ensure SQLite is installed
- Check file permissions (VPS)
- Verify `schema.sql` exists
- Railway/Render: May need paid tier for persistence

### 3. Plugin failures

**Symptoms:** Weather/news commands fail

**Fix:**
- Verify API keys in environment
- Check feature flags (`ENABLE_WEATHER=true`)
- Review plugin-specific logs

### 4. Memory issues

**Symptoms:** Bot crashes randomly

**Fix:**
- Upgrade to larger instance
- Check for memory leaks in logs
- Reduce `MAX_CONVERSATION_HISTORY`

---

## 🔄 Updating Deployed Bot

### Railway/Render (GitHub Auto-Deploy)
```bash
git add .
git commit -m "Update feature"
git push
# Auto-deploys!
```

### VPS (Manual Update)
```bash
ssh root@your_server
cd /opt/pyclaw-supercharged
git pull
pm2 restart pyclaw
```

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Railway** | $5 credit/mo | $5+ usage | Personal use, testing |
| **Render** | Limited (sleeps) | $7/mo | Small projects |
| **DigitalOcean** | None | $6/mo | Production, control |
| **Heroku** | None | $7/mo | Simplicity |

---

## 🎯 Recommendations

**For Testing:** Railway (free $5 credit)  
**For Personal Use:** Render ($7/mo)  
**For Production:** DigitalOcean VPS ($6/mo)  
**For Simplicity:** Railway or Render

---

## 📞 Need Help?

- Check platform-specific documentation
- Review logs for error messages
- Open GitHub issue
- Search Stack Overflow

---

**Happy Deploying! 🚀**
