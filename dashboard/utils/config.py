"""
===========================================================
Configuration Module
-----------------------------------------------------------
Centralized configuration for the Enterprise Fraud
Intelligence Dashboard.

Author : Gurrala Nikhil Reddy
Version : 1.0.0
===========================================================
"""

from pathlib import Path

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

ASSETS_DIR = BASE_DIR / "assets"

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_DIR = PROJECT_ROOT / "models"

REPORTS_DIR = PROJECT_ROOT / "reports"

# ==========================================================
# Dataset Paths
# ==========================================================

CLEAN_DATASET = PROCESSED_DATA_DIR / "cleaned_transactions.csv"

ISOLATION_RESULTS = (
    PROCESSED_DATA_DIR /
    "isolation_forest_predictions.csv"
)

AUTOENCODER_RESULTS = (
    PROCESSED_DATA_DIR /
    "autoencoder_predictions.csv"
)

FINAL_DATASET = (
    PROCESSED_DATA_DIR /
    "final_dashboard_dataset.csv"
)

# ==========================================================
# Model Paths
# ==========================================================

ISOLATION_MODEL = MODELS_DIR / "isolation_forest.pkl"

ISOLATION_SCALER = MODELS_DIR / "scaler.pkl"

AUTOENCODER_MODEL = MODELS_DIR / "autoencoder.keras"

AUTOENCODER_SCALER = (
    MODELS_DIR /
    "autoencoder_scaler.pkl"
)

THRESHOLD_FILE = MODELS_DIR / "threshold.pkl"

SUPERVISED_MODEL = MODELS_DIR / "supervised_model.pkl"

# ==========================================================
# Reports
# ==========================================================

MODEL_COMPARISON = (
    REPORTS_DIR /
    "model_comparison.csv"
)

FRAUD_ALERTS = (
    REPORTS_DIR /
    "fraud_alerts.csv"
)

DASHBOARD_KPIS = (
    REPORTS_DIR /
    "dashboard_kpis.csv"
)

DEPLOYMENT_RESULTS = (
    REPORTS_DIR /
    "deployment_test_results.csv"
)

# ==========================================================
# Dashboard Information
# ==========================================================

PROJECT_NAME = (
    "AI-Powered Financial Fraud Detection "
    "and Risk Analysis System"
)

SHORT_NAME = "AI Fraud Intelligence Center"

VERSION = "1.0.0"

AUTHOR = "Gurrala Nikhil Reddy"

# ==========================================================
# Theme
# ==========================================================

DEFAULT_THEME = "dark"

FONT_FAMILY = "Inter"

# ==========================================================
# Colors
# ==========================================================

COLORS = {

    "background": "#0F172A",

    "surface": "#1E293B",

    "surface_light": "#334155",

    "primary": "#2563EB",

    "secondary": "#3B82F6",

    "success": "#16A34A",

    "warning": "#F59E0B",

    "danger": "#DC2626",

    "text": "#F8FAFC",

    "text_secondary": "#CBD5E1",

    "border": "#475569",

    "chart1": "#2563EB",

    "chart2": "#16A34A",

    "chart3": "#F59E0B",

    "chart4": "#DC2626"

}

# ==========================================================
# KPI Names
# ==========================================================

KPI_NAMES = [

    "Total Transactions",

    "Fraud Alerts",

    "High Risk Transactions",

    "Safe Transactions"

]

# ==========================================================
# Risk Levels
# ==========================================================

RISK_LEVELS = {

    "Low": {
        "color": COLORS["success"],
        "icon": "🟢"
    },

    "Medium": {
        "color": COLORS["warning"],
        "icon": "🟡"
    },

    "High": {
        "color": COLORS["danger"],
        "icon": "🔴"
    }

}

# ==========================================================
# Sidebar
# ==========================================================

SIDEBAR_MENU = [

    ("🏠", "Home"),

    ("📊", "Analytics"),

    ("🤖", "Live Prediction"),

    ("🚨", "Fraud Alerts"),

    ("📑", "Reports"),

    ("📈", "Performance"),

    ("ℹ️", "About")

]

# ==========================================================
# Application Settings
# ==========================================================

MAX_UPLOAD_SIZE_MB = 100

DEFAULT_PAGE = "Home"

REFRESH_INTERVAL = 30

ENABLE_ANIMATIONS = True

ENABLE_THEME_SWITCH = True

# ==========================================================
# Plotly Theme
# ==========================================================

PLOTLY_TEMPLATE = "plotly_dark"

# ==========================================================
# Utility Functions
# ==========================================================

def model_exists() -> bool:
    """
    Check whether all trained models exist.
    """
    return all([
        ISOLATION_MODEL.exists(),
        AUTOENCODER_MODEL.exists(),
        ISOLATION_SCALER.exists(),
        AUTOENCODER_SCALER.exists(),
        THRESHOLD_FILE.exists()
    ])


def data_exists() -> bool:
    """
    Check whether processed datasets exist.
    """
    return FINAL_DATASET.exists()


def reports_exist() -> bool:
    """
    Check whether report files exist.
    """
    return all([
        MODEL_COMPARISON.exists(),
        FRAUD_ALERTS.exists(),
        DASHBOARD_KPIS.exists()
    ])


if __name__ == "__main__":

    print("=" * 60)
    print(PROJECT_NAME)
    print("=" * 60)

    print(f"Models Available   : {model_exists()}")
    print(f"Dataset Available  : {data_exists()}")
    print(f"Reports Available  : {reports_exist()}")