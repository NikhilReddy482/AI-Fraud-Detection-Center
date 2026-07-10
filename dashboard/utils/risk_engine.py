"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
Risk Engine

Business decision layer for fraud detection.
Converts ML predictions into enterprise risk scores,
risk levels, priorities, and recommendations.

Author  : Gurrala Nikhil Reddy
Version : 1.0.0
===========================================================
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np

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
# Risk Thresholds
# ==========================================================

CRITICAL_THRESHOLD = 90
HIGH_THRESHOLD = 75
MEDIUM_THRESHOLD = 50
LOW_THRESHOLD = 25

# ==========================================================
# Risk Metadata
# ==========================================================

RISK_LEVELS = {

    "Critical": {
        "priority": "P1",
        "color": "#DC2626",
        "badge": "🔴",
    },

    "High": {
        "priority": "P2",
        "color": "#F97316",
        "badge": "🟠",
    },

    "Medium": {
        "priority": "P3",
        "color": "#EAB308",
        "badge": "🟡",
    },

    "Low": {
        "priority": "P4",
        "color": "#22C55E",
        "badge": "🟢",
    }

}

# ==========================================================
# Recommendation Mapping
# ==========================================================

RECOMMENDATIONS = {

    "Critical":
        "Block transaction immediately and escalate to the Fraud Operations Team.",

    "High":
        "Temporarily hold the transaction and perform manual verification.",

    "Medium":
        "Request additional customer authentication before approval.",

    "Low":
        "Approve transaction and continue routine monitoring."

}

# ==========================================================
# Risk Report
# ==========================================================

@dataclass(slots=True)
class RiskReport:

    score: float

    level: str

    priority: str

    recommendation: str

    color: str

    badge: str

    confidence: float

    explanation: str

# ==========================================================
# Risk Engine
# ==========================================================

class RiskEngine:
    """
    Enterprise business risk engine.

    Responsibilities
    ----------------
    • Risk score calculation
    • Risk level assignment
    • Priority assignment
    • Recommendation generation
    • Dashboard formatting
    """

    def __init__(self) -> None:

        logger.info(
            "Risk engine initialized."
        )

# ==========================================================
# Risk Level
# ==========================================================

    @staticmethod
    def risk_level(
        score: float
    ) -> str:
        """
        Determine risk level from score.
        """

        if score >= CRITICAL_THRESHOLD:
            return "Critical"

        if score >= HIGH_THRESHOLD:
            return "High"

        if score >= MEDIUM_THRESHOLD:
            return "Medium"

        return "Low"

# ==========================================================
# Metadata
# ==========================================================

    @staticmethod
    def metadata(
        level: str
    ) -> dict:

        return RISK_LEVELS[level]

# ==========================================================
# Recommendation
# ==========================================================

    @staticmethod
    def recommendation(
        level: str
    ) -> str:

        return RECOMMENDATIONS[level]
# ==========================================================
# Risk Score
# ==========================================================

    @staticmethod
    def calculate_score(
        confidence: float,
        isolation_prediction: int,
        autoencoder_prediction: int,
        supervised_prediction: int,
    ) -> float:
        """
        Calculate enterprise risk score (0-100).

        Isolation Forest contributes 30%
        AutoEncoder contributes 30%
        Supervised Classifier contributes 30%
        Confidence contributes 10%
        """

        score = confidence * 0.10

        if isolation_prediction:
            score += 30

        if autoencoder_prediction:
            score += 30

        if supervised_prediction:
            score += 30

        return round(min(score, 100.0), 2)


# ==========================================================
# Business Explanation
# ==========================================================

    @staticmethod
    def explanation(
        isolation_prediction: int,
        autoencoder_prediction: int,
        supervised_prediction: int,
        confidence: float,
    ) -> str:
        """
        Generate human-readable explanation.
        """

        flags = []

        if supervised_prediction:
            flags.append("Supervised Classifier identified known fraud patterns")

        if isolation_prediction:
            flags.append("Isolation Forest detected outlier behavior")

        if autoencoder_prediction:
            flags.append("AutoEncoder reconstruction anomaly exceeded limits")

        if flags:
            return " & ".join(flags) + f" (confidence {confidence:.2f}%)."

        return (
            f"No significant anomalies detected "
            f"(confidence {confidence:.2f}%)."
        )


# ==========================================================
# Risk Analysis
# ==========================================================

    def analyze(
        self,
        isolation_prediction: int,
        autoencoder_prediction: int,
        supervised_prediction: int,
        confidence: float,
    ) -> RiskReport:
        """
        Complete business risk analysis.
        """

        score = self.calculate_score(
            confidence,
            isolation_prediction,
            autoencoder_prediction,
            supervised_prediction,
        )

        level = self.risk_level(score)

        metadata = self.metadata(level)

        recommendation = self.recommendation(level)

        explanation = self.explanation(
            isolation_prediction,
            autoencoder_prediction,
            supervised_prediction,
            confidence,
        )

        return RiskReport(

            score=score,

            level=level,

            priority=metadata["priority"],

            recommendation=recommendation,

            color=metadata["color"],

            badge=metadata["badge"],

            confidence=confidence,

            explanation=explanation,

        )


# ==========================================================
# Dashboard Card
# ==========================================================

    @staticmethod
    def dashboard_card(
        report: RiskReport,
    ) -> dict:
        """
        Streamlit-ready dashboard information.
        """

        return {

            "Risk Score":
                report.score,

            "Risk Level":
                report.level,

            "Priority":
                report.priority,

            "Badge":
                report.badge,

            "Color":
                report.color,

            "Confidence":
                report.confidence,

            "Recommendation":
                report.recommendation,

            "Explanation":
                report.explanation,

        }


# ==========================================================
# Alert Required
# ==========================================================

    @staticmethod
    def requires_alert(
        report: RiskReport,
    ) -> bool:
        """
        Determine whether an alert
        should be generated.
        """

        return report.level in (
            "Critical",
            "High",
        )


# ==========================================================
# Analyst Action
# ==========================================================

    @staticmethod
    def analyst_action(
        level: str,
    ) -> str:
        """
        Suggested analyst action.
        """

        actions = {

            "Critical":
                "Immediately escalate to Fraud Operations.",

            "High":
                "Assign to analyst for manual investigation.",

            "Medium":
                "Request customer verification.",

            "Low":
                "Approve and continue monitoring.",

        }

        return actions[level]
# ==========================================================
# Batch Risk Analysis
# ==========================================================

    def analyze_batch(
        self,
        predictions_df,
    ):
        """
        Perform risk analysis on an entire prediction dataframe.

        Required Columns
        ----------------
        Isolation_Prediction
        AutoEncoder_Prediction
        Confidence
        """

        reports = []

        for _, row in predictions_df.iterrows():

            report = self.analyze(

                isolation_prediction=int(
                    row["Isolation_Prediction"]
                ),

                autoencoder_prediction=int(
                    row["AutoEncoder_Prediction"]
                ),

                confidence=float(
                    row["Confidence"]
                ),

            )

            reports.append(report)

        return reports


# ==========================================================
# Risk Summary
# ==========================================================

    @staticmethod
    def summary(
        reports: list[RiskReport],
    ) -> dict:
        """
        Summary statistics.
        """

        if not reports:

            return {}

        levels = {}

        priorities = {}

        for report in reports:

            levels[report.level] = (

                levels.get(
                    report.level,
                    0,
                ) + 1

            )

            priorities[report.priority] = (

                priorities.get(
                    report.priority,
                    0,
                ) + 1

            )

        average_score = round(

            sum(

                report.score

                for report in reports

            ) / len(reports),

            2,

        )

        return {

            "Transactions":
                len(reports),

            "Average Risk":
                average_score,

            "Levels":
                levels,

            "Priorities":
                priorities,

        }


# ==========================================================
# Dashboard Metrics
# ==========================================================

    @staticmethod
    def dashboard_metrics(
        reports: list[RiskReport],
    ) -> dict:
        """
        Dashboard KPI metrics.
        """

        if not reports:

            return {}

        return {

            "Critical":

                sum(
                    r.level == "Critical"
                    for r in reports
                ),

            "High":

                sum(
                    r.level == "High"
                    for r in reports
                ),

            "Medium":

                sum(
                    r.level == "Medium"
                    for r in reports
                ),

            "Low":

                sum(
                    r.level == "Low"
                    for r in reports
                ),

            "Alerts":

                sum(
                    RiskEngine.requires_alert(r)
                    for r in reports
                ),

        }


# ==========================================================
# Export Report
# ==========================================================

    @staticmethod
    def export_dataframe(
        reports: list[RiskReport],
    ):
        """
        Convert reports to DataFrame.
        """

        import pandas as pd

        return pd.DataFrame(

            [

                {

                    "Risk Score":

                        r.score,

                    "Risk Level":

                        r.level,

                    "Priority":

                        r.priority,

                    "Confidence":

                        r.confidence,

                    "Recommendation":

                        r.recommendation,

                    "Explanation":

                        r.explanation,

                }

                for r in reports

            ]

        )


# ==========================================================
# Engine Status
# ==========================================================

    @staticmethod
    def status() -> dict:
        """
        Engine information.
        """

        return {

            "Engine":

                "Enterprise Risk Engine",

            "Version":

                "1.0.0",

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
# Singleton
# ==========================================================

risk_engine = RiskEngine()


def get_risk_engine() -> RiskEngine:
    """
    Return singleton instance.
    """

    return risk_engine


# ==========================================================
# Startup Test
# ==========================================================

if __name__ == "__main__":

    logger.info("=" * 60)

    logger.info("Enterprise Risk Engine")

    logger.info("=" * 60)

    logger.info(

        risk_engine.status()

    )

    logger.info("=" * 60)