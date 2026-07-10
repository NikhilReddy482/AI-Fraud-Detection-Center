"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
Analytics Dashboard

Deep analytical insights into fraud transactions.

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

from components.system_health import (
    render_system_health,
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
# Page Config
# ==========================================================

st.set_page_config(

    page_title="Analytics",

    page_icon="📊",

    layout="wide",

    initial_sidebar_state="expanded",

)

from utils.helpers import load_css

load_css()

# ==========================================================
# Backend
# ==========================================================

loader = get_loader()

prediction_engine = get_engine()

risk_engine = get_risk_engine()

# ==========================================================
# Cached Dataset
# ==========================================================

@st.cache_data
def load_data() -> pd.DataFrame:

    return loader.dashboard()

# ==========================================================
# KPI Builder
# ==========================================================

def build_metrics(df: pd.DataFrame):

    kpis = loader.dashboard_kpis(df)

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
            "value": f"{loader.fraud_rate(df):.2f}%",
            "icon": "📈",
            "color": "success",
            "delta": "Overall",
        },

    ]
# ==========================================================
# Filters
# ==========================================================

def render_filters(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Analytics filters.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            <span class="header-title-text">Analytics Filters</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    filtered = df.copy()

    numeric_columns = filtered.select_dtypes(
        include="number"
    ).columns.tolist()

    with col1:

        fraud_only = st.checkbox(
            "Show Fraud Only"
        )

    with col2:

        if numeric_columns:

            amount_column = st.selectbox(

                "Numeric Column",

                numeric_columns,

            )

        else:

            amount_column = None

    with col3:

        if amount_column:

            minimum = float(

                filtered[
                    amount_column
                ].min()

            )

            maximum = float(

                filtered[
                    amount_column
                ].max()

            )

            value = st.slider(

                "Minimum Value",

                minimum,

                maximum,

                minimum,

            )

            filtered = filtered[

                filtered[amount_column] >= value

            ]

    if fraud_only:

        if "Class" in filtered.columns:

            filtered = filtered[

                filtered["Class"] == 1

            ]

        elif "Final_Prediction" in filtered.columns:

            filtered = filtered[

                filtered["Final_Prediction"] == 1

            ]

    st.divider()

    return filtered
# ==========================================================
# KPI Section
# ==========================================================

def render_kpi_section(
    dataframe: pd.DataFrame,
) -> None:
    """
    Display analytics KPIs.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/></svg>
            <span class="header-title-text">Analytics Overview</span>
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
# Charts
# ==========================================================

def render_charts(
    dataframe: pd.DataFrame,
) -> None:
    """
    Analytics visualizations.
    """

    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
            <span class="header-title-text">Fraud Analytics</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:

        st.plotly_chart(

            fraud_distribution_chart(
                dataframe
            ),

            use_container_width=True,

        )

    with right:

        st.plotly_chart(

            monthly_transactions_chart(
                dataframe
            ),

            use_container_width=True,

        )

    left, right = st.columns(2)

    with left:

        st.plotly_chart(

            risk_distribution_chart(
                dataframe
            ),

            use_container_width=True,

        )

    with right:

        st.plotly_chart(

            model_performance_chart(),

            use_container_width=True,

        )

    st.divider()


# ==========================================================
# Business Insights
# ==========================================================

def render_business_insights(
    dataframe: pd.DataFrame,
) -> None:
    """
    Executive insights.
    """

    dataset = loader.dataset_info(
        dataframe
    )

    kpis = loader.dashboard_kpis(
        dataframe
    )

    runtime = risk_engine.status()

    left, right = st.columns(2)

    with left:

        st.info(
            f"""
### Dataset Insights

Rows : **{dataset.get("Rows",0):,}**

Columns : **{dataset.get("Columns",0)}**

Missing Values : **{dataset.get("Missing Values",0)}**

Duplicates : **{dataset.get("Duplicate Rows",0)}**
"""
        )

    with right:

        st.success(
            f"""
### AI Platform

Fraud Alerts : **{kpis.get("Fraud Alerts",0):,}**

Fraud Rate : **{loader.fraud_rate(dataframe):.2f}%**

Engine : **{runtime.get("Engine","Unknown")}**

Status : **{runtime.get("Status","Unknown")}**
"""
        )

    st.divider()


# ==========================================================
# Dataset Health
# ==========================================================

def render_health(
    dataframe: pd.DataFrame,
) -> None:
    """
    Dataset health.
    """

    render_system_health(

        loader.dataset_info(
            dataframe
        ),

        loader.status(),

    )


# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """
    Analytics entry point.
    """

    render_sidebar()

    render_header(

        title="Analytics Dashboard",

        subtitle="Fraud Analytics & Business Intelligence",

    )

    try:

        dataframe = load_data()

        if dataframe.empty:

            st.error(
                "Dataset is empty."
            )

            st.stop()

        filtered = render_filters(
            dataframe
        )

        render_kpi_section(
            filtered
        )

        render_charts(
            filtered
        )

        render_business_insights(
            filtered
        )

        render_health(
            filtered
        )

        render_footer()

    except Exception as error:

        logger.exception(error)

        st.error(
            f"""
Analytics page failed to load.

Error:

{error}
"""
        )

        st.stop()


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    main()