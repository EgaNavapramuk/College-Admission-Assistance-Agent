import streamlit as st
import base64

from components.ui import apply_custom_css

# -- Page Config must be the first command
st.set_page_config(
    page_title="College Admission Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global styling (Dark/Light mode adjustments and modern dashboard cards)
apply_custom_css()

# -- Define Pages
dash_page = st.Page("pages/dashboard.py", title="Dashboard", icon="📊", default=True)

# Exams
ecet_page = st.Page("pages/ecet.py", title="ECET", icon="📝")
eamcet_page = st.Page("pages/eamcet.py", title="EAMCET", icon="📝")
eapcet_page = st.Page("pages/eapcet.py", title="EAPCET", icon="📝")
jee_main_page = st.Page("pages/jee_main.py", title="JEE Main", icon="🥇")
jee_advanced_page = st.Page("pages/jee_advanced.py", title="JEE Advanced", icon="🏅")
polycet_page = st.Page("pages/polycet.py", title="POLYCET", icon="🛠️")

# Account / Extras
profile_page = st.Page("pages/profile.py", title="Profile", icon="👤")
settings_page = st.Page("pages/settings.py", title="Settings", icon="⚙️")

# -- Navigation Router
pg = st.navigation(
    {
        "Main": [dash_page],
        "Entrance Exams": [ecet_page, eamcet_page, eapcet_page, jee_main_page, jee_advanced_page, polycet_page],
        "Account": [profile_page, settings_page]
    }
)

# Sidebar styling additions
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
      <br>
      © 2026 Hackathon Team<br>
      College Admissions Platform
    </div>
    """,
    unsafe_allow_html=True
)

pg.run()