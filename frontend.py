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

# ==========================================================
# Backend Connection
# ==========================================================

def check_backend_connection():
    """
    Check and wake the FastAPI backend.

    The frontend automatically calls the backend health
    endpoint when the Streamlit session starts.

    The function makes several attempts because Render may
    need some time to wake a sleeping service.
    """

    # Do not repeatedly wake the backend on every Streamlit
    # rerun during the same browser session.
    if st.session_state.get(
        "backend_checked",
        False,
    ):

        return st.session_state.get(
            "backend_available",
            False,
        )

    st.session_state[
        "backend_checked"
    ] = True

    st.session_state[
        "backend_available"
    ] = False

    max_attempts = 4

    for attempt in range(
        1,
        max_attempts + 1,
    ):

        try:

            result = health_check()

            # Support either:
            # True
            # {"status": "healthy"}
            # {"status": "ok"}
            if result is True:

                st.session_state[
                    "backend_available"
                ] = True

                return True

            if isinstance(
                result,
                dict,
            ):

                status = str(
                    result.get(
                        "status",
                        "",
                    )
                ).lower()

                if status in {
                    "healthy",
                    "ok",
                    "online",
                    "running",
                    "success",
                }:

                    st.session_state[
                        "backend_available"
                    ] = True

                    return True

        except Exception:
            pass

        # Give Render time to wake up before trying again.
        if attempt < max_attempts:

            time.sleep(
                attempt * 2
            )

    return False


# ==========================================================
# Start Backend Connection
# ==========================================================

with st.spinner(
    "🔄 Connecting to backend...
    It May Take a Minute"
):

    backend_available = (
        check_backend_connection()
    )

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
