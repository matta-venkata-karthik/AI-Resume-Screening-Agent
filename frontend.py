# ==========================================================
# AI Resume Screening Agent
# Main Streamlit Application
# ==========================================================

import streamlit as st
import os
import requests

# ----------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------

st.set_page_config(
    page_title="AI Resume Screening Agent",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------
# Backend Configuration
# ----------------------------------------------------------

BACKEND_URL = "https://YOUR-BACKEND-NAME.onrender.com"

# ----------------------------------------------------------
# Wake Up Backend
# ----------------------------------------------------------

@st.cache_resource
def wake_backend():

    try:
        response = requests.get(
            BACKEND_URL,
            timeout=60
        )

        return response.status_code

    except requests.exceptions.RequestException:
        return None


backend_status = wake_backend()

# ----------------------------------------------------------
# Load Custom CSS
# ----------------------------------------------------------

css_path = "assets/style.css"

if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ----------------------------------------------------------
# Sidebar
# ----------------------------------------------------------

st.sidebar.image(
    "https://img.icons8.com/color/96/resume.png",
    width=80
)

st.sidebar.title("AI Resume Screening Agent")

st.sidebar.markdown("---")

st.sidebar.write("Version 1.0")

# ----------------------------------------------------------
# Main Home Screen
# ----------------------------------------------------------

st.title("📄 AI Resume Screening Agent")

col1, col2 = st.columns([2, 1])

with col1:

    st.header("Welcome")

    st.write(
        """
This application uses **Machine Learning** and **Artificial Intelligence**
to automate resume screening and assist recruiters in selecting the most
suitable candidates.

### Features

- Resume Screening
- Candidate Portal
- Recruiter Dashboard
- AI Resume Assistant
- Resume Match Score
- Skill Gap Analysis
- Interview Question Generation
- Hiring Reports
- Analytics Dashboard
"""
    )

with col2:

    st.image(
        "https://img.icons8.com/color/480/artificial-intelligence.png",
        use_container_width=280
    )

st.markdown("---")

st.subheader("Project Workflow")

st.code("""
Candidate
      │
      ▼
Upload Resume
      │
      ▼
Resume Parser
      │
      ▼
Feature Extraction
      │
      ▼
Decision Tree Prediction
      │
      ▼
AI Resume Assistant
      │
      ▼
Recruiter Dashboard
      │
      ▼
Admin Dashboard
""")

st.markdown("---")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("ML Model", "Decision Tree")

with c2:
    st.metric("Backend", "FastAPI")

with c3:
    st.metric("Frontend", "Streamlit")

with c4:
    st.metric("Dataset", "11,000 Records")

st.markdown("---")

st.success(
    "Use the pages in the left sidebar to navigate through the application."
)
