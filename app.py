from __future__ import annotations

from pathlib import Path
import json

import pandas as pd
import streamlit as st

from auth import authenticate, create_user
from college_data import (
    available_branches,
    available_categories,
    available_districts,
    cutoff_column,
    load_college_dataset,
)
from recommender import recommend
from rag_system import get_explanation
from chatbot import get_faq_response, SUGGESTED_QUESTIONS

st.set_page_config(
    page_title="College Compass",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL STYLES  –  3-D animations + premium UI
# ─────────────────────────────────────────────
st.markdown(
    """
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
  font-family: 'DM Sans', sans-serif;
  background: #05070f;
  color: #e2e8f0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ── Animated starfield background ── */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 10%, rgba(29,78,216,0.18) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(14,165,233,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 40% 30% at 50% 50%, rgba(99,102,241,0.08) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
}

/* Stars */
[data-testid="stAppViewContainer"]::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    radial-gradient(1px 1px at 10% 15%, rgba(255,255,255,0.6) 0%, transparent 100%),
    radial-gradient(1px 1px at 25% 35%, rgba(255,255,255,0.4) 0%, transparent 100%),
    radial-gradient(1px 1px at 40% 10%, rgba(255,255,255,0.5) 0%, transparent 100%),
    radial-gradient(1px 1px at 60% 55%, rgba(255,255,255,0.3) 0%, transparent 100%),
    radial-gradient(1px 1px at 75% 20%, rgba(255,255,255,0.6) 0%, transparent 100%),
    radial-gradient(1px 1px at 90% 70%, rgba(255,255,255,0.4) 0%, transparent 100%),
    radial-gradient(1px 1px at 15% 80%, rgba(255,255,255,0.5) 0%, transparent 100%),
    radial-gradient(1px 1px at 85% 40%, rgba(255,255,255,0.3) 0%, transparent 100%),
    radial-gradient(1px 1px at 55% 90%, rgba(255,255,255,0.4) 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 35% 65%, rgba(255,255,255,0.5) 0%, transparent 100%);
  pointer-events: none;
  z-index: 0;
  animation: starTwinkle 8s ease-in-out infinite alternate;
}
@keyframes starTwinkle {
  0%   { opacity: 0.6; }
  50%  { opacity: 1; }
  100% { opacity: 0.7; }
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #1d4ed8; border-radius: 99px; }

/* ── Main layout ── */
.block-container {
  padding: 1.5rem 2rem 3rem !important;
  max-width: 1400px !important;
  position: relative;
  z-index: 1;
}

/* ── 3-D Hero Card ── */
.hero-card {
  perspective: 1000px;
  margin-bottom: 1.6rem;
}
.hero-inner {
  background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 40%, #0c1a3b 100%);
  border: 1px solid rgba(56,189,248,0.2);
  border-radius: 24px;
  padding: 2rem 2.4rem;
  display: flex;
  align-items: center;
  gap: 1.4rem;
  position: relative;
  overflow: hidden;
  box-shadow:
    0 0 0 1px rgba(56,189,248,0.08),
    0 20px 60px rgba(0,0,0,0.5),
    0 4px 20px rgba(29,78,216,0.2),
    inset 0 1px 0 rgba(255,255,255,0.05);
  transform-style: preserve-3d;
  animation: heroFloat 6s ease-in-out infinite;
}
@keyframes heroFloat {
  0%, 100% { transform: rotateX(0deg) rotateY(-0.5deg) translateY(0px); box-shadow: 0 0 0 1px rgba(56,189,248,0.08), 0 20px 60px rgba(0,0,0,0.5), 0 4px 20px rgba(29,78,216,0.2), inset 0 1px 0 rgba(255,255,255,0.05); }
  50%       { transform: rotateX(0.5deg) rotateY(0.5deg) translateY(-6px); box-shadow: 0 0 0 1px rgba(56,189,248,0.15), 0 30px 80px rgba(0,0,0,0.5), 0 8px 30px rgba(29,78,216,0.3), inset 0 1px 0 rgba(255,255,255,0.08); }
}
.hero-inner::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(14,165,233,0.12) 0%, transparent 60%);
  pointer-events: none;
  animation: orbPulse 4s ease-in-out infinite;
}
.hero-inner::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: 30%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 60%);
  pointer-events: none;
  animation: orbPulse 6s ease-in-out infinite reverse;
}
@keyframes orbPulse {
  0%, 100% { transform: scale(1); opacity: 0.7; }
  50%       { transform: scale(1.2); opacity: 1; }
}
.hero-icon-wrap {
  width: 68px;
  height: 68px;
  min-width: 68px;
  border-radius: 20px;
  background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  box-shadow: 0 8px 32px rgba(29,78,216,0.4), 0 0 0 1px rgba(255,255,255,0.08);
  animation: iconGlow 3s ease-in-out infinite;
  position: relative;
  z-index: 2;
}
@keyframes iconGlow {
  0%, 100% { box-shadow: 0 8px 32px rgba(29,78,216,0.4), 0 0 0 1px rgba(255,255,255,0.08); }
  50%       { box-shadow: 0 8px 40px rgba(14,165,233,0.6), 0 0 20px rgba(14,165,233,0.2), 0 0 0 1px rgba(255,255,255,0.15); }
}
.hero-text { position: relative; z-index: 2; }
.hero-title {
  font-family: 'Syne', sans-serif;
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  background: linear-gradient(90deg, #e2e8f0 0%, #7dd3fc 50%, #a5b4fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.2;
  margin: 0 0 0.3rem;
}
.hero-sub {
  color: rgba(148,163,184,0.9);
  font-size: 0.95rem;
  font-weight: 400;
  margin: 0;
}

/* ── Section headings ── */
h2, .section-title {
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  letter-spacing: -0.02em !important;
  color: #f1f5f9 !important;
  font-size: 1.4rem !important;
}

/* ── Glass Cards ── */
.glass-card {
  background: rgba(15,23,42,0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(56,189,248,0.1);
  border-radius: 20px;
  padding: 1.4rem;
  margin-bottom: 1rem;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  transition: border-color 0.3s, box-shadow 0.3s, transform 0.3s;
}
.glass-card:hover {
  border-color: rgba(56,189,248,0.25);
  box-shadow: 0 12px 48px rgba(0,0,0,0.4), 0 0 0 1px rgba(56,189,248,0.08);
  transform: translateY(-2px);
}

/* ── 3-D Metric cards ── */
[data-testid="stMetric"] {
  background: linear-gradient(145deg, rgba(15,23,42,0.9), rgba(30,58,138,0.3));
  border: 1px solid rgba(56,189,248,0.12);
  border-radius: 16px;
  padding: 1rem 1.2rem !important;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.04);
  transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
  position: relative;
  overflow: hidden;
}
[data-testid="stMetric"]::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent 0%, rgba(14,165,233,0.04) 100%);
  pointer-events: none;
}
[data-testid="stMetric"]:hover {
  transform: translateY(-4px) scale(1.02);
  border-color: rgba(56,189,248,0.3);
  box-shadow: 0 12px 40px rgba(29,78,216,0.25), inset 0 1px 0 rgba(255,255,255,0.06);
}
[data-testid="stMetricLabel"] { color: rgba(148,163,184,0.8) !important; font-size: 0.78rem !important; font-weight: 500 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] { color: #f1f5f9 !important; font-family: 'Syne', sans-serif !important; font-size: 1.8rem !important; font-weight: 700 !important; }

/* ── Inputs & selects ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-baseweb="select"] {
  background: rgba(15,23,42,0.8) !important;
  border: 1px solid rgba(56,189,248,0.15) !important;
  border-radius: 10px !important;
  color: #e2e8f0 !important;
  font-family: 'DM Sans', sans-serif !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
  border-color: rgba(56,189,248,0.4) !important;
  box-shadow: 0 0 0 3px rgba(14,165,233,0.1) !important;
}
[data-baseweb="select"] > div { background: rgba(15,23,42,0.9) !important; border-color: rgba(56,189,248,0.15) !important; }

/* ── Labels ── */
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label,
.stSelectbox label { color: rgba(148,163,184,0.9) !important; font-size: 0.82rem !important; font-weight: 500 !important; letter-spacing: 0.04em !important; }

/* ── Buttons ── */
[data-testid="stButton"] > button {
  background: linear-gradient(135deg, #1d4ed8, #0ea5e9) !important;
  color: white !important;
  border: none !important;
  border-radius: 12px !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.92rem !important;
  letter-spacing: 0.03em !important;
  padding: 0.65rem 1.4rem !important;
  box-shadow: 0 4px 20px rgba(29,78,216,0.35) !important;
  transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1) !important;
  position: relative;
  overflow: hidden;
}
[data-testid="stButton"] > button::before {
  content: '';
  position: absolute;
  top: 0; left: -100%; right: 0; bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
  transition: left 0.4s ease;
}
[data-testid="stButton"] > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(29,78,216,0.5) !important;
}
[data-testid="stButton"] > button:hover::before { left: 100%; }
[data-testid="stButton"] > button:active { transform: translateY(0px) scale(0.97) !important; }

/* ── Form submit button ── */
[data-testid="stFormSubmitButton"] > button {
  background: linear-gradient(135deg, #059669, #0ea5e9) !important;
  width: 100% !important;
  border-radius: 14px !important;
  font-size: 1rem !important;
  padding: 0.8rem !important;
  box-shadow: 0 4px 20px rgba(5,150,105,0.35) !important;
  letter-spacing: 0.04em !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
  box-shadow: 0 8px 30px rgba(5,150,105,0.5) !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
  background: rgba(15,23,42,0.6);
  border-radius: 12px;
  padding: 4px;
  border: 1px solid rgba(56,189,248,0.1);
  gap: 2px;
}
[data-testid="stTabs"] [role="tab"] {
  border-radius: 8px !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  color: rgba(148,163,184,0.8) !important;
  transition: all 0.2s !important;
  border: none !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  background: linear-gradient(135deg, #1d4ed8, #0ea5e9) !important;
  color: white !important;
  box-shadow: 0 4px 12px rgba(29,78,216,0.4) !important;
}

/* ── Containers / borders ── */
[data-testid="stVerticalBlockBorderWrapper"] > div {
  background: rgba(15,23,42,0.6) !important;
  border: 1px solid rgba(56,189,248,0.1) !important;
  border-radius: 18px !important;
  backdrop-filter: blur(12px) !important;
  box-shadow: 0 4px 24px rgba(0,0,0,0.2) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #05070f 0%, #0d1424 100%) !important;
  border-right: 1px solid rgba(56,189,248,0.08) !important;
  padding-top: 1rem !important;
}
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
section[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
  background: rgba(30,58,138,0.3) !important;
  border-color: rgba(56,189,248,0.15) !important;
}
section[data-testid="stSidebar"] hr { border-color: rgba(56,189,248,0.12) !important; }
section[data-testid="stSidebar"] h1 {
  font-family: 'Syne', sans-serif !important;
  font-size: 1.1rem !important;
  color: #e2e8f0 !important;
  letter-spacing: -0.01em !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
  border-radius: 16px !important;
  overflow: hidden !important;
  border: 1px solid rgba(56,189,248,0.1) !important;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
}
[data-testid="stDataFrame"] table { background: rgba(15,23,42,0.9) !important; }
[data-testid="stDataFrame"] th { background: rgba(29,78,216,0.3) !important; color: #7dd3fc !important; font-family: 'Syne', sans-serif !important; font-weight: 600 !important; font-size: 0.8rem !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; }
[data-testid="stDataFrame"] td { color: #e2e8f0 !important; font-size: 0.88rem !important; }
[data-testid="stDataFrame"] tr:hover td { background: rgba(29,78,216,0.12) !important; }

/* ── Alerts / success / info ── */
[data-testid="stAlert"] { border-radius: 14px !important; border-width: 1px !important; font-family: 'DM Sans', sans-serif !important; }
.stSuccess { background: rgba(5,150,105,0.1) !important; border-color: rgba(5,150,105,0.3) !important; color: #6ee7b7 !important; }
.stError   { background: rgba(220,38,38,0.1) !important; border-color: rgba(220,38,38,0.3) !important; color: #fca5a5 !important; }
.stInfo    { background: rgba(14,165,233,0.1) !important; border-color: rgba(14,165,233,0.3) !important; color: #7dd3fc !important; }
.stWarning { background: rgba(245,158,11,0.1) !important; border-color: rgba(245,158,11,0.3) !important; color: #fcd34d !important; }

/* ── Slider ── */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
  background: linear-gradient(135deg, #1d4ed8, #0ea5e9) !important;
  box-shadow: 0 0 12px rgba(14,165,233,0.5) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
  background: rgba(15,23,42,0.6) !important;
  border: 1px solid rgba(56,189,248,0.1) !important;
  border-radius: 16px !important;
}
[data-testid="stExpander"] summary { font-family: 'Syne', sans-serif !important; font-weight: 600 !important; color: #7dd3fc !important; }

/* ── Caption ── */
[data-testid="stCaptionContainer"] { color: rgba(100,116,139,0.8) !important; font-size: 0.78rem !important; }

/* ── Charts ── */
[data-testid="stArrowVegaLiteChart"] { border-radius: 12px !important; overflow: hidden !important; }

/* ── Programme badge ── */
.prog-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: linear-gradient(135deg, rgba(29,78,216,0.3), rgba(14,165,233,0.2));
  border: 1px solid rgba(56,189,248,0.25);
  border-radius: 999px;
  padding: 0.3rem 0.9rem;
  font-family: 'Syne', sans-serif;
  font-size: 0.8rem;
  font-weight: 600;
  color: #7dd3fc;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 1rem;
  box-shadow: 0 0 16px rgba(14,165,233,0.15);
  animation: badgePulse 3s ease-in-out infinite;
}
@keyframes badgePulse {
  0%, 100% { box-shadow: 0 0 16px rgba(14,165,233,0.15); }
  50%       { box-shadow: 0 0 24px rgba(14,165,233,0.3); }
}

/* ── Photo gallery row ── */
.photo-row {
  display: flex;
  gap: 0.8rem;
  margin: 1rem 0 1.4rem;
  overflow-x: hidden;
}
.photo-item {
  flex: 1;
  height: 120px;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(56,189,248,0.12);
  position: relative;
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
  transition: transform 0.4s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.4s;
}
.photo-item:hover {
  transform: scale(1.04) translateY(-4px);
  box-shadow: 0 12px 40px rgba(29,78,216,0.3);
}
.photo-item img {
  width: 100%; height: 100%;
  object-fit: cover;
  filter: brightness(0.65) saturate(0.7);
  transition: filter 0.4s;
}
.photo-item:hover img { filter: brightness(0.75) saturate(0.9); }
.photo-label {
  position: absolute;
  bottom: 0.5rem;
  left: 0.7rem;
  font-family: 'Syne', sans-serif;
  font-size: 0.7rem;
  font-weight: 600;
  color: rgba(255,255,255,0.9);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  text-shadow: 0 2px 8px rgba(0,0,0,0.6);
}
.photo-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(5,15,40,0.7) 0%, transparent 60%);
}

/* ── Floating particles ── */
@keyframes particleFloat1 {
  0%   { transform: translate(0,0) scale(1); opacity: 0.4; }
  33%  { transform: translate(20px,-30px) scale(1.1); opacity: 0.6; }
  66%  { transform: translate(-10px,-50px) scale(0.9); opacity: 0.3; }
  100% { transform: translate(5px,-80px) scale(1); opacity: 0; }
}
.particle {
  position: fixed;
  width: 4px; height: 4px;
  border-radius: 50%;
  background: rgba(14,165,233,0.6);
  pointer-events: none;
  animation: particleFloat1 8s linear infinite;
}

/* ── Login card ── */
.login-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}
.login-bg-text {
  font-family: 'Syne', sans-serif;
  font-size: 8rem;
  font-weight: 800;
  color: rgba(29,78,216,0.06);
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  white-space: nowrap;
  pointer-events: none;
  z-index: 0;
  letter-spacing: -0.05em;
}

/* ── Recommendation result heading ── */
.results-heading {
  font-family: 'Syne', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: #6ee7b7;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.8rem;
}

/* ── form labels stronger ── */
.stForm label p { color: rgba(148,163,184,0.95) !important; font-weight: 500 !important; }

/* ── Number input arrows ── */
[data-testid="stNumberInput"] button { color: #7dd3fc !important; background: rgba(29,78,216,0.2) !important; }
</style>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────
#  HELPERS (unchanged logic)
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def _get_dataset(path: str):
    return load_college_dataset(path)


# ── Programme icon & accent map ──
PROG_META = {
    "Diploma":     {"icon": "📐", "accent": "#0ea5e9", "label": "Polytechnic · Diploma"},
    "Engineering": {"icon": "⚙️",  "accent": "#6366f1", "label": "B.Tech · Engineering"},
    "Medical":     {"icon": "🩺",  "accent": "#10b981", "label": "MBBS · Medical"},
}


def _header(programme: str = ""):
    meta = PROG_META.get(programme, {"icon": "🎓", "accent": "#0ea5e9", "label": "Higher Education · India"})
    subtitle = (
        f"{meta['label']} — personalised recommendations based on rank, category, and location."
        if programme
        else "Find the best-fit colleges in India. Powered by rank-based filtering & smart scoring."
    )
    st.markdown(
        f"""
<div class="hero-card">
  <div class="hero-inner">
    <div class="hero-icon-wrap">{meta['icon']}</div>
    <div class="hero-text">
      <p class="hero-title">College Compass</p>
      <p class="hero-sub">{subtitle}</p>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def _photo_row(programme: str):
    """Inline SVG placeholder images styled as college campus visuals."""
    photos = {
        "Diploma": [
            ("🏛️ Campus", "#1e3a5f"),
            ("🔧 Workshop", "#1a3a2f"),
            ("📚 Library", "#2d1b4e"),
            ("🎓 Convocation", "#1e2d5f"),
        ],
        "Engineering": [
            ("🏗️ Campus", "#1e3a5f"),
            ("💻 Lab", "#1a2f3a"),
            ("🔬 Research", "#1a1a3a"),
            ("⚙️ Workshop", "#2d2a1b"),
        ],
        "Medical": [
            ("🏥 Hospital", "#1a3a2a"),
            ("🔬 Lab", "#1a2a3a"),
            ("📖 Library", "#2d1b1b"),
            ("🩺 Clinical", "#1b2d1b"),
        ],
    }
    items = photos.get(programme, photos["Engineering"])
    cols = st.columns(len(items))
    for col, (label, bg) in zip(cols, items):
        icon = label.split()[0]
        name = " ".join(label.split()[1:])
        col.markdown(
            f"""
<div class="photo-item" style="background: linear-gradient(135deg, {bg} 0%, #050a14 100%); height:110px; display:flex; align-items:center; justify-content:center; flex-direction:column; gap:0.4rem;">
  <div style="font-size:2.2rem; filter: drop-shadow(0 0 12px rgba(14,165,233,0.5));">{icon}</div>
  <div class="photo-label" style="position:static; font-size:0.65rem;">{name.upper()}</div>
</div>
""",
            unsafe_allow_html=True,
        )


def _ensure_user_state():
    if "user" not in st.session_state:
        st.session_state["user"] = None


# Chatbot session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "chat_open" not in st.session_state:
    st.session_state["chat_open"] = False


def _render_chatbot():
    # Ensure chat state exists
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "chat_open" not in st.session_state:
        st.session_state["chat_open"] = False

    # Hidden input that JS will write into
    st.text_input(
        "chat_input",
        key="chat_input_field",
        label_visibility="collapsed",
    )

    user_message = st.session_state.get("chat_input_field", "").strip()
    if user_message:
        st.session_state["chat_history"].append({"role": "user", "content": user_message})
        bot_reply = get_faq_response(user_message)
        st.session_state["chat_history"].append({"role": "bot", "content": bot_reply})
        st.session_state["chat_input_field"] = ""
        st.session_state["chat_open"] = True
        st.rerun()

    chat_history = st.session_state.get("chat_history", [])
    suggested = SUGGESTED_QUESTIONS
    chat_open = bool(st.session_state.get("chat_open", False))

    chat_history_json = json.dumps(chat_history, ensure_ascii=False)
    suggested_json = json.dumps(suggested, ensure_ascii=False)

    # Prevent accidental </script> termination
    chat_history_json = chat_history_json.replace("</", "<\\/")
    suggested_json = suggested_json.replace("</", "<\\/")

    html_template = """
<script>
  const chatHistoryData = __CHAT_HISTORY__;
  const suggestedQuestionsData = __SUGGESTED__;
  const chatInitiallyOpen = __CHAT_OPEN__;
</script>

<style>
  :root {
    --bg-deep: #05070f;
    --bg-card: rgba(15,23,42,0.97);
    --border-glow: rgba(56,189,248,0.2);
    --accent-blue: #1d4ed8;
    --accent-cyan: #0ea5e9;
    --text-primary: #e2e8f0;
    --text-muted: rgba(148,163,184,0.8);
  }

  @keyframes chatPulse {
    0% { box-shadow: 0 0 0 0 rgba(14,165,233,0.4); }
    70% { box-shadow: 0 0 0 14px rgba(14,165,233,0); }
    100% { box-shadow: 0 0 0 0 rgba(14,165,233,0); }
  }

  @keyframes typingBounce {
    0%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-6px); }
  }

  @keyframes chatSlideUp {
    from { opacity: 0; transform: translateY(20px) scale(0.95); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
  }

  .compass-chat-root {
    position: fixed;
    right: 24px;
    bottom: 24px;
    z-index: 9999;
    font-family: 'DM Sans', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }

  .compass-chat-toggle {
    width: 56px;
    height: 56px;
    border-radius: 999px;
    border: none;
    cursor: pointer;
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan));
    color: #f9fafb;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 12px 40px rgba(15,23,42,0.8), 0 0 24px rgba(14,165,233,0.6);
    animation: chatPulse 2.4s infinite;
    position: relative;
    overflow: hidden;
  }

  .compass-chat-toggle span {
    font-size: 1.6rem;
  }

  .compass-chat-window {
    width: 380px;
    max-height: 520px;
    position: absolute;
    bottom: 76px;
    right: 0;
    background: rgba(5,10,25,0.97);
    border-radius: 20px;
    border: 1px solid rgba(56,189,248,0.2);
    box-shadow:
      0 20px 60px rgba(15,23,42,0.9),
      0 0 40px rgba(8,47,73,0.8);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    display: none;
    flex-direction: column;
    overflow: hidden;
    animation: chatSlideUp 0.35s ease-out;
  }

  .compass-chat-header {
    padding: 0.85rem 1rem;
    background: linear-gradient(135deg, rgba(37,99,235,0.95), rgba(14,165,233,0.95));
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.6rem;
  }

  .compass-chat-header-main {
    display: flex;
    flex-direction: column;
    gap: 0.1rem;
  }

  .compass-chat-title {
    font-family: 'Syne', system-ui, sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    color: #f9fafb;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  .compass-chat-subtitle {
    font-size: 0.78rem;
    color: rgba(241,245,249,0.85);
  }

  .compass-chat-close {
    width: 26px;
    height: 26px;
    border-radius: 999px;
    border: 1px solid rgba(248,250,252,0.4);
    background: transparent;
    color: #f9fafb;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
  }

  .compass-chat-body {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: radial-gradient(circle at top, rgba(37,99,235,0.2), transparent 55%),
                radial-gradient(circle at bottom, rgba(8,47,73,0.65), #020617);
  }

  .compass-chat-messages {
    padding: 0.9rem 0.9rem 0.4rem;
    flex: 1;
    overflow-y: auto;
    scroll-behavior: smooth;
  }

  .compass-chat-message {
    max-width: 90%;
    padding: 0.55rem 0.75rem;
    border-radius: 14px;
    margin-bottom: 0.5rem;
    font-size: 0.8rem;
    line-height: 1.4;
    display: inline-block;
    word-break: break-word;
  }

  .compass-chat-message.user {
    margin-left: auto;
    background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
    color: #f9fafb;
    border-bottom-right-radius: 4px;
    box-shadow: 0 8px 18px rgba(37,99,235,0.55);
  }

  .compass-chat-message.bot {
    margin-right: auto;
    background: rgba(15,23,42,0.9);
    color: var(--text-primary);
    border-left: 3px solid rgba(56,189,248,0.7);
    box-shadow: 0 6px 16px rgba(15,23,42,0.9);
  }

  .compass-chat-typing {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 0.45rem 0.6rem;
    border-radius: 999px;
    background: rgba(15,23,42,0.9);
    border: 1px solid rgba(56,189,248,0.25);
    margin-bottom: 0.6rem;
  }

  .compass-chat-typing-dot {
    width: 6px;
    height: 6px;
    border-radius: 999px;
    background: rgba(148,163,184,0.9);
    animation: typingBounce 1.2s infinite;
  }

  .compass-chat-typing-dot:nth-child(2) {
    animation-delay: 0.15s;
  }

  .compass-chat-typing-dot:nth-child(3) {
    animation-delay: 0.3s;
  }

  .compass-chat-footer {
    padding: 0.45rem 0.8rem 0.75rem;
    border-top: 1px solid rgba(51,65,85,0.9);
    background: linear-gradient(180deg, rgba(15,23,42,0.96), rgba(15,23,42,0.98));
  }

  .compass-chat-chips {
    display: flex;
    gap: 0.4rem;
    overflow-x: auto;
    padding-bottom: 0.35rem;
    margin-bottom: 0.35rem;
  }

  .compass-chat-chip {
    border-radius: 999px;
    border: 1px solid rgba(56,189,248,0.4);
    background: rgba(15,23,42,0.9);
    color: var(--text-muted);
    font-size: 0.7rem;
    padding: 0.25rem 0.65rem;
    cursor: pointer;
    white-space: nowrap;
  }

  .compass-chat-input-row {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    background: rgba(15,23,42,0.95);
    border-radius: 999px;
    border: 1px solid rgba(51,65,85,0.9);
    padding: 0.25rem 0.4rem 0.25rem 0.75rem;
  }

  .compass-chat-input-row input {
    flex: 1;
    border: none;
    outline: none;
    background: transparent;
    color: var(--text-primary);
    font-size: 0.8rem;
  }

  .compass-chat-input-row input::placeholder {
    color: rgba(148,163,184,0.7);
  }

  .compass-chat-send {
    width: 30px;
    height: 30px;
    border-radius: 999px;
    border: none;
    background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
    color: #f9fafb;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 0 0 1px rgba(15,23,42,0.9);
  }

  @media (max-width: 600px) {
    .compass-chat-window {
      width: 100vw;
      right: 0;
      bottom: 0;
      border-radius: 18px 18px 0 0;
    }
  }
</style>

<div class="compass-chat-root">
  <div class="compass-chat-window" id="compassChatWindow">
    <div class="compass-chat-header">
      <div class="compass-chat-header-main">
        <div class="compass-chat-title">🎓 Compass AI</div>
        <div class="compass-chat-subtitle">Ask me anything about admissions</div>
      </div>
      <button class="compass-chat-close" id="compassChatClose" aria-label="Close chatbot">✕</button>
    </div>
    <div class="compass-chat-body">
      <div class="compass-chat-messages" id="compassChatMessages"></div>
      <div class="compass-chat-footer">
        <div class="compass-chat-chips" id="compassChatChips"></div>
        <div class="compass-chat-input-row">
          <input id="compassChatInput" type="text" placeholder="Type your question about ranks, fees, branches..." />
          <button class="compass-chat-send" id="compassChatSend" aria-label="Send message">➤</button>
        </div>
      </div>
    </div>
  </div>

  <button class="compass-chat-toggle" id="compassChatToggle" aria-label="Open Compass AI chat">
    <span>🎓</span>
  </button>
</div>

<script>
  (function() {
    const chatWindow = document.getElementById("compassChatWindow");
    const toggleBtn = document.getElementById("compassChatToggle");
    const closeBtn = document.getElementById("compassChatClose");
    const messagesEl = document.getElementById("compassChatMessages");
    const chipsEl = document.getElementById("compassChatChips");
    const inputEl = document.getElementById("compassChatInput");
    const sendBtn = document.getElementById("compassChatSend");

    function findHiddenInput() {
      return document.querySelector('input[aria-label="chat_input"]');
    }

    function scrollToBottom() {
      if (!messagesEl) return;
      messagesEl.scrollTop = messagesEl.scrollHeight + 100;
    }

    function createBubble(role, content) {
      const div = document.createElement("div");
      div.className = "compass-chat-message " + (role === "user" ? "user" : "bot");
      div.textContent = content;
      return div;
    }

    function renderHistoryFromServer() {
      if (!messagesEl) return;
      messagesEl.innerHTML = "";
      if (Array.isArray(chatHistoryData)) {
        chatHistoryData.forEach(msg => {
          if (!msg || !msg.content) return;
          const role = msg.role === "user" ? "user" : "bot";
          messagesEl.appendChild(createBubble(role, msg.content));
        });
      }
      scrollToBottom();
    }

    function renderChips() {
      if (!chipsEl) return;
      chipsEl.innerHTML = "";
      if (Array.isArray(suggestedQuestionsData)) {
        suggestedQuestionsData.forEach(text => {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "compass-chat-chip";
          btn.textContent = text;
          btn.addEventListener("click", () => {
            handleSend(text);
          });
          chipsEl.appendChild(btn);
        });
      }
    }

    let typingEl = null;
    function showTyping() {
      if (!messagesEl) return;
      if (typingEl) {
        messagesEl.removeChild(typingEl);
      }
      typingEl = document.createElement("div");
      typingEl.className = "compass-chat-typing";
      for (let i = 0; i < 3; i++) {
        const dot = document.createElement("div");
        dot.className = "compass-chat-typing-dot";
        typingEl.appendChild(dot);
      }
      messagesEl.appendChild(typingEl);
      scrollToBottom();
    }

    function hideTyping() {
      if (typingEl && messagesEl && typingEl.parentNode === messagesEl) {
        messagesEl.removeChild(typingEl);
      }
      typingEl = null;
    }

    function sendToStreamlit(text) {
      const hidden = findHiddenInput();
      if (!hidden) return;
      hidden.value = text;
      const ev1 = new Event("input", { bubbles: true });
      const ev2 = new Event("change", { bubbles: true });
      hidden.dispatchEvent(ev1);
      hidden.dispatchEvent(ev2);
    }

    function handleSend(textFromChip) {
      const text = (typeof textFromChip === "string" ? textFromChip : inputEl.value).trim();
      if (!text) return;

      // Show user message immediately in UI
      messagesEl.appendChild(createBubble("user", text));
      scrollToBottom();
      inputEl.value = "";

      // Show typing indicator, then trigger Streamlit update
      showTyping();
      setTimeout(() => {
        hideTyping();
        sendToStreamlit(text);
      }, 600);
    }

    if (toggleBtn && chatWindow) {
      toggleBtn.addEventListener("click", () => {
        const isVisible = chatWindow.style.display === "flex";
        chatWindow.style.display = isVisible ? "none" : "flex";
        if (!isVisible) {
          setTimeout(scrollToBottom, 100);
        }
      });
    }

    if (closeBtn && chatWindow) {
      closeBtn.addEventListener("click", () => {
        chatWindow.style.display = "none";
      });
    }

    if (sendBtn && inputEl) {
      sendBtn.addEventListener("click", () => handleSend());
      inputEl.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          handleSend();
        }
      });
    }

    renderHistoryFromServer();
    renderChips();

    if (chatInitiallyOpen && chatWindow) {
      chatWindow.style.display = "flex";
      setTimeout(scrollToBottom, 150);
    }
  })();
</script>
"""

    html = (
        html_template.replace("__CHAT_HISTORY__", chat_history_json)
        .replace("__SUGGESTED__", suggested_json)
        .replace("__CHAT_OPEN__", "true" if chat_open else "false")
    )

    st.markdown(html, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  AUTH PAGE
# ─────────────────────────────────────────────
def _render_auth_page():
    _header()

    # Decorative background text
    st.markdown('<div class="login-bg-text">COMPASS</div>', unsafe_allow_html=True)

    st.write("")

    # Feature pills
    feat_col1, feat_col2, feat_col3 = st.columns([1.5, 1.5, 1.5])
    with feat_col1:
        st.markdown(
            '<div class="prog-badge">🎯 Rank-based matching</div>',
            unsafe_allow_html=True,
        )
    with feat_col2:
        st.markdown(
            '<div class="prog-badge" style="background:linear-gradient(135deg,rgba(99,102,241,0.3),rgba(14,165,233,0.2));border-color:rgba(165,180,252,0.25);color:#a5b4fc;">📊 Live dashboards</div>',
            unsafe_allow_html=True,
        )
    with feat_col3:
        st.markdown(
            '<div class="prog-badge" style="background:linear-gradient(135deg,rgba(16,185,129,0.3),rgba(14,165,233,0.2));border-color:rgba(110,231,183,0.25);color:#6ee7b7;">🤖 Smart explanations</div>',
            unsafe_allow_html=True,
        )

    st.write("")

    left, center, right = st.columns([1, 1.1, 1])
    with center:
        with st.container(border=True):
            st.markdown(
                """
<div style="text-align:center; margin-bottom:1.2rem;">
  <div style="font-size:2.5rem; margin-bottom:0.4rem; animation: iconGlow 3s ease-in-out infinite;">🎓</div>
  <p style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700; color:#f1f5f9; margin:0;">Welcome Back</p>
  <p style="color:rgba(148,163,184,0.7); font-size:0.82rem; margin-top:0.2rem;">Sign in to explore your college options</p>
</div>
""",
                unsafe_allow_html=True,
            )

            mode = st.tabs(["🔐 Login", "✨ Sign up"])

            with mode[0]:
                username = st.text_input("Username", placeholder="your username", key="login_user")
                password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
                st.write("")
                if st.button("Login →", use_container_width=True):
                    ok, msg = authenticate(username, password)
                    if ok:
                        st.session_state["user"] = username.strip()
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

            with mode[1]:
                username = st.text_input("Username", placeholder="choose a username", key="signup_user")
                password = st.text_input("Password", type="password", placeholder="choose a password", key="signup_pass")
                st.write("")
                if st.button("Create account →", use_container_width=True):
                    ok, msg = create_user(username, password)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)

        st.caption("🔒 Passwords are stored as SHA-256 hashes in users.json")

    _render_chatbot()


# ─────────────────────────────────────────────
#  DATASET LOADER (unchanged logic)
# ─────────────────────────────────────────────
def _dataset_or_upload(program_label: str, default_path: str):
    if Path(default_path).exists():
        return _get_dataset(default_path), default_path

    uploaded = st.file_uploader(
        f"Upload {program_label} dataset (.xlsx)",
        type=["xlsx"],
        key=f"upload_{program_label}",
    )
    if uploaded is None:
        return None, default_path

    temp_path = Path(f".uploaded_{program_label.lower()}.xlsx")
    temp_path.write_bytes(uploaded.getvalue())
    return _get_dataset(str(temp_path)), str(temp_path)


# ─────────────────────────────────────────────
#  RECOMMENDATIONS PAGE
# ─────────────────────────────────────────────
def _render_recommendations(program_label: str, dataset):
    meta = PROG_META.get(program_label, {"icon": "🎓", "accent": "#0ea5e9"})

    st.markdown(
        f'<div class="prog-badge">{meta["icon"]} {program_label} · Recommendations</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown(
            "<p style='font-family:Syne,sans-serif;font-weight:700;font-size:0.95rem;color:#7dd3fc;margin-bottom:0.8rem;'>🎯 Your Preferences</p>",
            unsafe_allow_html=True,
        )
        with st.form(key=f"form_{program_label}"):
            c1, c2, c3 = st.columns(3)
            rank = c1.number_input("Rank", min_value=1, step=1, key=f"rank_{program_label}")
            gender = c2.selectbox("Gender", ["BOYS", "GIRLS"], key=f"gender_{program_label}")
            cats = available_categories(dataset)
            if not cats:
                df_cols = set(str(c) for c in dataset.df.columns)
                fallback_order = ["OC", "BC_A", "BC_B", "BC_C", "BC_D", "BC_E", "SC", "ST", "EWS"]
                inferred = [c for c in fallback_order if f"{c}_BOYS" in df_cols or f"{c}_GIRLS" in df_cols]
                cats = inferred or fallback_order
            category = c3.selectbox("Category", cats, key=f"cat_{program_label}")

            c4, c5 = st.columns(2)
            branch_options = available_branches(dataset)
            branch = c4.selectbox(
                "Branch",
                branch_options,
                index=0 if branch_options else None,
                key=f"branch_{program_label}",
            )
            districts = ["(Any)"] + available_districts(dataset)
            district_choice = c5.selectbox("Preferred district", districts, key=f"district_{program_label}")
            district_query = "" if district_choice == "(Any)" else district_choice

            c6, c7 = st.columns(2)
            budget = c6.number_input(
                "Max fee (0 = no limit)",
                min_value=0,
                step=1000,
                key=f"budget_{program_label}",
            )
            top_k = c7.slider(
                "Results to show",
                min_value=5,
                max_value=30,
                value=15,
                step=5,
                key=f"topk_{program_label}",
            )

            st.write("")
            submitted = st.form_submit_button("🔍 Find My Colleges", use_container_width=True)

    if not submitted:
        return

    with st.spinner("Scanning college database…"):
        results = recommend(
            rank=int(rank),
            category=str(category),
            gender=str(gender),
            branch=str(branch or ""),
            budget=int(budget),
            district_query=str(district_query or ""),
            top_k=int(top_k),
            dataset=dataset,
        )

    if results.empty:
        st.error("No eligible colleges found. Try increasing budget, changing district, or adjusting branch/category.")
        return

    # Results header
    st.markdown(
        f"""
<div class="results-heading">
  ✅ {len(results)} colleges matched your profile
</div>
""",
        unsafe_allow_html=True,
    )

    # Category badges row
    if "Category_Type" in results.columns:
        dream = (results["Category_Type"] == "Dream").sum()
        target = (results["Category_Type"] == "Target").sum()
        safe = (results["Category_Type"] == "Safe").sum()
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Total", f"{len(results)}")
        b2.metric("🌟 Dream", f"{dream}")
        b3.metric("🎯 Target", f"{target}")
        b4.metric("✅ Safe", f"{safe}")
        st.write("")

    display_columns = [
        "Institute_Name", "District", "Co_Education", "Branch_Name",
        "Fee", "Cutoff_Rank", "Category_Type", "Score",
    ]
    display_columns = [c for c in display_columns if c in results.columns]
    st.dataframe(results[display_columns], use_container_width=True, hide_index=True)

    with st.expander("💡 Why this recommendation?", expanded=True):
        top_row = results.iloc[0].to_dict()
        explanation = get_explanation(
            {
                "student": {
                    "rank": int(rank),
                    "gender": str(gender),
                    "category": str(category),
                    "branch": str(branch),
                    "budget": int(budget),
                    "district": str(district_query),
                },
                "top_college": top_row,
            }
        )
        st.write(explanation)


# ─────────────────────────────────────────────
#  DASHBOARDS PAGE
# ─────────────────────────────────────────────
def _render_dashboards(program_label: str, dataset):
    meta = PROG_META.get(program_label, {"icon": "🎓", "accent": "#0ea5e9"})
    st.markdown(
        f'<div class="prog-badge">{meta["icon"]} {program_label} · Analytics Dashboard</div>',
        unsafe_allow_html=True,
    )

    df = dataset.df

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Rows", f"{len(df):,}")
    c2.metric("Institutes", f"{df['Institute_Name'].nunique():,}")
    c3.metric("Branches", f"{df['Branch_Name'].nunique():,}")
    c4.metric("Districts", f"{df['District'].nunique():,}" if "District" in df.columns else "—")

    st.write("")
    _photo_row(program_label)

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown(
                "<p style='font-family:Syne,sans-serif;font-weight:700;font-size:0.9rem;color:#7dd3fc;'>💰 Fee Distribution</p>",
                unsafe_allow_html=True,
            )
            fee = pd.to_numeric(df.get("Fee"), errors="coerce").dropna()
            if fee.empty:
                st.info("No fee data available.")
            else:
                bins = pd.cut(fee, bins=10)
                fee_hist = bins.value_counts().sort_index()
                fee_hist.index = fee_hist.index.astype(str)
                st.bar_chart(fee_hist, color="#0ea5e9")
                st.caption(f"Min: ₹{int(fee.min()):,}  ·  Median: ₹{int(fee.median()):,}  ·  Max: ₹{int(fee.max()):,}")

        with st.container(border=True):
            st.markdown(
                "<p style='font-family:Syne,sans-serif;font-weight:700;font-size:0.9rem;color:#7dd3fc;'>🏫 Top Branches</p>",
                unsafe_allow_html=True,
            )
            top_branches = (
                df["Branch_Name"].astype(str).str.strip()
                .replace("", pd.NA).dropna()
                .value_counts().head(15)
            )
            st.bar_chart(top_branches, color="#6366f1")

    with right:
        with st.container(border=True):
            st.markdown(
                "<p style='font-family:Syne,sans-serif;font-weight:700;font-size:0.9rem;color:#7dd3fc;'>📍 Top Districts</p>",
                unsafe_allow_html=True,
            )
            if "District" in df.columns:
                top_districts = (
                    df["District"].astype(str).str.strip()
                    .replace("", pd.NA).dropna()
                    .value_counts().head(15)
                )
                st.bar_chart(top_districts, color="#10b981")
            else:
                st.info("District column not found in dataset.")

        with st.container(border=True):
            st.markdown(
                "<p style='font-family:Syne,sans-serif;font-weight:700;font-size:0.9rem;color:#7dd3fc;'>📈 Cutoff Explorer</p>",
                unsafe_allow_html=True,
            )
            dash_category = st.selectbox(
                "Category",
                available_categories(dataset),
                key=f"dash_category_{program_label}",
            )
            dash_gender = st.selectbox("Gender", ["BOYS", "GIRLS"], key=f"dash_gender_{program_label}")
            dash_branch = st.selectbox(
                "Branch (optional)",
                ["(Any)"] + available_branches(dataset),
                key=f"dash_branch_{program_label}",
            )
            dash_district = st.selectbox(
                "District (optional)",
                ["(Any)"] + available_districts(dataset),
                key=f"dash_district_{program_label}",
            )

            cut_col = cutoff_column(dataset, dash_category, dash_gender)
            if not cut_col:
                st.warning("No cutoff column found for this category/gender.")
            else:
                df_cut = df.copy()
                df_cut[cut_col] = pd.to_numeric(df_cut[cut_col], errors="coerce")
                if dash_branch != "(Any)":
                    df_cut = df_cut[df_cut["Branch_Name"].astype(str).str.strip() == dash_branch]
                if dash_district != "(Any)":
                    df_cut = df_cut[df_cut["District"].astype(str).str.strip() == dash_district]

                cut = df_cut[cut_col].dropna()
                cut_clean = cut[(cut > 0) & (cut < 999999)]
                if cut_clean.empty:
                    st.info("No usable cutoff values for this selection.")
                else:
                    cut_bins = pd.cut(cut_clean, bins=10)
                    cut_hist = cut_bins.value_counts().sort_index()
                    cut_hist.index = cut_hist.index.astype(str)
                    st.bar_chart(cut_hist, color="#f59e0b")


# ─────────────────────────────────────────────
#  APP SHELL (unchanged routing logic)
# ─────────────────────────────────────────────
def _render_app_shell():
    # Sidebar
    with st.sidebar:
        st.markdown(
            """
<div style="display:flex;align-items:center;gap:0.7rem;padding:0.8rem;border-radius:14px;background:linear-gradient(135deg,rgba(29,78,216,0.25),rgba(14,165,233,0.15));border:1px solid rgba(56,189,248,0.15);margin-bottom:1.2rem;">
  <span style="font-size:1.5rem;">🎓</span>
  <div>
    <p style="font-family:Syne,sans-serif;font-weight:800;font-size:0.95rem;color:#e2e8f0;margin:0;letter-spacing:-0.02em;">College Compass</p>
    <p style="font-size:0.7rem;color:rgba(148,163,184,0.7);margin:0;">India · Admission Guide</p>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown("**Programme**")
        programme = st.selectbox(
            "Programme",
            ["Diploma", "Engineering", "Medical"],
            label_visibility="collapsed",
        )

        st.write("")
        st.markdown("**Page**")
        page = st.radio(
            "Page",
            ["🔍 Recommendations", "📊 Dashboards"],
            horizontal=False,
            label_visibility="collapsed",
        )

        st.divider()

        # User info card
        st.markdown(
            f"""
<div style="padding:0.7rem;border-radius:12px;background:rgba(15,23,42,0.6);border:1px solid rgba(56,189,248,0.1);">
  <p style="font-size:0.7rem;color:rgba(148,163,184,0.6);margin:0 0 0.2rem;letter-spacing:0.04em;text-transform:uppercase;">Logged in as</p>
  <p style="font-family:Syne,sans-serif;font-weight:700;font-size:0.9rem;color:#7dd3fc;margin:0;">👤 {st.session_state['user']}</p>
</div>
""",
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("🚪 Log out", use_container_width=True):
            st.session_state["user"] = None
            st.rerun()

    # Strip the emoji prefix from page selection
    page_key = "Recommendations" if "Recommendations" in page else "Dashboards"

    default_paths = {
        "Diploma":     "cleaned.xlsx",
        "Engineering": r"C:\Users\lokit\Downloads\engineering.xlsx",
        "Medical":     r"C:\Users\lokit\Downloads\NEW MEDICAL CUTOFF.xlsx",
    }

    _header(programme)

    dataset, source = _dataset_or_upload(programme, default_paths[programme])
    if dataset is None:
        st.info(f"Add `{default_paths[programme]}` to the project or upload an Excel file to continue.")
        return

    st.caption(f"📂 Dataset: `{source}`")

    if page_key == "Recommendations":
        _render_recommendations(programme, dataset)
    else:
        _render_dashboards(programme, dataset)

    _render_chatbot()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
_ensure_user_state()
if not st.session_state.get("user"):
    _render_auth_page()
else:
    _render_app_shell()