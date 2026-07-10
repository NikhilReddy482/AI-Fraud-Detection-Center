"""
===========================================================
AI Fraud Intelligence Center
-----------------------------------------------------------
Enterprise Data Access Layer

This module provides a centralized interface for loading,
validating, caching, and managing all datasets required by
the Fraud Intelligence Dashboard.

Author  : Gurrala Nikhil Reddy
Version : 2.0.0
===========================================================
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

import pandas as pd
import streamlit as st

from utils.config import (
    CLEAN_DATASET,
    FINAL_DATASET,
    DASHBOARD_KPIS,
    FRAUD_ALERTS,
    MODEL_COMPARISON,
    DEPLOYMENT_RESULTS,
)

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
# Synthetic Data Generator Fallback
# ==========================================================

def generate_synthetic_data(path: Path) -> pd.DataFrame:
    import numpy as np

    logger.info("Generating synthetic dataset for path: %s", path.name)
    np.random.seed(42)
    n_samples = 1000

    # 1. Base time and amounts
    time = np.sort(np.random.randint(0, 86400, n_samples))
    amount = np.random.exponential(scale=100.0, size=n_samples) + 1.0

    # 2. PCA features V1..V28
    data = {f"V{i}": np.random.normal(loc=0.0, scale=1.0, size=n_samples) for i in range(1, 29)}
    data["Time"] = time
    data["Amount"] = amount

    # 3. Class (fraud label): 1.5% fraud
    class_label = np.random.choice([0, 1], size=n_samples, p=[0.985, 0.015])
    data["Class"] = class_label
    data["Prediction"] = class_label

    df = pd.DataFrame(data)

    # 4. Derived features
    df["Hour"] = (df["Time"] % 86400) // 3600
    df["Scaled_Amount"] = (df["Amount"] - 88.4726) / 250.399

    df["Time_Period_Evening"] = ((df["Hour"] >= 17) & (df["Hour"] < 21)).astype(float)
    df["Time_Period_Morning"] = ((df["Hour"] >= 5) & (df["Hour"] < 12)).astype(float)
    df["Time_Period_Night"] = ((df["Hour"] >= 21) | (df["Hour"] < 5)).astype(float)

    # 5. Risk score and level
    risk_scores = []
    for idx, row in df.iterrows():
        if row["Class"] == 1:
            score = np.random.uniform(75, 99)
        else:
            base = min(row["Amount"] / 50.0, 35)
            score = np.random.uniform(5, 45) + base
        risk_scores.append(score)

    df["Risk_Score"] = np.round(risk_scores, 2)

    def get_risk_level(s):
        if s >= 85: return "Critical"
        if s >= 60: return "High"
        if s >= 30: return "Medium"
        return "Low"

    df["Risk_Level"] = df["Risk_Score"].apply(get_risk_level)

    # Ensure directory exists and save
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logger.info("Successfully saved synthetic dataset to %s", path)
    return df


# ==========================================================
# Cached CSV Reader
# ==========================================================

@st.cache_data(show_spinner=False)
def read_csv(path: Path) -> pd.DataFrame:
    """
    Read a CSV file using Streamlit cache.
    """

    if not path.exists():

        if path.name in ["final_dashboard_dataset.csv", "cleaned_transactions.csv"]:
            return generate_synthetic_data(path)

        logger.error("%s not found.", path)

        raise FileNotFoundError(
            f"{path.name} does not exist."
        )

    logger.info("Loading %s", path.name)

    return pd.read_csv(path)


# ==========================================================
# Date Parser
# ==========================================================

def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Automatically parse datetime columns.
    """

    date_columns = [
        "Date",
        "Transaction_Date",
        "Timestamp"
    ]

    for column in date_columns:

        if column in df.columns:

            try:
                df[column] = pd.to_datetime(df[column], errors="raise")
            except Exception:
                pass

    return df


# ==========================================================
# Required Columns
# ==========================================================

def validate_columns(

    df: pd.DataFrame,

    required: Iterable[str],

) -> None:
    """
    Validate dataframe columns.
    """

    missing = [

        col

        for col in required

        if col not in df.columns

    ]

    if missing:

        raise ValueError(

            "Missing columns : "

            + ", ".join(missing)

        )


# ==========================================================
# Dashboard Loader
# ==========================================================

class DashboardDataLoader:
    """
    Enterprise Data Access Layer.

    Every page should use this class instead
    of reading CSV files directly.
    """

    def __init__(self) -> None:

        self.dashboard_file = FINAL_DATASET

        self.cleaned_file = CLEAN_DATASET

        self.kpi_file = DASHBOARD_KPIS

        self.alert_file = FRAUD_ALERTS

        self.comparison_file = MODEL_COMPARISON

        self.deployment_file = DEPLOYMENT_RESULTS

        self.loaded = False

# ==========================================================
# File Utilities
# ==========================================================

    @staticmethod
    def exists(path: Path) -> bool:

        return path.exists()


    def available_files(self) -> dict[str, bool]:
        """
        Check all dashboard resources.
        """

        return {

            "Dashboard":
                self.exists(self.dashboard_file),

            "Clean Dataset":
                self.exists(self.cleaned_file),

            "KPIs":
                self.exists(self.kpi_file),

            "Fraud Alerts":
                self.exists(self.alert_file),

            "Model Comparison":
                self.exists(self.comparison_file),

            "Deployment":
                self.exists(self.deployment_file),

        }


# ==========================================================
# Health Check
# ==========================================================

    def health(self) -> dict:
        """
        Dashboard resource status.
        """

        files = self.available_files()

        total = len(files)

        available = sum(files.values())

        return {

            "ready":
                available == total,

            "available":
                available,

            "missing":
                total - available,

            "files":
                files,

        }


# ==========================================================
# Internal Loader
# ==========================================================

    @staticmethod
    def _load(path: Path) -> pd.DataFrame:
        """
        Internal loader.
        """

        df = read_csv(path)

        df = parse_dates(df)

        return df


# ==========================================================
# Ready Status
# ==========================================================

    def is_ready(self) -> bool:
        """
        Is dashboard ready?
        """

        return self.health()["ready"]


# ==========================================================
# Dashboard Status
# ==========================================================

    def status(self) -> dict:
        """
        Dashboard status.
        """

        return {

            "Ready":
                self.is_ready(),

            "Loaded":
                self.loaded,

            "Version":
                "2.0",

            "Resources":
                self.health(),

        }
# ==========================================================
# Dashboard Dataset
# ==========================================================

    def dashboard(self) -> pd.DataFrame:
        """
        Return dashboard dataset.
        """

        df = self._load(self.dashboard_file)

        self.loaded = True

        return df


# ==========================================================
# Clean Dataset
# ==========================================================

    def clean(self) -> pd.DataFrame:
        """
        Return cleaned transaction dataset.
        """

        return self._load(self.cleaned_file)


# ==========================================================
# KPI Dataset
# ==========================================================

    def kpis(self) -> pd.DataFrame:
        """
        Return KPI dataset.
        """

        return self._load(self.kpi_file)


# ==========================================================
# Fraud Alerts
# ==========================================================

    def alerts(self) -> pd.DataFrame:
        """
        Return fraud alert dataset.
        """

        return self._load(self.alert_file)


# ==========================================================
# Model Comparison
# ==========================================================

    def comparison(self) -> pd.DataFrame:
        """
        Return model comparison dataset.
        """

        return self._load(self.comparison_file)


# ==========================================================
# Deployment Results
# ==========================================================

    def deployment(self) -> pd.DataFrame:
        """
        Return deployment report.
        """

        return self._load(self.deployment_file)


# ==========================================================
# Dataset Information
# ==========================================================

    @staticmethod
    def dataset_info(
        df: pd.DataFrame
    ) -> dict:
        """
        Dataset metadata.
        """

        memory = int(
            df.memory_usage(
                deep=True
            ).sum()
        )

        return {

            "Rows": len(df),

            "Columns": len(df.columns),

            "Missing Values":

                int(
                    df.isna().sum().sum()
                ),

            "Duplicate Rows":

                int(
                    df.duplicated().sum()
                ),

            "Memory (MB)":

                round(
                    memory / 1024 / 1024,
                    2,
                ),

        }


# ==========================================================
# Dashboard KPIs
# ==========================================================

    @staticmethod
    def dashboard_kpis(
        df: pd.DataFrame
    ) -> dict:
        """
        Calculate dashboard KPIs.
        """

        kpis = {

            "Total Transactions":

                len(df)

        }

        # Fraud Count

        fraud_columns = [

            "Prediction",

            "Fraud",

            "Class"

        ]

        fraud_count = 0

        for col in fraud_columns:

            if col in df.columns:

                fraud_count = int(

                    (df[col] == 1).sum()

                )

                break

        kpis["Fraud Alerts"] = fraud_count

        # Risk Levels

        if "Risk_Level" in df.columns:

            counts = (

                df["Risk_Level"]

                .value_counts()

            )

            kpis["High Risk"] = int(

                counts.get("High", 0)

            )

            kpis["Medium Risk"] = int(

                counts.get("Medium", 0)

            )

            kpis["Low Risk"] = int(

                counts.get("Low", 0)

            )

        return kpis


# ==========================================================
# Fraud Summary
# ==========================================================

    @staticmethod
    def fraud_summary(
        df: pd.DataFrame
    ) -> dict:
        """
        Return fraud summary.
        """

        summary = {

            "Transactions":

                len(df)

        }

        if "Risk_Level" in df.columns:

            summary.update(

                df["Risk_Level"]

                .value_counts()

                .to_dict()

            )

        return summary


# ==========================================================
# Missing Values
# ==========================================================

    @staticmethod
    def missing_values(
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Missing values table.
        """

        return (

            df

            .isna()

            .sum()

            .rename("Missing")

            .reset_index()

            .rename(

                columns={

                    "index":

                        "Column"

                }

            )

        )


# ==========================================================
# Numeric Columns
# ==========================================================

    @staticmethod
    def numeric_columns(
        df: pd.DataFrame
    ) -> list[str]:

        return list(

            df.select_dtypes(

                include="number"

            ).columns

        )


# ==========================================================
# Categorical Columns
# ==========================================================

    @staticmethod
    def categorical_columns(
        df: pd.DataFrame
    ) -> list[str]:

        return list(

            df.select_dtypes(

                exclude="number"

            ).columns

        )


# ==========================================================
# Datetime Columns
# ==========================================================

    @staticmethod
    def datetime_columns(
        df: pd.DataFrame
    ) -> list[str]:

        return list(

            df.select_dtypes(

                include="datetime"

            ).columns

        )
# ==========================================================
# Search
# ==========================================================

    @staticmethod
    def search(
        df: pd.DataFrame,
        keyword: str
    ) -> pd.DataFrame:
        """
        Global search across all non-datetime columns.
        """

        if not keyword:
            return df

        keyword = keyword.lower()

        mask = pd.Series(False, index=df.index)

        for column in df.columns:

            if pd.api.types.is_datetime64_any_dtype(df[column]):
                continue

            mask |= (
                df[column]
                .astype(str)
                .str.lower()
                .str.contains(
                    keyword,
                    na=False
                )
            )

        return df[mask]


# ==========================================================
# Risk Filter
# ==========================================================

    @staticmethod
    def filter_risk(
        df: pd.DataFrame,
        level: str
    ) -> pd.DataFrame:
        """
        Filter by risk level.
        """

        if "Risk_Level" not in df.columns:
            return df

        return df[
            df["Risk_Level"] == level
        ]


# ==========================================================
# Date Filter
# ==========================================================

    @staticmethod
    def filter_date(
        df: pd.DataFrame,
        start_date,
        end_date,
        column: str = "Date",
    ) -> pd.DataFrame:
        """
        Filter by date range.
        """

        if column not in df.columns:
            return df

        return df[
            (df[column] >= pd.to_datetime(start_date))
            &
            (df[column] <= pd.to_datetime(end_date))
        ]


# ==========================================================
# Monthly Trend
# ==========================================================

    @staticmethod
    def monthly_trend(
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Monthly transaction count.
        """

        if "Date" not in df.columns:
            return pd.DataFrame()

        temp = df.copy()

        temp["Month"] = (
            temp["Date"]
            .dt.to_period("M")
            .astype(str)
        )

        return (
            temp
            .groupby("Month")
            .size()
            .reset_index(name="Transactions")
        )


# ==========================================================
# Risk Distribution
# ==========================================================

    @staticmethod
    def risk_distribution(
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Risk level distribution.
        """

        if "Risk_Level" not in df.columns:
            return pd.DataFrame()

        return (
            df["Risk_Level"]
            .value_counts()
            .rename_axis("Risk_Level")
            .reset_index(name="Count")
        )


# ==========================================================
# Top Categories
# ==========================================================

    @staticmethod
    def top_categories(
        df: pd.DataFrame,
        column: str = "Category",
        top: int = 10,
    ) -> pd.DataFrame:
        """
        Top categories.
        """

        if column not in df.columns:
            return pd.DataFrame()

        return (
            df[column]
            .value_counts()
            .head(top)
            .rename_axis(column)
            .reset_index(name="Count")
        )


# ==========================================================
# Average Transaction
# ==========================================================

    @staticmethod
    def average_transaction(
        df: pd.DataFrame,
        amount_column: str = "Amount"
    ) -> float:

        if amount_column not in df.columns:
            return 0.0

        return round(
            float(df[amount_column].mean()),
            2
        )


# ==========================================================
# Fraud Rate
# ==========================================================

    @staticmethod
    def fraud_rate(
        df: pd.DataFrame
    ) -> float:

        total = len(df)

        if total == 0:
            return 0.0

        for col in [
            "Prediction",
            "Fraud",
            "Class"
        ]:

            if col in df.columns:

                fraud = (
                    df[col] == 1
                ).sum()

                return round(
                    fraud * 100 / total,
                    2
                )

        return 0.0


# ==========================================================
# Cache Management
# ==========================================================

    @staticmethod
    def clear_cache():

        st.cache_data.clear()


# ==========================================================
# Reload Dashboard
# ==========================================================

    def reload(self):

        self.clear_cache()

        self.loaded = False

        logger.info(
            "Dashboard cache cleared."
        )


# ==========================================================
# Dashboard Summary
# ==========================================================

    def summary(self) -> dict:

        report = {

            "Status":
                self.status(),

            "Health":
                self.health(),

            "Files":
                self.available_files(),

        }

        if self.is_ready():

            df = self.dashboard()

            report["Dataset"] = (
                self.dataset_info(df)
            )

            report["KPIs"] = (
                self.dashboard_kpis(df)
            )

            report["Fraud Summary"] = (
                self.fraud_summary(df)
            )

            report["Fraud Rate"] = (
                self.fraud_rate(df)
            )

        return report


# ==========================================================
# Singleton
# ==========================================================

loader = DashboardDataLoader()


# ==========================================================
# Helper
# ==========================================================

def get_loader() -> DashboardDataLoader:
    """
    Return the singleton loader.
    """

    return loader


# ==========================================================
# Startup Test
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print("Fraud Dashboard Data Layer")

    print("=" * 60)

    dashboard = DashboardDataLoader()

    print(dashboard.summary())

    print("=" * 60)
