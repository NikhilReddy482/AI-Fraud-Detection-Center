"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
Model Health Component

Reusable component for displaying AI model status.

Author  : Gurrala Nikhil Reddy
Version : 1.0.0
===========================================================
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st


# ==========================================================
# Model Health
# ==========================================================

def render_model_health(
    model_info: dict,
) -> None:
    """
    Display AI model information.

    Expected model_info
    -------------------

    {
        "Isolation Forest":"IsolationForest",
        "AutoEncoder":"Sequential",
        "Threshold":0.0031,
        "Status":"Ready"
    }
    """

    st.markdown("## 🤖 AI Model Health")

    left, right = st.columns([3, 2])

    # ======================================================
    # Models
    # ======================================================

    with left:

        c1, c2 = st.columns(2)

        c1.metric(

            "Isolation Forest",

            model_info.get(
                "Isolation Forest",
                "N/A",
            ),

        )

        c2.metric(

            "AutoEncoder",

            model_info.get(
                "AutoEncoder",
                "N/A",
            ),

        )

        threshold = model_info.get(
            "Threshold",
            0,
        )

        st.metric(

            "Threshold",

            f"{threshold:.6f}",

        )

    # ======================================================
    # Status
    # ======================================================

    with right:

        status = model_info.get(
            "Status",
            "Unknown",
        )

        if status.lower() == "ready":

            st.success(
                "🟢 Models Loaded"
            )

        else:

            st.error(
                "🔴 Models Not Ready"
            )

        st.metric(

            "Status",

            status,

        )

        st.metric(

            "Version",

            "1.0.0",

        )

        st.metric(

            "Checked",

            datetime.now().strftime(
                "%H:%M:%S"
            ),

        )

    st.divider()


# ==========================================================
# Compact Status
# ==========================================================

def render_model_badge(
    model_info: dict,
) -> None:
    """
    Small reusable model status badge.
    """

    status = model_info.get(
        "Status",
        "Unknown",
    )

    if status.lower() == "ready":

        st.success(
            "🤖 AI Models Ready"
        )

    else:

        st.error(
            "⚠ AI Models Offline"
        )


# ==========================================================
# Model Summary
# ==========================================================

def render_model_summary(
    model_info: dict,
) -> None:
    """
    Compact horizontal summary.
    """

    st.markdown("### Model Summary")

    cols = st.columns(4)

    cols[0].metric(

        "Isolation",

        model_info.get(
            "Isolation Forest",
            "N/A",
        ),

    )

    cols[1].metric(

        "AutoEncoder",

        model_info.get(
            "AutoEncoder",
            "N/A",
        ),

    )

    cols[2].metric(

        "Threshold",

        f"{model_info.get('Threshold',0):.4f}",

    )

    cols[3].metric(

        "Status",

        model_info.get(
            "Status",
            "Unknown",
        ),

    )