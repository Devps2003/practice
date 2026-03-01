# 🚀 Deployment Guide — Streamlit Cloud

## Quick Deploy (5 minutes)

### Step 1: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `founding-engineer-hq` (or any name)
3. **Make it PRIVATE** (contains API keys in secrets)
4. Click "Create repository"
5. **Copy the repository URL** (e.g., `https://github.com/yourusername/founding-engineer-hq.git`)

### Step 2: Push Code to GitHub

```bash
cd /Users/devps/Desktop/founding-engineer-coach

# Initialize git
git init
git add .
git commit -m "Initial commit: Founding Engineer HQ"

# Add your GitHub repo as remote
git remote add origin https://github.com/yourusername/founding-engineer-hq.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note:** `.env` and `learning_profile.json` are already in `.gitignore` — they won't be pushed.

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your **GitHub account**
3. Click **"New app"**
4. Fill in:
   - **Repository**: Select `yourusername/founding-engineer-hq`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: `founding-engineer-hq` (or your choice)
5. Click **"Advanced settings"** → **"Secrets"**
6. Paste this (replace placeholders with your actual values):

```toml
GROQ_API_KEY = "your_groq_api_key_here"
LLM_PROVIDER = "groq"
APP_PASSWORD = "your_login_password_here"
```

**Get your Groq API key:** [console.groq.com/keys](https://console.groq.com/keys)
**APP_PASSWORD** — this locks the app so only you can access it.

7. Click **"Deploy"** → Wait ~2 minutes

### Step 4: Add to Phone Home Screen

**iPhone:**
1. Open the Streamlit Cloud URL in **Safari**
2. Tap **Share** button (square with arrow)
3. Tap **"Add to Home Screen"**
4. Name it "Engineer HQ" → **Add**

**Android:**
1. Open the URL in **Chrome**
2. Tap **Menu** (3 dots) → **"Add to Home screen"**
3. Name it → **Add**

---

## 🔒 Security Checklist

- ✅ `.env` is in `.gitignore` (won't be pushed)
- ✅ `.streamlit/secrets.toml` is in `.gitignore` (won't be pushed)
- ✅ `learning_profile.json` is in `.gitignore` (personal data)
- ✅ API keys & password go in Streamlit Cloud **Secrets** (not in code)
- ✅ `APP_PASSWORD` locks the app — only you can access it
- ✅ Repository should be **PRIVATE** on GitHub

---

## 📝 Files Included in Deployment

- ✅ `app.py` — Main app (coach + academy + daily brief + progress)
- ✅ `context.py` — Edviron context, 14 challenge categories, prompts
- ✅ `ai_curriculum.py` — 222 topics across 20 sections (AI + Leadership + Business + Product + Communication + Edviron)
- ✅ `feeds.py` — RSS feed parser
- ✅ `requirements.txt` — Dependencies
- ✅ `.streamlit/config.toml` — Streamlit config
- ✅ `.gitignore` — Excludes secrets & profile

---

## 🐛 Troubleshooting

**"Module not found" errors:**
- Check `requirements.txt` has all packages
- Streamlit Cloud auto-installs from `requirements.txt`

**"No secrets found":**
- Go to App Settings → Secrets
- Make sure format is exactly:
  ```toml
  GROQ_API_KEY = "your_key"
  LLM_PROVIDER = "groq"
  ```

**App won't start:**
- Check logs in Streamlit Cloud dashboard
- Common issue: `set_page_config()` must be first (already fixed)

**Profile not saving:**
- Profile saves to `session_state` (works on cloud)
- Use "Export Profile" in sidebar to backup
- Restore via "Restore Profile" button

---

## 🔄 Updating the App

After making changes:

```bash
cd /Users/devps/Desktop/founding-engineer-coach
git add .
git commit -m "Your update message"
git push origin main
```

Streamlit Cloud **auto-deploys** on every push to `main` branch.

---

## 📱 Accessing from Phone

Once deployed, bookmark the Streamlit Cloud URL:
- Format: `https://your-app-name.streamlit.app`
- Add to home screen for one-tap access

---

## 💡 Pro Tips

1. **Keep repo private** — contains business context
2. **Export profile regularly** — backup your progress
3. **Use Streamlit Cloud Secrets** — never commit API keys
4. **Monitor usage** — Groq free tier is generous but has limits

---

**Need help?** Check Streamlit Cloud docs: [docs.streamlit.io/streamlit-community-cloud](https://docs.streamlit.io/streamlit-community-cloud)
