"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
Reporting Center

Business reports and export dashboard.

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

# ==========================================================
# Backend
# ==========================================================

from utils.load_data import get_loader

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

    page_title="Reports",

    page_icon="📄",

    layout="wide",

    initial_sidebar_state="expanded",

)

from utils.helpers import load_css

load_css()

# ==========================================================
# Backend
# ==========================================================

loader = get_loader()

# ==========================================================
# Cached Data
# ==========================================================

@st.cache_data(show_spinner=False)
def load_dashboard():

    return loader.dashboard()


@st.cache_data(show_spinner=False)
def load_alerts():

    return loader.alerts()
# ==========================================================
# KPI Builder
# ==========================================================

def build_metrics(
    dataframe: pd.DataFrame,
):

    kpis = loader.dashboard_kpis(
        dataframe
    )

    return [

        {

            "title": "Transactions",

            "value": f"{kpis.get('Total Transactions',0):,}",

            "icon": "💳",

            "color": "primary",

            "delta": "Dataset",

        },

        {

            "title": "Fraud Alerts",

            "value": f"{kpis.get('Fraud Alerts',0):,}",

            "icon": "🚨",

            "color": "danger",

            "delta": "Detected",

        },

        {

            "title": "High Risk",

            "value": f"{kpis.get('High Risk',0):,}",

            "icon": "⚠️",

            "color": "warning",

            "delta": "Active",

        },

        {

            "title": "Fraud Rate",

            "value": f"{loader.fraud_rate(dataframe):.2f}%",

            "icon": "📈",

            "color": "success",

            "delta": "Overall",

        },

    ]


# ==========================================================
# KPI Section
# ==========================================================

def render_kpis(
    dataframe: pd.DataFrame,
):

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Executive Summary</span>
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
# Report Selector
# ==========================================================

def report_selector():

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Available Reports</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    report = st.radio(

        "Select Report",

        [

            "Dashboard Summary",

            "Fraud Alerts",

            "Transaction Dataset",

        ],

        horizontal=True,

    )

    st.divider()

    return report
# ==========================================================
# Report Preview
# ==========================================================

def render_preview(
    report_name: str,
    dashboard_df: pd.DataFrame,
    alerts_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Display report preview and
    return the dataframe for export.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Report Preview</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if report_name == "Dashboard Summary":

        preview = dashboard_df.copy()

    elif report_name == "Fraud Alerts":

        preview = alerts_df.copy()

    else:

        preview = dashboard_df.copy()

    if preview.empty:

        st.warning(
            "No data available."
        )

        return preview

    # Filter to show only clean, business-relevant columns (hide raw PCA / ML features)
    clean_cols = [
        'Time', 'Amount', 'Hour', 'Time_Period', 'Time Period', 
        'Risk_Score', 'Risk_Level', 'Risk Score', 'Risk Level', 
        'Recommendation', 'Alert_Priority', 'Alert Priority', 'Alert'
    ]
    cols_to_show = [c for c in clean_cols if c in preview.columns]
    if cols_to_show:
        preview = preview[cols_to_show]

    st.dataframe(

        preview.head(20),

        use_container_width=True,

        hide_index=True,

    )

    st.divider()

    return preview
# ==========================================================
# Export
# ==========================================================

def render_export(
    dataframe: pd.DataFrame,
    filename: str,
) -> None:
    """
    Export report as CSV.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Export Report</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    csv = dataframe.to_csv(

        index=False

    ).encode("utf-8")

    st.download_button(

        label="Download CSV",

        data=csv,

        file_name=filename,

        mime="text/csv",

        use_container_width=True,

    )

    st.divider()
# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """
    Reports page entry point.
    """

    render_sidebar()

    render_header()

    try:

        dashboard_df = load_dashboard()

        alerts_df = load_alerts()

        if dashboard_df.empty:

            st.error(
                "Dashboard dataset is empty."
            )

            st.stop()

        render_kpis(
            dashboard_df
        )

        report = report_selector()

        preview = render_preview(

            report,

            dashboard_df,

            alerts_df,

        )

        filename = (

            report.lower()

            .replace(" ", "_")

            + ".csv"

        )

        render_export(

            preview,

            filename,

        )

        render_footer()

    except Exception as error:

        logger.exception(error)

        st.error(
            f"""
Reports page failed to load.

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