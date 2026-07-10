"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
Enterprise Header Component

Reusable header for all dashboard pages.

Author  : Gurrala Nikhil Reddy
Version : 1.0.0
===========================================================
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import streamlit as st

# ==========================================================
# Assets
# ==========================================================

ASSETS_DIR = (
    Path(__file__).resolve().parents[1]
    / "assets"
)

LOGO_PATH = ASSETS_DIR / "logo.png"

# ==========================================================
# Render Header
# ==========================================================


def render_header(
    title: str = "AI Fraud Intelligence Center",
    subtitle: str = "Enterprise Fraud Detection Dashboard",
    show_logo: bool = True,
    show_clock: bool = True,
    show_status: bool = True,
) -> None:
    """
    Render enterprise dashboard header.

    Parameters
    ----------
    title : str
        Main dashboard title.

    subtitle : str
        Dashboard subtitle.

    show_logo : bool
        Display logo.

    show_clock : bool
        Display current time.

    show_status : bool
        Display system status.
    """

    left, center, right = st.columns(
        [1.2, 6, 2]
    )

    # ======================================================
    # Logo
    # ======================================================

    with left:

        if show_logo and LOGO_PATH.exists():

            st.image(
                str(LOGO_PATH),
                width=80,
            )

    # ======================================================
    # Title
    # ======================================================

    with center:

        st.markdown(
            f"""
<div style="padding-top:10px;">

<h1 style="
margin-bottom:0;
font-size:34px;
font-weight:700;">

{title}

</h1>

<p style="
font-size:16px;
color:#94A3B8;
margin-top:6px;">

{subtitle}

</p>

</div>
""",
            unsafe_allow_html=True,
        )

    # ======================================================
    # Status
    # ======================================================

    with right:

        if show_status:

            st.success("🟢 System Online")

        if show_clock:

            st.caption(
                datetime.now().strftime(
                    "%d %b %Y"
                )
            )

            st.caption(
                datetime.now().strftime(
                    "%I:%M:%S %p"
                )
            )

    st.divider()


# ==========================================================
# Compact Header
# ==========================================================


def render_compact_header(
    title: str,
) -> None:
    """
    Compact page header.
    """

    st.markdown(
        f"""
## {title}
""",
    )

    st.caption(
        datetime.now().strftime(
            "%d %b %Y • %I:%M %p"
        )
    )

    st.divider()


# ==========================================================
# Banner
# ==========================================================


def render_banner(
    text: str,
    icon: str = "ℹ️",
) -> None:
    """
    Display dashboard banner.
    """

    st.info(f"{icon} {text}")


# ==========================================================
# Page Title
# ==========================================================


def render_page_title(
    title: str,
    description: str,
) -> None:
    """
    Page title section.
    """

    st.markdown(
        f"""
### {title}

{description}
"""
    )


# ==========================================================
# Status Badge
# ==========================================================


def status_badge(
    online: bool = True,
) -> None:
    """
    Render online/offline badge.
    """

    if online:

        st.success(
            "System Status : Online"
        )

    else:

        st.error(
            "System Status : Offline"
        )