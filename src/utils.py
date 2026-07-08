"""
===========================================================
NeuralRetail
Utility Functions
===========================================================

Shared helper functions used throughout the project.

Author : Shalvi Surve
"""

from __future__ import annotations

import json
import logging
import time
from functools import wraps
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

import streamlit as st

from src.config import (
    PROJECT_NAME,
    VERSION,
)

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

MODELS_DIR = PROJECT_ROOT / "models"

APP_DIR = PROJECT_ROOT / "app"

NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

LOGS_DIR = PROJECT_ROOT / "logs"

# ==========================================================
# Create Required Directories
# ==========================================================

for directory in [

    ARTIFACTS_DIR,

    MODELS_DIR,

    LOGS_DIR,

]:

    directory.mkdir(

        parents=True,

        exist_ok=True,

    )

# ==========================================================
# Logger
# ==========================================================

def get_logger(
    name: str,
) -> logging.Logger:
    """
    Create project logger.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(message)s",

        "%Y-%m-%d %H:%M:%S",

    )

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter
    )

    log_file = LOGS_DIR / "neural_retail.log"

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )

    logger.addHandler(
        file_handler
    )

    logger.propagate = False

    return logger


logger = get_logger(__name__)

# ==========================================================
# Timer Decorator
# ==========================================================

def timer(func):
    """
    Measure execution time.
    """

    @wraps(func)

    def wrapper(
        *args,
        **kwargs,
    ):

        start = time.time()

        result = func(
            *args,
            **kwargs,
        )

        elapsed = (
            time.time() - start
        )

        logger.info(

            "%s completed in %.2f seconds",

            func.__name__,

            elapsed,

        )

        return result

    return wrapper

# ==========================================================
# File Validation
# ==========================================================

def file_exists(
    path: Path,
):
    """
    Verify file exists.
    """

    if not path.exists():

        raise FileNotFoundError(

            f"{path} not found."

        )
    
# ==========================================================
# CSV Utilities
# ==========================================================

def load_csv(
    path: Path,
    **kwargs,
) -> pd.DataFrame:
    """
    Load CSV safely.
    """

    file_exists(path)

    logger.info(
        "Loading %s",
        path.name,
    )

    return pd.read_csv(
        path,
        **kwargs,
    )


def save_csv(
    df: pd.DataFrame,
    path: Path,
):
    """
    Save dataframe.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        path,
        index=False,
    )

    logger.info(
        "Saved %s",
        path.name,
    )

# ==========================================================
# JSON Utilities
# ==========================================================

def save_json(
    data: dict,
    path: str | Path,
):
    """
    Save JSON file.

    If only a filename is provided,
    it will automatically be saved
    inside the models directory.
    """

    if isinstance(path, str):

        path = MODELS_DIR / path

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
        )

    logger.info(
        "Saved %s",
        path.name,
    )


def load_json(
    path: str | Path,
):
    """
    Load JSON file.
    """

    if isinstance(path, str):

        path = MODELS_DIR / path

    file_exists(path)

    with open(
        path,
        encoding="utf-8",
    ) as file:

        return json.load(file)
    
# ==========================================================
# Model Utilities
# ==========================================================

def save_model(
    model: Any,
    filename: str,
):
    """
    Save ML model.
    """

    path = MODELS_DIR / filename

    joblib.dump(
        model,
        path,
    )

    logger.info(
        "Saved model: %s",
        filename,
    )


def load_model(
    filename: str,
):
    """
    Load ML model.
    """

    path = MODELS_DIR / filename

    file_exists(path)

    logger.info(
        "Loading model: %s",
        filename,
    )

    return joblib.load(path)

# ==========================================================
# Data Validation
# ==========================================================

def validate_columns(
    df: pd.DataFrame,
    required_columns: list[str],
):
    """
    Validate dataframe columns.
    """

    missing = [

        column

        for column in required_columns

        if column not in df.columns

    ]

    if missing:

        raise ValueError(

            f"Missing columns: {missing}"

        )

    logger.info(
        "Column validation successful."
    )


def validate_not_empty(
    df: pd.DataFrame,
):
    """
    Ensure dataframe is not empty.
    """

    if df.empty:

        raise ValueError(
            "DataFrame is empty."
        )
    
# ==========================================================
# Metadata Helpers
# ==========================================================

def create_metadata(
    model_name: str,
    algorithm: str,
    metrics: dict,
):
    """
    Create metadata dictionary.
    """

    return {

        "project": PROJECT_NAME,

        "version": VERSION,

        "model_name": model_name,

        "algorithm": algorithm,

        "metrics": metrics,

        "generated_on": pd.Timestamp.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    }

# ==========================================================
# Generic Utilities
# ==========================================================

def percentage(
    numerator: float,
    denominator: float,
) -> float:
    """
    Safe percentage calculation.
    """

    if denominator == 0:

        return 0.0

    return round(

        (numerator / denominator) * 100,

        2,

    )


def currency(
    value: float,
) -> float:
    """
    Round currency values.
    """

    return round(

        float(value),

        2,

    )

# ==========================================================
# Display Banner
# ==========================================================

def print_banner(
    title: str,
):
    """
    Print console banner.
    """

    line = "=" * 60

    print()

    print(line)

    print(title)

    print(line)

# ==========================================================
# Common Data Loaders
# ==========================================================

def load_cleaned_data() -> pd.DataFrame:
    """
    Load cleaned transaction dataset.
    """

    path = ARTIFACTS_DIR / "cleaned_data.csv"

    return load_csv(
        path,
        parse_dates=["InvoiceDate"],
    )


def load_feature_data() -> pd.DataFrame:
    """
    Load feature engineered dataset.
    """

    path = ARTIFACTS_DIR / "feature_data.csv"

    return load_csv(path)


def load_customer_features() -> pd.DataFrame:
    """
    Load customer features.
    """

    path = ARTIFACTS_DIR / "customer_features.csv"

    return load_csv(path)


def load_product_features() -> pd.DataFrame:
    """
    Load product features.
    """

    path = ARTIFACTS_DIR / "product_features.csv"

    return load_csv(path)


def load_daily_sales() -> pd.DataFrame:
    """
    Load daily sales.
    """

    path = ARTIFACTS_DIR / "daily_sales.csv"

    return load_csv(
        path,
        parse_dates=["Date"],
    )


def load_customer_segments() -> pd.DataFrame:
    """
    Load segmented customers.
    """

    path = ARTIFACTS_DIR / "customer_segments.csv"

    return load_csv(path)


def load_churn_predictions() -> pd.DataFrame:
    """
    Load churn predictions.
    """

    path = ARTIFACTS_DIR / "customer_churn_predictions.csv"

    return load_csv(path)

# ==========================================================
# Business Summary Loader
# ==========================================================

def load_business_summary():
    """
    Load dashboard summary.
    """

    path = MODELS_DIR / "business_summary.json"

    return load_json(path)

# ==========================================================
# Data Repository
# ==========================================================

class DataRepository:
    """
    Central data access layer for
    Streamlit pages.
    """

    @staticmethod
    def cleaned():

        return load_cleaned_data()

    @staticmethod
    def features():

        return load_feature_data()

    @staticmethod
    def customers():

        return load_customer_features()

    @staticmethod
    def products():

        return load_product_features()

    @staticmethod
    def daily_sales():

        return load_daily_sales()

    @staticmethod
    def segments():

        return load_customer_segments()

    @staticmethod
    def churn():

        return load_churn_predictions()

    @staticmethod
    def business_summary():

        return load_business_summary()
    
    @staticmethod
    def inventory():

        path = ARTIFACTS_DIR / "inventory_recommendations.csv"

        return load_csv(path)


    @staticmethod
    def inventory_summary():

        path = ARTIFACTS_DIR / "inventory_summary.json"

        return load_json(path)


    @staticmethod
    def forecast():

        path = ARTIFACTS_DIR / "demand_forecast.csv"

        return load_csv(path)


    @staticmethod
    def forecast_metrics():

        path = ARTIFACTS_DIR / "forecast_metrics.csv"

        return load_csv(path)


    @staticmethod
    def classification_report():

        path = ARTIFACTS_DIR / "classification_report.csv"

        return load_csv(path)


    @staticmethod
    def rfm():

        path = ARTIFACTS_DIR / "rfm_table.csv"

        return load_csv(path)
    
# ==========================================================
# Project Information
# ==========================================================

def project_info():
    """
    Return project metadata.
    """

    return {

        "project": PROJECT_NAME,

        "version": VERSION,

        "root": str(PROJECT_ROOT),

        "artifacts": str(ARTIFACTS_DIR),

        "models": str(MODELS_DIR),

    }

# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    print_banner(PROJECT_NAME)

    info = project_info()

    for key, value in info.items():

        print(f"{key:<12}: {value}")

    print("\nUtilities loaded successfully.")