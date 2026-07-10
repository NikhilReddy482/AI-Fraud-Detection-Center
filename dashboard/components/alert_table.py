"""
===========================================================
Enterprise Alert Table Component
-----------------------------------------------------------
Reusable alert table for displaying suspicious and
fraudulent transactions.

Author  : Gurrala Nikhil Reddy
Version : 1.0.0
===========================================================
"""

from __future__ import annotations

import io
import pandas as pd
import streamlit as st


# ==========================================================
# RISK COLORS
# ==========================================================

RISK_COLORS = {
    "Low": "#16A34A",
    "Medium": "#F59E0B",
    "High": "#DC2626",
}


# ==========================================================
# Highlight Risk
# ==========================================================

def highlight_risk(value):

    color = RISK_COLORS.get(str(value), "#2563EB")

    return (
        f"background-color:{color};"
        "color:white;"
        "font-weight:bold;"
        "text-align:center;"
    )


# ==========================================================
# Export CSV
# ==========================================================

def export_csv(df: pd.DataFrame):

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Export CSV",
        data=csv,
        file_name="fraud_alerts.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ==========================================================
# Search Filter
# ==========================================================

def filter_dataframe(df: pd.DataFrame):

    search = st.text_input(
        "🔍 Search Transaction",
        placeholder="Search by ID, Customer, Merchant..."
    )

    if search:

        mask = pd.Series(False, index=df.index)

        for col in df.columns:

            mask |= (
                df[col]
                .astype(str)
                .str.contains(search, case=False, na=False)
            )

        df = df[mask]

    return df


# ==========================================================
# Risk Filter
# ==========================================================

def risk_filter(df):

    if "Risk_Level" not in df.columns:
        return df

    risk = st.multiselect(
        "Risk Level",
        ["Low", "Medium", "High"],
        default=["Low", "Medium", "High"],
    )

    return df[df["Risk_Level"].isin(risk)]


# ==========================================================
# Summary Cards
# ==========================================================

def summary(df):

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Alerts",
            len(df),
        )

    with col2:

        if "Risk_Level" in df.columns:

            high = (
                df["Risk_Level"]
                .eq("High")
                .sum()
            )

        else:
            high = 0

        st.metric(
            "High Risk",
            high,
        )

    with col3:

        if "Risk_Level" in df.columns:

            safe = (
                df["Risk_Level"]
                .eq("Low")
                .sum()
            )

        else:
            safe = 0

        st.metric(
            "Low Risk",
            safe,
        )


# ==========================================================
# Alert Table
# ==========================================================

def render_alert_table(df: pd.DataFrame):

    if df.empty:

        st.warning("No alerts available.")

        return

    df = filter_dataframe(df)

    df = risk_filter(df)

    summary(df)

    st.markdown("### 🚨 Fraud Alert Table")

    display = df.copy()

    # Filter to show only clean, business-relevant columns (hide raw PCA / ML features)
    clean_cols = [
        'Time', 'Amount', 'Hour', 'Time_Period', 'Time Period', 
        'Risk_Score', 'Risk_Level', 'Risk Score', 'Risk Level', 
        'Recommendation', 'Alert_Priority', 'Alert Priority', 'Alert'
    ]
    cols_to_show = [c for c in clean_cols if c in display.columns]
    if cols_to_show:
        display = display[cols_to_show]

    # Find the active risk level column for highlighting
    risk_col = None
    for col in ["Risk_Level", "Risk Level"]:
        if col in display.columns:
            risk_col = col
            break

    if risk_col:

        styled = display.style.map(
            highlight_risk,
            subset=[risk_col]
        )

        st.dataframe(
            styled,
            use_container_width=True,
            hide_index=True,
            height=500,
        )

    else:

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True,
            height=500,
        )

    export_csv(display)


# ==========================================================
# Recent Alerts Widget
# ==========================================================

def recent_alerts(df: pd.DataFrame, rows: int = 5):

    st.subheader("Recent Fraud Alerts")

    if df.empty:

        st.info("No alerts found.")

        return

    display = df.copy()
    clean_cols = [
        'Time', 'Amount', 'Hour', 'Time_Period', 'Time Period', 
        'Risk_Score', 'Risk_Level', 'Risk Score', 'Risk Level', 
        'Recommendation', 'Alert_Priority', 'Alert Priority', 'Alert'
    ]
    cols_to_show = [c for c in clean_cols if c in display.columns]
    if cols_to_show:
        display = display[cols_to_show]

    st.dataframe(
        display.head(rows),
        use_container_width=True,
        hide_index=True,
    )


# ==========================================================
# High Risk Only
# ==========================================================

def high_risk_alerts(df: pd.DataFrame):

    if "Risk_Level" not in df.columns:

        return pd.DataFrame()

    return df[df["Risk_Level"] == "High"]


# ==========================================================
# Alert Counter
# ==========================================================

def alert_statistics(df: pd.DataFrame):

    stats = {}

    if "Risk_Level" not in df.columns:
        return stats

    stats["Low"] = (
        df["Risk_Level"]
        .eq("Low")
        .sum()
    )

    stats["Medium"] = (
        df["Risk_Level"]
        .eq("Medium")
        .sum()
    )

    stats["High"] = (
        df["Risk_Level"]
        .eq("High")
        .sum()
    )

    stats["Total"] = len(df)

    return stats