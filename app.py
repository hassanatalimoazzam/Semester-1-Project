import streamlit as st
import pandas as pd
from scamshield.analyzer import ScamAnalyzer
from scamshield.storage import load_history, save_analysis, clear_history

st.set_page_config(page_title="ScamShield Pakistan", page_icon="🛡️", layout="wide")

# ---------- THEMES ----------
THEMES = {
    "Classic Editorial": {
        "fonts": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Serif+4:wght@400;600&display=swap",
        "bg": "#f7f3e9", "surface": "#fffdf7", "sidebar": "#efe9d8",
        "text": "#2a2a2a", "heading": "#111111", "muted": "#6b6454",
        "accent": "#8b1e1e", "accent_text": "#ffffff",
        "border": "1px solid #d8d0bd", "radius": "2px", "shadow": "none",
        "font_body": "'Source Serif 4', Georgia, serif",
        "font_head": "'Playfair Display', Georgia, serif",
        "hero_bg": "#1c1c1c", "hero_text": "#f7f3e9",
    },
    "Corporate Blue": {
        "fonts": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        "bg": "#f4f6fa", "surface": "#ffffff", "sidebar": "#e8edf5",
        "text": "#2b3445", "heading": "#0b2a5b", "muted": "#64748b",
        "accent": "#0b4fb3", "accent_text": "#ffffff",
        "border": "1px solid #e1e6ef", "radius": "6px",
        "shadow": "0 2px 6px rgba(11,42,91,.08)",
        "font_body": "Inter, 'Segoe UI', Helvetica, Arial, sans-serif",
        "font_head": "Inter, 'Segoe UI', Helvetica, Arial, sans-serif",
        "hero_bg": "linear-gradient(120deg,#0b2a5b,#0b4fb3)", "hero_text": "#ffffff",
    },
    "Swiss Minimal": {
        "fonts": "",
        "bg": "#ffffff", "surface": "#ffffff", "sidebar": "#f2f2f2",
        "text": "#1a1a1a", "heading": "#000000", "muted": "#555555",
        "accent": "#e63312", "accent_text": "#ffffff",
        "border": "1px solid #000000", "radius": "0", "shadow": "none",
        "font_body": "'Helvetica Neue', Helvetica, Arial, sans-serif",
        "font_head": "'Helvetica Neue', Helvetica, Arial, sans-serif",
        "hero_bg": "#e63312", "hero_text": "#ffffff",
    },
    "Classic Dark": {
        "fonts": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Merriweather:wght@700&display=swap",
        "bg": "#14171c", "surface": "#1d2229", "sidebar": "#101317",
        "text": "#d6dbe3", "heading": "#f2f4f8", "muted": "#8d97a6",
        "accent": "#d4a955", "accent_text": "#14171c",
        "border": "1px solid #2c333d", "radius": "8px",
        "shadow": "0 4px 14px rgba(0,0,0,.4)",
        "font_body": "Inter, system-ui, sans-serif",
        "font_head": "Merriweather, Georgia, serif",
        "hero_bg": "linear-gradient(120deg,#1d2229,#2a2f1f)", "hero_text": "#f2f4f8",
    },
    "Retro Windows 95": {
        "fonts": "",
        "bg": "#008080", "surface": "#c0c0c0", "sidebar": "#c0c0c0",
        "text": "#000000", "heading": "#000000", "muted": "#404040",
        "accent": "#000080", "accent_text": "#ffffff",
        "border": "2px outset #ffffff", "radius": "0", "shadow": "none",
        "font_body": "'Courier New', Courier, monospace",
        "font_head": "'Courier New', Courier, monospace",
        "hero_bg": "#000080", "hero_text": "#ffffff",
    },
}

_CSS = """
@import url('__FONTS__');
:root {
  --bg: __bg__; --surface: __surface__; --sidebar: __sidebar__;
  --text: __text__; --heading: __heading__; --muted: __muted__;
  --accent: __accent__; --accent-text: __accent_text__;
  --border: __border__; --radius: __radius__; --shadow: __shadow__;
  --font-body: __font_body__; --font-head: __font_head__;
  --hero-bg: __hero_bg__; --hero-text: __hero_text__;
}
.stApp, .main { background: var(--bg); font-family: var(--font-body); }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; max-width: 1150px; }

.stApp p, .stApp li, .stApp label, .stApp span,
.stApp [data-testid="stMarkdownContainer"] { color: var(--text); font-family: var(--font-body); }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: var(--heading); font-family: var(--font-head); }
[data-testid="stCaptionContainer"], .small-note { color: var(--muted); }

[data-testid="stSidebar"] { background: var(--sidebar); border-right: var(--border); }

/* Hero banner */
.hero { padding: 1.4rem 1.6rem; border-radius: var(--radius); background: var(--hero-bg);
        border: var(--border); box-shadow: var(--shadow); }
.stApp .hero, .stApp .hero * { color: var(--hero-text) !important; font-family: var(--font-head); }
.hero p { font-family: var(--font-body) !important; opacity: .9; }

/* Inputs */
.stTextArea textarea, .stTextInput input {
  background: var(--surface); color: var(--text); border: var(--border);
  border-radius: var(--radius); font-family: var(--font-body);
}
[data-baseweb="textarea"], [data-baseweb="input"], [data-baseweb="select"] > div {
  background: var(--surface); border-radius: var(--radius);
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
  background: var(--surface); color: var(--text); border: var(--border);
  border-radius: var(--radius); font-family: var(--font-body); box-shadow: var(--shadow);
}
.stButton > button[kind="primary"], .stButton > button[data-testid="stBaseButton-primary"] {
  background: var(--accent); color: var(--accent-text); border: var(--border);
}
.stButton > button[kind="primary"] p, .stButton > button[data-testid="stBaseButton-primary"] p {
  color: var(--accent-text);
}
.stButton > button:hover { filter: brightness(1.08); }

/* Result cards */
[data-testid="stMetric"] {
  background: var(--surface); border: var(--border); border-radius: var(--radius);
  box-shadow: var(--shadow); padding: 1rem 1.2rem;
}
[data-testid="stAlert"] { border-radius: var(--radius); }
[data-testid="stDataFrame"] { border: var(--border); border-radius: var(--radius); }
hr { border-color: var(--muted); opacity: .3; }
"""


def apply_theme(name: str) -> None:
    """Inject the CSS for the chosen theme into the Streamlit page."""
    t = THEMES[name]
    css = _CSS.replace("@import url('__FONTS__');",
                       f"@import url('{t['fonts']}');" if t["fonts"] else "")
    for key, value in t.items():
        css = css.replace(f"__{key}__", value)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
# ---------- END THEMES ----------

with st.sidebar:
    theme_name = st.selectbox("Design theme", list(THEMES), key="theme")
    st.header("About this project")
    st.write("A first-semester Python project demonstrating OOP, discrete logic, vectors, and basic probability concepts.")
    st.warning("This prototype cannot prove that something is a scam or guarantee that a link is safe.")
    page = st.radio("Navigate", ["Analyze", "History", "About & learning"])

apply_theme(theme_name)

analyzer = ScamAnalyzer()

st.markdown("""
<div class="hero">
  <h1>🛡️ ScamShield Pakistan</h1>
  <p>Pause. Check the warning signs. Protect your information.</p>
</div>
""", unsafe_allow_html=True)
st.write("Analyze suspicious messages and URLs using transparent, rule-based checks.")

if page == "Analyze":
    st.subheader("Analyze a message")
    message = st.text_area(
        "Paste a suspicious SMS, WhatsApp message, job offer, or scholarship notice",
        height=180,
        placeholder="Example: Congratulations! You have been selected. Pay a processing fee now and send your OTP..."
    )
    url = st.text_input("Optional URL to inspect", placeholder="https://example.com")
    if st.button("Analyze warning signs", type="primary", use_container_width=True):
        if not message.strip() and not url.strip():
            st.error("Please enter a message or a URL first.")
        else:
            result = analyzer.analyze(message=message, url=url)
            save_analysis(result, message, url)
            st.session_state["latest_result"] = result

    result = st.session_state.get("latest_result")
    if result:
        st.divider()
        st.subheader("Analysis result")
        c1, c2 = st.columns([1, 2])
        with c1:
            st.metric("Rule-based risk score", f'{result["score"]}/100')
            if result["category"] == "High":
                st.error("High warning level")
            elif result["category"] == "Medium":
                st.warning("Medium warning level")
            else:
                st.success("Low warning level")
        with c2:
            st.write("**What this means**")
            st.write(result["summary"])
            st.caption("The score is a heuristic indicator, not a statistically validated probability.")
        st.write("**Warning signs found**")
        if result["findings"]:
            for finding in result["findings"]:
                st.markdown(f"- **{finding['label']}** (+{finding['weight']} points): {finding['explanation']}")
        else:
            st.info("No configured warning signs were found. That does not mean the content is safe.")
        st.write("**Recommended next steps**")
        for tip in result["recommendations"]:
            st.markdown(f"- {tip}")

elif page == "History":
    st.subheader("Recent analysis history")
    history = load_history()
    if history:
        df = pd.DataFrame(history)
        show_cols = [c for c in ["timestamp", "category", "score", "message_preview", "url"] if c in df.columns]
        st.dataframe(df[show_cols], use_container_width=True, hide_index=True)
        left, right = st.columns([1, 3])
        with left:
            if st.button("Clear local history"):
                clear_history()
                st.success("History cleared. Refresh the page if old entries remain visible.")
    else:
        st.info("No analyses saved yet. Run an analysis to populate this page.")

else:
    st.subheader("How to use ScamShield safely")
    st.markdown("""
    1. Paste the message or enter the URL without opening it.
    2. Review each warning sign, not just the overall score.
    3. Verify offers through the organization's official website or a phone number you find independently.
    4. Never share passwords, PINs, or one-time passcodes with someone who contacts you.
    5. If money is involved, pause and verify with the relevant bank or service using its official contact details.
    """)
    st.subheader("Semester concepts demonstrated")
    st.markdown("""
    - **OOP:** `ScamAnalyzer` groups analysis behavior into a class.
    - **Discrete Structures:** Boolean conditions and sets of indicators drive the rule checks.
    - **Linear Algebra:** Each detected indicator can be represented as a binary feature vector and combined with a weight vector.
    - **Basic Mathematics-II:** Weighted sums and thresholds produce a bounded score.
    - **Probability Distributions:** Later, evaluate indicator frequencies on a labeled dataset and discuss uncertainty. The current score itself is not a probability.
    """)
    st.caption("Educational prototype only. Do not use it as the sole basis for financial or security decisions.")
