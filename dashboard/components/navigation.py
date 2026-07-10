"""
===========================================================
Enterprise Navigation Component
-----------------------------------------------------------
Reusable navigation helpers for the Fraud Intelligence
Dashboard.

Author  : Gurrala Nikhil Reddy
Version : 1.0.0
===========================================================
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from utils.config import (
    PROJECT_NAME,
    VERSION,
)

# ==========================================================
# PAGE HEADER
# ==========================================================


def page_header(
    title: str,
    subtitle: str = "",
    icon: str = "📊"
):
    """
    Standard page header used by every page.
    """

    col1, col2 = st.columns([8, 2])

    with col1:

        st.markdown(
            f"""
<div class="page-header fade-in">

<h1>{icon} {title}</h1>

<p>{subtitle}</p>

</div>
""",
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
<div class="glass-card text-center">

<b>{datetime.now().strftime("%d %b %Y")}</b>

<br>

<small>
{datetime.now().strftime("%I:%M %p")}
</small>

</div>
""",
            unsafe_allow_html=True,
        )


# ==========================================================
# BREADCRUMB
# ==========================================================


def breadcrumb(items: list[str]):
    """
    Render breadcrumb navigation.

    Example
    -------

    Home > Analytics
    """

    path = "  >  ".join(items)

    st.caption(path)

    st.divider()


# ==========================================================
# SYSTEM STATUS
# ==========================================================


def system_banner():

    col1, col2, col3 = st.columns(3)

    with col1:

        st.success("🟢 Dashboard Online")

    with col2:

        st.info("🤖 Models Ready")

    with col3:

        st.warning("⏱ Last Sync : Just Now")


# ==========================================================
# PAGE ACTIONS
# ==========================================================


def page_actions():

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.button(
            "🔄 Refresh",
            use_container_width=True
        )

    with col2:

        st.button(
            "📥 Export",
            use_container_width=True
        )

    with col3:

        st.button(
            "⚙ Settings",
            use_container_width=True
        )

    with col4:

        st.button(
            "❓ Help",
            use_container_width=True
        )


# ==========================================================
# SECTION TITLE
# ==========================================================


def section(title: str):

    st.markdown(
        f"## {title}"
    )

    st.markdown("---")


# ==========================================================
# PAGE FOOTER
# ==========================================================


def page_footer():

    st.markdown("---")

    st.caption(

        f"{PROJECT_NAME} | Enterprise Edition | Version {VERSION}"

    )


# ==========================================================
# COMPLETE PAGE
# ==========================================================


def render_page(
    title: str,
    subtitle: str,
    icon: str,
    breadcrumb_items: list[str],
):
    """
    Render complete page structure.

    This function should be called
    at the beginning of every page.
    """

    page_header(
        title,
        subtitle,
        icon,
    )

    breadcrumb(breadcrumb_items)

    system_banner()

    st.write("")