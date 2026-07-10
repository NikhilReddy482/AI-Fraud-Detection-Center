"""
===========================================================
Enterprise Sidebar Component
-----------------------------------------------------------
Reusable sidebar used across all dashboard pages.

Author  : Gurrala Nikhil Reddy
Version : 1.0.0
===========================================================
"""

from __future__ import annotations

from pathlib import Path
import base64

import streamlit as st

from utils.config import (
    ASSETS_DIR,
    SHORT_NAME,
    VERSION,
    SIDEBAR_MENU,
)
from utils.helpers import load_css


# ==========================================================
# Logo Loader
# ==========================================================

def _load_logo() -> str | None:
    """
    Return the logo encoded as Base64.

    Returns
    -------
    str | None
        Base64 string if logo exists.
    """

    logo = ASSETS_DIR / "logo.png"

    if not logo.exists():
        return None

    with open(logo, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    return encoded


# ==========================================================
# Sidebar Header
# ==========================================================


def sidebar_header() -> None:
    """
    Render dashboard logo and title.
    """

    logo = _load_logo()

    if logo:

        st.sidebar.markdown(
            f"""
<div class="sidebar-logo">

<img src="data:image/png;base64,{logo}">

</div>
""",
            unsafe_allow_html=True,
        )

    else:

        st.sidebar.markdown(
            """
<div class="sidebar-logo">

<div style="
width:80px;
height:80px;
border-radius:50%;
background:linear-gradient(135deg, var(--primary), var(--accent));
display:flex;
justify-content:center;
align-items:center;
box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
">

<svg style="width: 40px; height: 40px; stroke: white; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;" viewBox="0 0 24 24">
  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
</svg>

</div>

</div>
""",
            unsafe_allow_html=True,
        )

    st.sidebar.markdown(
        f"""
<div class="sidebar-title">

{SHORT_NAME}

</div>

<div class="sidebar-subtitle">

Enterprise Banking Risk Platform

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Sidebar Status
# ==========================================================


def sidebar_status() -> None:
    """
    Display system status.
    """

    st.sidebar.markdown("---")

    st.sidebar.success("🟢 System Online")

    st.sidebar.caption("Models Loaded")

    st.sidebar.caption("Database Connected")

    st.sidebar.caption("Dashboard Ready")


# ==========================================================
# Theme Switch
# ==========================================================


def theme_toggle() -> None:
    """
    Theme switch.
    """

    st.sidebar.markdown("---")

    if "dark_theme" not in st.session_state:
        st.session_state.dark_theme = True

    val = st.sidebar.toggle(
        "Dark Theme",
        value=st.session_state.dark_theme,
        key="theme_toggle_widget",
    )

    if val != st.session_state.dark_theme:
        st.session_state.dark_theme = val
        st.rerun()


# ==========================================================
# Footer
# ==========================================================


def sidebar_footer() -> None:
    """
    Footer information.
    """

    st.sidebar.markdown("---")

    st.sidebar.caption(
        f"Version {VERSION}"
    )

    st.sidebar.caption(
        "AI Fraud Intelligence Center"
    )


# ==========================================================
# Navigation
# ==========================================================


def sidebar_navigation() -> None:
    """
    Render navigation menu.
    """

    st.sidebar.page_link(
        "app.py",
        label="Dashboard",
        icon=":material/dashboard:",
    )

    st.sidebar.page_link(
        "pages/Analytics.py",
        label="Analytics",
        icon=":material/query_stats:",
    )

    st.sidebar.page_link(
        "pages/Live_Prediction.py",
        label="Live Prediction",
        icon=":material/smart_toy:",
    )

    st.sidebar.page_link(
        "pages/Fraud_Alerts.py",
        label="Fraud Alerts",
        icon=":material/notifications_active:",
    )

    st.sidebar.page_link(
        "pages/Reports.py",
        label="Reports",
        icon=":material/assessment:",
    )

    st.sidebar.page_link(
        "pages/Performance.py",
        label="Performance",
        icon=":material/trending_up:",
    )

    st.sidebar.page_link(
        "pages/About.py",
        label="About",
        icon=":material/info:",
    )


# ==========================================================
# Render Sidebar
# ==========================================================


def render_sidebar() -> None:
    """
    Render complete sidebar.
    """

    load_css()

    sidebar_header()

    sidebar_navigation()

    theme_toggle()

    sidebar_status()

    sidebar_footer()