"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
Enterprise Plotly Charts

Reusable visualization library for the dashboard.

Author  : Gurrala Nikhil Reddy
Version : 2.0.0
===========================================================
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.config import COLORS

# ==========================================================
# Dashboard Theme
# ==========================================================

CHART_HEIGHT = 420

ENTERPRISE_LAYOUT = dict(

    paper_bgcolor=COLORS["background"],

    plot_bgcolor=COLORS["surface"],

    font=dict(

        family="Inter",

        size=13,

        color=COLORS["text"],

    ),

    margin=dict(

        l=20,

        r=20,

        t=55,

        b=20,

    ),

    hovermode="x unified",

    legend=dict(

        orientation="h",

        y=1.08,

        x=0,

    ),

)

# ==========================================================
# Apply Enterprise Theme
# ==========================================================

def apply_theme(
    fig: go.Figure,
) -> go.Figure:
    """
    Apply enterprise dashboard styling.
    """

    fig.update_layout(

        **ENTERPRISE_LAYOUT,

        height=CHART_HEIGHT,

    )

    fig.update_xaxes(

        showgrid=False,

        zeroline=False,

    )

    fig.update_yaxes(

        gridcolor="rgba(255,255,255,.08)",

        zeroline=False,

    )

    return fig

# ==========================================================
# Empty Figure
# ==========================================================

def empty_chart(
    title: str,
) -> go.Figure:
    """
    Display when no data exists.
    """

    fig = go.Figure()

    fig.update_layout(

        title=title,

        annotations=[

            dict(

                text="No data available",

                showarrow=False,

                font=dict(

                    size=18,

                ),

            )

        ],

    )

    return apply_theme(fig)
# ==========================================================
# Fraud Distribution
# ==========================================================

def fraud_distribution_chart(
    df: pd.DataFrame,
) -> go.Figure:
    """
    Fraud vs Safe transaction distribution.
    """

    if df.empty:
        return empty_chart("Fraud Distribution")

    prediction_column = None

    for column in [

        "Final_Prediction",

        "Prediction",

        "Fraud",

        "Class",

    ]:

        if column in df.columns:

            prediction_column = column

            break

    if prediction_column is None:

        return empty_chart("Fraud Distribution")

    summary = (

        df[prediction_column]

        .replace({

            0: "Safe",

            1: "Fraud",

        })

        .value_counts()

        .reset_index()

    )

    summary.columns = [

        "Status",

        "Count",

    ]

    fig = px.pie(

        summary,

        names="Status",

        values="Count",

        hole=0.60,

        color="Status",

        color_discrete_map={

            "Safe": COLORS["success"],

            "Fraud": COLORS["danger"],

        },

        title="Fraud Distribution",

    )

    fig.update_traces(

        textinfo="percent+label"

    )

    return apply_theme(fig)


# ==========================================================
# Monthly Transactions
# ==========================================================

def monthly_transactions_chart(
    df: pd.DataFrame,
) -> go.Figure:
    """
    Monthly transaction volume.
    """

    if df.empty:

        return empty_chart(

            "Monthly Transactions"

        )

    if "Date" not in df.columns:

        return empty_chart(

            "Monthly Transactions"

        )

    temp = df.copy()

    temp["Month"] = (

        pd.to_datetime(

            temp["Date"]

        )

        .dt.to_period("M")

        .astype(str)

    )

    monthly = (

        temp

        .groupby("Month")

        .size()

        .reset_index(

            name="Transactions"

        )

    )

    fig = px.line(

        monthly,

        x="Month",

        y="Transactions",

        markers=True,

        title="Monthly Transactions",

        color_discrete_sequence=[

            COLORS["primary"]

        ],

    )

    return apply_theme(fig)


# ==========================================================
# Risk Distribution
# ==========================================================

def risk_distribution_chart(
    df: pd.DataFrame,
) -> go.Figure:
    """
    Risk level distribution.
    """

    if df.empty:

        return empty_chart(

            "Risk Distribution"

        )

    if "Risk_Level" not in df.columns:

        return empty_chart(

            "Risk Distribution"

        )

    summary = (

        df["Risk_Level"]

        .value_counts()

        .reset_index()

    )

    summary.columns = [

        "Risk",

        "Count",

    ]

    fig = px.bar(

        summary,

        x="Risk",

        y="Count",

        color="Risk",

        color_discrete_map={

            "Low": COLORS["success"],

            "Medium": COLORS["warning"],

            "High": COLORS["danger"],

            "Critical": "#991B1B",

        },

        title="Risk Distribution",

    )

    return apply_theme(fig)


# ==========================================================
# Model Performance
# ==========================================================

def model_performance_chart(
) -> go.Figure:
    """
    Model comparison chart.
    """

    performance = pd.DataFrame(

        {

            "Metric": [

                "Accuracy",

                "Precision",

                "Recall",

                "F1 Score",

            ],

            "Isolation Forest": [

                96.8,

                95.6,

                94.1,

                94.8,

            ],

            "AutoEncoder": [

                98.4,

                97.5,

                96.8,

                97.1,

            ],

        }

    )

    fig = go.Figure()

    fig.add_bar(

        name="Isolation Forest",

        x=performance["Metric"],

        y=performance["Isolation Forest"],

        marker_color=COLORS["primary"],

    )

    fig.add_bar(

        name="AutoEncoder",

        x=performance["Metric"],

        y=performance["AutoEncoder"],

        marker_color=COLORS["success"],

    )

    fig.update_layout(

        barmode="group",

        title="Model Performance",

    )

    return apply_theme(fig)
# ==========================================================
# Confidence Distribution
# ==========================================================

def confidence_distribution_chart(
    df: pd.DataFrame,
) -> go.Figure:
    """
    Confidence score distribution.
    """

    if df.empty or "Confidence" not in df.columns:
        return empty_chart("Confidence Distribution")

    fig = px.histogram(

        df,

        x="Confidence",

        nbins=30,

        title="Confidence Distribution",

        color_discrete_sequence=[
            COLORS["primary"]
        ],

    )

    fig.update_layout(

        bargap=0.08

    )

    return apply_theme(fig)


# ==========================================================
# Transaction Amount Distribution
# ==========================================================

def transaction_amount_chart(
    df: pd.DataFrame,
) -> go.Figure:
    """
    Transaction amount histogram.
    """

    if df.empty or "Amount" not in df.columns:
        return empty_chart("Transaction Amount")

    fig = px.histogram(

        df,

        x="Amount",

        nbins=40,

        title="Transaction Amount Distribution",

        color_discrete_sequence=[
            COLORS["warning"]
        ],

    )

    return apply_theme(fig)


# ==========================================================
# Prediction Breakdown
# ==========================================================

def prediction_breakdown_chart(
    df: pd.DataFrame,
) -> go.Figure:
    """
    Fraud vs Safe stacked bar chart.
    """

    if df.empty:
        return empty_chart("Prediction Breakdown")

    prediction_column = None

    for column in [

        "Final_Prediction",

        "Prediction",

        "Fraud",

        "Class",

    ]:

        if column in df.columns:

            prediction_column = column

            break

    if prediction_column is None:
        return empty_chart("Prediction Breakdown")

    summary = (

        df[prediction_column]

        .replace({

            0: "Safe",

            1: "Fraud",

        })

        .value_counts()

        .reset_index()

    )

    summary.columns = [

        "Prediction",

        "Transactions",

    ]

    fig = px.bar(

        summary,

        x="Prediction",

        y="Transactions",

        color="Prediction",

        title="Prediction Breakdown",

        color_discrete_map={

            "Safe": COLORS["success"],

            "Fraud": COLORS["danger"],

        }

    )

    return apply_theme(fig)


# ==========================================================
# Risk Gauge
# ==========================================================

def risk_gauge_chart(
    score: float,
) -> go.Figure:
    """
    Enterprise risk gauge.
    """

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=score,

            title={

                "text": "Average Risk Score"

            },

            gauge={

                "axis": {

                    "range": [0,100]

                },

                "bar": {

                    "color": COLORS["primary"]

                },

                "steps":[

                    {

                        "range":[0,30],

                        "color":"#16A34A"

                    },

                    {

                        "range":[30,70],

                        "color":"#F59E0B"

                    },

                    {

                        "range":[70,100],

                        "color":"#DC2626"

                    }

                ]

            }

        )

    )

    return apply_theme(fig)


# ==========================================================
# Fraud Timeline
# ==========================================================

def fraud_timeline_chart(
    df: pd.DataFrame,
) -> go.Figure:
    """
    Fraud trend over time.
    """

    if df.empty:
        return empty_chart("Fraud Timeline")

    if "Date" not in df.columns:
        return empty_chart("Fraud Timeline")

    prediction_column = None

    for column in [

        "Final_Prediction",

        "Prediction",

        "Fraud",

        "Class",

    ]:

        if column in df.columns:

            prediction_column = column

            break

    if prediction_column is None:
        return empty_chart("Fraud Timeline")

    temp = df.copy()

    temp["Date"] = pd.to_datetime(temp["Date"])

    fraud = temp[

        temp[prediction_column] == 1

    ]

    timeline = (

        fraud

        .groupby("Date")

        .size()

        .reset_index(name="Frauds")

    )

    fig = px.line(

        timeline,

        x="Date",

        y="Frauds",

        markers=True,

        title="Fraud Timeline",

        color_discrete_sequence=[
            COLORS["danger"]
        ],

    )

    return apply_theme(fig)
# ==========================================================
# Category Distribution
# ==========================================================

def category_distribution_chart(
    df: pd.DataFrame,
) -> go.Figure:
    """
    Transaction category distribution.
    """

    if df.empty or "Category" not in df.columns:
        return empty_chart("Category Distribution")

    summary = (

        df["Category"]

        .value_counts()

        .head(10)

        .reset_index()

    )

    summary.columns = [

        "Category",

        "Transactions",

    ]

    fig = px.bar(

        summary,

        x="Category",

        y="Transactions",

        color="Transactions",

        color_continuous_scale="Blues",

        title="Top Transaction Categories",

    )

    return apply_theme(fig)


# ==========================================================
# Top Merchants
# ==========================================================

def top_merchants_chart(
    df: pd.DataFrame,
) -> go.Figure:
    """
    Most frequent merchants.
    """

    if df.empty:
        return empty_chart("Top Merchants")

    merchant_column = None

    for column in [

        "Merchant",

        "Merchant_Name",

        "Vendor",

    ]:

        if column in df.columns:

            merchant_column = column

            break

    if merchant_column is None:
        return empty_chart("Top Merchants")

    summary = (

        df[merchant_column]

        .value_counts()

        .head(10)

        .reset_index()

    )

    summary.columns = [

        "Merchant",

        "Transactions",

    ]

    fig = px.bar(

        summary,

        x="Transactions",

        y="Merchant",

        orientation="h",

        color="Transactions",

        color_continuous_scale="Viridis",

        title="Top Merchants",

    )

    fig.update_layout(

        yaxis=dict(

            categoryorder="total ascending"

        )

    )

    return apply_theme(fig)


# ==========================================================
# Correlation Heatmap
# ==========================================================

def correlation_heatmap(
    df: pd.DataFrame,
) -> go.Figure:
    """
    Correlation between numeric features.
    """

    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        return empty_chart("Correlation Heatmap")

    correlation = numeric.corr()

    fig = px.imshow(

        correlation,

        text_auto=".2f",

        color_continuous_scale="RdBu",

        title="Feature Correlation",

        aspect="auto",

    )

    return apply_theme(fig)


# ==========================================================
# Enterprise Dashboard Summary
# ==========================================================

def dashboard_summary(
    df: pd.DataFrame,
) -> dict:
    """
    Dashboard quick statistics.
    """

    summary = {

        "Rows": len(df),

        "Columns": len(df.columns),

    }

    if "Amount" in df.columns:

        summary["Total Amount"] = round(

            float(df["Amount"].sum()),

            2,

        )

        summary["Average Amount"] = round(

            float(df["Amount"].mean()),

            2,

        )

    return summary


# ==========================================================
# Chart Registry
# ==========================================================

AVAILABLE_CHARTS = {

    "Fraud Distribution":

        fraud_distribution_chart,

    "Monthly Transactions":

        monthly_transactions_chart,

    "Risk Distribution":

        risk_distribution_chart,

    "Model Performance":

        model_performance_chart,

    "Confidence Distribution":

        confidence_distribution_chart,

    "Prediction Breakdown":

        prediction_breakdown_chart,

    "Transaction Amount":

        transaction_amount_chart,

    "Fraud Timeline":

        fraud_timeline_chart,

    "Risk Gauge":

        risk_gauge_chart,

    "Category Distribution":

        category_distribution_chart,

    "Top Merchants":

        top_merchants_chart,

    "Correlation Heatmap":

        correlation_heatmap,

}