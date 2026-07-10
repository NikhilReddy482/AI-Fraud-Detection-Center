"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
Fraud Alert Center

Enterprise fraud monitoring dashboard.

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

import pandas as pd
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
from components.alert_table import render_alert_table

# ==========================================================
# Backend
# ==========================================================

from utils.load_data import get_loader
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
# Page
# ==========================================================

st.set_page_config(

    page_title="Fraud Alerts",

    page_icon="🚨",

    layout="wide",

    initial_sidebar_state="expanded",

)

from utils.helpers import load_css

load_css()

# ==========================================================
# Backend
# ==========================================================

loader = get_loader()

risk_engine = get_risk_engine()

# ==========================================================
# Cache
# ==========================================================

@st.cache_data(show_spinner=False)
def load_alerts() -> pd.DataFrame:

    return loader.alerts()
# ==========================================================
# KPI Cards
# ==========================================================

def build_metrics(
    dataframe: pd.DataFrame,
):

    metrics = {

        "Critical": 0,

        "High": 0,

        "Medium": 0,

        "Low": 0,

    }

    if "Risk Level" in dataframe.columns:

        counts = dataframe[
            "Risk Level"
        ].value_counts()

        for level in metrics:

            metrics[level] = int(
                counts.get(level, 0)
            )

    return [

        {

            "title": "Critical",

            "value": metrics["Critical"],

            "icon": "🔴",

            "color": "danger",

            "delta": "Immediate",

        },

        {

            "title": "High",

            "value": metrics["High"],

            "icon": "🟠",

            "color": "warning",

            "delta": "Review",

        },

        {

            "title": "Medium",

            "value": metrics["Medium"],

            "icon": "🟡",

            "color": "primary",

            "delta": "Monitor",

        },

        {

            "title": "Low",

            "value": metrics["Low"],

            "icon": "🟢",

            "color": "success",

            "delta": "Normal",

        },

    ]


# ==========================================================
# Filters
# ==========================================================

def render_filters(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Alert Filters</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, center, right = st.columns(3)

    filtered = dataframe.copy()

    with left:

        search = st.text_input(
            "Search"
        )

    with center:

        if "Risk Level" in filtered.columns:

            level = st.selectbox(

                "Risk Level",

                ["All"]

                + sorted(

                    filtered[
                        "Risk Level"
                    ].dropna().unique()

                ),

            )

        else:

            level = "All"

    with right:

        rows = st.slider(

            "Maximum Alerts",

            10,

            500,

            100,

        )

    if search:

        filtered = filtered.astype(
            str
        ).apply(

            lambda col:
            col.str.contains(
                search,
                case=False,
                na=False,
            )

        ).any(axis=1)

        filtered = dataframe[
            filtered
        ]

    if level != "All":

        filtered = filtered[
            filtered[
                "Risk Level"
            ] == level
        ]

    return filtered.head(rows)
# ==========================================================
# KPI Section
# ==========================================================

def render_kpi_section(
    dataframe: pd.DataFrame,
) -> None:
    """
    Display fraud alert KPIs.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Alert Overview</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    metric_grid(

        build_metrics(
            dataframe
        )

    )

    st.divider()


# ==========================================================
# Alert Table
# ==========================================================

def render_alerts(
    dataframe: pd.DataFrame,
) -> None:
    """
    Display alert table.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><line x1="8" x2="21" y1="6" y2="6"/><line x1="8" x2="21" y1="12" y2="12"/><line x1="8" x2="21" y1="18" y2="18"/><line x1="3" x2="3.01" y1="6" y2="6"/><line x1="3" x2="3.01" y1="12" y2="12"/><line x1="3" x2="3.01" y1="18" y2="18"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Live Fraud Alerts</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if dataframe.empty:

        st.info(
            "No alerts found."
        )

        return

    render_alert_table(
        dataframe
    )

    st.divider()


# ==========================================================
# Analyst Ticket Operations
# ==========================================================

def render_analyst_queue_controls(dataframe: pd.DataFrame) -> None:
    """
    Provide interactive controls for analysts to review, claim, and update alert statuses.
    """
    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Analyst Operations Center</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if dataframe.empty:
        st.info("No active alerts to manage.")
        return
        
    # Check if audit status is in session state, if not initialize it
    if "alert_status_log" not in st.session_state:
        st.session_state.alert_status_log = {}
        
    st.write("Select an alert reference to update status or record investigation notes:")
    
    # Form option lists
    alert_options = []
    for idx, row in dataframe.iterrows():
        # Get custom status from session state if updated, default to New
        current_status = st.session_state.alert_status_log.get(idx, {}).get("Status", "New")
        alert_options.append({
            "idx": idx,
            "label": f"ID {idx} | Time: {row['Time']:.0f} | Amount: ${row['Amount']:.2f} | Risk: {row['Risk_Level']} | Status: {current_status}"
        })
        
    selected_option = st.selectbox(
        "Select Alert Reference ID",
        options=alert_options,
        format_func=lambda x: x["label"]
    )
    
    if selected_option:
        idx = selected_option["idx"]
        row = dataframe.loc[idx]
        current_log = st.session_state.alert_status_log.get(idx, {"Status": "New", "Analyst": "", "Notes": ""})
        
        col1, col2 = st.columns(2)
        with col1:
            status = st.selectbox(
                "Update Investigation Status",
                ["New", "Under Investigation", "Escalated to Fraud Ops", "Resolved - True Fraud", "Resolved - False Positive"],
                index=["New", "Under Investigation", "Escalated to Fraud Ops", "Resolved - True Fraud", "Resolved - False Positive"].index(current_log["Status"])
            )
            analyst = st.text_input("Assigned Analyst Name", value=current_log["Analyst"])
        with col2:
            notes = st.text_area("Analyst Investigation Notes / Action Taken", value=current_log["Notes"])
            
        if st.button("Update Alert Ticket Status", use_container_width=True):
            st.session_state.alert_status_log[idx] = {
                "Status": status,
                "Analyst": analyst,
                "Notes": notes,
                "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.toast("Alert ticket updated successfully!", icon="✅")
            st.rerun()
            
    # Show active audit logs table if logs exist
    if st.session_state.alert_status_log:
        st.markdown(
            """
            <div class="header-container" style="margin-bottom: 12px; padding: 5px 0;">
                <svg class="header-icon" viewBox="0 0 24 24" style="width: 24px; height: 24px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                <span class="header-title-text" style="font-size: 20px;">Analyst Action History</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        log_records = []
        for l_idx, log in st.session_state.alert_status_log.items():
            if l_idx in dataframe.index:
                row = dataframe.loc[l_idx]
                log_records.append({
                    "Alert ID": l_idx,
                    "Tx Time": row["Time"],
                    "Amount": row["Amount"],
                    "Risk Level": row["Risk_Level"],
                    "Current Status": log["Status"],
                    "Analyst": log["Analyst"],
                    "Notes": log["Notes"],
                    "Updated At": log["Timestamp"]
                })
        if log_records:
            st.dataframe(pd.DataFrame(log_records), use_container_width=True, hide_index=True)
            
    st.divider()


# ==========================================================
# Alert Summary
# ==========================================================

def render_summary(
    dataframe: pd.DataFrame,
) -> None:
    """
    Display dataset summary.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Alert Summary</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:

        st.info(
            f"""
### Dataset

Total Alerts : **{len(dataframe):,}**

Columns : **{len(dataframe.columns)}**
"""
        )

    with right:

        status = risk_engine.status()

        st.success(
            f"""
### Risk Engine

Engine : **{status.get("Engine","Unknown")}**

Version : **{status.get("Version","-")}**

Status : **{status.get("Status","Unknown")}**
"""
        )

    st.divider()


# ==========================================================
# Export
# ==========================================================

def render_export(
    dataframe: pd.DataFrame,
) -> None:
    """
    Export alerts.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Export Alerts</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    csv = dataframe.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label="📥 Download CSV",

        data=csv,

        file_name="fraud_alerts.csv",

        mime="text/csv",

        use_container_width=True,

    )

    st.divider()


# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """
    Fraud Alerts entry point.
    """

    render_sidebar()

    render_header()

    try:

        dataframe = load_alerts()

        if dataframe.empty:

            st.warning(
                "No fraud alerts available."
            )

            render_footer()

            return

        filtered = render_filters(
            dataframe
        )

        render_kpi_section(
            filtered
        )

        render_alerts(
            filtered
        )

        render_analyst_queue_controls(
            filtered
        )

        render_summary(
            filtered
        )

        render_export(
            filtered
        )

        render_footer()

    except Exception as error:

        logger.exception(error)

        st.error(
            f"""
Fraud Alerts page failed to load.

Error:

{error}
"""
        )

        st.stop()


# ==========================================================
# Run Application
# ==========================================================

if __name__ == "__main__":

    main()