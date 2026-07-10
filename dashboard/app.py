"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
Enterprise Dashboard

Home Page

Author  : Gurrala Nikhil Reddy
Version : 3.0.0
===========================================================
"""

from __future__ import annotations

# ==========================================================
# Standard Library
# ==========================================================

import logging
import sys
from datetime import datetime
from pathlib import Path

# ==========================================================
# Third Party
# ==========================================================

import streamlit as st
import pandas as pd

# ==========================================================
# Project Root
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# ==========================================================
# Components
# ==========================================================

from components.sidebar import render_sidebar
from components.header import render_header
from components.footer import render_footer

from components.metric_cards import metric_grid

from components.system_health import (
    render_system_health,
)

from components.model_health import (
    render_model_health,
)

from components.alert_table import (
    render_alert_table,
)

from components.plotly_charts import (
    fraud_distribution_chart,
    monthly_transactions_chart,
    risk_distribution_chart,
    model_performance_chart,
)

# ==========================================================
# Backend
# ==========================================================

from utils.load_data import get_loader

from utils.predict import get_engine

from utils.risk_engine import (
    get_risk_engine,
)

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
# Streamlit Page
# ==========================================================

st.set_page_config(

    page_title="AI Fraud Intelligence Center",

    page_icon="🛡️",

    layout="wide",

    initial_sidebar_state="expanded",

)

# ==========================================================
# Load Global CSS
# ==========================================================

CSS_FILE = (
    ROOT_DIR /
    "assets" /
    "styles.css"
)


from utils.helpers import load_css

load_css()

# ==========================================================
# Backend Singletons
# ==========================================================

loader = get_loader()

prediction_engine = get_engine()

risk_engine = get_risk_engine()

# ==========================================================
# Cached Dashboard Dataset
# ==========================================================

@st.cache_data(show_spinner=False)
def load_dashboard() -> pd.DataFrame:
    """
    Load dashboard dataset.
    """

    return loader.dashboard()

# ==========================================================
# Cached Prediction Result
# ==========================================================

@st.cache_data(show_spinner=False)
def load_prediction_results(
    dataframe: pd.DataFrame,
) -> dict:
    """
    Run prediction engine once.
    """

    return prediction_engine.predict_for_dashboard(
        dataframe
    )

# ==========================================================
# KPI Builder
# ==========================================================

def build_kpis(
    dataframe: pd.DataFrame,
) -> list[dict]:
    """
    Dashboard KPI cards.
    """

    kpis = loader.dashboard_kpis(
        dataframe
    )

    total = kpis.get(
        "Total Transactions",
        0,
    )

    fraud = kpis.get(
        "Fraud Alerts",
        0,
    )

    high = kpis.get(
        "High Risk",
        0,
    )

    rate = loader.fraud_rate(
        dataframe
    )

    return [

        {

            "title": "Transactions",

            "value": f"{total:,}",

            "icon": "💳",

            "color": "primary",

            "delta": "Live",

        },

        {

            "title": "Fraud Alerts",

            "value": f"{fraud:,}",

            "icon": "🚨",

            "color": "danger",

            "delta": "Detected",

        },

        {

            "title": "High Risk",

            "value": f"{high:,}",

            "icon": "⚠️",

            "color": "warning",

            "delta": "Active",

        },

        {

            "title": "Fraud Rate",

            "value": f"{rate:.2f}%",

            "icon": "🛡️",

            "color": "success",

            "delta": "Current",

        },

    ]
# ==========================================================
# Executive KPI Section
# ==========================================================

def render_kpi_section(
    dataframe: pd.DataFrame,
) -> None:
    """
    Render executive KPI cards.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
            <span class="header-title-text">Executive Dashboard</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    metric_grid(

        build_kpis(
            dataframe
        )

    )

    st.divider()


# ==========================================================
# Prediction Summary
# ==========================================================

def render_prediction_summary(
    predictions: dict,
) -> None:
    """
    Prediction summary panel.
    """

    summary = predictions.get(
        "summary",
        {},
    )

    left, right = st.columns(
        [3, 2]
    )

    with left:

        st.info(
            f"""
### Prediction Summary

• Total Transactions : **{summary.get('Transactions',0):,}**

• Fraudulent : **{summary.get('Fraud',0):,}**

• Safe : **{summary.get('Safe',0):,}**

• Fraud Rate : **{summary.get('Fraud Rate',0):.2f}%**
"""
        )

    with right:

        st.success(
            """
### Dashboard Status

✔ Dataset Loaded

✔ Models Ready

✔ Risk Engine Active

✔ Live Monitoring Enabled
"""
        )

    st.divider()


# ==========================================================
# Analytics Charts
# ==========================================================

def render_chart_section(
    dataframe: pd.DataFrame,
) -> None:
    """
    Display dashboard charts.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
            <span class="header-title-text">Analytics Overview</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(

            fraud_distribution_chart(
                dataframe
            ),

            use_container_width=True,

        )

    with col2:

        st.plotly_chart(

            monthly_transactions_chart(
                dataframe
            ),

            use_container_width=True,

        )

    col3, col4 = st.columns(2)

    with col3:

        st.plotly_chart(

            risk_distribution_chart(
                dataframe
            ),

            use_container_width=True,

        )

    with col4:

        st.plotly_chart(

            model_performance_chart(),

            use_container_width=True,

        )

    st.divider()


# ==========================================================
# Fraud Alert Section
# ==========================================================

def render_alert_section() -> None:
    """
    Display latest fraud alerts.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>
            <span class="header-title-text">Recent Fraud Alerts</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    try:

        alerts = loader.alerts()

        if alerts.empty:

            st.info(
                "No fraud alerts available."
            )

        else:

            render_alert_table(

                alerts.head(10)

            )

    except Exception as error:

        logger.exception(error)

        st.error(

            "Unable to load fraud alerts."

        )

    st.divider()
# ==========================================================
# System Health
# ==========================================================

def render_health_section(
    dataframe: pd.DataFrame,
) -> None:
    """
    Render dataset and model health.
    """

    dataset_info = loader.dataset_info(
        dataframe
    )

    dashboard_status = loader.status()

    model_info = (
        prediction_engine.model_summary()
    )

    render_system_health(

        dataset_info,

        dashboard_status,

    )

    render_model_health(

        model_info,

    )


# ==========================================================
# Runtime Information
# ==========================================================

def render_runtime_section() -> None:
    """
    Dashboard runtime information.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
            <span class="header-title-text">Runtime Information</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    runtime = risk_engine.status()

    left, right = st.columns(2)

    with left:

        st.info(
            f"""
### Application

Version : 3.0.0

Engine : {runtime.get("Engine","Unknown")}

Status : {runtime.get("Status","Unknown")}
"""
        )

    with right:

        st.success(
            f"""
### Runtime

Current Time

{datetime.now().strftime('%d %b %Y')}

{datetime.now().strftime('%I:%M:%S %p')}
"""
        )

    st.divider()


# ==========================================================
# Dashboard Renderer
# ==========================================================

def render_dashboard(
    dataframe: pd.DataFrame,
) -> None:
    """
    Render complete dashboard.
    """

    prediction_result = load_prediction_results(
        dataframe
    )

    render_kpi_section(
        dataframe
    )

    render_prediction_summary(
        prediction_result
    )

    render_chart_section(
        dataframe
    )

    render_alert_section()

    render_health_section(
        dataframe
    )

    render_runtime_section()
# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """
    Dashboard entry point.
    """

    render_sidebar()

    render_header()

    try:

        with st.spinner(

            "Loading AI Fraud Intelligence Center..."

        ):

            dataframe = load_dashboard()

        render_dashboard(
            dataframe
        )

        render_footer()

    except Exception as error:

        logger.exception(error)

        st.error(
            f"""
### Dashboard Initialization Failed

The dashboard could not be loaded.

Please verify:

• Dataset files

• Trained models

• Configuration

• Project structure

Error:

{error}
"""
        )

        st.stop()


# ==========================================================
# Sidebar Controls
# ==========================================================

st.sidebar.divider()

if st.sidebar.button(

    "🔄 Refresh Dashboard",

    use_container_width=True,

):

    loader.reload()

    st.rerun()


# ==========================================================
# Application
# ==========================================================

if __name__ == "__main__":

    main()