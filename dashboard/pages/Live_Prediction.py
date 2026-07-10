"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
Live Prediction Dashboard

Real-time fraud prediction for single transactions
and batch CSV analysis.

Author  : Gurrala Nikhil Reddy
Version : 2.0.0
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
import numpy as np
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
from components.model_health import render_model_health

# ==========================================================
# Backend
# ==========================================================
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
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="Live Prediction",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.helpers import load_css

load_css()

# ==========================================================
# Backend Engines
# ==========================================================
prediction_engine = get_engine()
risk_engine = get_risk_engine()

# ==========================================================
# Cache Sample Transactions Dataset
# ==========================================================
@st.cache_data(show_spinner=False)
def load_sample_dataset() -> pd.DataFrame:
    try:
        from utils.load_data import get_loader
        return get_loader().dashboard()
    except Exception as e:
        logger.error(f"Error loading sample dataset: {e}")
        return pd.DataFrame()

# ==========================================================
# Session State Initialization
# ==========================================================
if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

if "live_amount" not in st.session_state:
    st.session_state["live_amount"] = 1000.0

if "live_time" not in st.session_state:
    st.session_state["live_time"] = 0.0

for i in range(1, 29):
    key = f"live_v{i}"
    if key not in st.session_state:
        st.session_state[key] = 0.0

# ==========================================================
# Render Inputs Form
# ==========================================================
def render_input_form() -> dict:
    """
    Manual transaction form with session state bindings.
    """
    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Transaction Details</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:
        amount = st.number_input(
            "Transaction Amount ($)",
            min_value=0.0,
            key="live_amount"
        )

        time = st.number_input(
            "Transaction Time (Seconds)",
            min_value=0.0,
            key="live_time"
        )

        merchant = st.text_input(
            "Merchant (Cosmetic)",
            "Amazon",
        )

        category = st.selectbox(
            "Category (Cosmetic)",
            [
                "Shopping",
                "Food",
                "Travel",
                "Bills",
                "Transfer",
                "Other",
            ],
        )

    with right:
        location = st.text_input(
            "Location (Cosmetic)",
            "Hyderabad",
        )

        device = st.selectbox(
            "Device (Cosmetic)",
            [
                "Mobile",
                "Desktop",
                "POS",
            ],
        )

        card = st.selectbox(
            "Card Type (Cosmetic)",
            [
                "Debit",
                "Credit",
            ],
        )

    # Advanced PCA Features
    st.write("")
    with st.expander("🧠 Advanced Model Features (PCA Components V1 - V28)"):
        st.info("These 28 variables represent mathematical projections of the transaction. Modify them as needed or leave them at their defaults.")
        
        pca_cols = st.columns(4)
        pca_values = {}
        for i in range(1, 29):
            col_idx = (i - 1) % 4
            with pca_cols[col_idx]:
                pca_values[f"V{i}"] = st.number_input(
                    f"V{i}",
                    format="%.6f",
                    key=f"live_v{i}"
                )

    transaction = {
        "Amount": amount,
        "Time": time,
        "Merchant": merchant,
        "Category": category,
        "Location": location,
        "Device": device,
        "Card": card,
    }
    # Add PCA values
    transaction.update(pca_values)
    return transaction

# ==========================================================
# Prediction Helpers
# ==========================================================
def build_dataframe(transaction: dict) -> pd.DataFrame:
    """
    Convert transaction into prediction dataframe.
    """
    data = {
        "Time": [transaction["Time"]],
        "Amount": [transaction["Amount"]]
    }
    # Add PCA components
    for i in range(1, 29):
        col = f"V{i}"
        if col in transaction:
            data[col] = [transaction[col]]
            
    return pd.DataFrame(data)

def run_prediction(transaction: dict):
    """
    Execute AI prediction pipeline.
    """
    dataframe = build_dataframe(transaction)
    prediction = prediction_engine.predict_transaction(dataframe)
    
    report = risk_engine.analyze(
        isolation_prediction=int(prediction.get("Isolation Prediction", 0)),
        autoencoder_prediction=int(prediction.get("AutoEncoder Prediction", 0)),
        supervised_prediction=int(prediction.get("Supervised Prediction", 0)),
        confidence=float(prediction.get("Confidence", 0.0)),
    )

    return prediction, report

# ==========================================================
# Render Prediction Result
# ==========================================================
def render_prediction_result(prediction: dict, risk: dict) -> None:
    """
    Display AI prediction.
    """
    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            <span class="header-title-text" style="font-size: 24px;">AI Decision</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    final_prediction = prediction.get("Final Prediction", "Unknown")
    confidence = prediction.get("Confidence", 0)
    
    risk_score = risk.get("Risk Score", 0)
    risk_level = risk.get("Risk Level", "Unknown")
    priority = risk.get("Priority", "-")
    recommendation = risk.get("Recommendation", "No recommendation.")
    explanation = risk.get("Explanation", "No explanation available.")

    if str(final_prediction).lower() == "fraud":
        st.error("## 🔴 FRAUD ALERT GENERATED")
    else:
        st.success("## 🟢 SAFE TRANSACTION")

    left, right = st.columns(2)

    with left:
        st.metric("Confidence", f"{confidence:.2f}%")
        st.metric("Risk Score", f"{risk_score:.2f}")
        st.metric("Alert Priority", priority)

    with right:
        st.metric("Risk Level", risk_level)
        st.info(f"**Recommendation:** {recommendation}")

    st.markdown("### 📝 Explanation")
    st.write(explanation)
    
    st.write("")
    with st.expander("🔍 Model Breakdown Details"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Isolation Forest Anomaly", "Yes (Fraud)" if prediction.get("Isolation Prediction") == 1 else "No (Safe)")
            st.caption(f"Score: {prediction.get('Isolation Score', 0.0):.4f}")
        with col2:
            st.metric("AutoEncoder Anomaly", "Yes (Fraud)" if prediction.get("AutoEncoder Prediction") == 1 else "No (Safe)")
            st.caption(f"Reconstruction Error: {prediction.get('Reconstruction Error', 0.0):.4f}")
        with col3:
            st.metric("Supervised Classifier", "Yes (Fraud)" if prediction.get("Supervised Prediction") == 1 else "No (Safe)")
            st.caption(f"Probability: {prediction.get('Supervised Probability', 0.0):.4f}")
            
    st.divider()

# ==========================================================
# Model Info Component
# ==========================================================
def render_model_information() -> None:
    """
    Display model status.
    """
    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="M12 6v6l4 2"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Model Information</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    model_info = prediction_engine.model_summary()
    render_model_health(model_info)
    st.divider()

# ==========================================================
# Prediction History Component
# ==========================================================
def render_prediction_history() -> None:
    """
    Display session prediction history.
    """
    st.markdown(
        """
        <div class="header-container">
            <svg class="header-icon" viewBox="0 0 24 24"><line x1="8" x2="21" y1="6" y2="6"/><line x1="8" x2="21" y1="12" y2="12"/><line x1="8" x2="21" y1="18" y2="18"/><line x1="3" x2="3.01" y1="6" y2="6"/><line x1="3" x2="3.01" y1="12" y2="12"/><line x1="3" x2="3.01" y1="18" y2="18"/></svg>
            <span class="header-title-text" style="font-size: 24px;">Recent Predictions</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    history = st.session_state.prediction_history

    if not history:
        st.info("No predictions in the history yet.")
        return

    history_df = pd.DataFrame(history)
    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True,
    )
    st.divider()

# ==========================================================
# Main Layout
# ==========================================================
def main() -> None:
    render_sidebar()

    render_header(
        title="Live Prediction",
        subtitle="Real-Time Transaction Risk Evaluation"
    )

    tab1, tab2 = st.tabs(["💳 Single Transaction", "📥 Batch CSV Prediction"])

    # ------------------
    # Tab 1: Single Prediction
    # ------------------
    with tab1:
        df_samples = load_sample_dataset()
        
        sample_options = ["None (Manual Entry)"]
        sample_records = []

        if not df_samples.empty:
            # Filter some safe and some fraud transactions to load as templates
            safe_col = "Class" if "Class" in df_samples.columns else ("Final_Prediction" if "Final_Prediction" in df_samples.columns else None)
            if safe_col:
                safe_df = df_samples[df_samples[safe_col] == 0].head(5)
                fraud_df = df_samples[df_samples[safe_col] == 1].head(5)
            else:
                safe_df = df_samples.head(5)
                fraud_df = df_samples.tail(5)

            for i, row in enumerate(safe_df.itertuples(index=False)):
                sample_options.append(f"Safe Transaction Template {i+1} (Amount: ${row.Amount:.2f})")
                sample_records.append(row)
            for i, row in enumerate(fraud_df.itertuples(index=False)):
                sample_options.append(f"Fraud Transaction Template {i+1} (Amount: ${row.Amount:.2f})")
                sample_records.append(row)

        def on_sample_change():
            sel = st.session_state.selected_sample_dropdown
            if sel == "None (Manual Entry)":
                st.session_state["live_amount"] = 1000.0
                st.session_state["live_time"] = 0.0
                for i in range(1, 29):
                    st.session_state[f"live_v{i}"] = 0.0
            else:
                idx = sample_options.index(sel) - 1
                record = sample_records[idx]
                st.session_state["live_amount"] = float(record.Amount)
                st.session_state["live_time"] = float(record.Time)
                for i in range(1, 29):
                    val = getattr(record, f"V{i}", 0.0)
                    st.session_state[f"live_v{i}"] = float(val)

        st.selectbox(
            "💡 Load Sample Transaction Template",
            sample_options,
            index=0,
            key="selected_sample_dropdown",
            on_change=on_sample_change
        )
        st.write("")

        transaction = render_input_form()

        if st.button("🚀 Predict Transaction", use_container_width=True):
            try:
                prediction, report = run_prediction(transaction)

                render_prediction_result(
                    prediction,
                    {
                        "Risk Score": report.score,
                        "Risk Level": report.level,
                        "Priority": report.priority,
                        "Recommendation": report.recommendation,
                        "Explanation": report.explanation,
                    },
                )

                st.session_state.prediction_history.insert(
                    0,
                    {
                        "Amount": transaction["Amount"],
                        "Prediction": prediction.get("Final Prediction", "Unknown"),
                        "Confidence": round(report.confidence, 2),
                        "Risk": report.level,
                        "Priority": report.priority,
                        "Recommendation": report.recommendation
                    },
                )

            except Exception as error:
                logger.exception(error)
                st.error(f"Prediction failed.\n\n{error}")

        render_prediction_history()
        render_model_information()

    # ------------------
    # Tab 2: Batch CSV Upload
    # ------------------
    with tab2:
        st.markdown(
            """
            <div class="header-container">
                <svg class="header-icon" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
                <span class="header-title-text" style="font-size: 24px;">Batch CSV Prediction</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("Upload a CSV file containing transactions. The file must contain at least `Time` and `Amount` columns. PCA variables `V1`-`V28` will be automatically populated with `0.0` if not present.")
        
        uploaded_file = st.file_uploader("Upload CSV transaction list", type=["csv"])
        
        if uploaded_file is not None:
            try:
                batch_df = pd.read_csv(uploaded_file)
                st.success(f"File loaded successfully: {len(batch_df)} records found.")
                
                # Check minimum required columns
                if "Time" not in batch_df.columns or "Amount" not in batch_df.columns:
                    st.error("Uploaded CSV must contain 'Time' and 'Amount' columns.")
                else:
                    st.write("### Data Preview")
                    st.dataframe(batch_df.head(5), use_container_width=True)
                    
                    if st.button("🚀 Run Batch Inference", use_container_width=True):
                        with st.spinner("Executing machine learning predictions..."):
                            # Run prediction engine
                            results = prediction_engine.predict_dataframe(batch_df)
                            
                            # Run risk engine
                            reports = risk_engine.analyze_batch(results)
                            risk_df = risk_engine.export_dataframe(reports)
                            
                            # Combine dataframes
                            final_df = pd.concat([results.reset_index(drop=True), risk_df.reset_index(drop=True)], axis=1)
                            
                            # Calculate metrics
                            metrics = risk_engine.dashboard_metrics(reports)
                            
                            st.markdown("### 📊 Metrics Summary")
                            m1, m2, m3, m4 = st.columns(4)
                            m1.metric("Total Rows Processed", len(final_df))
                            m2.metric("Fraud Alerts", metrics.get("Alerts", 0))
                            m3.metric("Critical Alerts", metrics.get("Critical", 0))
                            m4.metric("High Alerts", metrics.get("High", 0))
                            
                            st.markdown("### 📋 Prediction Results Preview")
                            disp_cols = ['Time', 'Amount', 'Final_Prediction', 'Confidence', 'Risk Level', 'Risk Score', 'Priority', 'Recommendation']
                            st.dataframe(final_df[disp_cols].head(10), use_container_width=True)
                            
                            # Convert to CSV for download
                            csv_data = final_df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="📥 Download Complete Prediction Report (CSV)",
                                data=csv_data,
                                file_name="batch_predictions_report.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
            except Exception as e:
                logger.error(f"Batch prediction error: {e}")
                st.error(f"Failed to process CSV file. Error: {e}")

    render_footer()

if __name__ == "__main__":
    main()