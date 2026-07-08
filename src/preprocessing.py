"""
===========================================================
NeuralRetail
Data Preprocessing Pipeline
===========================================================

Author  : Shalvi Surve
Project : NeuralRetail

Description
-----------
This module cleans and validates the UCI Online Retail II
dataset before feature engineering.

Processing Steps
----------------
1. Load raw dataset
2. Standardize column names
3. Validate required columns
4. Remove missing Customer IDs
5. Remove cancelled invoices
6. Remove invalid quantities
7. Remove invalid prices
8. Remove duplicate rows
9. Convert InvoiceDate to datetime
10. Create Revenue feature
11. Remove revenue outliers (optional)
12. Save cleaned dataset

Output
------
artifacts/cleaned_data.csv
"""

from pathlib import Path

import pandas as pd

from utils import (
    DATA_DIR,
    ARTIFACTS_DIR,
    get_logger,
    load_csv,
    save_csv,
    validate_columns,
    timer,
)

logger = get_logger(__name__)

INPUT_FILE = DATA_DIR / "retail.csv"
OUTPUT_FILE = ARTIFACTS_DIR / "cleaned_data.csv"


# ==========================================================
# Standardize Column Names
# ==========================================================

COLUMN_MAPPING = {
    "Invoice": "InvoiceNo",
    "InvoiceNo": "InvoiceNo",
    "Customer ID": "CustomerID",
    "CustomerID": "CustomerID",
    "Price": "UnitPrice",
    "UnitPrice": "UnitPrice",
    "InvoiceDate": "InvoiceDate",
    "StockCode": "StockCode",
    "Description": "Description",
    "Quantity": "Quantity",
    "Country": "Country",
}


REQUIRED_COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
]


# ==========================================================
# Cleaning Functions
# ==========================================================

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename dataset columns into standard names."""

    df = df.rename(columns=COLUMN_MAPPING)

    validate_columns(df, REQUIRED_COLUMNS)

    logger.info("Column validation successful.")

    return df


def remove_missing_customers(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows without Customer ID."""

    before = len(df)

    df = df.dropna(subset=["CustomerID"])

    logger.info(
        "Removed %d rows with missing CustomerID",
        before - len(df),
    )

    return df


def remove_cancelled_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Remove invoices beginning with 'C'."""

    before = len(df)

    df = df[
        ~df["InvoiceNo"].astype(str).str.startswith("C")
    ]

    logger.info(
        "Removed %d cancelled invoices",
        before - len(df),
    )

    return df


def remove_invalid_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Remove zero/negative quantity and price."""

    before = len(df)

    df = df[
        (df["Quantity"] > 0)
        &
        (df["UnitPrice"] > 0)
    ]

    logger.info(
        "Removed %d invalid transactions",
        before - len(df),
    )

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicated rows."""

    before = len(df)

    df = df.drop_duplicates()

    logger.info(
        "Removed %d duplicate rows",
        before - len(df),
    )

    return df


def convert_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """Convert InvoiceDate into datetime."""

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"]
    )

    return df


def create_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Create Revenue feature."""

    df["Revenue"] = (
        df["Quantity"] *
        df["UnitPrice"]
    )

    return df


def remove_outliers(
    df: pd.DataFrame,
    enabled: bool = True,
) -> pd.DataFrame:
    """
    Remove revenue outliers using IQR.

    Set enabled=False if you want to retain
    all observations.
    """

    if not enabled:
        return df

    q1 = df["Revenue"].quantile(0.25)

    q3 = df["Revenue"].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr

    upper = q3 + 1.5 * iqr

    before = len(df)

    df = df[
        (df["Revenue"] >= lower)
        &
        (df["Revenue"] <= upper)
    ]

    logger.info(
        "Removed %d revenue outliers",
        before - len(df),
    )

    return df


# ==========================================================
# Pipeline
# ==========================================================

@timer
def preprocess_data() -> pd.DataFrame:
    """Execute preprocessing pipeline."""

    logger.info("Loading raw retail dataset...")

    df = load_csv(INPUT_FILE)

    logger.info("Dataset Shape : %s", df.shape)

    df = standardize_columns(df)

    df = remove_missing_customers(df)

    df = remove_cancelled_orders(df)

    df = remove_invalid_transactions(df)

    df = remove_duplicates(df)

    df = convert_datetime(df)

    df = create_revenue(df)

    df = remove_outliers(df)

    save_csv(df, OUTPUT_FILE)

    logger.info("Cleaned dataset saved successfully.")

    logger.info("Final Shape : %s", df.shape)

    return df


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    cleaned_df = preprocess_data()

    print("\nFirst Five Rows\n")

    print(cleaned_df.head())