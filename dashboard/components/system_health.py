"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
System Health Component

Reusable dashboard component for displaying
dataset and system health.

Author  : Gurrala Nikhil Reddy
Version : 1.0.0
===========================================================
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st


# ==========================================================
# Dataset Health
# ==========================================================

def render_system_health(
    dataset_info: dict,
    status: dict,
) -> None:
    """
    Render enterprise system health panel.

    Parameters
    ----------
    dataset_info : dict

    Example
    -------
    {
        "Rows":10000,
        "Columns":31,
        "Missing Values":0,
        "Duplicate Rows":0,
        "Memory (MB)":5.21
    }

    status : dict

    Example
    -------
    {
        "Ready":True,
        "Version":"1.0.0",
        "Resources":{
            "available":4
        }
    }
    """

    st.markdown("## 🖥️ System Health")

    left, right = st.columns(2)

    # ======================================================
    # Dataset Information
    # ======================================================

    with left:

        st.markdown("### Dataset")

        c1, c2 = st.columns(2)

        c1.metric(
            "Rows",
            f"{dataset_info.get('Rows',0):,}",
        )

        c2.metric(
            "Columns",
            dataset_info.get("Columns",0),
        )

        c1.metric(
            "Missing Values",
            dataset_info.get(
                "Missing Values",
                0,
            ),
        )

        c2.metric(
            "Duplicate Rows",
            dataset_info.get(
                "Duplicate Rows",
                0,
            ),
        )

        st.metric(
            "Memory Usage",
            f"{dataset_info.get('Memory (MB)',0):.2f} MB",
        )

    # ======================================================
    # Dashboard Status
    # ======================================================

    with right:

        st.markdown("### Dashboard")

        ready = status.get(
            "Ready",
            False,
        )

        version = status.get(
            "Version",
            "Unknown",
        )

        resources = (

            status.get(
                "Resources",
                {}
            )

            .get(
                "available",
                0,
            )

        )

        if ready:

            st.success(
                "System Ready"
            )

        else:

            st.error(
                "System Offline"
            )

        st.metric(
            "Resources Loaded",
            resources,
        )

        st.metric(
            "Version",
            version,
        )

        st.metric(
            "Last Refresh",
            datetime.now().strftime(
                "%H:%M:%S"
            ),
        )

    st.divider()


# ==========================================================
# Compact Health Card
# ==========================================================

def render_health_badge(
    ready: bool,
) -> None:
    """
    Small health badge.
    """

    if ready:

        st.success(
            "🟢 Healthy"
        )

    else:

        st.error(
            "🔴 Unhealthy"
        )


# ==========================================================
# Dataset Summary
# ==========================================================

def dataset_summary(
    dataset_info: dict,
) -> None:
    """
    Compact dataset summary.
    """

    st.markdown("### Dataset Summary")

    cols = st.columns(4)

    cols[0].metric(
        "Rows",
        f"{dataset_info.get('Rows',0):,}",
    )

    cols[1].metric(
        "Columns",
        dataset_info.get(
            "Columns",
            0,
        ),
    )

    cols[2].metric(
        "Missing",
        dataset_info.get(
            "Missing Values",
            0,
        ),
    )

    cols[3].metric(
        "Duplicates",
        dataset_info.get(
            "Duplicate Rows",
            0,
        ),
    )