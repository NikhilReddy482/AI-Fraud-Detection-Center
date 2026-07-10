"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
Model Loader

Loads all trained Machine Learning models used by
the Enterprise Fraud Detection Dashboard.

Author  : Gurrala Nikhil Reddy
Version : 1.0.0
===========================================================
"""

from __future__ import annotations

from pathlib import Path
import joblib
import streamlit as st

TENSORFLOW_AVAILABLE = True
try:
    import tensorflow
except ImportError:
    TENSORFLOW_AVAILABLE = False

from utils.config import (
    ISOLATION_MODEL,
    ISOLATION_SCALER,
    AUTOENCODER_MODEL,
    AUTOENCODER_SCALER,
    THRESHOLD_FILE,
    SUPERVISED_MODEL,
)

# ==========================================================
# Model Validation
# ==========================================================


def validate_model_files() -> tuple[bool, list[str]]:
    """
    Check whether every required model file exists.

    Returns
    -------
    (bool, list)
    """

    missing = []

    required = {

        "Isolation Forest": ISOLATION_MODEL,

        "Isolation Scaler": ISOLATION_SCALER,

        "AutoEncoder": AUTOENCODER_MODEL,

        "AutoEncoder Scaler": AUTOENCODER_SCALER,

        "Threshold": THRESHOLD_FILE,

        "Supervised Model": SUPERVISED_MODEL,

    }

    for name, file in required.items():

        if not Path(file).exists():

            missing.append(name)

    return len(missing) == 0, missing


# ==========================================================
# Cached Loader
# ==========================================================


@st.cache_resource(show_spinner=False)
def load_all_models():
    """
    Load every trained model only once.

    Returns
    -------
    dict
    """

    ok, missing = validate_model_files()

    if not ok:

        raise FileNotFoundError(

            f"Missing model files : {', '.join(missing)}"

        )

    models = {

        "isolation_model":

            joblib.load(ISOLATION_MODEL),

        "isolation_scaler":

            joblib.load(ISOLATION_SCALER),

        "autoencoder_model":

            load_autoencoder(),

        "autoencoder_scaler":

            joblib.load(AUTOENCODER_SCALER),

        "threshold":

            joblib.load(THRESHOLD_FILE),

        "supervised_model":

            joblib.load(SUPERVISED_MODEL),

    }

    return models


# ==========================================================
# Individual Loaders
# ==========================================================


@st.cache_resource(show_spinner=False)
def load_isolation_model():

    return joblib.load(ISOLATION_MODEL)


@st.cache_resource(show_spinner=False)
def load_autoencoder():

    if not TENSORFLOW_AVAILABLE:
        return None

    from tensorflow.keras.models import load_model
    return load_model(AUTOENCODER_MODEL)


@st.cache_resource(show_spinner=False)
def load_isolation_scaler():

    return joblib.load(ISOLATION_SCALER)


@st.cache_resource(show_spinner=False)
def load_autoencoder_scaler():

    return joblib.load(AUTOENCODER_SCALER)


@st.cache_resource(show_spinner=False)
def load_threshold():

    return joblib.load(THRESHOLD_FILE)


# ==========================================================
# Model Information
# ==========================================================


def model_information() -> dict:
    """
    Dashboard information.
    """

    return {

        "Isolation Forest": {

            "Algorithm":

                "Isolation Forest",

            "Type":

                "Unsupervised",

            "Purpose":

                "Anomaly Detection",

        },

        "AutoEncoder": {

            "Algorithm":

                "Deep Learning",

            "Type":

                "Neural Network",

            "Purpose":

                "Reconstruction Error Detection",

        },

        "Supervised Classifier": {

            "Algorithm":

                "HistGradientBoosting",

            "Type":

                "Supervised Classifier",

            "Purpose":

                "Known Fraud Pattern Recognition",

        }

    }


# ==========================================================
# Dashboard Status
# ==========================================================


def dashboard_status() -> dict:
    """
    Return current model status.
    """

    ok, missing = validate_model_files()

    return {

        "ready": ok,

        "missing": missing,

        "total_models": 6,

        "loaded_models":

            6 - len(missing)

    }


# ==========================================================
# Health Check
# ==========================================================


def health_check():

    status = dashboard_status()

    if status["ready"]:

        return {

            "status": "Healthy",

            "icon": "🟢",

            "message":

                "All models successfully loaded."

        }

    return {

        "status": "Error",

        "icon": "🔴",

        "message":

            "Some model files are missing."

    }


# ==========================================================
# Dashboard Startup
# ==========================================================


def initialize_dashboard():
    """
    Startup initialization.
    """

    try:

        models = load_all_models()

        health = health_check()

        return {

            "success": True,

            "models": models,

            "health": health

        }

    except Exception as error:

        return {

            "success": False,

            "models": None,

            "health": {

                "status": "Failed",

                "icon": "🔴",

                "message": str(error)

            }

        }


# ==========================================================
# Main Test
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print("Fraud Detection Dashboard")

    print("=" * 60)

    status = initialize_dashboard()

    print(status["health"])