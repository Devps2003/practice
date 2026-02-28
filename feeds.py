"""
Curated RSS/Atom feeds and content fetching for the Daily Brief.
Optimized for a founding engineer at a fintech company.
"""

import feedparser
import json
import hashlib
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

CACHE_DIR = Path(__file__).parent / ".cache"
CACHE_DIR.mkdir(exist_ok=True)

# ── Curated Feed Sources ─────────────────────────────────────────────
# Each feed has: url, category, priority (1=must-read, 2=important, 3=nice-to-have)

FEEDS = [
    # ── FINTECH & PAYMENTS ──
    {"url": "https://techcrunch.com/category/fintech/feed/", "category": "fintech", "source": "TechCrunch Fintech", "priority": 1},
    {"url": "https://www.finextra.com/rss/headlines.aspx", "category": "fintech", "source": "Finextra", "priority": 1},
    {"url": "https://inc42.com/category/fintech/feed/", "category": "fintech", "source": "Inc42 Fintech", "priority": 1},
    {"url": "https://entrackr.com/category/fintech/feed/", "category": "fintech", "source": "Entrackr Fintech", "priority": 2},
    {"url": "https://restofworld.org/feed/", "category": "fintech", "source": "Rest of World", "priority": 2},
    
    # ── AI & MACHINE LEARNING ──
    {"url": "https://blog.google/technology/ai/rss/", "category": "ai", "source": "Google AI Blog", "priority": 1},
    {"url": "https://openai.com/blog/rss/", "category": "ai", "source": "OpenAI Blog", "priority": 1},
    {"url": "https://techcrunch.com/category/artificial-intelligence/feed/", "category": "ai", "source": "TechCrunch AI", "priority": 1},
    {"url": "https://www.technologyreview.com/feed/", "category": "ai", "source": "MIT Tech Review", "priority": 2},
    {"url": "https://simonwillison.net/atom/everything/", "category": "ai", "source": "Simon Willison", "priority": 2},
    
    # ── ENGINEERING & ARCHITECTURE ──
    {"url": "https://martinfowler.com/feed.atom", "category": "engineering", "source": "Martin Fowler", "priority": 1},
    {"url": "https://blog.pragmaticengineer.com/rss/", "category": "engineering", "source": "Pragmatic Engineer", "priority": 1},
    {"url": "https://netflixtechblog.com/feed", "category": "engineering", "source": "Netflix Tech Blog", "priority": 1},
    {"url": "https://engineering.fb.com/feed/", "category": "engineering", "source": "Meta Engineering", "priority": 2},
    {"url": "https://aws.amazon.com/blogs/architecture/feed/", "category": "engineering", "source": "AWS Architecture", "priority": 2},
    {"url": "https://www.infoq.com/feed/", "category": "engineering", "source": "InfoQ", "priority": 2},
    {"url": "https://github.blog/feed/", "category": "engineering", "source": "GitHub Blog", "priority": 3},
    {"url": "https://stripe.com/blog/feed.rss", "category": "engineering", "source": "Stripe Blog", "priority": 1},
    
    # ── BUSINESS & ENTREPRENEURSHIP ──
    {"url": "https://review.firstround.com/feed.xml", "category": "business", "source": "First Round Review", "priority": 1},
    {"url": "https://a16z.com/feed/", "category": "business", "source": "a16z", "priority": 1},
    {"url": "https://www.ycombinator.com/blog/rss/", "category": "business", "source": "Y Combinator", "priority": 1},
    {"url": "https://hbr.org/feed", "category": "business", "source": "Harvard Business Review", "priority": 2},
    {"url": "https://bothsidesofthetable.com/feed", "category": "business", "source": "Both Sides of the Table", "priority": 2},
    
    # ── INDIA STARTUP & TECH ──
    {"url": "https://inc42.com/feed/", "category": "india_tech", "source": "Inc42", "priority": 1},
    {"url": "https://yourstory.com/feed", "category": "india_tech", "source": "YourStory", "priority": 2},
    {"url": "https://entrackr.com/feed/", "category": "india_tech", "source": "Entrackr", "priority": 2},
]

CATEGORY_LABELS = {
    "fintech": {"emoji": "💰", "name": "Fintech & Payments"},
    "ai": {"emoji": "🤖", "name": "AI & Engineering"},
    "engineering": {"emoji": "⚙️", "name": "Engineering Deep-Dives"},
    "business": {"emoji": "📈", "name": "Business & Entrepreneurship"},
    "india_tech": {"emoji": "🇮🇳", "name": "India Startup Ecosystem"},
}


def _fetch_single_feed(feed_config: dict, max_entries: int = 5) -> list:
    """Fetch entries from a single RSS feed."""
    try:
        parsed = feedparser.parse(feed_config["url"])
        articles = []
        for entry in parsed.entries[:max_entries]:
            # Extract date
            published = ""
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                try:
                    published = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
                except Exception:
                    published = ""
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                try:
                    published = datetime(*entry.updated_parsed[:6]).strftime("%Y-%m-%d")
                except Exception:
                    published = ""
            
            # Extract summary (clean HTML)
            summary = ""
            if hasattr(entry, "summary"):
                summary = entry.summary
                # Basic HTML strip
                import re
                summary = re.sub(r'<[^>]+>', '', summary)
                summary = summary[:300].strip()
            
            articles.append({
                "title": entry.get("title", "Untitled"),
                "link": entry.get("link", ""),
                "summary": summary,
                "published": published,
                "source": feed_config["source"],
                "category": feed_config["category"],
                "priority": feed_config["priority"],
            })
        return articles
    except Exception as e:
        return []


def fetch_all_feeds(max_per_feed: int = 4) -> dict:
    """Fetch all feeds in parallel. Returns articles grouped by category.
    Uses in-memory cache (for Streamlit Cloud) and optional file cache (local dev).
    """
    import streamlit as st
    cache_key = f"feeds_{date.today().isoformat()}"

    # 1. Check in-memory (session_state) cache first — works on Streamlit Cloud
    if hasattr(st, "session_state"):
        sc = getattr(st.session_state, "feed_cache", {})
        if cache_key in sc:
            cached = sc[cache_key]
            age = datetime.now().timestamp() - cached.get("fetched_at", 0)
            if age < 6 * 3600:
                return cached["articles"]

    # 2. Check file cache (local dev)
    cache_file = CACHE_DIR / f"{cache_key}.json"
    if cache_file.exists():
        try:
            cached = json.loads(cache_file.read_text())
            cache_age = datetime.now().timestamp() - cached.get("fetched_at", 0)
            if cache_age < 6 * 3600:  # 6 hours
                return cached["articles"]
        except Exception:
            pass
    
    all_articles = []
    
    # Fetch in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(_fetch_single_feed, feed, max_per_feed): feed
            for feed in FEEDS
        }
        for future in as_completed(futures, timeout=30):
            try:
                articles = future.result(timeout=10)
                all_articles.extend(articles)
            except Exception:
                continue
    
    # Group by category
    grouped = {}
    for cat_key in CATEGORY_LABELS:
        cat_articles = [a for a in all_articles if a["category"] == cat_key]
        # Sort by priority then date
        cat_articles.sort(key=lambda x: (x["priority"], x.get("published", "") or ""), reverse=False)
        # Priority first (1 before 2), then newest date
        cat_articles.sort(key=lambda x: x["priority"])
        # Deduplicate by title similarity
        seen_titles = set()
        deduped = []
        for a in cat_articles:
            title_key = a["title"].lower()[:50]
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                deduped.append(a)
        grouped[cat_key] = deduped[:8]  # Max 8 per category
    
    payload = {"fetched_at": datetime.now().timestamp(), "articles": grouped}

    # Save to in-memory cache (session_state)
    try:
        if hasattr(st, "session_state"):
            if not hasattr(st.session_state, "feed_cache"):
                st.session_state.feed_cache = {}
            st.session_state.feed_cache[cache_key] = payload
    except Exception:
        pass

    # Also save to file (local dev, silently skip on cloud)
    try:
        cache_file.write_text(json.dumps(payload, indent=2))
        for f in CACHE_DIR.glob("feeds_*.json"):
            if f.name != f"{cache_key}.json":
                f.unlink()
    except Exception:
        pass

    return grouped


def get_daily_brief_prompt(articles: dict) -> str:
    """Create a prompt for the LLM to generate a curated daily brief."""
    article_text = ""
    for cat_key, cat_articles in articles.items():
        if not cat_articles:
            continue
        label = CATEGORY_LABELS[cat_key]
        article_text += f"\n### {label['emoji']} {label['name']}\n"
        for a in cat_articles[:5]:
            article_text += f"- **{a['title']}** ({a['source']}) — {a['summary'][:150]}\n"
            if a.get("link"):
                article_text += f"  Link: {a['link']}\n"
    
    prompt = f"""You are creating a **Daily Brief** for a founding engineer who is joining a fintech company (Edviron — payment aggregator for education) in 3 months.

Their goal: Become the best founding engineer possible in 6 months. They spend 15-20 minutes reading this daily.

Here are today's articles from curated sources:
{article_text}

Create a structured daily brief with these sections:

## 🔥 Today's Must-Reads (pick the 3-4 most important articles for THIS person)
For each, write:
- Why it matters for them specifically
- One key takeaway they should remember
- Include the link

## 💰 Fintech & Payments Pulse
- 2-3 key developments relevant to payments, fintech regulation, or payment aggregators
- Connect to their Edviron context where possible

## 🤖 AI & Tech Watch
- 1-2 AI developments that an engineer should know about
- Focus on practical applications, not hype

## 📈 Business & Strategy Insight
- 1 business/entrepreneurship insight they can apply
- Think: what would a founder/CTO care about?

## 🧠 Today's Learning Nugget
- Pick ONE concept from today's articles and explain it in 2-3 paragraphs
- Make it a mini-lesson they'll remember

## ⚡ Action Item
- One specific thing they should DO today based on what they read
- Could be: research something, implement something, write something, read a specific paper

Keep it concise, scannable, and high-signal. No fluff. Use bullet points.
Target reading time: 15-20 minutes.
Include all relevant links so they can deep-dive if interested."""
    
    return prompt


def get_cached_brief(today_str: str) -> Optional[str]:
    """Get cached daily brief if it exists."""
    brief_file = CACHE_DIR / f"brief_{today_str}.md"
    if brief_file.exists():
        return brief_file.read_text()
    return None


def save_brief(today_str: str, brief: str):
    """Cache the daily brief."""
    brief_file = CACHE_DIR / f"brief_{today_str}.md"
    try:
        brief_file.write_text(brief)
    except Exception:
        pass
    # Clean old briefs
    try:
        for f in CACHE_DIR.glob("brief_*.md"):
            if f.name != f"brief_{today_str}.md":
                f.unlink()
    except Exception:
        pass
