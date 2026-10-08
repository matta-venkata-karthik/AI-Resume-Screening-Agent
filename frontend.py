# ==========================================================
# AI Resume Screening Agent
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
    Check the deployed FastAPI backend.

    The backend root endpoint is used because the original
    application uses the root URL for its health check.
    """

    try:

        response = requests.get(
            BACKEND_URL,
            timeout=15,
        )

        response.raise_for_status()

        return True

    except requests.exceptions.Timeout:

        return False

    except requests.exceptions.ConnectionError:

        return False

    except requests.exceptions.RequestException:

        return False

    except Exception:

        return False


# ==========================================================
# Backend Connection
# ==========================================================

def check_backend_connection():
    """
    Automatically connect to the Render backend.

    Render may put the backend to sleep after inactivity.
    Multiple attempts are therefore made automatically to
    allow the backend time to wake up.
    """

    # ------------------------------------------------------
    # Already connected during this Streamlit session
    # ------------------------------------------------------

    if st.session_state.get(
        "backend_available",
        False,
    ):

        return True


    # ------------------------------------------------------
    # Already checked and failed
    # ------------------------------------------------------

    if st.session_state.get(
        "backend_checked",
        False,
    ):

        return False


    # ------------------------------------------------------
    # Initial state
    # ------------------------------------------------------

    st.session_state[
        "backend_checked"
    ] = False

    st.session_state[
        "backend_available"
    ] = False

    st.session_state[
        "backend_attempts"
    ] = 0


    # ------------------------------------------------------
    # Automatic connection attempts
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
        # Give Render time to wake the backend
        # --------------------------------------------------

        if attempt < max_attempts:

            time.sleep(
                attempt * 2
            )


    # ------------------------------------------------------
    # Backend could not be reached
    # ------------------------------------------------------

    st.session_state[
        "backend_available"
    ] = False

    st.session_state[
        "backend_checked"
    ] = True

    return False


# ==========================================================
# Load Custom CSS
# ==========================================================

css_path = Path(
    "assets/style.css"
)

if css_path.exists():

    try:

        with open(
            css_path,
            encoding="utf-8",
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )

    except Exception:

        pass


# ==========================================================
# Session State Initialization
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
# Start Backend Connection
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
    # Logo
    # ------------------------------------------------------

    st.image(
        "https://img.icons8.com/color/96/resume.png",
        width=80,
    )


    # ------------------------------------------------------
    # Application Title
    # ------------------------------------------------------

    st.title(
        "AI Resume Screening Agent"
    )


    st.markdown(
        """
        <div style="
            font-size:13px;
            opacity:0.7;
            margin-bottom:10px;
        ">
            AI-powered resume screening and recruitment
            assistance platform
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.divider()


    # ------------------------------------------------------
    # Backend Status
    # ------------------------------------------------------

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
    # Retry Button
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


    # ------------------------------------------------------
    # Version
    # ------------------------------------------------------

    st.markdown("---")

    st.write(
        "Version 1.0"
    )


# ==========================================================
# Backend Warning
# ==========================================================

if not backend_available:

    st.warning(
        """
⚠️ **The FastAPI backend is currently unavailable.**

The frontend is running, but features that require the
backend may not work until the backend becomes available.

Please wait a few seconds and use **🔄 Retry Backend**
from the sidebar.
"""
    )


# ==========================================================
# Main Home Screen
# ==========================================================

st.title(
    "📄 AI Resume Screening Agent"
)


# ==========================================================
# Main Backend Status
# ==========================================================

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
# Connection Information
# ==========================================================

if backend_available:

    st.success(
        """
        ✅ The AI Resume Screening Agent is connected to
        the FastAPI backend and ready for use.
        """
    )

else:

    st.warning(
        """
        ⏳ The frontend is available, but the FastAPI
        backend could not be reached.

        Render may still be waking the backend.
        Use **Retry Backend** in the sidebar.
        """
    )


# ==========================================================
# Navigation Information
# ==========================================================

st.markdown("---")

st.info(
    """
👈 Use the pages in the left sidebar to navigate
through the application.

Available sections may include:

• Resume Screening

• Candidate Portal

• Recruiter Dashboard

• AI Resume Assistant

• Resume Match Score

• Skill Gap Analysis

• Interview Questions

• Hiring Reports

• Analytics Dashboard

• Admin Dashboard
"""
)


# ==========================================================
# Footer Message
# ==========================================================

st.markdown("---")

st.success(
    "Use the pages in the left sidebar to navigate "
    "through the application."
)


# ==========================================================
# Footer
# ==========================================================

st.markdown("---")

st.caption(
    "© 2026 AI Resume Screening Agent | "
    "Built with Python, Streamlit, FastAPI and Machine Learning"
)
