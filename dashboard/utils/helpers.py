"""
===========================================================
Helper Utilities
-----------------------------------------------------------
Reusable helper functions used across the dashboard.

Author  : Gurrala Nikhil Reddy
Version : 1.0.0
===========================================================
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import base64

import pandas as pd
import streamlit as st

from utils.config import (
    ASSETS_DIR,
    PROJECT_NAME,
    SHORT_NAME,
    VERSION,
)

# ==========================================================
# Page Configuration
# ==========================================================


def configure_page(title: str, icon: str = "🛡️") -> None:
    """
    Configure a Streamlit page.
    """

    st.set_page_config(
        page_title=f"{title} | {SHORT_NAME}",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )


# ==========================================================
# CSS Loader
# ==========================================================


def load_css() -> None:
    """
    Load custom CSS.
    """

    css_file = ASSETS_DIR / "styles.css"

    if css_file.exists():

        with open(css_file, encoding="utf-8") as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )

    # Initialize theme state if not exists
    if "dark_theme" not in st.session_state:
        st.session_state.dark_theme = True

    # If light theme, inject overrides
    if not st.session_state.dark_theme:
        st.markdown(
            """
            <style>
            :root {
                --bg: #F8FAFC !important;
                --surface: #FFFFFF !important;
                --surface-light: #F1F5F9 !important;
                --border: rgba(0, 0, 0, 0.08) !important;
                --primary: #4F46E5 !important;
                --primary-light: #6366F1 !important;
                --success: #10B981 !important;
                --warning: #D97706 !important;
                --danger: #DC2626 !important;
                --accent: #0891B2 !important;
                --accent-light: #06B6D4 !important;
                --text: #0F172A !important;
                --text-secondary: #475569 !important;
                --shadow: 0 4px 20px rgba(0, 0, 0, 0.06), 0 0 10px rgba(99, 102, 241, 0.03) !important;
            }
            .stApp {
                background: linear-gradient(135deg, #F8FAFC, #F1F5F9, #F8FAFC) !important;
            }
            /* Sidebar Light Mode Overrides */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #F1F5F9, #E2E8F0) !important;
                border-right: 1px solid rgba(0, 0, 0, 0.08) !important;
            }
            [data-testid="stSidebar"] * {
                color: #0F172A !important;
            }
            [data-testid="stSidebar"] [data-testid="stSidebarLink"],
            [data-testid="stSidebar"] .evng2kd1 {
                background-color: rgba(0, 0, 0, 0.02) !important;
                border: 1px solid rgba(0, 0, 0, 0.06) !important;
                color: #0F172A !important;
            }
            [data-testid="stSidebar"] [data-testid="stSidebarLink"]:hover,
            [data-testid="stSidebar"] .evng2kd1:hover {
                background-color: rgba(6, 182, 212, 0.08) !important;
                border-color: rgba(6, 182, 212, 0.2) !important;
                color: #0891B2 !important;
            }
            [data-testid="stSidebar"] [data-testid="stSidebarLink"]:not([href]),
            [data-testid="stSidebar"] .evng2kd1:not([href]) {
                background: linear-gradient(135deg, var(--primary), var(--accent)) !important;
                border-color: var(--accent) !important;
                color: white !important;
            }
            
            /* Text inputs, selects, textareas in Light Mode */
            div[data-baseweb="select"] > div,
            input[type="text"],
            input[type="number"],
            textarea {
                background-color: #FFFFFF !important;
                color: #0F172A !important;
                border-color: rgba(0, 0, 0, 0.15) !important;
            }
            
            /* KPI Card Adjustments */
            div.metric-card-container {
                background-color: #FFFFFF !important;
                border-color: rgba(0, 0, 0, 0.08) !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
            }
            div.metric-card-title {
                color: #475569 !important;
            }
            div.metric-card-value {
                color: #0F172A !important;
            }
            
            /* General text contrast adjustments */
            h1, h2, h3, h4, h5, h6, span, label, p {
                color: #0F172A !important;
            }
            .header-title-text {
                background: linear-gradient(135deg, #0F172A 40%, #0891B2 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
            }
            /* Toast message color rules */
            div[role="status"] {
                background-color: #FFFFFF !important;
                color: #0F172A !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


# ==========================================================
# Logo Loader
# ==========================================================


def load_logo() -> str | None:
    """
    Return base64 encoded logo.
    """

    logo = ASSETS_DIR / "logo.png"

    if not logo.exists():
        return None

    with open(logo, "rb") as image:

        encoded = base64.b64encode(image.read()).decode()

    return encoded


# ==========================================================
# Header
# ==========================================================


def page_header(
    title: str,
    subtitle: str = "",
) -> None:
    """
    Dashboard page header.
    """

    st.markdown(
        f"""
<div class="page-header">

<h1>{title}</h1>

<p>{subtitle}</p>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Footer
# ==========================================================


def footer() -> None:
    """
    Global footer.
    """

    st.markdown("---")

    st.caption(
        f"{PROJECT_NAME} • Version {VERSION}"
    )


# ==========================================================
# Status Badge
# ==========================================================


def status_badge(
    text: str,
    color: str = "#16A34A",
):
    """
    Display a colored badge.
    """

    st.markdown(
        f"""
<span
style="
background:{color};
padding:6px 14px;
border-radius:20px;
color:white;
font-weight:600;
font-size:13px;
">

{text}

</span>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Number Formatting
# ==========================================================


def format_number(value: float) -> str:
    """
    Format large numbers.
    """

    if value >= 1_000_000:

        return f"{value/1_000_000:.2f} M"

    if value >= 1_000:

        return f"{value/1_000:.2f} K"

    return f"{value:.0f}"


# ==========================================================
# Currency Formatting
# ==========================================================


def format_currency(amount: float) -> str:
    """
    Format currency.
    """

    return f"₹ {amount:,.2f}"


# ==========================================================
# Percentage Formatting
# ==========================================================


def format_percent(value: float) -> str:
    """
    Format percentages.
    """

    return f"{value:.2f}%"


# ==========================================================
# Current Date
# ==========================================================


def current_date() -> str:
    """
    Today's date.
    """

    return datetime.now().strftime("%d %B %Y")


# ==========================================================
# Current Time
# ==========================================================


def current_time() -> str:
    """
    Current time.
    """

    return datetime.now().strftime("%I:%M:%S %p")


# ==========================================================
# Timestamp
# ==========================================================


def timestamp() -> str:
    """
    Current timestamp.
    """

    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


# ==========================================================
# Empty Chart
# ==========================================================


def empty_chart(message: str):

    st.info(message)


# ==========================================================
# Empty Table
# ==========================================================


def empty_table():

    df = pd.DataFrame()

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )


# ==========================================================
# Divider
# ==========================================================


def section(title: str):

    st.markdown(f"## {title}")

    st.divider()


# ==========================================================
# Spacer
# ==========================================================


def space(lines: int = 1):

    for _ in range(lines):

        st.write("")


# ==========================================================
# System Status
# ==========================================================


def system_status():

    col1, col2 = st.columns([8, 2])

    with col2:

        status_badge(
            "🟢 ONLINE",
            "#16A34A",
        )


# ==========================================================
# File Checker
# ==========================================================


def file_exists(path: Path) -> bool:
    """
    Check file existence.
    """

    return path.exists()