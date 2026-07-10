"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
About

Project overview, architecture and technology stack.

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

    page_title="About",

    page_icon="ℹ️",

    layout="wide",

    initial_sidebar_state="expanded",

)

from utils.helpers import load_css

load_css()


# ==========================================================
# Project Overview
# ==========================================================

def render_project_overview():

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            <span class="header-title-text" style="font-size: 24px;">AI Fraud Intelligence Center</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        """
The **AI Fraud Intelligence Center** is an enterprise-style fraud
detection dashboard designed to identify suspicious financial
transactions using Artificial Intelligence and Machine Learning.

The application combines an **Isolation Forest** and an
**AutoEncoder** with a business-oriented **Risk Engine** to
provide real-time fraud detection, risk analysis and reporting.

The system is designed with a modular architecture to ensure
scalability, maintainability and ease of deployment.
"""
    )

    st.divider()


# ==========================================================
# Features
# ==========================================================

def render_features():

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Features</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.success("""
✔ Real-Time Fraud Detection

✔ AI Risk Analysis

✔ Interactive Analytics

✔ Fraud Alert Center

✔ Live Transaction Prediction

✔ Business Reports
""")

    with col2:

        st.info("""
✔ Enterprise Dashboard

✔ Interactive Charts

✔ CSV Export

✔ Modular Architecture

✔ Responsive UI

✔ Professional Reporting
""")

    st.divider()


# ==========================================================
# Technology Stack
# ==========================================================

def render_stack():

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><rect width="16" height="14" x="4" y="4" rx="2" ry="2"/><line x1="12" x2="12" y1="20" y2="14"/><line x1="8" x2="16" y1="20" y2="20"/><line x1="8" x2="8" y1="8" y2="8"/><line x1="12" x2="12" y1="8" y2="8"/><line x1="16" x2="16" y1="8" y2="8"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Technology Stack</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.table({

        "Layer": [

            "Frontend",

            "Backend",

            "Machine Learning",

            "Visualization",

            "Framework",

        ],

        "Technology": [

            "Streamlit",

            "Python",

            "Ensemble: Isolation Forest + AutoEncoder + HistGradientBoosting",

            "Plotly",

            "Pandas / NumPy",

        ],

    })

    st.divider()


# ==========================================================
# Architecture
# ==========================================================

def render_architecture():

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><line x1="9" x2="15" y1="3" y2="3"/><line x1="9" x2="15" y1="21" y2="21"/><line x1="3" x2="3" y1="9" y2="15"/><line x1="21" x2="21" y1="9" y2="15"/><line x1="9" x2="9" y1="9" y2="15"/><line x1="15" x2="15" y1="9" y2="15"/><line x1="9" x2="15" y1="9" y2="9"/><line x1="9" x2="15" y1="15" y2="15"/></svg>
            <span class="header-title-text" style="font-size: 24px;">System Architecture</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.code("""

User

   │

   ▼

Dashboard

   │

   ▼

Prediction Engine

   │

   ▼

Risk Engine

   │

   ▼

Analytics & Reports

""")

    st.divider()


# ==========================================================
# Authors
# ==========================================================

def render_authors():

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Developer</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("""

**Project**

AI Fraud Intelligence Center

**Developer**

Gurrala Nikhil Reddy

**Department**

Computer Science and Engineering (Data Science)

**Technology**

Artificial Intelligence

Machine Learning

Data Analytics

Python

""")

    st.divider()


# ==========================================================
# Future Scope
# ==========================================================

def render_future():

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/><path d="M2 12h20"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Future Scope & Enhancements</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("""

• Bank API Integration

• Real-Time Streaming

• Email Alert System

• PDF Report Generation

• Cloud Deployment

• Explainable AI (XAI)

• Multi-user Authentication

• Continuous Model Retraining

""")

    st.divider()


# ==========================================================
# Main
# ==========================================================

def main():

    render_sidebar()

    render_header()

    render_project_overview()

    render_features()

    render_stack()

    render_architecture()

    render_authors()

    render_future()

    render_footer()


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    main()