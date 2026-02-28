"""
Founding Engineer HQ — Principal Engineer Coach + Daily Brief
Streamlit Cloud-ready, voice-enabled, adaptive learning platform.
"""

import streamlit as st

# ══════════════════════════════════════════════════════════════════════
# ── PAGE CONFIG — MUST be the VERY FIRST st.* call ───────────────────
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Founding Engineer HQ",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Now safe to do all other imports ────────────────────────────────
from groq import Groq
import google.generativeai as genai
import random
import json
import time
import os
import re
import tempfile
from datetime import datetime, date
from pathlib import Path
from typing import Optional

# ── Try importing optional packages gracefully ───────────────────────
try:
    from audio_recorder_streamlit import audio_recorder
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

try:
    from feeds import (
        fetch_all_feeds,
        get_daily_brief_prompt,
        CATEGORY_LABELS,
    )
    FEEDS_AVAILABLE = True
except ImportError:
    FEEDS_AVAILABLE = False

from context import (
    SYSTEM_PROMPT,
    CHALLENGE_CATEGORIES,
    DIFFICULTY_LEVELS,
    QUESTION_STYLES,
    WELCOME_MESSAGE,
)

# ══════════════════════════════════════════════════════════════════════
# ── CONFIG: Load API keys (Streamlit Secrets → .env → env vars) ──────
# ══════════════════════════════════════════════════════════════════════
def _load_env():
    """Load .env file for local development (silently skip if missing)."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())

_load_env()

def get_config(key: str, default: str = "") -> str:
    """Get config value: Streamlit Secrets > env vars > default.
    NOTE: only call AFTER set_page_config()."""
    try:
        val = st.secrets.get(key, "")
        if val:
            return str(val)
    except Exception:
        pass
    return os.environ.get(key, default)

GROQ_KEY   = get_config("GROQ_API_KEY")
GEMINI_KEY = get_config("GEMINI_API_KEY")
PROVIDER   = get_config("LLM_PROVIDER", "groq")

# ── CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { max-width: 860px; margin: 0 auto; }
    .block-container { padding-top: 1rem !important; padding-bottom: 0.5rem !important; }
    .streak-bar {
        background: linear-gradient(90deg,#ff6b35 0%,#f7c948 100%);
        border-radius: 8px; padding: 8px 16px; color:#000;
        font-weight:bold; text-align:center; margin: 6px 0;
    }
    .level-badge {
        background: linear-gradient(135deg,#667eea 0%,#764ba2 100%);
        border-radius: 20px; padding: 4px 16px; color:white;
        font-weight:bold; display:inline-block; margin: 4px 0;
    }
    .mic-row {
        display: flex; align-items: center; gap: 12px;
        padding: 8px 0; margin-bottom: 4px;
    }
    .mic-hint { color:#888; font-size:13px; margin-top:4px; }
    .section-hdr {
        font-size:17px; font-weight:bold; margin:16px 0 8px 0;
        padding-bottom:4px; border-bottom:1px solid #333;
    }
    @media(max-width:768px){
        .block-container{ padding-left:.8rem!important; padding-right:.8rem!important; }
    }
    div[data-testid="stChatMessage"]{ font-size:15px; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# ── PROFILE (session-state backed, JSON export for backup) ───────────
# ══════════════════════════════════════════════════════════════════════
PROFILE_PATH = Path(__file__).parent / "learning_profile.json"

_PROFILE_DEFAULTS = {
    "total_challenges": 0,
    "session_count": 0,
    "streak_days": 0,
    "last_session_date": None,
    "current_level": "sde1",
    "scores": [],
    "category_counts": {},
    "category_scores": {},
    "styles_used": [],
    "topics_covered": [],
    "level_up_suggestions": 0,
    "created_at": date.today().isoformat(),
    "briefs_read": 0,
}

def _load_profile_from_disk() -> dict:
    """Load from disk (local dev). Falls back to defaults."""
    if PROFILE_PATH.exists():
        try:
            saved = json.loads(PROFILE_PATH.read_text())
            for k, v in _PROFILE_DEFAULTS.items():
                if k not in saved:
                    saved[k] = v
            return saved
        except Exception:
            pass
    return dict(_PROFILE_DEFAULTS)

def save_profile(profile: dict):
    """Save to session_state; also persist to disk if possible."""
    st.session_state["profile"] = profile
    try:
        PROFILE_PATH.write_text(json.dumps(profile, indent=2))
    except Exception:
        pass  # Streamlit Cloud has ephemeral FS — silently ignore

def profile() -> dict:
    return st.session_state["profile"]


# ══════════════════════════════════════════════════════════════════════
# ── SESSION STATE INIT ───────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════
_defaults = {
    "profile": _load_profile_from_disk(),
    "messages": [],
    "api_configured": False,
    "groq_client": None,
    "gemini_model": None,
    "gemini_chat": None,
    "chat_history": [],
    "current_category": None,
    "challenge_active": False,
    "last_audio_hash": None,
    "fetched_articles": None,
    "daily_brief_cache": {},   # {date_str: brief_text}
    "brief_loading": False,
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ══════════════════════════════════════════════════════════════════════
# ── LLM HELPERS ─────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════
def _build_system_prompt() -> str:
    p = profile()
    level = p.get("current_level", "sde1")
    diff  = DIFFICULTY_LEVELS[level]
    prompt = SYSTEM_PROMPT.replace("{difficulty_modifier}", diff["prompt_modifier"])

    # Inject trainee's learning state
    cat_counts = p.get("category_counts", {})
    cat_scores = p.get("category_scores", {})
    ctx  = "\n## TRAINEE PROGRESS\n"
    ctx += f"- Level: {level}\n"
    ctx += f"- Challenges done: {p.get('total_challenges', 0)}\n"
    ctx += f"- Streak: {p.get('streak_days', 0)} days\n"

    if cat_counts:
        weak = []
        for cat in CHALLENGE_CATEGORIES:
            cnt = cat_counts.get(cat, 0)
            sc  = cat_scores.get(cat, [])
            avg = (sum(sc[-5:]) / len(sc[-5:])) if sc else 0
            ctx += f"- {cat}: {cnt} done, avg {avg:.1f}/5\n"
            if cnt < 3 or (sc and avg < 3.0):
                weak.append(cat)
        if weak:
            ctx += f"\nFOCUS AREAS: {', '.join(weak)}\n"

    recent_topics  = p.get("topics_covered", [])[-15:]
    recent_styles  = p.get("styles_used", [])[-3:]
    fresh_styles   = [s for s in QUESTION_STYLES if s not in recent_styles]
    if recent_topics:
        ctx += f"\nAvoid repeating topics: {', '.join(recent_topics)}\n"
    if fresh_styles:
        ctx += f"\nPrefer question style: {', '.join(fresh_styles[:4])}\n"

    return prompt + ctx


def configure_llm():
    """Configure LLM. Called once at startup and on level change."""
    try:
        if PROVIDER == "groq" and GROQ_KEY:
            os.environ["GROQ_API_KEY"] = GROQ_KEY
            st.session_state.groq_client = Groq()
            history = [{"role": "system", "content": _build_system_prompt()}]
            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "assistant"
                history.append({"role": role, "content": msg["content"]})
            st.session_state.chat_history = history
            st.session_state.api_configured = True
            return True
        elif PROVIDER == "gemini" and GEMINI_KEY:
            genai.configure(api_key=GEMINI_KEY)
            st.session_state.gemini_model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                system_instruction=_build_system_prompt(),
            )
            history = []
            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "model"
                history.append({"role": role, "parts": [msg["content"]]})
            st.session_state.gemini_chat = st.session_state.gemini_model.start_chat(history=history)
            st.session_state.api_configured = True
            return True
    except Exception as e:
        st.error(f"❌ LLM config failed: {e}")
    return False


def refresh_prompt():
    """Update system prompt after level change without clearing chat."""
    if PROVIDER == "groq" and st.session_state.get("groq_client"):
        new_prompt = _build_system_prompt()
        if st.session_state.chat_history and st.session_state.chat_history[0]["role"] == "system":
            st.session_state.chat_history[0]["content"] = new_prompt
        else:
            st.session_state.chat_history.insert(0, {"role": "system", "content": new_prompt})
    elif PROVIDER == "gemini":
        configure_llm()


def get_response(user_msg: str, max_retries: int = 3) -> str:
    """Send to coach LLM with retry + exponential backoff."""
    for attempt in range(max_retries):
        try:
            if PROVIDER == "groq":
                st.session_state.chat_history.append({"role": "user", "content": user_msg})
                resp = st.session_state.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.chat_history,
                    temperature=0.8,
                    max_tokens=4000,
                )
                msg = resp.choices[0].message.content
                st.session_state.chat_history.append({"role": "assistant", "content": msg})
                return msg
            else:
                return st.session_state.gemini_chat.send_message(user_msg).text
        except Exception as e:
            err = str(e)
            if "429" in err or "quota" in err.lower() or "rate" in err.lower():
                if attempt < max_retries - 1:
                    time.sleep((2 ** attempt) * 2)
                    continue
                return "⚠️ API quota exceeded. Wait a moment and try again."
            return f"⚠️ Error: {err}"
    return "⚠️ Max retries exceeded. Please try again."


def get_brief_llm(prompt: str, max_retries: int = 3) -> str:
    """Separate stateless LLM call for brief/assessment — doesn't pollute coach history."""
    system = "You are a content curator for a founding engineer. Be concise, high-signal, no fluff."
    for attempt in range(max_retries):
        try:
            if GROQ_KEY:
                os.environ["GROQ_API_KEY"] = GROQ_KEY
                c = Groq()
                resp = c.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.5,
                    max_tokens=4000,
                )
                return resp.choices[0].message.content
            elif GEMINI_KEY:
                genai.configure(api_key=GEMINI_KEY)
                m = genai.GenerativeModel("gemini-2.0-flash", system_instruction=system)
                return m.generate_content(prompt).text
            return "⚠️ No API key configured."
        except Exception as e:
            err = str(e)
            if "429" in err or "quota" in err.lower():
                if attempt < max_retries - 1:
                    time.sleep((2 ** attempt) * 3)
                    continue
                return "⚠️ API quota exceeded. Wait a minute and try again."
            return f"⚠️ Error: {err}"
    return "⚠️ Failed."


def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribe voice using Groq Whisper (free, fast, accurate)."""
    if not GROQ_KEY:
        return "⚠️ Groq API key required for voice transcription."
    try:
        os.environ["GROQ_API_KEY"] = GROQ_KEY
        client = Groq()
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_bytes)
            tmp = f.name
        try:
            with open(tmp, "rb") as af:
                result = client.audio.transcriptions.create(
                    model="whisper-large-v3-turbo",
                    file=af,
                    language="en",
                    response_format="text",
                )
            text = result if isinstance(result, str) else getattr(result, "text", str(result))
            return text.strip()
        finally:
            os.unlink(tmp)
    except Exception as e:
        return f"⚠️ Voice transcription failed: {str(e)}"


# ══════════════════════════════════════════════════════════════════════
# ── PROFILE HELPERS ──────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════
def update_streak():
    p = profile()
    today = date.today().isoformat()
    if p["last_session_date"] != today:
        last = p["last_session_date"]
        if last:
            delta = (date.today() - date.fromisoformat(last)).days
            if delta == 1:   p["streak_days"] += 1
            elif delta > 1:  p["streak_days"] = 1
        else:
            p["streak_days"] = 1
        p["last_session_date"] = today
        p["session_count"] += 1
        save_profile(p)


def record_challenge(category: str, topic: str, style: str):
    p = profile()
    p["total_challenges"] += 1
    p["category_counts"][category] = p["category_counts"].get(category, 0) + 1
    p["styles_used"] = (p["styles_used"] + [style])[-5:]
    p["topics_covered"] = (p["topics_covered"] + [topic])[-30:]
    save_profile(p)


def record_score(category: str, score: int):
    if not (1 <= score <= 5):
        return
    p = profile()
    if category not in p["category_scores"]:
        p["category_scores"][category] = []
    p["category_scores"][category] = (p["category_scores"][category] + [score])[-20:]
    p["scores"] = (p["scores"] + [{"score": score, "category": category, "date": date.today().isoformat()}])[-100:]
    save_profile(p)
    # Check level up eligibility
    _check_level_up(p)


def _check_level_up(p: dict):
    level = p["current_level"]
    lc = DIFFICULTY_LEVELS[level]
    if p["total_challenges"] < lc.get("promote_at", 999):
        return
    recent = [s["score"] for s in p["scores"][-10:] if s.get("score", 0) > 0]
    if recent and (sum(recent) / len(recent)) >= lc.get("min_score_to_promote", 5.0):
        p["level_up_suggestions"] = p.get("level_up_suggestions", 0) + 1


def extract_score(text: str) -> int:
    for pat in [r'\*\*Score:\s*(\d)/5\*\*', r'Score:\s*(\d)/5', r'\*\*(\d)/5\*\*', r'(\d)/5']:
        m = re.search(pat, text)
        if m:
            s = int(m.group(1))
            if 1 <= s <= 5:
                return s
    return 0


def get_suggested_level() -> tuple:
    p = profile()
    level = p["current_level"]
    lc = DIFFICULTY_LEVELS[level]
    total, promote_at, min_score = p["total_challenges"], lc.get("promote_at", 999), lc.get("min_score_to_promote", 5.0)
    if total < promote_at:
        return None, f"{promote_at - total} more challenges to next level"
    recent = [s["score"] for s in p["scores"][-10:] if s.get("score", 0) > 0]
    if not recent:
        return None, "Need scored challenges"
    avg = sum(recent) / len(recent)
    if avg >= min_score:
        levels = list(DIFFICULTY_LEVELS.keys())
        idx = levels.index(level)
        if idx < len(levels) - 1:
            return levels[idx + 1], f"Avg {avg:.1f}/5 — ready to level up!"
    return None, f"Avg {avg:.1f}/5 (need {min_score}+ to advance)"


def get_weak_cats() -> list:
    p = profile()
    weak = []
    for cat in CHALLENGE_CATEGORIES:
        cnt = p["category_counts"].get(cat, 0)
        sc = p["category_scores"].get(cat, [])
        if cnt < 3:
            weak.append((cat, "underpracticed", cnt))
        elif sc and (sum(sc[-5:]) / len(sc[-5:])) < 3.0:
            weak.append((cat, f"avg {sum(sc[-5:])/len(sc[-5:]):.1f}/5", cnt))
    return weak


def get_strong_cats() -> list:
    p = profile()
    strong = []
    for cat in CHALLENGE_CATEGORIES:
        sc = p["category_scores"].get(cat, [])
        if len(sc) >= 3 and (sum(sc[-5:]) / len(sc[-5:])) >= 4.0:
            strong.append((cat, f"avg {sum(sc[-5:])/len(sc[-5:]):.1f}/5"))
    return strong


def smart_category() -> str:
    weak = get_weak_cats()
    if weak and random.random() < 0.6:
        return random.choice([w[0] for w in weak])
    return random.choice(list(CHALLENGE_CATEGORIES.keys()))


def fresh_style() -> str:
    recent = profile().get("styles_used", [])[-3:]
    pool = [s for s in QUESTION_STYLES if s not in recent] or QUESTION_STYLES
    return random.choice(pool)


def fresh_topic(cat_key: str) -> str:
    recent = set(profile().get("topics_covered", [])[-15:])
    topics = CHALLENGE_CATEGORIES[cat_key]["topics"]
    pool = [t for t in topics if t not in recent] or topics
    return random.choice(pool)


def _send_challenge(category: str, topic: str, style: str, is_edviron: Optional[bool] = None):
    """Build and send a challenge prompt, update state."""
    if is_edviron is None:
        is_edviron = random.random() < 0.4
    cat = CHALLENGE_CATEGORIES[category]
    level_name = DIFFICULTY_LEVELS[profile()["current_level"]]["name"]
    ctx = (
        "SPECIFICALLY about Edviron — reference actual code, files, and architecture."
        if is_edviron else
        "GENERAL engineering challenge — different company/domain, teach transferable skills."
    )
    prompt = (
        f"Give me a {style} style challenge from {cat['name']}. "
        f"Topic: {topic}. {ctx} "
        f"Include realistic names, numbers, timelines, constraints. "
        f"End with a clear, specific question. Difficulty: {level_name}."
    )
    st.session_state.current_category = category
    st.session_state.challenge_active = True
    record_challenge(category, topic, style)
    update_streak()
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})


def _handle_user_turn(user_input: str):
    """Record user message, get response, record score."""
    update_streak()
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)
    with st.chat_message("assistant", avatar="⚡"):
        with st.spinner("Thinking..."):
            response = get_response(user_input)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    score = extract_score(response)
    if score > 0 and st.session_state.current_category:
        record_score(st.session_state.current_category, score)


# ── Auto-configure on first load ────────────────────────────────────
if not st.session_state.api_configured:
    configure_llm()


# ══════════════════════════════════════════════════════════════════════
# ── SIDEBAR ──────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚡ Founding Engineer HQ")
    st.markdown("---")

    p = profile()
    level     = p["current_level"]
    lv_info   = DIFFICULTY_LEVELS[level]

    st.markdown(f'<div class="level-badge">{lv_info["emoji"]} {lv_info["name"]}</div>', unsafe_allow_html=True)
    st.caption(f"*{lv_info['description']}*")

    next_lv, prog_msg = get_suggested_level()
    if next_lv:
        st.success(f"🎉 Ready for **{DIFFICULTY_LEVELS[next_lv]['name']}**!")
        if st.button("⬆️ Level Up", key="sb_levelup", use_container_width=True, type="primary"):
            p["current_level"] = next_lv
            save_profile(p)
            refresh_prompt()
            st.rerun()
    else:
        st.caption(f"📈 {prog_msg}")

    st.markdown("---")
    st.markdown("### 🎯 Level")
    for key, lv in DIFFICULTY_LEVELS.items():
        if st.button(f"{lv['emoji']} {lv['name']}", key=f"sb_lv_{key}", use_container_width=True,
                     type="primary" if level == key else "secondary"):
            p["current_level"] = key
            save_profile(p)
            refresh_prompt()
            st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Stats")
    c1, c2 = st.columns(2)
    c1.metric("Sessions", p["session_count"])
    c2.metric("Challenges", p["total_challenges"])
    st.metric("🔥 Streak", f"{p['streak_days']} days")
    recent_sc = [s["score"] for s in p.get("scores", [])[-20:] if s.get("score", 0) > 0]
    if recent_sc:
        st.metric("Avg Score", f"{sum(recent_sc)/len(recent_sc):.1f}/5")

    weak, strong = get_weak_cats(), get_strong_cats()
    if weak:
        st.markdown("### 🎯 Focus")
        for ck, reason, _ in weak[:3]:
            st.caption(f"{CHALLENGE_CATEGORIES[ck]['emoji']} {CHALLENGE_CATEGORIES[ck]['name']} — {reason}")
    if strong:
        st.markdown("### 💪 Strengths")
        for ck, si in strong[:3]:
            st.caption(f"{CHALLENGE_CATEGORIES[ck]['emoji']} {CHALLENGE_CATEGORIES[ck]['name']} — {si}")

    st.markdown("---")

    # Profile backup / restore
    with st.expander("💾 Backup / Restore Profile"):
        st.caption("Export your progress to keep it safe.")
        st.download_button(
            "⬇️ Export Profile",
            data=json.dumps(p, indent=2),
            file_name=f"engineer_profile_{date.today().isoformat()}.json",
            mime="application/json",
            use_container_width=True,
        )
        uploaded = st.file_uploader("⬆️ Restore Profile", type=["json"], key="restore_upload")
        if uploaded:
            try:
                restored = json.loads(uploaded.read())
                save_profile(restored)
                st.success("Profile restored!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed: {e}")

    with st.expander("⚙️ Config"):
        st.caption(f"Provider: {PROVIDER}")
        st.caption(f"API: {'✅ Set' if st.session_state.api_configured else '❌ Missing'}")
        st.caption(f"Audio: {'✅' if AUDIO_AVAILABLE else '❌ (pip install audio-recorder-streamlit)'}")
        st.caption(f"Feeds: {'✅' if FEEDS_AVAILABLE else '❌ (pip install feedparser)'}")

    st.markdown("---")
    if st.button("🗑️ Reset Chat", use_container_width=True, key="sb_reset_chat"):
        st.session_state.messages = []
        st.session_state.challenge_active = False
        st.session_state.current_category = None
        st.session_state.last_audio_hash = None
        configure_llm()
        st.rerun()
    if st.button("🔄 Reset All Progress", use_container_width=True, key="sb_reset_all"):
        if PROFILE_PATH.exists():
            try: PROFILE_PATH.unlink()
            except: pass
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# ══════════════════════════════════════════════════════════════════════
# ── HEADER ───────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════
p = profile()
level   = p["current_level"]
lv_info = DIFFICULTY_LEVELS[level]

st.markdown("# ⚡ Founding Engineer HQ")
if p["streak_days"] > 0:
    st.markdown(
        f'<div class="streak-bar">🔥 {p["streak_days"]}-day streak — keep going!</div>',
        unsafe_allow_html=True,
    )

if not st.session_state.api_configured:
    st.error("""
**API key not set.**

**Local dev:** Create `.env` in the project folder:
```
GROQ_API_KEY=your_key_here
LLM_PROVIDER=groq
```

**Streamlit Cloud:** Go to App Settings → Secrets and add:
```
GROQ_API_KEY = "your_key_here"
LLM_PROVIDER = "groq"
```
Get a free Groq key: [console.groq.com/keys](https://console.groq.com/keys)
""")
    st.stop()


# ══════════════════════════════════════════════════════════════════════
# ── TABS ─────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════
tab_coach, tab_brief, tab_browse, tab_stats = st.tabs([
    "🎯 Coach", "📰 Daily Brief", "🔍 Articles", "📊 Progress"
])


# ══════════════════════════════════════════════════════════════════════
# ── TAB 1: COACH ─────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════
with tab_coach:
    st.markdown(f'<div class="level-badge">{lv_info["emoji"]} {lv_info["name"]}</div>', unsafe_allow_html=True)

    # Level up banner
    next_lv, _ = get_suggested_level()
    if next_lv:
        st.success(f"🎉 Ready to level up to **{DIFFICULTY_LEVELS[next_lv]['name']}**! →  See sidebar.")

    # ── Category buttons ────────────────────────────────────────────
    st.markdown("**Pick a training category:**")
    cols = st.columns(3)
    for i, (key, cat) in enumerate(CHALLENGE_CATEGORIES.items()):
        with cols[i % 3]:
            cnt = p["category_counts"].get(key, 0)
            label = f"{cat['emoji']} {cat['name']}" + (f" ({cnt})" if cnt else "")
            if st.button(label, key=f"cat_{key}", use_container_width=True):
                with st.spinner("Generating challenge..."):
                    _send_challenge(key, fresh_topic(key), fresh_style())
                st.rerun()

    # ── Quick actions ───────────────────────────────────────────────
    st.markdown("")
    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        if st.button("🎲 Random", use_container_width=True, key="qa_random",
                     help="Smart pick — biased toward weak areas"):
            ck = smart_category()
            with st.spinner("Generating..."):
                _send_challenge(ck, fresh_topic(ck), fresh_style())
            st.rerun()
    with qa2:
        if st.button("📚 Teach Me", use_container_width=True, key="qa_teach",
                     help="Deep-dive lesson on a weak area"):
            weak = get_weak_cats()
            ck = random.choice([w[0] for w in weak]) if weak else random.choice(list(CHALLENGE_CATEGORIES.keys()))
            topic = fresh_topic(ck)
            prompt = (
                f"Teach me about: **{topic}**. Explain from scratch with real-world examples and analogies. "
                f"Connect to Edviron codebase where relevant, but also teach the general concept. "
                f"Difficulty: {lv_info['name']}."
            )
            update_streak()
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Preparing lesson..."):
                resp = get_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": resp})
            st.rerun()
    with qa3:
        if st.button("🧠 Quiz Me", use_container_width=True, key="qa_quiz",
                     help="5 rapid-fire questions"):
            cats = random.sample(list(CHALLENGE_CATEGORIES.keys()), min(3, len(CHALLENGE_CATEGORIES)))
            cat_names = [CHALLENGE_CATEGORIES[c]["name"] for c in cats]
            prompt = (
                f"Rapid-fire quiz — 5 questions on: {', '.join(cat_names)}. "
                f"Mix Edviron-specific and general. Mix easy and hard. Number 1-5. "
                f"Difficulty: {lv_info['name']}."
            )
            for c in cats:
                record_challenge(c, "rapid_fire_quiz", "RAPID_FIRE")
            update_streak()
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Generating quiz..."):
                resp = get_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": resp})
            st.rerun()

    st.markdown("---")

    # ── Chat messages (scrollable container) ────────────────────────
    HIDDEN_PREFIXES = (
        "Give me a ", "Teach me about:", "Rapid-fire quiz",
        "Give me a detailed", "Progress assessment for",
    )
    chat_box = st.container(height=480)
    with chat_box:
        if not st.session_state.messages:
            st.markdown(WELCOME_MESSAGE)
        else:
            for msg in st.session_state.messages:
                if msg["role"] == "user" and msg["content"].startswith(HIDDEN_PREFIXES):
                    continue
                with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "⚡"):
                    st.markdown(msg["content"])

    # ── Input area: mic + text, side by side, BELOW chat ────────────
    mic_col, hint_col = st.columns([1, 9])
    with mic_col:
        if AUDIO_AVAILABLE:
            audio_bytes = audio_recorder(
                text="",
                icon_size="2x",
                recording_color="#ff6b35",
                neutral_color="#667eea",
                pause_threshold=2.5,
                key="voice_input",
            )
        else:
            audio_bytes = None
            st.caption("🎤")
    with hint_col:
        if AUDIO_AVAILABLE:
            st.caption("🎤 **Speak your answer** — click mic, talk, it auto-stops after 2s of silence.\nOr type below ↓")
        else:
            st.caption("Type your answer below ↓")

    # Handle voice input
    if AUDIO_AVAILABLE and audio_bytes:
        audio_hash = hash(audio_bytes)
        if st.session_state.last_audio_hash != audio_hash:
            st.session_state.last_audio_hash = audio_hash
            with st.spinner("🎤 Transcribing..."):
                transcribed = transcribe_audio(audio_bytes)
            if transcribed and not transcribed.startswith("⚠️"):
                st.info(f"🎤 **You said:** _{transcribed}_")
                _handle_user_turn(transcribed)
                st.rerun()
            else:
                st.warning(transcribed or "Couldn't transcribe. Please try again.")

    # Text input (always available, sticky at bottom)
    if user_text := st.chat_input("Type your answer or ask anything...", key="coach_text_input"):
        _handle_user_turn(user_text)
        st.rerun()


# ══════════════════════════════════════════════════════════════════════
# ── TAB 2: DAILY BRIEF ───────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════
with tab_brief:
    st.markdown("## 📰 Your Daily Brief")
    st.caption("Curated content optimized for your goal: best founding engineer in 6 months. ~15 min read.")
    st.markdown("---")

    today_str = date.today().isoformat()
    cached = st.session_state.daily_brief_cache.get(today_str)

    if cached:
        st.markdown(cached)
        st.markdown("---")
        col_regen, _ = st.columns([1, 3])
        with col_regen:
            if st.button("🔄 Regenerate", key="btn_regen"):
                del st.session_state.daily_brief_cache[today_str]
                st.rerun()
    else:
        if not FEEDS_AVAILABLE:
            st.warning("`feedparser` not installed. Run: `pip install feedparser`")
        else:
            st.info("Click to fetch today's articles from 25+ curated sources and generate your personalized brief.")
            if st.button("⚡ Generate Today's Brief", use_container_width=True, type="primary", key="btn_gen_brief"):
                with st.spinner("📡 Fetching from 25+ sources across fintech, AI, engineering, startups..."):
                    articles = fetch_all_feeds()
                total = sum(len(v) for v in articles.values())
                if total == 0:
                    st.error("Couldn't fetch articles. Check your internet connection and try again.")
                else:
                    st.success(f"✅ Fetched {total} articles — generating your personalized brief...")
                    with st.spinner("🤖 AI curating your brief..."):
                        prompt = get_daily_brief_prompt(articles)
                        brief  = get_brief_llm(prompt)
                    if brief and not brief.startswith("⚠️"):
                        st.session_state.daily_brief_cache[today_str] = brief
                        p = profile()
                        p["briefs_read"] = p.get("briefs_read", 0) + 1
                        save_profile(p)
                        st.rerun()
                    else:
                        st.error(brief)

    st.caption(f"📚 Total briefs read: {profile().get('briefs_read', 0)}")


# ══════════════════════════════════════════════════════════════════════
# ── TAB 3: BROWSE ARTICLES ───────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════
with tab_browse:
    st.markdown("## 🔍 Browse Latest Articles")
    st.caption("Raw feed from 25+ curated sources. Filter by category, click to read.")
    st.markdown("---")

    if not FEEDS_AVAILABLE:
        st.warning("`feedparser` not installed. Run: `pip install feedparser`")
    else:
        if CATEGORY_LABELS:
            all_cats = ["all"] + list(CATEGORY_LABELS.keys())
            sel_cat  = st.radio(
                "Category:",
                all_cats,
                format_func=lambda x: "📋 All" if x == "all" else f"{CATEGORY_LABELS[x]['emoji']} {CATEGORY_LABELS[x]['name']}",
                horizontal=True,
                key="browse_cat",
            )

        if st.button("📡 Fetch Latest", use_container_width=True, key="btn_fetch"):
            with st.spinner("Fetching articles from all sources..."):
                st.session_state.fetched_articles = fetch_all_feeds()

        arts = st.session_state.get("fetched_articles")
        if arts:
            for cat_key, cat_arts in arts.items():
                if sel_cat != "all" and cat_key != sel_cat:
                    continue
                if not cat_arts:
                    continue
                label = CATEGORY_LABELS.get(cat_key, {"emoji": "📄", "name": cat_key})
                st.markdown(f'<div class="section-hdr">{label["emoji"]} {label["name"]}</div>', unsafe_allow_html=True)
                for a in cat_arts:
                    title   = a.get("title", "Untitled")
                    link    = a.get("link", "")
                    source  = a.get("source", "")
                    summary = a.get("summary", "")[:220]
                    pub     = a.get("published", "")
                    st.markdown(f"**[{title}]({link})**" if link else f"**{title}**")
                    meta = f"*{source}*" + (f" · {pub}" if pub else "")
                    st.caption(meta)
                    if summary:
                        st.caption(summary + ("…" if len(a.get("summary", "")) > 220 else ""))
                    st.markdown("---")
        else:
            st.info("Click **Fetch Latest** to load articles.")


# ══════════════════════════════════════════════════════════════════════
# ── TAB 4: PROGRESS ──────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════
with tab_stats:
    p = profile()
    st.markdown("## 📊 Progress Dashboard")
    st.markdown("---")

    # Key metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Sessions",   p["session_count"])
    m2.metric("Challenges", p["total_challenges"])
    m3.metric("🔥 Streak",  f"{p['streak_days']}d")
    recent_sc = [s["score"] for s in p.get("scores", [])[-20:] if s.get("score", 0) > 0]
    m4.metric("Avg Score", f"{sum(recent_sc)/len(recent_sc):.1f}/5" if recent_sc else "—")

    st.markdown("---")

    # Level
    st.markdown(f"### Level: {lv_info['emoji']} {lv_info['name']}")
    next_lv, prog_msg = get_suggested_level()
    if next_lv:
        st.success(f"🎉 {prog_msg} → **{DIFFICULTY_LEVELS[next_lv]['name']}**")
        if st.button("⬆️ Level Up Now", type="primary", key="ps_levelup"):
            p["current_level"] = next_lv
            save_profile(p)
            refresh_prompt()
            st.rerun()
    else:
        st.info(f"📈 {prog_msg}")

    # Level override
    lvc = st.columns(4)
    for i, (key, lv) in enumerate(DIFFICULTY_LEVELS.items()):
        with lvc[i]:
            if st.button(f"{lv['emoji']} {lv['name']}", key=f"ps_lv_{key}",
                         use_container_width=True,
                         type="primary" if level == key else "secondary"):
                p["current_level"] = key
                save_profile(p)
                refresh_prompt()
                st.rerun()

    st.markdown("---")

    # Category breakdown
    st.markdown("### Category Performance")
    for cat_key in CHALLENGE_CATEGORIES:
        cat   = CHALLENGE_CATEGORIES[cat_key]
        cnt   = p["category_counts"].get(cat_key, 0)
        sc    = p["category_scores"].get(cat_key, [])
        avg   = (sum(sc[-5:]) / len(sc[-5:])) if sc else 0
        cn, cc, cs, cb = st.columns([3, 1, 1, 3])
        cn.markdown(f"{cat['emoji']} **{cat['name']}**")
        cc.caption(f"{cnt} done")
        cs.caption(("🟢" if avg >= 4 else "🟡" if avg >= 3 else "🔴") + f" {avg:.1f}" if sc else "—")
        cb.progress(min(cnt / 10.0, 1.0))

    st.markdown("---")

    # Weak / strong
    wc, sc_col = st.columns(2)
    with wc:
        st.markdown("### 🎯 Focus Areas")
        weak = get_weak_cats()
        if weak:
            for ck, reason, _ in weak:
                st.caption(f"{CHALLENGE_CATEGORIES[ck]['emoji']} {CHALLENGE_CATEGORIES[ck]['name']} — {reason}")
        else:
            st.caption("No weak areas detected yet!")
    with sc_col:
        st.markdown("### 💪 Strengths")
        strong = get_strong_cats()
        if strong:
            for ck, si in strong:
                st.caption(f"{CHALLENGE_CATEGORIES[ck]['emoji']} {CHALLENGE_CATEGORIES[ck]['name']} — {si}")
        else:
            st.caption("Keep practicing to reveal strengths!")

    st.markdown("---")

    # AI assessment
    if st.button("🤖 AI Progress Assessment", use_container_width=True, key="ps_assess"):
        weak, strong = get_weak_cats(), get_strong_cats()
        weak_s  = ", ".join([f"{CHALLENGE_CATEGORIES[w[0]]['name']} ({w[1]})" for w in weak]) or "None"
        strong_s= ", ".join([f"{CHALLENGE_CATEGORIES[s[0]]['name']} ({s[1]})" for s in strong]) or "None"
        prompt  = (
            f"Founding engineer trainee progress assessment:\n"
            f"- Level: {lv_info['name']}\n- Challenges: {p['total_challenges']}\n"
            f"- Streak: {p['streak_days']}d\n- Weak: {weak_s}\n- Strong: {strong_s}\n"
            f"- Category counts: {json.dumps(p['category_counts'])}\n\n"
            "Give me:\n1) Am I ready to level up?\n2) This week's top focus?\n3) Biggest gap?\n4) Specific 5-day plan.\nBe brutally honest."
        )
        with st.spinner("Analysing your progress..."):
            result = get_brief_llm(prompt)
        st.markdown(result)

    st.markdown("---")

    # Backup / Reset
    bc1, bc2 = st.columns(2)
    with bc1:
        st.download_button(
            "💾 Export Progress",
            data=json.dumps(p, indent=2),
            file_name=f"engineer_profile_{today_str}.json",
            mime="application/json",
            use_container_width=True,
        )
    with bc2:
        if st.button("🗑️ Reset Chat", use_container_width=True, key="ps_reset_chat"):
            st.session_state.messages = []
            st.session_state.challenge_active = False
            st.session_state.current_category = None
            configure_llm()
            st.rerun()

    if st.button("🔄 Reset ALL Progress", use_container_width=True, key="ps_reset_all"):
        if PROFILE_PATH.exists():
            try: PROFILE_PATH.unlink()
            except: pass
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
