import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="EduPath India",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── SESSION STATE ──────────────────────────────────────
if "dark" not in st.session_state:
    st.session_state.dark = True

# ── THEME ──────────────────────────────────────────────
D = st.session_state.dark
if D:
    BG        = "#0D1117"
    BG2       = "#161B22"
    BG3       = "#1C2333"
    CARD      = "#1C2333"
    CARD2     = "#212B3A"
    T1        = "#F0F6FC"
    T2        = "#8B949E"
    T3        = "#484F58"
    BORDER    = "#30363D"
    A1        = "#58A6FF"   # blue
    A2        = "#3FB950"   # green
    A3        = "#F0883E"   # orange
    A4        = "#F78166"   # red
    A5        = "#D2A8FF"   # purple
    NAV_BG    = "rgba(13,17,23,0.96)"
    INPUT_BG  = "#0D1117"
    SHADOW    = "rgba(0,0,0,0.5)"
    GLOW1     = "rgba(88,166,255,0.25)"
    GLOW2     = "rgba(63,185,80,0.2)"
else:
    BG        = "#FFFFFF"
    BG2       = "#F6F8FA"
    BG3       = "#EAEEF2"
    CARD      = "#FFFFFF"
    CARD2     = "#F6F8FA"
    T1        = "#1C2128"
    T2        = "#4B5563"
    T3        = "#9CA3AF"
    BORDER    = "#D0D7DE"
    A1        = "#0969DA"   # blue
    A2        = "#1A7F37"   # green
    A3        = "#BC4C00"   # orange
    A4        = "#CF222E"   # red
    A5        = "#8250DF"   # purple
    NAV_BG    = "rgba(255,255,255,0.97)"
    INPUT_BG  = "#FFFFFF"
    SHADOW    = "rgba(0,0,0,0.1)"
    GLOW1     = "rgba(9,105,218,0.15)"
    GLOW2     = "rgba(26,127,55,0.12)"

# ── GLOBAL STYLES ──────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* === RESET === */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

/* === APP BASE === */
html, body, .stApp, [data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {{
    background: {BG} !important;
    color: {T1} !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}

/* === HIDE STREAMLIT CHROME === */
#MainMenu, footer, header,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stStatusWidget"],
.stDeployButton,
[data-testid="stDecoration"] {{ display: none !important; }}

/* === SCROLLBAR === */
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: {BG2}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 4px; }}

/* === BLOCK CONTAINER === */
.block-container {{
    padding: 0 !important;
    max-width: 100% !important;
}}

[data-testid="column"] {{ padding: 0 8px !important; }}

/* =========================================
   NAVBAR  — sticky bar with logo + radio pills
   ========================================= */

/* The navbar wrapper is the FIRST element in stMain */
div[data-testid="stMain"] > div > div > div:first-child {{
    position: sticky !important;
    top: 0 !important;
    z-index: 9999 !important;
    background: {NAV_BG} !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-bottom: 1px solid {BORDER} !important;
    box-shadow: 0 2px 20px {SHADOW} !important;
    padding: 0 2rem !important;
    margin: 0 !important;
}}

/* The horizontal block inside — make it a flex row */
div[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] {{
    display: flex !important;
    align-items: center !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
    height: 60px !important;
    gap: 0 !important;
    flex-wrap: nowrap !important;
}}

/* Logo column — tight, no grow */
div[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {{
    flex: 0 0 auto !important;
    padding: 0 20px 0 0 !important;
    min-width: 0 !important;
}}

/* Radio column — takes remaining space */
div[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {{
    flex: 1 1 auto !important;
    padding: 0 !important;
}}

/* Theme button column — tight on right */
div[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {{
    flex: 0 0 auto !important;
    padding: 0 0 0 12px !important;
}}

/* Logo text */
.nav-logo {{
    font-size: 1.2rem;
    font-weight: 800;
    color: {A1};
    letter-spacing: -0.5px;
    white-space: nowrap;
    font-family: 'Plus Jakarta Sans', sans-serif;
    line-height: 60px;
}}

/* ── RADIO as nav pills ── */
/* Hide the label */
div[data-testid="stRadio"] > label {{
    display: none !important;
}}
/* Row layout */
div[data-testid="stRadio"] > div[role="radiogroup"] {{
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 2px !important;
    align-items: center !important;
    background: transparent !important;
    height: 60px !important;
}}
/* Each pill label */
div[data-testid="stRadio"] > div[role="radiogroup"] > label {{
    display: flex !important;
    align-items: center !important;
    padding: 7px 14px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    color: {T1} !important;
    white-space: nowrap !important;
    border: 1px solid transparent !important;
    transition: all 0.18s ease !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: transparent !important;
    gap: 6px !important;
    user-select: none !important;
}}
div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {{
    color: {A1} !important;
    background: {A1}20 !important;
    border-color: {A1}40 !important;
}}
/* Hide the radio circle dot */
div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {{
    display: none !important;
}}
/* Active / selected pill */
div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
div[data-testid="stRadio"] > div[role="radiogroup"] > label[aria-checked="true"] {{
    color: {T1} !important;
    background: {A1} !important;
    border-color: {A1} !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 10px {GLOW1} !important;
}}
/* Radio span text color inherit */
div[data-testid="stRadio"] > div[role="radiogroup"] > label > span {{
    color: inherit !important;
    font-size: inherit !important;
    font-weight: inherit !important;
}}

/* =========================================
   ALL BUTTONS — default minimal style
   ========================================= */
.stButton > button {{
    background: {BG3} !important;
    color: {T1} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    padding: 7px 14px !important;
    font-size: 0.88rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: background 0.18s ease, border-color 0.18s ease !important;
    box-shadow: none !important;
    width: auto !important;
    min-width: unset !important;
    line-height: 1.4 !important;
    letter-spacing: 0 !important;
}}
.stButton > button:hover {{
    background: {A1}25 !important;
    border-color: {A1}70 !important;
    color: {T1} !important;
    transform: none !important;
    box-shadow: none !important;
}}

/* =========================================
   CANVAS BACKGROUND
   ========================================= */
#bg-canvas {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    opacity: 0.6;
}}

/* =========================================
   HERO SECTION
   ========================================= */
.hero {{
    position: relative;
    z-index: 1;
    max-width: 1400px;
    margin: 0 auto;
    padding: 4rem 2rem 3rem;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
    align-items: center;
}}
.hero-left {{  }}
.hero-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 20px;
    background: {A2}18;
    border: 1px solid {A2}40;
    color: {A2};
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    animation: fadeUp 0.5s ease both;
}}
.hero-title {{
    font-size: clamp(2.4rem, 4.5vw, 4rem);
    font-weight: 800;
    color: {T1};
    line-height: 1.1;
    letter-spacing: -1.5px;
    margin-bottom: 1rem;
    animation: fadeUp 0.5s 0.1s ease both;
}}
.hero-title .accent {{
    color: {A1};
}}
.hero-title .accent2 {{
    color: {A2};
}}
.hero-desc {{
    font-size: 1rem;
    color: {T2};
    line-height: 1.7;
    margin-bottom: 2rem;
    max-width: 460px;
    animation: fadeUp 0.5s 0.2s ease both;
    font-weight: 400;
}}
.hero-stats {{
    display: flex;
    gap: 2rem;
    animation: fadeUp 0.5s 0.3s ease both;
}}
.stat {{
    border-left: 3px solid {A1};
    padding-left: 12px;
}}
.stat-num {{
    font-size: 1.8rem;
    font-weight: 800;
    color: {T1};
    letter-spacing: -1px;
    line-height: 1;
}}
.stat-lbl {{
    font-size: 0.72rem;
    color: {T3};
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 3px;
}}

/* 3D Orb */
.orb-scene {{
    display: flex;
    justify-content: center;
    align-items: center;
    animation: fadeUp 0.6s 0.2s ease both;
}}
.orb-outer {{
    position: relative;
    width: 340px;
    height: 340px;
}}
.orb-ring {{
    position: absolute;
    border-radius: 50%;
    border: 1.5px solid {A1}30;
    animation: spin 14s linear infinite;
}}
.orb-ring.r1 {{ inset: 0; animation-duration: 14s; }}
.orb-ring.r2 {{ inset: 10%; border-color: {A2}25; animation-duration: 20s; animation-direction: reverse; }}
.orb-ring.r3 {{ inset: 20%; border-color: {A5}20; animation-duration: 30s; }}
.ring-dot {{
    position: absolute;
    top: -5px; left: calc(50% - 5px);
    width: 10px; height: 10px;
    border-radius: 50%;
    background: {A1};
    box-shadow: 0 0 12px {A1};
}}
.ring-dot.g {{ background: {A2}; box-shadow: 0 0 12px {A2}; width: 8px; height: 8px; top: -4px; left: calc(50% - 4px); }}
.ring-dot.p {{ background: {A5}; box-shadow: 0 0 12px {A5}; width: 6px; height: 6px; top: -3px; left: calc(50% - 3px); }}
.orb-core {{
    position: absolute;
    inset: 24%;
    border-radius: 50%;
    background: radial-gradient(circle at 38% 35%, {A1}CC, {A2}80 45%, {A5}50 70%, transparent);
    animation: pulse 3.5s ease-in-out infinite;
    box-shadow: 0 0 60px {A1}50, 0 0 100px {A2}30;
}}
.fi {{
    position: absolute;
    font-size: 1.8rem;
    filter: drop-shadow(0 2px 8px {SHADOW});
}}
.fi.f1 {{ top: 8%; left: 2%; animation: flt 3.2s ease-in-out infinite; }}
.fi.f2 {{ top: 6%; right: 2%; animation: flt 3.8s 0.5s ease-in-out infinite; }}
.fi.f3 {{ bottom: 10%; left: 4%; animation: flt 4s 1s ease-in-out infinite; }}
.fi.f4 {{ bottom: 8%; right: 4%; animation: flt 3.5s 1.5s ease-in-out infinite; }}

/* =========================================
   SECTION WRAPPER
   ========================================= */
.sw {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 1.5rem 2rem 3rem;
    position: relative;
    z-index: 1;
}}
.pg-header {{
    margin-bottom: 1.8rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid {BORDER};
}}
.pg-sup {{
    font-size: 0.72rem;
    font-weight: 700;
    color: {A1};
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 4px;
}}
.pg-title {{
    font-size: 1.8rem;
    font-weight: 800;
    color: {T1};
    letter-spacing: -0.8px;
    line-height: 1.2;
}}
.pg-sub {{
    font-size: 0.88rem;
    color: {T3};
    margin-top: 5px;
}}

/* =========================================
   FEATURE CARDS (Home)
   ========================================= */
.feat-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
    gap: 16px;
    margin-top: 1.5rem;
}}
.feat-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 24px 22px 20px;
    cursor: pointer;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}}
.feat-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--fclr);
    transform: scaleX(0);
    transition: transform 0.25s ease;
}}
.feat-card:hover {{
    border-color: var(--fclr);
    transform: translateY(-4px);
    box-shadow: 0 12px 32px {SHADOW};
}}
.feat-card:hover::before {{ transform: scaleX(1); }}
.feat-card:nth-child(1) {{ --fclr: {A1}; }}
.feat-card:nth-child(2) {{ --fclr: {A2}; }}
.feat-card:nth-child(3) {{ --fclr: {A3}; }}
.feat-card:nth-child(4) {{ --fclr: {A4}; }}
.feat-card:nth-child(5) {{ --fclr: {A5}; }}
.feat-card:nth-child(6) {{ --fclr: {A1}; }}
.feat-icon {{
    font-size: 2rem;
    margin-bottom: 12px;
    display: block;
}}
.feat-title {{
    font-size: 1rem;
    font-weight: 700;
    color: {T1};
    margin-bottom: 6px;
}}
.feat-desc {{
    font-size: 0.82rem;
    color: {T2};
    line-height: 1.6;
}}
.feat-arr {{
    position: absolute;
    bottom: 16px;
    right: 16px;
    font-size: 0.9rem;
    color: {T3};
    transition: all 0.2s ease;
}}
.feat-card:hover .feat-arr {{
    color: var(--fclr);
    transform: translate(2px, -2px);
}}

/* =========================================
   INPUT PANEL
   ========================================= */
.inp-panel {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 28px 24px 20px;
    margin-bottom: 24px;
}}

/* =========================================
   RESULT CARDS
   ========================================= */
.rc {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 10px;
    transition: all 0.2s ease;
    position: relative;
    padding-left: 24px;
}}
.rc::before {{
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    border-radius: 12px 0 0 12px;
    background: var(--rclr);
}}
.rc:hover {{
    border-color: var(--rclr);
    box-shadow: 0 4px 20px {SHADOW};
    transform: translateX(3px);
}}
.rc.dream {{ --rclr: {A4}; }}
.rc.moderate {{ --rclr: {A3}; }}
.rc.safe {{ --rclr: {A2}; }}
.rc.info {{ --rclr: {A1}; }}
.rc-top {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 10px;
}}
.rc-name {{
    font-size: 1rem;
    font-weight: 700;
    color: {T1};
    line-height: 1.3;
}}
.rc-chips {{
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}}
.chip {{
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.74rem;
    font-weight: 500;
    background: {BG3};
    border: 1px solid {BORDER};
    color: {T2};
    white-space: nowrap;
}}
.chip.fee {{
    background: {A2}15;
    border-color: {A2}35;
    color: {A2};
}}
.chip.rank {{
    background: {A1}15;
    border-color: {A1}35;
    color: {A1};
}}
.badge {{
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.74rem;
    font-weight: 700;
    white-space: nowrap;
    flex-shrink: 0;
}}
.badge.dream {{ background: {A4}18; border: 1px solid {A4}35; color: {A4}; }}
.badge.moderate {{ background: {A3}18; border: 1px solid {A3}35; color: {A3}; }}
.badge.safe {{ background: {A2}18; border: 1px solid {A2}35; color: {A2}; }}
.badge.none {{ background: {T3}18; border: 1px solid {T3}35; color: {T3}; }}

/* =========================================
   METRIC CARDS
   ========================================= */
.metrics {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 12px;
    margin: 18px 0;
}}
.mc {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
}}
.mc::after {{
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: var(--mclr);
}}
.mc:nth-child(1) {{ --mclr: {A1}; }}
.mc:nth-child(2) {{ --mclr: {A2}; }}
.mc:nth-child(3) {{ --mclr: {A3}; }}
.mc:nth-child(4) {{ --mclr: {A4}; }}
.mc-lbl {{
    font-size: 0.7rem;
    color: {T3};
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 6px;
    font-weight: 600;
}}
.mc-val {{
    font-size: 1.7rem;
    font-weight: 800;
    color: {T1};
    letter-spacing: -0.5px;
    line-height: 1;
}}
.mc-sub {{
    font-size: 0.74rem;
    color: {T3};
    margin-top: 4px;
}}

/* Results count */
.res-count {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 16px;
    background: {A1}15;
    border: 1px solid {A1}30;
    border-radius: 8px;
    color: {A1};
    font-size: 0.84rem;
    font-weight: 700;
    margin-bottom: 16px;
}}

/* =========================================
   PLACEMENTS CHARTS
   ========================================= */
.chart-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 16px;
}}
.chart-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 22px;
}}
.chart-title {{
    font-size: 0.92rem;
    font-weight: 700;
    color: {T1};
    margin-bottom: 14px;
}}
.bar-chart {{ display: flex; flex-direction: column; gap: 9px; }}
.bar-row {{ display: flex; align-items: center; gap: 10px; }}
.bar-lbl {{ font-size: 0.74rem; color: {T2}; min-width: 44px; text-align: right; flex-shrink: 0; }}
.bar-track {{
    flex: 1; height: 24px; border-radius: 6px;
    background: {BG3}; overflow: hidden;
}}
.bar-fill {{
    height: 100%; border-radius: 6px;
    background: var(--bclr);
    animation: growBar 0.9s cubic-bezier(.22,1,.36,1) both;
    display: flex; align-items: center;
    padding: 0 8px; justify-content: flex-end;
}}
.bar-num {{ font-size: 0.7rem; color: white; font-weight: 700; white-space: nowrap; }}

/* Donut */
.donut-wrap {{ display: flex; align-items: center; gap: 20px; margin-top: 6px; }}
.donut-ring {{
    width: 96px; height: 96px;
    border-radius: 50%;
    background: conic-gradient({A2} 0deg var(--pdeg), {A4} var(--pdeg) 360deg);
    position: relative;
    flex-shrink: 0;
    box-shadow: 0 0 24px {A2}30;
}}
.donut-ring::after {{
    content: '';
    position: absolute;
    inset: 22px;
    border-radius: 50%;
    background: {CARD};
}}
.donut-labels {{ display: flex; flex-direction: column; gap: 8px; }}
.dl {{ display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: {T2}; }}
.dl-dot {{ width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }}

/* =========================================
   ANIMATIONS
   ========================================= */
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes spin {{
    from {{ transform: rotate(0deg); }}
    to   {{ transform: rotate(360deg); }}
}}
@keyframes pulse {{
    0%,100% {{ transform: scale(1); box-shadow: 0 0 60px {A1}50,0 0 100px {A2}30; }}
    50%      {{ transform: scale(1.05); box-shadow: 0 0 90px {A1}70,0 0 140px {A2}50; }}
}}
@keyframes flt {{
    0%,100% {{ transform: translateY(0) rotate(0deg); }}
    50%      {{ transform: translateY(-12px) rotate(5deg); }}
}}
@keyframes growBar {{
    from {{ width: 0 !important; opacity: 0; }}
}}

/* =========================================
   STREAMLIT WIDGET OVERRIDES
   ========================================= */
/* Select boxes */
.stSelectbox > div > div,
[data-testid="stSelectbox"] > div > div {{
    background: {INPUT_BG} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    color: {T1} !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.88rem !important;
}}
/* Inputs */
.stNumberInput > div > div > input,
.stTextInput > div > div > input,
.stTextArea > div > textarea {{
    background: {INPUT_BG} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    color: {T1} !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 9px 12px !important;
}}
.stNumberInput > div > div > input:focus,
.stTextInput > div > div > input:focus {{
    border-color: {A1} !important;
    box-shadow: 0 0 0 2px {A1}20 !important;
}}
/* Widget labels */
.stSelectbox > label,
.stNumberInput > label,
.stTextInput > label,
.stTextArea > label,
[data-testid="stWidgetLabel"] > label,
[data-testid="stWidgetLabel"] > div {{
    color: {T2} !important;
    font-size: 0.77rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}
/* Search / action buttons (non-nav) */
div.search-btn .stButton > button,
.search-area .stButton > button {{
    background: {A1} !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.6rem !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    box-shadow: 0 3px 12px {GLOW1} !important;
    width: 100% !important;
}}
div.search-btn .stButton > button:hover {{
    background: {A1}DD !important;
    box-shadow: 0 6px 20px {GLOW1} !important;
    transform: translateY(-1px) !important;
}}
/* Native metrics */
[data-testid="stMetric"] {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    padding: 14px !important;
}}
/* Expander */
[data-testid="stExpander"] {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
}}
/* Alerts */
.stAlert {{ border-radius: 10px !important; }}
/* Dataframe */
[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}}
/* Markdown text */
[data-testid="stMarkdownContainer"] p {{
    color: {T2} !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}
</style>
""", unsafe_allow_html=True)

# ── PARTICLE CANVAS ─────────────────────────────────
a1_js = A1
a2_js = A2
st.markdown(f"""
<canvas id="bg-canvas"></canvas>
<script>
(function() {{
    const c = document.getElementById('bg-canvas');
    if (!c) return;
    const ctx = c.getContext('2d');
    function resize() {{ c.width = window.innerWidth; c.height = window.innerHeight; }}
    resize();
    window.addEventListener('resize', resize);
    const pts = Array.from({{length: 55}}, () => ({{
        x: Math.random() * c.width, y: Math.random() * c.height,
        vx: (Math.random() - .5) * .3, vy: (Math.random() - .5) * .3,
        r: Math.random() * 1.5 + .5, p: Math.random() * Math.PI * 2
    }}));
    let t = 0;
    function draw() {{
        ctx.clearRect(0, 0, c.width, c.height);
        t += 0.007;
        pts.forEach(p => {{
            p.x += p.vx; p.y += p.vy;
            if (p.x < 0 || p.x > c.width) p.vx *= -1;
            if (p.y < 0 || p.y > c.height) p.vy *= -1;
        }});
        for (let i = 0; i < pts.length; i++) {{
            for (let j = i+1; j < pts.length; j++) {{
                const dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y;
                const d = Math.sqrt(dx*dx + dy*dy);
                if (d < 120) {{
                    ctx.beginPath();
                    const a = Math.floor((1 - d/120) * 30).toString(16).padStart(2,'0');
                    ctx.strokeStyle = '{a1_js}' + a;
                    ctx.lineWidth = .5;
                    ctx.moveTo(pts[i].x, pts[i].y);
                    ctx.lineTo(pts[j].x, pts[j].y);
                    ctx.stroke();
                }}
            }}
            const g = (Math.sin(t + pts[i].p) * .5 + .5);
            ctx.beginPath();
            ctx.arc(pts[i].x, pts[i].y, pts[i].r * (1 + g * .4), 0, Math.PI*2);
            const a2 = Math.floor((100 + g * 100)).toString(16).padStart(2,'0');
            ctx.fillStyle = (i % 3 === 0 ? '{a2_js}' : '{a1_js}') + a2;
            ctx.fill();
        }}
        requestAnimationFrame(draw);
    }}
    draw();
}})();
</script>
""", unsafe_allow_html=True)

# ── NAVBAR ────────────────────────────────────────────
PAGE_OPTS = ["🏠 Home", "🎓 Polytechnic", "🏫 Engineering", "🩺 Medical", "📊 JEE Cutoff", "💼 Placements", "🏆 Top Colleges"]
THEME_ICO = "☀️" if D else "🌙"

logo_col, nav_col, theme_col = st.columns([2, 10, 1])
with logo_col:
    st.markdown('<div class="nav-logo">⬡ EduPath</div>', unsafe_allow_html=True)
with nav_col:
    page = st.radio("nav", PAGE_OPTS, horizontal=True, label_visibility="collapsed", key="nav_radio")
with theme_col:
    if st.button(THEME_ICO, key="theme_btn", help="Toggle theme"):
        st.session_state.dark = not st.session_state.dark
        st.rerun()

# ── HELPERS ─────────────────────────────────────────
@st.cache_data
def load_poly():
    try:
        df = pd.read_csv("data/polytechnic.csv")
        df.columns = df.columns.str.strip().str.replace('\n',' ').str.replace('\r',' ').str.replace('  ',' ').str.strip()
        return df
    except: return None

@st.cache_data
def load_eng():
    try: return pd.read_csv("data/engineering_data.csv")
    except: return None

@st.cache_data
def load_med():
    try: return pd.read_csv("data/medical_data.csv")
    except: return None

@st.cache_data
def load_place():
    for p in ["data/placedata v2.0 synthetic.csv","data/placedata_v2_0_synthetic.csv"]:
        try: return pd.read_csv(p)
        except: continue
    return None

@st.cache_data
def load_top():
    for p in ["data/update_data_of_300.csv","data/200_top_Engineering_Colleges_india.csv"]:
        try: return pd.read_csv(p)
        except: continue
    return None

@st.cache_data
def load_jee():
    try: return pd.read_csv("data/jee_cutoff.csv")
    except: return None

def classify(rank, closing):
    if rank <= closing * 0.35: return "dream"
    if rank <= closing: return "moderate"
    return "safe"

def badge_html(cls):
    labels = {"dream":("🔥 Dream","dream"), "moderate":("⚖ Moderate","moderate"), "safe":("✅ Safe","safe")}
    txt, css = labels.get(cls, ("—","none"))
    return f'<span class="badge {css}">{txt}</span>'

def result_card(name, chips_html, badge_cls, badge_txt=None, msg=""):
    bh = badge_html(badge_cls) if badge_txt is None else f'<span class="badge {badge_cls}">{badge_txt}</span>'
    return f"""
<div class="rc {badge_cls}">
  <div class="rc-top">
    <div class="rc-name">{name}</div>
    {bh}
  </div>
  {"<p style='font-size:0.84rem;color:"+T2+";margin:-2px 0 10px;'>"+msg+"</p>" if msg else ""}
  <div class="rc-chips">{chips_html}</div>
</div>"""

def chip(text, cls=""): return f'<span class="chip {cls}">{text}</span>'
def mcard(label, val, sub="", idx=1): return f'<div class="mc" style="--mclr:var(--mc{idx})"><div class="mc-lbl">{label}</div><div class="mc-val">{val}</div><div class="mc-sub">{sub}</div></div>'

# ════════════════════════════════════════════
#  HOME
# ════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown(f"""
    <div class="hero">
      <div class="hero-left">
        <div class="hero-badge">🇮🇳 India's Smart Education Platform</div>
        <div class="hero-title">
          Find Your <span class="accent">Perfect</span><br>
          <span class="accent2">College</span> Journey
        </div>
        <div class="hero-desc">
          AI-powered search across Polytechnic, Engineering, Medical &amp; JEE.
          Compare cutoffs, fees, and placements — make smarter decisions.
        </div>
        <div class="hero-stats">
          <div class="stat"><div class="stat-num">500+</div><div class="stat-lbl">Colleges</div></div>
          <div class="stat"><div class="stat-num">50+</div><div class="stat-lbl">Branches</div></div>
          <div class="stat"><div class="stat-num">10K+</div><div class="stat-lbl">Data Points</div></div>
        </div>
      </div>
      <div class="orb-scene">
        <div class="orb-outer">
          <div class="orb-ring r1"><div class="ring-dot"></div></div>
          <div class="orb-ring r2"><div class="ring-dot g"></div></div>
          <div class="orb-ring r3"><div class="ring-dot p"></div></div>
          <div class="orb-core"></div>
          <div class="fi f1">🎓</div>
          <div class="fi f2">🏫</div>
          <div class="fi f3">🩺</div>
          <div class="fi f4">📊</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sw">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="pg-header">
      <div class="pg-sup">Explore</div>
      <div class="pg-title">All Tools</div>
      <div class="pg-sub">Six powerful tools to discover and compare India's best institutions</div>
    </div>
    <div class="feat-grid">
      <div class="feat-card"><span class="feat-icon">🎓</span><div class="feat-title">Polytechnic Finder</div><div class="feat-desc">Filter diploma colleges by rank, category, branch &amp; budget.</div><span class="feat-arr">↗</span></div>
      <div class="feat-card"><span class="feat-icon">🏫</span><div class="feat-title">Engineering Explorer</div><div class="feat-desc">Check B.Tech cutoffs across 150+ colleges by district and branch.</div><span class="feat-arr">↗</span></div>
      <div class="feat-card"><span class="feat-icon">🩺</span><div class="feat-title">Medical Colleges</div><div class="feat-desc">Explore MBBS, BDS, BHMS across private and government colleges.</div><span class="feat-arr">↗</span></div>
      <div class="feat-card"><span class="feat-icon">📊</span><div class="feat-title">JEE Cutoff Trends</div><div class="feat-desc">Historical cutoffs, trend charts and ML rank prediction.</div><span class="feat-arr">↗</span></div>
      <div class="feat-card"><span class="feat-icon">💼</span><div class="feat-title">Placement Insights</div><div class="feat-desc">Analyze 10,000+ records — CGPA trends, placement rates and more.</div><span class="feat-arr">↗</span></div>
      <div class="feat-card"><span class="feat-icon">🏆</span><div class="feat-title">Top 300 Rankings</div><div class="feat-desc">NIRF rankings with detailed scoring for India's top institutions.</div><span class="feat-arr">↗</span></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
#  POLYTECHNIC
# ════════════════════════════════════════════
elif page == "🎓 Polytechnic":
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="pg-header">
      <div class="pg-sup">Diploma Admissions</div>
      <div class="pg-title">Polytechnic Finder</div>
      <div class="pg-sub">Find diploma colleges that match your rank, category and budget</div>
    </div>""", unsafe_allow_html=True)

    df = load_poly()
    if df is None:
        st.error("⚠️ `data/polytechnic.csv` not found.")
    else:
        st.markdown('<div class="inp-panel">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: rank = st.number_input("Your Rank", min_value=1, value=5000, step=100)
        with c2: cat  = st.selectbox("Category", ["OC","BC_A","BC_B","BC_C","BC_D","BC_E","SC","ST","EWS"])
        with c3:
            br_opts = ["All Branches"] + sorted(df["BRANCH NAME"].dropna().unique())
            branch = st.selectbox("Branch", br_opts)
        with c4: budget = st.number_input("Max Fee (₹)", min_value=0, value=20000, step=1000)
        c5, c6 = st.columns([3,1])
        with c5: sort = st.selectbox("Sort By", ["Best Rank Fit","Low Fee First","Name A–Z"])
        with c6:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="search-btn">', unsafe_allow_html=True)
            go = st.button("🔍 Search", key="poly_go")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if go:
            rank_col = None
            for col in df.columns:
                if cat in col and "BOYS" in col: rank_col = col; break
            if rank_col is None:
                for col in df.columns:
                    if cat in col: rank_col = col; break

            if rank_col is None:
                st.warning(f"Category '{cat}' column not found in data.")
            else:
                df[rank_col] = pd.to_numeric(df[rank_col], errors="coerce")
                res = df[df[rank_col] >= rank].copy()
                if branch != "All Branches": res = res[res["BRANCH NAME"] == branch]
                if budget > 0: res = res[res["FEE"] <= budget]

                if res.empty:
                    st.warning("No colleges found — try relaxing filters.")
                else:
                    if sort == "Low Fee First": res = res.sort_values("FEE")
                    elif sort == "Name A–Z": res = res.sort_values("INSTITUTE NAME")
                    else: res = res.sort_values(rank_col)

                    st.markdown(f'<div class="res-count">🎯 {len(res)} colleges found</div>', unsafe_allow_html=True)
                    for i, (_, row) in enumerate(res.iterrows()):
                        cls = classify(rank, row[rank_col])
                        fee = f"₹{int(row['FEE']):,}" if pd.notna(row.get('FEE')) else "N/A"
                        closing = f"{int(row[rank_col]):,}" if pd.notna(row[rank_col]) else "N/A"
                        chips = (chip(f"📚 {row['BRANCH NAME']}") +
                                 chip(f"📍 {row['DISTRICT']}") +
                                 chip(f"🏛 {row.get('COLLEGE TYPE','—')}") +
                                 chip(f"Closing: {closing}", "rank") +
                                 chip(fee, "fee"))
                        st.markdown(result_card(row['INSTITUTE NAME'], chips, cls), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
#  ENGINEERING
# ════════════════════════════════════════════
elif page == "🏫 Engineering":
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="pg-header">
      <div class="pg-sup">B.Tech Admissions</div>
      <div class="pg-title">Engineering Explorer</div>
      <div class="pg-sub">Check cutoff ranks and eligibility for B.Tech colleges in Telangana</div>
    </div>""", unsafe_allow_html=True)

    df = load_eng()
    if df is None:
        st.error("⚠️ `data/engineering_data.csv` not found.")
    else:
        st.markdown('<div class="inp-panel">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: dist  = st.selectbox("District", sorted(df["DISTRICT"].dropna().unique()))
        ddf = df[df["DISTRICT"] == dist]
        with c2: coll  = st.selectbox("College", sorted(ddf["INSTITUTE NAME"].dropna().unique()))
        cdf = ddf[ddf["INSTITUTE NAME"] == coll]
        with c3: brnch = st.selectbox("Branch", sorted(cdf["BRANCH NAME"].dropna().unique()))
        bdf = cdf[cdf["BRANCH NAME"] == brnch]

        CATS = ["OC BOYS","OC GIRLS","BC_A BOYS","BC_A GIRLS","BC_B BOYS","BC_B GIRLS",
                "BC_C BOYS","BC_C GIRLS","BC_D BOYS","BC_D GIRLS","BC_E BOYS","BC_E GIRLS",
                "SC BOYS","SC GIRLS","ST BOYS","ST GIRLS","EWS GEN OU","EWS GIRLS OU"]
        c4, c5 = st.columns(2)
        with c4: cat   = st.selectbox("Category", CATS)
        with c5: rank  = st.number_input("Your Rank", min_value=1, value=15000, step=500)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="search-btn">', unsafe_allow_html=True)
        go = st.button("✅ Check Eligibility", key="eng_go")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if go:
            if bdf.empty:
                st.warning("No data for this selection.")
            elif cat not in bdf.columns:
                st.warning(f"Column '{cat}' not found.")
            else:
                row = bdf.iloc[0]
                cutoff = row[cat]
                fee    = row.get("FEE", 0)
                if pd.isna(cutoff) or int(cutoff) >= 999999:
                    st.markdown(result_card(coll,
                        chip(f"📚 {brnch}") + chip(f"🏷 {cat}"),
                        "none", "⚠️ No Seat"), unsafe_allow_html=True)
                else:
                    cutoff = int(cutoff)
                    cls    = classify(rank, cutoff)
                    gap    = cutoff - rank
                    msgs   = {
                        "dream":    "🎉 Your rank is well within cutoff — strong admission chances.",
                        "moderate": "👍 Your rank is within cutoff but competition may be high.",
                        "safe":     "⚠️ Your rank exceeds the closing rank — not eligible.",
                    }
                    # metric cards
                    mc_colors = {1: A1, 2: A2, 3: A3, 4: A4}
                    st.markdown(f"""
                    <div class="metrics" style="--mc1:{A1};--mc2:{A2};--mc3:{A3};--mc4:{A4};">
                      <div class="mc" style="--mclr:{A1}"><div class="mc-lbl">Closing Rank</div><div class="mc-val">{cutoff:,}</div><div class="mc-sub">{cat}</div></div>
                      <div class="mc" style="--mclr:{A2}"><div class="mc-lbl">Annual Fee</div><div class="mc-val">₹{int(fee):,}</div><div class="mc-sub">Per year</div></div>
                      <div class="mc" style="--mclr:{A3}"><div class="mc-lbl">Your Rank</div><div class="mc-val">{rank:,}</div><div class="mc-sub">Entered</div></div>
                      <div class="mc" style="--mclr:{A4}"><div class="mc-lbl">Rank Gap</div><div class="mc-val">{gap:+,}</div><div class="mc-sub">vs closing</div></div>
                    </div>
                    """, unsafe_allow_html=True)
                    chips = (chip(f"📚 {brnch}") + chip(f"📍 {dist}") + chip(f"🏷 {cat}"))
                    st.markdown(result_card(coll, chips, cls, msg=msgs[cls]), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
#  MEDICAL
# ════════════════════════════════════════════
elif page == "🩺 Medical":
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="pg-header">
      <div class="pg-sup">MBBS &amp; Allied Courses</div>
      <div class="pg-title">Medical Colleges</div>
      <div class="pg-sub">Explore MBBS, BDS, BHMS and more across Telangana</div>
    </div>""", unsafe_allow_html=True)

    df = load_med()
    if df is None:
        st.error("⚠️ `data/medical_data.csv` not found.")
    else:
        st.markdown('<div class="inp-panel">', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1: dist   = st.selectbox("District", sorted(df["DISTRICT"].dropna().unique()))
        ddf = df[df["DISTRICT"]==dist]
        with c2: coll   = st.selectbox("College", sorted(ddf["INSTITUTE NAME"].dropna().unique()))
        cdf = ddf[ddf["INSTITUTE NAME"]==coll]
        with c3: course = st.selectbox("Course", sorted(cdf["COURSE NAME"].dropna().unique()))
        final = cdf[cdf["COURSE NAME"]==course]

        CATS = ["OC BOYS","OC GIRLS","BC_A BOYS","BC_A GIRLS","BC_B BOYS","BC_B GIRLS","SC BOYS","SC GIRLS","ST BOYS","ST GIRLS","EWS GEN OU"]
        av_cats = [c for c in CATS if c in df.columns]
        c4,c5 = st.columns(2)
        with c4: cat  = st.selectbox("Category (for eligibility)", av_cats) if av_cats else None
        with c5: rank = st.number_input("Your Rank (0 = skip)", min_value=0, value=0, step=100)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="search-btn">', unsafe_allow_html=True)
        go = st.button("🔍 View Info", key="med_go")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if go:
            if final.empty:
                st.warning("No data found.")
            else:
                for _, row in final.iterrows():
                    is_govt  = any(k in str(row.get("COLLEGE TYPE","")).upper() for k in ["GOVT","GOV"])
                    ct_color = A2 if is_govt else A3
                    badge_cls, badge_str = "none", ""
                    cutoff_chip = ""
                    if cat and cat in row.index and rank > 0:
                        cv = row[cat]
                        if pd.notna(cv) and int(cv) < 999999:
                            cls      = classify(rank, int(cv))
                            badge_cls = cls
                            badge_str = {"dream":"🔥 Dream","moderate":"⚖ Moderate","safe":"✅ Safe"}.get(cls,"")
                            cutoff_chip = chip(f"{cat}: {int(cv):,}", "rank")
                    fee = f"₹{int(row['FEE']):,}" if pd.notna(row.get('FEE')) else "N/A"
                    chips = (chip(f"📋 {row['COURSE NAME']}") +
                             chip(f"📍 {row['DISTRICT']}") +
                             f'<span class="chip" style="background:{ct_color}15;border-color:{ct_color}35;color:{ct_color}">🏥 {row["COLLEGE TYPE"]}</span>' +
                             chip(fee, "fee") +
                             cutoff_chip)
                    bh = f'<span class="badge {badge_cls}">{badge_str}</span>' if badge_str else '<span class="badge none">ℹ Info</span>'
                    st.markdown(f"""
                    <div class="rc info">
                      <div class="rc-top"><div class="rc-name">{row['INSTITUTE NAME']}</div>{bh}</div>
                      <div class="rc-chips">{chips}</div>
                    </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
#  JEE CUTOFF
# ════════════════════════════════════════════
elif page == "📊 JEE Cutoff":
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="pg-header">
      <div class="pg-sup">JoSAA Data</div>
      <div class="pg-title">JEE Main Cutoff Explorer</div>
      <div class="pg-sub">Historical cutoffs, year-on-year trends and ML rank prediction</div>
    </div>""", unsafe_allow_html=True)

    df = load_jee()
    if df is None:
        st.info("ℹ️ Place `jee_cutoff.csv` in your `data/` folder to use this feature.")
        st.markdown(f"""
        <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:24px;color:{T2};font-size:0.88rem;line-height:1.7;">
        Expected columns: <code>Institute</code>, <code>Year</code>, <code>Round</code>,
        <code>Academic Program Name</code>, <code>Seat Type</code>, <code>Gender</code>,
        <code>Opening Rank</code>, <code>Closing Rank</code>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="inp-panel">', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1: inst = st.selectbox("Institute", sorted(df["Institute"].unique()))
        idf = df[df["Institute"]==inst]
        with c2: year = st.selectbox("Year", sorted(idf["Year"].unique(), reverse=True))
        ydf = idf[idf["Year"]==year]
        c3,c4 = st.columns(2)
        with c3: rnd  = st.selectbox("Round", sorted(ydf["Round"].unique()))
        rdf = ydf[ydf["Round"]==rnd]
        prog = st.selectbox("Program", sorted(rdf["Academic Program Name"].unique()))
        pdf = rdf[rdf["Academic Program Name"]==prog]
        c5,c6 = st.columns(2)
        with c5: stype = st.selectbox("Category", sorted(pdf["Seat Type"].unique()))
        sdf = pdf[pdf["Seat Type"]==stype]
        with c6: gend  = st.selectbox("Gender", sorted(sdf["Gender"].unique()))
        final = sdf[sdf["Gender"]==gend]
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="search-btn">', unsafe_allow_html=True)
        go = st.button("📊 View Cutoff", key="jee_go")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if go:
            if final.empty:
                st.warning("No data found for this selection.")
            else:
                op = int(final.iloc[0]["Opening Rank"])
                cl = int(final.iloc[0]["Closing Rank"])
                st.markdown(f"""
                <div class="metrics">
                  <div class="mc" style="--mclr:{A1}"><div class="mc-lbl">Opening Rank</div><div class="mc-val">{op:,}</div><div class="mc-sub">{stype}</div></div>
                  <div class="mc" style="--mclr:{A2}"><div class="mc-lbl">Closing Rank</div><div class="mc-val">{cl:,}</div><div class="mc-sub">{gend}</div></div>
                  <div class="mc" style="--mclr:{A3}"><div class="mc-lbl">Round</div><div class="mc-val">{rnd}</div><div class="mc-sub">Year {year}</div></div>
                </div>""", unsafe_allow_html=True)

                trend = df[(df["Institute"]==inst)&(df["Academic Program Name"]==prog)&(df["Seat Type"]==stype)&(df["Gender"]==gend)]
                td = trend.groupby("Year")["Closing Rank"].mean().reset_index()
                st.markdown(f'<div style="font-weight:700;color:{T1};margin:20px 0 8px;font-size:1rem;">📈 Closing Rank Trend</div>', unsafe_allow_html=True)
                st.line_chart(td.set_index("Year"), height=260, use_container_width=True)

                if len(td) > 1:
                    from sklearn.linear_model import LinearRegression
                    import numpy as np
                    mdl = LinearRegression()
                    mdl.fit(td["Year"].values.reshape(-1,1), td["Closing Rank"].values)
                    ny   = int(td["Year"].max()) + 1
                    pred = int(mdl.predict([[ny]])[0])
                    diff = pred - cl
                    st.markdown(f"""
                    <div class="metrics" style="margin-top:16px;">
                      <div class="mc" style="--mclr:{A5}"><div class="mc-lbl">Predicted {ny}</div><div class="mc-val">{pred:,}</div><div class="mc-sub">{'📈 Rising' if diff > 0 else '📉 Falling'}</div></div>
                      <div class="mc" style="--mclr:{A4}"><div class="mc-lbl">Change</div><div class="mc-val">{diff:+,}</div><div class="mc-sub">vs {year}</div></div>
                    </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
#  PLACEMENTS
# ════════════════════════════════════════════
elif page == "💼 Placements":
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="pg-header">
      <div class="pg-sup">Career Analytics</div>
      <div class="pg-title">Placement Insights</div>
      <div class="pg-sub">10,000+ student records — CGPA trends, placement rates and success factors</div>
    </div>""", unsafe_allow_html=True)

    df = load_place()
    if df is None:
        st.error("⚠️ Placement data not found in `data/` folder.")
    else:
        total = len(df)
        placed = int((df["PlacementStatus"]=="Placed").sum())
        not_pl = total - placed
        rate   = round(placed/total*100, 1)
        pdeg   = int(rate/100*360)

        st.markdown(f"""
        <div class="metrics">
          <div class="mc" style="--mclr:{A1}"><div class="mc-lbl">Total Students</div><div class="mc-val">{total:,}</div><div class="mc-sub">Records</div></div>
          <div class="mc" style="--mclr:{A2}"><div class="mc-lbl">Placed</div><div class="mc-val">{placed:,}</div><div class="mc-sub">Got Jobs</div></div>
          <div class="mc" style="--mclr:{A4}"><div class="mc-lbl">Not Placed</div><div class="mc-val">{not_pl:,}</div><div class="mc-sub">Awaiting</div></div>
          <div class="mc" style="--mclr:{A3}"><div class="mc-lbl">Success Rate</div><div class="mc-val">{rate}%</div><div class="mc-sub">Overall</div></div>
        </div>""", unsafe_allow_html=True)

        # CGPA bars
        cp = df[df["PlacementStatus"]=="Placed"]["CGPA"].value_counts().sort_index()
        cn = df[df["PlacementStatus"]=="NotPlaced"]["CGPA"].value_counts().sort_index()
        all_c = sorted(df["CGPA"].unique())
        mx = max([cp.get(c,0)+cn.get(c,0) for c in all_c], default=1)
        COLS = [A1, A2, A3, A4, A5]
        bars_html = ""
        for i,cgpa in enumerate(all_c):
            pv = cp.get(cgpa,0); nv = cn.get(cgpa,0); tot = pv+nv
            pct = tot/mx*100; pp = pv/tot*100 if tot else 0
            bc = COLS[i%len(COLS)]
            bars_html += f'<div class="bar-row" style="animation-delay:{i*0.05}s"><div class="bar-lbl">{cgpa}</div><div class="bar-track"><div class="bar-fill" style="width:{pct:.1f}%;--bclr:linear-gradient(90deg,{bc},{COLS[(i+1)%len(COLS)]})" ><span class="bar-num">{tot} ({pp:.0f}%✓)</span></div></div></div>'

        # Internship bars
        ig = df.groupby("Internships")["PlacementStatus"].apply(lambda x:(x=="Placed").mean()*100).reset_index()
        int_bars = ""
        for i,r in ig.iterrows():
            bc = COLS[i%len(COLS)]
            int_bars += f'<div class="bar-row" style="animation-delay:{i*0.08}s"><div class="bar-lbl" style="min-width:52px">{int(r["Internships"])} int.</div><div class="bar-track"><div class="bar-fill" style="width:{r["PlacementStatus"]:.1f}%;--bclr:{bc}"><span class="bar-num">{r["PlacementStatus"]:.1f}%</span></div></div></div>'

        st.markdown(f"""
        <div class="chart-grid">
          <div class="chart-card">
            <div class="chart-title">📊 Students by CGPA — bar width = total, % = placed</div>
            <div class="bar-chart">{bars_html}</div>
          </div>
          <div class="chart-card">
            <div class="chart-title">🎯 Placement Rate by Internships Count</div>
            <div class="bar-chart">{int_bars}</div>
            <div style="margin-top:22px;">
              <div class="chart-title" style="font-size:0.86rem;">🍩 Overall Split</div>
              <div class="donut-wrap">
                <div class="donut-ring" style="--pdeg:{pdeg}deg"></div>
                <div class="donut-labels">
                  <div class="dl"><div class="dl-dot" style="background:{A2}"></div><strong style="color:{T1}">{rate}%</strong>&nbsp;Placed ({placed:,})</div>
                  <div class="dl"><div class="dl-dot" style="background:{A4}"></div><strong style="color:{T1}">{100-rate:.1f}%</strong>&nbsp;Not Placed ({not_pl:,})</div>
                </div>
              </div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        with st.expander("📋 Raw Dataset (first 50 rows)"):
            st.dataframe(df.head(50), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
#  TOP COLLEGES
# ════════════════════════════════════════════
elif page == "🏆 Top Colleges":
    st.markdown('<div class="sw">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="pg-header">
      <div class="pg-sup">NIRF Rankings</div>
      <div class="pg-title">Top 300 Engineering Colleges</div>
      <div class="pg-sub">NIRF-ranked institutions with detailed score breakdown</div>
    </div>""", unsafe_allow_html=True)

    df = load_top()
    if df is None:
        st.error("⚠️ Rankings data not found in `data/` folder.")
    else:
        st.markdown('<div class="inp-panel">', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1: q   = st.text_input("Search Name", placeholder="IIT, NIT, Osmania…")
        with c2:
            if "owner_ship" in df.columns:
                ow_opts = ["All"] + sorted(df["owner_ship"].dropna().unique())
                ow = st.selectbox("Ownership", ow_opts)
            else: ow = "All"
        with c3: top_n = st.selectbox("Show", [10,25,50,100,200,300], index=2)
        st.markdown('</div>', unsafe_allow_html=True)

        res = df.copy()
        if q: res = res[res["name"].str.lower().str.contains(q.lower(), na=False)]
        if ow != "All" and "owner_ship" in res.columns: res = res[res["owner_ship"]==ow]
        res = res.head(top_n)

        st.markdown(f'<div class="res-count">🏆 {len(res)} colleges</div>', unsafe_allow_html=True)

        sc = next((c for c in ["total","nirf_score","perc"] if c in res.columns), None)
        gc = "grade" if "grade" in res.columns else None

        for i,(_, row) in enumerate(res.iterrows()):
            rk   = int(row.get("rank", i+1)) if pd.notna(row.get("rank",None)) else i+1
            scv  = f"{float(row[sc]):.1f}" if sc and pd.notna(row.get(sc)) else "—"
            grv  = str(row[gc]) if gc and pd.notna(row.get(gc)) else "—"
            own  = str(row.get("owner_ship","—"))
            city = str(row.get("city", row.get("state","—")))
            med  = "🥇" if rk==1 else "🥈" if rk==2 else "🥉" if rk==3 else f"#{rk}"
            cls  = "dream" if rk<=10 else "moderate" if rk<=50 else "safe"
            bstr = "🔥 Top 10" if rk<=10 else "⭐ Top 50" if rk<=50 else "✅ Ranked"
            chips = chip(f"🏛 {own}") + chip(f"📍 {city}") + chip(f"⭐ {grv}") + chip(f"Score: {scv}", "rank")
            st.markdown(f"""
            <div class="rc {cls}" style="animation-delay:{min(i*0.025,0.6)}s">
              <div class="rc-top">
                <div class="rc-name">{med} {str(row['name']).title()}</div>
                <span class="badge {cls}">{bstr}</span>
              </div>
              <div class="rc-chips">{chips}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)