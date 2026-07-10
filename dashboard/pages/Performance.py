"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
AI Performance Dashboard

Monitor model health, engine status and deployment.

Author  : Gurrala Nikhil Reddy
Version : 1.0.0
===========================================================
"""

from __future__ import annotations

# ==========================================================
# Standard Library
# ==========================================================

import logging
import sys
from pathlib import Path

# ==========================================================
# Third Party
# ==========================================================

import streamlit as st

# ==========================================================
# Project Root
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# ==========================================================
# Components
# ==========================================================

from components.sidebar import render_sidebar
from components.header import render_header
from components.footer import render_footer

from components.metric_cards import metric_grid

from components.model_health import (
    render_model_health,
)

# ==========================================================
# Backend
# ==========================================================

from utils.predict import get_engine
from utils.risk_engine import get_risk_engine

# ==========================================================
# Logger
# ==========================================================

logger = logging.getLogger(__name__)

if not logger.handlers:

    logging.basicConfig(

        level=logging.INFO,

        format="%(levelname)s | %(message)s",

    )

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(

    page_title="Performance",

    page_icon="📈",

    layout="wide",

    initial_sidebar_state="expanded",

)

from utils.helpers import load_css

load_css()

# ==========================================================
# Backend
# ==========================================================

prediction_engine = get_engine()

risk_engine = get_risk_engine()
# ==========================================================
# KPI Builder
# ==========================================================

def build_metrics():

    engine = risk_engine.status()

    model = prediction_engine.model_summary()

    return [

        {

            "title": "Prediction Engine",

            "value": engine.get(

                "Status",

                "Unknown",

            ),

            "icon": "🤖",

            "color": "success",

            "delta": "Online",

        },

        {

            "title": "Risk Engine",

            "value": "Ready",

            "icon": "🛡️",

            "color": "primary",

            "delta": engine.get(

                "Version",

                "-",

            ),

        },

        {

            "title": "Models",

            "value": "3",

            "icon": "🧠",

            "color": "warning",

            "delta": "Loaded",

        },

        {

            "title": "Deployment",

            "value": "Production",

            "icon": "🚀",

            "color": "danger",

            "delta": "Healthy",

        },

    ]


# ==========================================================
# KPI Section
# ==========================================================

def render_kpis():

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/></svg>
            <span class="header-title-text" style="font-size: 24px;">AI Performance Overview</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    metric_grid(

        build_metrics()

    )

    st.divider()
# ==========================================================
# Model Information
# ==========================================================

def render_models():

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="M12 6v6l4 2"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Model Information</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    model_summary = (

        prediction_engine.model_summary()

    )

    render_model_health(

        model_summary

    )

    st.divider()
# ==========================================================
# Runtime Status
# ==========================================================

def render_runtime_status() -> None:
    """
    Display runtime information.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Runtime Status</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    status = risk_engine.status()

    left, right = st.columns(2)

    with left:

        st.info(
            f"""
### Prediction Services

Engine : **{status.get('Engine','Unknown')}**

Version : **{status.get('Version','-')}**

Status : **{status.get('Status','Unknown')}**
"""
        )

    with right:

        st.success(
            """
### Deployment

Inference : **Real-Time**

Backend : **Healthy**

Models : **Loaded**

Deployment : **Production Ready**
"""
        )

    st.divider()


# ==========================================================
# AI Assessment
# ==========================================================

def render_assessment() -> None:
    """
    AI deployment assessment.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            <span class="header-title-text" style="font-size: 24px;">AI Deployment Assessment</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.success(
        """
### Enterprise Readiness

★★★★★ **System Ready**

✔ Prediction Engine initialized

✔ Risk Engine operational

✔ Models loaded successfully

✔ Suitable for real-time fraud detection

✔ Ready for dashboard inference
"""
    )

    st.info(
        """
### Recommendations

• Monitor prediction confidence regularly.

• Retrain models periodically with fresh transaction data.

• Review high-risk alerts through the Fraud Alert Center.

• Export reports for compliance and auditing.
"""
    )

    st.divider()


# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """
    Performance page entry point.
    """

    render_sidebar()

    render_header()

    try:

        render_kpis()

        render_models()

        render_runtime_status()

        render_assessment()

        render_footer()

    except Exception as error:

        logger.exception(error)

        st.error(
            f"""
Performance page failed to load.

Error:

{error}
"""
        )

        st.stop()


# ==========================================================
# Application
# ==========================================================

if __name__ == "__main__":

    main()