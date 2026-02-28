# ⚡ Founding Engineer HQ

**Principal Engineer Coach + Daily Brief** — Your personal training platform to become a world-class founding engineer.

## 🎯 What This Is

- **Adaptive Learning Coach**: Gets harder as you improve, tracks your progress
- **Daily Brief**: Curated 15-min reading from 25+ sources (fintech, AI, engineering, startups)
- **Voice Input**: Speak your answers, get instant feedback
- **Progress Tracking**: Level up from SDE-1 → Principal Engineer

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys:**
   - Create `.streamlit/secrets.toml`:
     ```toml
     GROQ_API_KEY = "your_groq_key_here"
     LLM_PROVIDER = "groq"
     ```
   - Or create `.env`:
     ```
     GROQ_API_KEY=your_groq_key_here
     LLM_PROVIDER=groq
     ```

3. **Run:**
   ```bash
   streamlit run app.py
   ```

4. **Open:** http://localhost:8501

### Deploy to Streamlit Cloud

See **[DEPLOY.md](./DEPLOY.md)** for step-by-step instructions.

---

## 📁 Project Structure

```
founding-engineer-coach/
├── app.py              # Main Streamlit app
├── context.py          # Edviron context & system prompts
├── feeds.py            # RSS feed parser & daily brief
├── requirements.txt   # Python dependencies
├── .streamlit/
│   ├── config.toml    # Streamlit config
│   └── secrets.toml   # API keys (gitignored)
├── .env                # Local dev keys (gitignored)
├── learning_profile.json  # Your progress (gitignored)
└── DEPLOY.md           # Deployment guide
```

---

## 🔑 Getting API Keys

**Groq (Recommended — Free, Fast):**
1. Go to [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up (free)
3. Create API key
4. Copy to `.streamlit/secrets.toml` or `.env`

**Gemini (Optional Fallback):**
1. Go to [ai.google.dev](https://ai.google.dev)
2. Get API key
3. Add `GEMINI_API_KEY` to secrets

---

## 🎓 Features

### Coach Tab
- **Category-based challenges**: Architecture, System Design, Fintech, etc.
- **Adaptive difficulty**: Questions get harder as you level up
- **Edviron-specific**: 40% Edviron context, 60% general engineering
- **Voice input**: Speak your answers, get transcribed automatically
- **Progress tracking**: Scores, streaks, weak areas identified

### Daily Brief Tab
- **25+ curated sources**: Fintech, AI, Engineering, Business, India Startups
- **AI-curated**: Personalized 15-min reading optimized for your goals
- **Fresh daily**: New brief every day, cached for convenience

### Progress Tab
- **Dashboard**: Sessions, challenges, streak, average score
- **Category breakdown**: See where you're strong/weak
- **AI assessment**: Get personalized feedback and 5-day plan
- **Export/Import**: Backup your progress as JSON

---

## 🔒 Security

- ✅ API keys stored in Streamlit Secrets (cloud) or `.env` (local)
- ✅ `.gitignore` excludes secrets and personal data
- ✅ Profile data stays in `session_state` (ephemeral on cloud)

---

## 📝 License

Private — Internal use only.

---

## 🆘 Support

- **Deployment issues?** See [DEPLOY.md](./DEPLOY.md)
- **API errors?** Check your keys in Streamlit Cloud Secrets
- **Profile lost?** Use Export/Import in sidebar

---

**Built for becoming the best founding engineer. 🚀**
