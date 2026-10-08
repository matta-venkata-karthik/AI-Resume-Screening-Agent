# ==========================================================
# AI Resume Screening Agent
# Main Streamlit Application
# ==========================================================

import streamlit as st
import os
import time
import requests


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="AI Resume Screening Agent",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# Backend Configuration
# ==========================================================

BACKEND_URL = "https://YOUR-BACKEND-NAME.onrender.com"


# ==========================================================
# Backend Health Check
# ==========================================================

def health_check():
    """
    Check and wake the FastAPI backend.

    The frontend automatically calls the backend when
    the Streamlit session starts.

    Returns:
        True if backend is available.
        False otherwise.
    """

    try:

        response = requests.get(
            BACKEND_URL,
            timeout=60
        )

        if response.status_code == 200:
            return True

        return False

    except requests.exceptions.RequestException:
        return False


# ==========================================================
# Backend Connection
# ==========================================================

def check_backend_connection():

    # Do not repeatedly wake the backend on every
    # Streamlit rerun during the same browser session.
    if st.session_state.get(
        "backend_checked",
        False
    ):

        return st.session_state.get(
            "backend_available",
            False
        )

    st.session_state[
        "backend_checked"
    ] = True

    st.session_state[
        "backend_available"
    ] = False

    # Number of attempts
    max_attempts = 4

    for attempt in range(
        1,
        max_attempts + 1
    ):

        try:

            result = health_check()

            if result is True:

                st.session_state[
                    "backend_available"
                ] = True

                return True

        except Exception:
            pass

        # Give Render time to wake up
        if attempt < max_attempts:

            time.sleep(
                attempt * 2
            )

    return False


# ==========================================================
# Start Backend Connection
# ==========================================================

with st.spinner(
    "🔄 Connecting to backend... It may take a minute."
):

    backend_available = (
        check_backend_connection()
    )


# ==========================================================
# Load Custom CSS
# ==========================================================

css_path = "assets/style.css"

if os.path.exists(css_path):

    with open(
        css_path,
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.image(
    "https://img.icons8.com/color/96/resume.png",
    width=80
)

st.sidebar.title(
    "AI Resume Screening Agent"
)

st.sidebar.markdown("---")

st.sidebar.write(
    "Version 1.0"
)


# ==========================================================
# Backend Status
# ==========================================================

st.sidebar.markdown("---")

st.sidebar.subheader(
    "Backend Status"
)

if backend_available:

    st.sidebar.success(
        "🟢 Backend Connected"
    )

    st.sidebar.caption(
        BACKEND_URL
    )

else:

    st.sidebar.error(
        "🔴 Backend Unavailable"
    )

    st.sidebar.caption(
        BACKEND_URL
    )

    if st.sidebar.button(
        "🔄 Retry Backend",
        use_container_width=True
    ):

        st.session_state[
            "backend_checked"
        ] = False

        st.session_state[
            "backend_available"
        ] = False

        st.rerun()


# ==========================================================
# Backend Warning
# ==========================================================

if not backend_available:

    st.warning(
        """
⚠️ The FastAPI backend is currently unavailable.

The application will continue to load, but features that
require the backend may not work until the backend becomes
available.

Use **Retry Backend** from the sidebar after a short wait.
"""
    )


# ==========================================================
# Main Home Screen
# ==========================================================

st.title(
    "📄 AI Resume Screening Agent"
)


col1, col2 = st.columns(
    [2, 1]
)


# ==========================================================
# Welcome Section
# ==========================================================

with col1:

    st.header(
        "Welcome"
    )

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


# ==========================================================
# AI Image
# ==========================================================

with col2:

    st.image(
        "https://img.icons8.com/color/480/artificial-intelligence.png",
        use_container_width=280
    )


# ==========================================================
# Project Workflow
# ==========================================================

st.markdown("---")

st.subheader(
    "Project Workflow"
)

st.code(
    """
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
"""
)


# ==========================================================
# Project Technologies
# ==========================================================

st.markdown("---")

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "ML Model",
        "Decision Tree"
    )


with c2:

    st.metric(
        "Backend",
        "FastAPI"
    )


with c3:

    st.metric(
        "Frontend",
        "Streamlit"
    )


with c4:

    st.metric(
        "Dataset",
        "11,000 Records"
    )


# ==========================================================
# Application Status
# ==========================================================

st.markdown("---")

if backend_available:

    st.success(
        "🟢 Backend is connected. "
        "The application is ready to use."
    )

else:

    st.warning(
        "🟡 Frontend is running, but the backend "
        "has not connected yet."
    )


# ==========================================================
# Footer Message
# ==========================================================

st.markdown("---")

st.success(
    "Use the pages in the left sidebar to navigate "
    "through the application."
)
