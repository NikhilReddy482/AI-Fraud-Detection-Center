"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
Prediction Engine

Enterprise inference engine for fraud detection using
Isolation Forest and AutoEncoder models.

Author  : Gurrala Nikhil Reddy
Version : 1.0.0
===========================================================
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd

from utils.load_models import initialize_dashboard

# ==========================================================
# Logger
# ==========================================================

logger = logging.getLogger(__name__)

if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s"
    )

# ==========================================================
# Prediction Engine
# ==========================================================


class PredictionEngine:
    """
    Enterprise ML Prediction Engine.

    Responsibilities
    ----------------
    • Validate input
    • Prepare features
    • Run Isolation Forest
    • Run AutoEncoder
    • Generate unified prediction
    """

    def __init__(self):

        state = initialize_dashboard()

        if not state["success"]:

            raise RuntimeError(
                state["health"]["message"]
            )

        self.models = state["models"]

        self.isolation_model = (
            self.models["isolation_model"]
        )

        self.isolation_scaler = (
            self.models["isolation_scaler"]
        )

        self.autoencoder_model = (
            self.models["autoencoder_model"]
        )

        self.autoencoder_scaler = (
            self.models["autoencoder_scaler"]
        )

        self.threshold = (
            self.models["threshold"]
        )

        self.supervised_model = (
            self.models["supervised_model"]
        )

        logger.info("Prediction engine initialized.")

# ==========================================================
# Validation
# ==========================================================

    @staticmethod
    def validate_dataframe(
        df: pd.DataFrame
    ) -> None:
        """
        Validate dataframe before prediction.
        """

        if df.empty:

            raise ValueError(
                "Input dataframe is empty."
            )

        if df.isna().sum().sum() > 0:

            raise ValueError(
                "Input contains missing values."
            )

# ==========================================================
# Numeric Features
# ==========================================================

    @staticmethod
    def numeric_features(
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Keep only numeric columns.
        """

        numeric = df.select_dtypes(
            include=np.number
        )

        if numeric.empty:

            raise ValueError(
                "No numeric features found."
            )

        return numeric

# ==========================================================
# Feature Preparation
# ==========================================================

    def prepare_raw_features(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Prepare raw unscaled features for prediction.
        """
        self.validate_dataframe(df)

        df_prepared = df.copy()

        # 1. Calculate Time-based features if missing
        if "Hour" not in df_prepared.columns and "Time" in df_prepared.columns:
            df_prepared["Hour"] = (df_prepared["Time"] % 86400) // 3600

        if "Scaled_Amount" not in df_prepared.columns and "Amount" in df_prepared.columns:
            # Using scaler statistics (mean: 88.4726873, std: 250.398996)
            df_prepared["Scaled_Amount"] = (df_prepared["Amount"] - 88.4726873) / 250.398996

        # 2. Add one-hot encoded Time Period columns if missing
        if "Time_Period_Evening" not in df_prepared.columns:
            hour = df_prepared["Hour"] if "Hour" in df_prepared.columns else (df_prepared["Time"] % 86400) // 3600
            df_prepared["Time_Period_Evening"] = ((hour >= 17) & (hour < 21)).astype(float)

        if "Time_Period_Morning" not in df_prepared.columns:
            hour = df_prepared["Hour"] if "Hour" in df_prepared.columns else (df_prepared["Time"] % 86400) // 3600
            df_prepared["Time_Period_Morning"] = ((hour >= 5) & (hour < 12)).astype(float)

        if "Time_Period_Night" not in df_prepared.columns:
            hour = df_prepared["Hour"] if "Hour" in df_prepared.columns else (df_prepared["Time"] % 86400) // 3600
            df_prepared["Time_Period_Night"] = ((hour >= 21) | (hour < 5)).astype(float)

        # 3. Add default PCA features if missing (e.g. for manual single transaction prediction)
        for i in range(1, 29):
            col = f"V{i}"
            if col not in df_prepared.columns:
                df_prepared[col] = 0.0

        # 4. Filter and order the exact 35 columns
        expected_cols = [
            'Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
            'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20',
            'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28',
            'Amount', 'Scaled_Amount', 'Hour',
            'Time_Period_Evening', 'Time_Period_Morning', 'Time_Period_Night'
        ]

        return df_prepared[expected_cols]

    def prepare_features(
        self,
        df: pd.DataFrame
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Prepare and scale features for both models.
        """
        features = self.prepare_raw_features(df)

        isolation = (
            self.isolation_scaler
            .transform(features)
        )

        autoencoder = (
            self.autoencoder_scaler
            .transform(features)
        )

        return isolation, autoencoder

# ==========================================================
# Model Information
# ==========================================================

    def information(self) -> dict:
        """
        Information about loaded models.
        """

        return {

            "Isolation Forest":

                type(
                    self.isolation_model
                ).__name__,

            "AutoEncoder":

                type(
                    self.autoencoder_model
                ).__name__ if self.autoencoder_model is not None else "Not Loaded (TensorFlow Unsupported)",

            "Supervised Classifier":

                type(
                    self.supervised_model
                ).__name__,

            "Threshold":

                float(self.threshold)

        }

# ==========================================================
# Health
# ==========================================================

    def health(self):

        return {

            "Loaded": True,

            "Models": self.information()

        }


# ==========================================================
# Singleton
# ==========================================================

# ==========================================================
# Isolation Forest Prediction
# ==========================================================

    def predict_isolation(
        self,
        features: np.ndarray
    ) -> dict:
        """
        Run Isolation Forest inference.
        """

        prediction = self.isolation_model.predict(features)

        scores = self.isolation_model.decision_function(features)

        prediction = np.where(
            prediction == -1,
            1,
            0
        )

        return {

            "prediction": prediction,

            "score": scores

        }


# ==========================================================
# AutoEncoder Prediction
# ==========================================================

    def predict_autoencoder(
        self,
        features: np.ndarray
    ) -> dict:
        """
        Run AutoEncoder inference.
        """
        if self.autoencoder_model is None:
            # Fallback when TensorFlow is not installed
            zeros_pred = np.zeros(len(features), dtype=int)
            zeros_err = np.zeros(len(features), dtype=float)
            return {
                "prediction": zeros_pred,
                "reconstruction_error": zeros_err
            }

        reconstruction = self.autoencoder_model.predict(

            features,

            verbose=0

        )

        error = np.mean(

            np.square(

                features -

                reconstruction

            ),

            axis=1,

        )

        prediction = (

            error >

            self.threshold

        ).astype(int)

        return {

            "prediction": prediction,

            "reconstruction_error": error

        }


# ==========================================================
# Confidence Score
# ==========================================================

    @staticmethod
    def confidence_score(
        anomaly_score: np.ndarray,
        reconstruction_error: np.ndarray,
        supervised_probs: np.ndarray,
    ) -> np.ndarray:
        """
        Estimate confidence score.
        """

        anomaly = np.abs(anomaly_score)

        anomaly = anomaly / (
            anomaly.max() + 1e-8
        )

        reconstruction = (

            reconstruction_error /

            (

                reconstruction_error.max()

                + 1e-8

            )

        )

        # Average the three models: outlier score, reconstruction anomaly, and supervised probability
        confidence = (

            anomaly +

            reconstruction +

            supervised_probs

        ) / 3

        confidence = confidence * 100

        confidence = np.clip(

            confidence,

            0,

            100

        )

        return np.round(

            confidence,

            2

        )


# ==========================================================
# Batch Prediction
# ==========================================================

    def batch_predict(
        self,
        df: pd.DataFrame
    ) -> dict:
        """
        Perform model inference on
        an entire dataframe.
        """
        raw_features = self.prepare_raw_features(df)

        isolation_features, auto_features = (

            self.prepare_features(df)

        )

        isolation = self.predict_isolation(

            isolation_features

        )

        autoencoder = self.predict_autoencoder(

            auto_features

        )

        supervised_probs = self.supervised_model.predict_proba(raw_features)[:, 1]
        supervised_pred = (supervised_probs > 0.5).astype(int)

        confidence = self.confidence_score(

            isolation["score"],

            autoencoder["reconstruction_error"],

            supervised_probs

        )

        return {

            "Isolation":

                isolation,

            "AutoEncoder":

                autoencoder,

            "Supervised": {

                "prediction": supervised_pred,

                "probability": supervised_probs

            },

            "Confidence":

                confidence

        }


# ==========================================================
# Single Prediction
# ==========================================================

    def single_predict(
        self,
        row: pd.DataFrame
    ) -> dict:
        """
        Predict one transaction.
        """

        result = self.batch_predict(row)

        return {

            "Isolation":

                int(

                    result["Isolation"]

                    ["prediction"][0]

                ),

            "Isolation Score":

                float(

                    result["Isolation"]

                    ["score"][0]

                ),

            "AutoEncoder":

                int(

                    result["AutoEncoder"]

                    ["prediction"][0]

                ),

            "Reconstruction Error":

                float(

                    result["AutoEncoder"]

                    ["reconstruction_error"][0]

                ),

            "Supervised":

                int(

                    result["Supervised"]

                    ["prediction"][0]

                ),

            "Supervised Probability":

                float(

                    result["Supervised"]

                    ["probability"][0]

                ),

            "Confidence":

                float(

                    result["Confidence"][0]

                )

        }
# ==========================================================
# Ensemble Decision
# ==========================================================

    @staticmethod
    def ensemble_prediction(
        isolation_prediction: np.ndarray,
        autoencoder_prediction: np.ndarray,
        supervised_prediction: np.ndarray,
    ) -> np.ndarray:
        """
        Combine predictions from all three models.

        Rule:
        -----
        If any of the three models flags fraud,
        mark the transaction as fraud.
        """

        return np.logical_or(
            np.logical_or(isolation_prediction, autoencoder_prediction),
            supervised_prediction
        ).astype(int)


# ==========================================================
# Predict DataFrame
# ==========================================================

    def predict_dataframe(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Run complete inference pipeline.
        """

        result = self.batch_predict(df)

        isolation = result["Isolation"]

        autoencoder = result["AutoEncoder"]

        supervised = result["Supervised"]

        confidence = result["Confidence"]

        final_prediction = self.ensemble_prediction(

            isolation["prediction"],

            autoencoder["prediction"],

            supervised["prediction"]

        )

        output = df.copy()

        output["Isolation_Prediction"] = (

            isolation["prediction"]

        )

        output["Isolation_Score"] = (

            np.round(
                isolation["score"],
                4
            )

        )

        output["AutoEncoder_Prediction"] = (

            autoencoder["prediction"]

        )

        output["Reconstruction_Error"] = (

            np.round(
                autoencoder[
                    "reconstruction_error"
                ],
                6
            )

        )

        output["Supervised_Prediction"] = (

            supervised["prediction"]

        )

        output["Supervised_Probability"] = (

            np.round(
                supervised["probability"],
                6
            )

        )

        output["Confidence"] = confidence

        output["Final_Prediction"] = (

            final_prediction

        )

        return output


# ==========================================================
# Prediction Summary
# ==========================================================

    @staticmethod
    def prediction_summary(
        df: pd.DataFrame
    ) -> dict:
        """
        Summary of predictions.
        """

        if "Final_Prediction" not in df.columns:

            return {}

        fraud = int(

            (df["Final_Prediction"] == 1)

            .sum()

        )

        safe = int(

            (df["Final_Prediction"] == 0)

            .sum()

        )

        total = len(df)

        fraud_rate = round(

            fraud * 100 / total,

            2

        ) if total else 0

        return {

            "Transactions": total,

            "Fraud": fraud,

            "Safe": safe,

            "Fraud Rate": fraud_rate

        }


# ==========================================================
# Streamlit Prediction
# ==========================================================

    def predict_for_dashboard(
        self,
        df: pd.DataFrame
    ) -> dict:
        """
        Complete prediction response
        used by Streamlit pages.
        """

        predictions = self.predict_dataframe(df)

        summary = self.prediction_summary(
            predictions
        )

        return {

            "predictions": predictions,

            "summary": summary,

            "status": "Success"

        }


# ==========================================================
# Single Transaction API
# ==========================================================

    def predict_transaction(
        self,
        row: pd.DataFrame
    ) -> dict:
        """
        Predict a single transaction
        with complete output.
        """

        prediction = self.predict_dataframe(
            row
        )

        record = prediction.iloc[0]

        return {

            "Isolation Prediction":

                int(
                    record[
                        "Isolation_Prediction"
                    ]
                ),

            "Isolation Score":

                float(
                    record[
                        "Isolation_Score"
                    ]
                ),

            "AutoEncoder Prediction":

                int(
                    record[
                        "AutoEncoder_Prediction"
                    ]
                ),

            "Reconstruction Error":

                float(
                    record[
                        "Reconstruction_Error"
                    ]
                ),

            "Supervised Prediction":

                int(
                    record[
                        "Supervised_Prediction"
                    ]
                ),

            "Supervised Probability":

                float(
                    record[
                        "Supervised_Probability"
                    ]
                ),

            "Confidence":

                float(
                    record[
                        "Confidence"
                    ]
                ),

            "Final Prediction":

                "Fraud"

                if record[
                    "Final_Prediction"
                ]

                else "Safe"

        }


# ==========================================================
# Model Information
# ==========================================================

    def model_summary(self) -> dict:
        """
        Model metadata.
        """

        return {

            "Isolation Forest":

                type(
                    self.isolation_model
                ).__name__,

            "AutoEncoder":

                type(
                    self.autoencoder_model
                ).__name__,

            "Supervised Classifier":

                type(
                    self.supervised_model
                ).__name__,

            "Threshold":

                float(self.threshold),

            "Status":

                "Ready"

        }


# ==========================================================
# Version
# ==========================================================

    @staticmethod
    def version() -> str:

        return "1.0.0"
# ==========================================================
# Singleton Instance
# ==========================================================

engine = PredictionEngine()


def get_engine() -> PredictionEngine:
    """
    Return singleton prediction engine.
    """
    return engine


# ==========================================================
# Startup Test
# ==========================================================

if __name__ == "__main__":

    logger.info("=" * 60)
    logger.info("Prediction Engine")
    logger.info("=" * 60)

    engine = PredictionEngine()

    logger.info(engine.model_summary())

    logger.info("=" * 60)