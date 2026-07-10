"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
Footer Component

Reusable enterprise footer.

Author  : Gurrala Nikhil Reddy
Version : 1.0.0
===========================================================
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

# ==========================================================
# Footer
# ==========================================================

APP_NAME = "AI Fraud Intelligence Center"

VERSION = "1.0.0"

TECH_STACK = (
    "Python • Streamlit • Plotly • "
    "Scikit-Learn • TensorFlow"
)


def render_footer() -> None:
    """
    Render dashboard footer.
    """

    st.divider()

    current_year = datetime.now().year

    st.markdown(
        f"""
<div style="padding:18px 0;text-align:center;">

<h4 style="margin-bottom:6px;">
{APP_NAME}
</h4>

<p style="margin:0;color:#94A3B8;">
Enterprise Fraud Detection Dashboard
</p>

<p style="margin-top:12px;font-size:14px;">
{TECH_STACK}
</p>

<p style="margin-top:10px;
font-size:13px;
color:#64748B;">

Version {VERSION}
&nbsp;&nbsp;|&nbsp;&nbsp;
© {current_year}
&nbsp;&nbsp;|&nbsp;&nbsp;
Developed by Gurrala Nikhil Reddy

</p>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Small Footer
# ==========================================================

def render_small_footer() -> None:
    """
    Compact footer for
    smaller pages.
    """

    st.caption(
        f"{APP_NAME} • Version {VERSION}"
    )


# ==========================================================
# Version Badge
# ==========================================================

def version_badge() -> None:
    """
    Display version badge.
    """

    st.success(
        f"Version {VERSION}"
    )