# ==========================================================
# AI RESUME SCREENING AGENT
# Main Streamlit Application
# ==========================================================

import os
import time
from pathlib import Path

import requests
import streamlit as st


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="AI Resume Screening Agent",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# Project Paths
# ==========================================================

FRONTEND_DIR = Path(
    __file__
).resolve().parent

ASSETS_DIR = (
    FRONTEND_DIR
    / "assets"
)

CSS_PATH = (
    ASSETS_DIR
    / "style.css"
)

LOGO_PATH = (
    ASSETS_DIR
    / "logo.png"
)


# ==========================================================
# Backend Configuration
# ==========================================================

BACKEND_URL = (
    "https://ai-resume-screening-agent-cxgp.onrender.com"
)


# ==========================================================
# Backend Health Check
# ==========================================================

def health_check():
    """
    Check whether the deployed FastAPI backend is available.

    First tries /health.
    If /health is not available, falls back to the root URL.
    """

    # ------------------------------------------------------
    # Try /health endpoint
    # ------------------------------------------------------

    try:

        response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=15,
        )

        if response.status_code == 200:

            return True

    except requests.exceptions.Timeout:

        pass

    except requests.exceptions.ConnectionError:

        pass

    except requests.exceptions.RequestException:

        pass

    except Exception:

        pass


    # ------------------------------------------------------
    # Try root endpoint
    # ------------------------------------------------------

    try:

        response = requests.get(
            BACKEND_URL,
            timeout=15,
        )

        if response.status_code == 200:

            return True

    except requests.exceptions.Timeout:

        pass

    except requests.exceptions.ConnectionError:

        pass

    except requests.exceptions.RequestException:

        pass

    except Exception:

        pass


    return False


# ==========================================================
# Backend Connection
# ==========================================================

def check_backend_connection():
    """
    Automatically connect to the Render backend.

    Render may put the backend to sleep after inactivity.
    Several attempts are made to give the backend enough
    time to wake up.
    """

    # ------------------------------------------------------
    # Already connected
    # ------------------------------------------------------

    if st.session_state.get(
        "backend_available",
        False,
    ):

        return True


    # ------------------------------------------------------
    # Already checked
    # ------------------------------------------------------

    if st.session_state.get(
        "backend_checked",
        False,
    ):

        return False


    # ------------------------------------------------------
    # Reset state
    # ------------------------------------------------------

    st.session_state[
        "backend_available"
    ] = False

    st.session_state[
        "backend_attempts"
    ] = 0


    # ------------------------------------------------------
    # Automatic attempts
    # ------------------------------------------------------

    max_attempts = 4

    for attempt in range(
        1,
        max_attempts + 1,
    ):

        st.session_state[
            "backend_attempts"
        ] = attempt


        if health_check():

            st.session_state[
                "backend_available"
            ] = True

            st.session_state[
                "backend_checked"
            ] = True

            return True


        # --------------------------------------------------
        # Give Render time to wake up
        # --------------------------------------------------

        if attempt < max_attempts:

            time.sleep(
                attempt * 2
            )


    # ------------------------------------------------------
    # Backend unavailable
    # ------------------------------------------------------

    st.session_state[
        "backend_available"
    ] = False

    st.session_state[
        "backend_checked"
    ] = True

    return False


# ==========================================================
# Session State
# ==========================================================

if "backend_available" not in st.session_state:

    st.session_state[
        "backend_available"
    ] = False


if "backend_checked" not in st.session_state:

    st.session_state[
        "backend_checked"
    ] = False


if "backend_attempts" not in st.session_state:

    st.session_state[
        "backend_attempts"
    ] = 0


# ==========================================================
# Load Custom CSS
# ==========================================================

if CSS_PATH.exists():

    try:

        with open(
            CSS_PATH,
            encoding="utf-8",
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )

    except Exception:

        pass


# ==========================================================
# Backend Startup Connection
# ==========================================================

if not st.session_state.get(
    "backend_checked",
    False,
):

    with st.spinner(
        "🔄 Connecting to backend... "
        "It may take a minute while Render wakes up."
    ):

        backend_available = (
            check_backend_connection()
        )

else:

    backend_available = (
        st.session_state.get(
            "backend_available",
            False,
        )
    )


# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    # ------------------------------------------------------
    # Project Logo
    # ------------------------------------------------------

    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            width=100,
        )

    else:

        st.image(
            "https://img.icons8.com/color/96/resume.png",
            width=80,
        )


    # ------------------------------------------------------
    # Project Title
    # ------------------------------------------------------

    st.markdown(
        """
        <div style="
            font-size:22px;
            font-weight:700;
            line-height:1.25;
            margin-top:12px;
            margin-bottom:16px;
        ">
            AI Resume Screening Agent
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.divider()


    # ======================================================
    # BACKEND STATUS
    # ======================================================

    if backend_available:

        st.success(
            "🟢 Backend Connected"
        )

    else:

        st.error(
            "🔴 Backend Unavailable"
        )


    # ------------------------------------------------------
    # Backend URL
    # ------------------------------------------------------

    st.caption(
        f"Backend: {BACKEND_URL}"
    )


    # ------------------------------------------------------
    # Retry Backend
    # ------------------------------------------------------

    if not backend_available:

        if st.button(
            "🔄 Retry Backend",
            use_container_width=True,
            key="retry_backend",
        ):

            st.session_state[
                "backend_checked"
            ] = False

            st.session_state[
                "backend_available"
            ] = False

            st.session_state[
                "backend_attempts"
            ] = 0

            st.rerun()


    st.divider()


    # ======================================================
    # Project Information
    # ======================================================

    st.markdown(
        """
        <div style="
            font-size:18px;
            font-weight:700;
            margin-bottom:10px;
        ">
            Project
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.caption(
        "Version: 1.0"
    )

    st.caption(
        "Model: Decision Tree"
    )

    st.caption(
        "Framework: Streamlit"
    )


# ==========================================================
# Main Backend Status
# ==========================================================

if backend_available:

    st.success(
        "🟢 Backend is connected. "
        "The AI Resume Screening Agent is ready to use."
    )

else:

    st.warning(
        """
        ⚠️ **The FastAPI backend is currently unavailable.**

        The frontend is running, but backend-dependent
        features may not work yet.

        Render may still be waking the backend.

        Please use **🔄 Retry Backend** in the sidebar
        after a short wait.
        """
    )


# ==========================================================
# Main Home Screen
# ==========================================================

st.title(
    "📄 AI Resume Screening Agent"
)


# ==========================================================
# Welcome / AI Image
# ==========================================================

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
This application uses **Machine Learning** and
**Artificial Intelligence** to automate resume screening
and assist recruiters in selecting the most suitable
candidates.
"""
    )

    st.subheader(
        "Features"
    )

    st.markdown(
        """
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
        width=280,
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

st.subheader(
    "Project Technologies"
)

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "ML Model",
        "Decision Tree",
    )


with c2:

    st.metric(
        "Backend",
        "FastAPI",
    )


with c3:

    st.metric(
        "Frontend",
        "Streamlit",
    )


with c4:

    st.metric(
        "Dataset",
        "11,000 Records",
    )


# ==========================================================
# Application Status
# ==========================================================

st.markdown("---")

st.subheader(
    "💻 Application Status"
)

status_col1, status_col2 = st.columns(2)


with status_col1:

    if backend_available:

        st.success(
            "🟢 Backend Connected"
        )

    else:

        st.error(
            "🔴 Backend Unavailable"
        )


with status_col2:

    st.info(
        f"Backend: {BACKEND_URL}"
    )


# ==========================================================
# Backend Connection Information
# ==========================================================

st.markdown("---")

st.subheader(
    "🔗 Backend Connection"
)

st.code(
    BACKEND_URL
)


if backend_available:

    st.success(
        "✅ FastAPI backend is online and responding."
    )

else:

    st.warning(
        "⚠️ FastAPI backend is not responding yet."
    )


# ==========================================================
# Navigation Information
# ==========================================================

st.markdown("---")

st.info(
    """
👈 Use the pages in the left sidebar to navigate
through the application.

Available sections include:

• Resume Screening

• Candidate Portal

• Recruiter Dashboard

• AI Resume Assistant

• Reports

• Analytics

• Admin Dashboard
"""
)


# ==========================================================
# Footer
# ==========================================================

st.markdown("---")

st.success(
    "Use the pages in the left sidebar to navigate "
    "through the application."
)


st.caption(
    "© 2026 AI Resume Screening Agent | "
    "Built with Python, Streamlit, FastAPI and Machine Learning"
)
