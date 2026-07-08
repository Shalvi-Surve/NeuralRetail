"""
============================================================
NeuralRetail
Feature Engineering Pipeline
============================================================

Author  : Shalvi Surve
Project : NeuralRetail

Description
-----------
Generates all engineered datasets required for

1. Demand Forecasting
2. Customer Segmentation
3. Churn Prediction
4. Inventory Recommendation
5. Business Dashboard

Outputs
-------
artifacts/

feature_data.csv
rfm_table.csv
customer_features.csv
daily_sales.csv
product_features.csv
business_summary.json
feature_metadata.json
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import numpy as np

from config import (
    ROLLING_WINDOW,
    FORECAST_HORIZON,
)

from utils import (
    ARTIFACTS_DIR,
    get_logger,
    load_cleaned_data,
    save_csv,
    save_json,
    timer,
)

logger = get_logger(__name__)


# ==========================================================
# Output Files
# ==========================================================

FEATURE_OUTPUT = ARTIFACTS_DIR / "feature_data.csv"

RFM_OUTPUT = ARTIFACTS_DIR / "rfm_table.csv"

CUSTOMER_OUTPUT = ARTIFACTS_DIR / "customer_features.csv"

PRODUCT_OUTPUT = ARTIFACTS_DIR / "product_features.csv"

DAILY_OUTPUT = ARTIFACTS_DIR / "daily_sales.csv"

BUSINESS_OUTPUT = "business_summary.json"

METADATA_OUTPUT = "feature_metadata.json"


# ==========================================================
# Time Features
# ==========================================================

def create_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create calendar based features.
    """

    logger.info("Creating time features...")

    invoice_date = df["InvoiceDate"]

    df["Year"] = invoice_date.dt.year

    df["Quarter"] = invoice_date.dt.quarter

    df["Month"] = invoice_date.dt.month

    df["Week"] = invoice_date.dt.isocalendar().week.astype(int)

    df["Day"] = invoice_date.dt.day

    df["Hour"] = invoice_date.dt.hour

    df["DayOfWeek"] = invoice_date.dt.dayofweek

    df["MonthName"] = invoice_date.dt.month_name()

    df["DayName"] = invoice_date.dt.day_name()

    df["IsWeekend"] = (
        df["DayOfWeek"] >= 5
    ).astype(int)

    return df


# ==========================================================
# Daily Sales
# ==========================================================

def create_daily_sales(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Generate daily business metrics.
    """

    logger.info("Generating daily sales table...")

    daily = (
        df.assign(Date=df["InvoiceDate"].dt.normalize())
        .groupby("Date")
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("InvoiceNo", "nunique"),
            Customers=("CustomerID", "nunique"),
            Quantity=("Quantity", "sum"),
        )
        .reset_index()
        .sort_values("Date")
    )

    return daily


# ==========================================================
# Weekly Sales
# ==========================================================

def create_weekly_sales(
    df: pd.DataFrame
) -> pd.DataFrame:

    logger.info("Creating weekly statistics...")

    weekly = (
        df
        .groupby(
            [
                "Year",
                "Week"
            ]
        )
        .agg(
            WeeklyRevenue=("Revenue", "sum"),
            WeeklyOrders=("InvoiceNo", "nunique")
        )
        .reset_index()
    )

    return weekly


# ==========================================================
# Monthly Sales
# ==========================================================

def create_monthly_sales(
    df: pd.DataFrame
) -> pd.DataFrame:

    logger.info("Creating monthly statistics...")

    monthly = (
        df
        .groupby(
            [
                "Year",
                "Month"
            ]
        )
        .agg(
            MonthlyRevenue=("Revenue", "sum"),
            MonthlyOrders=("InvoiceNo", "nunique"),
            MonthlyCustomers=("CustomerID", "nunique")
        )
        .reset_index()
    )

    return monthly


# ==========================================================
# Product Features
# ==========================================================

def create_product_features(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Product level business statistics.
    """

    logger.info("Generating product intelligence...")

    products = (
        df
        .groupby(
            [
                "StockCode",
                "Description"
            ]
        )
        .agg(
            TotalRevenue=("Revenue", "sum"),
            QuantitySold=("Quantity", "sum"),
            InvoiceCount=("InvoiceNo", "nunique"),
            CustomerCount=("CustomerID", "nunique"),
            AveragePrice=("UnitPrice", "mean")
        )
        .reset_index()
    )

    products["PopularityScore"] = (
        products["InvoiceCount"] *
        products["CustomerCount"]
    )

    products = products.sort_values(
        "TotalRevenue",
        ascending=False
    )

    return products

# ==========================================================
# Customer RFM
# ==========================================================

def create_rfm_table(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Create RFM metrics for every customer.
    """

    logger.info("Generating RFM table...")

    snapshot_date = (
        df["InvoiceDate"].max()
        + pd.Timedelta(days=1)
    )

    rfm = (
        df.groupby("CustomerID")
        .agg(
            Recency=(
                "InvoiceDate",
                lambda x: (
                    snapshot_date - x.max()
                ).days,
            ),
            Frequency=("InvoiceNo", "nunique"),
            Monetary=("Revenue", "sum"),
        )
        .reset_index()
    )

    return rfm


# ==========================================================
# Customer Statistics
# ==========================================================

def create_customer_features(
    df: pd.DataFrame,
    rfm: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate customer intelligence features.
    """

    logger.info("Generating customer features...")

    customer = (
        df.groupby("CustomerID")
        .agg(
            TotalRevenue=("Revenue", "sum"),
            TotalQuantity=("Quantity", "sum"),
            InvoiceCount=("InvoiceNo", "nunique"),
            ProductVariety=("StockCode", "nunique"),
            AverageOrderValue=("Revenue", "mean"),
            AverageQuantity=("Quantity", "mean"),
        )
        .reset_index()
    )

    customer = customer.merge(
        rfm,
        on="CustomerID",
        how="left",
    )

    customer["RevenuePerInvoice"] = (
        customer["TotalRevenue"]
        / customer["InvoiceCount"]
    )

    customer["RevenuePerProduct"] = (
        customer["TotalRevenue"]
        / customer["ProductVariety"]
    )

    return customer


# ==========================================================
# Rolling Features
# ==========================================================

def create_rolling_features(
    daily: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate forecasting features.
    """

    logger.info("Generating rolling features...")

    daily = daily.copy()

    daily["Lag1"] = daily["Revenue"].shift(1)

    daily["Lag7"] = daily["Revenue"].shift(7)

    daily["Lag30"] = daily["Revenue"].shift(30)

    daily["RollingMean"] = (
        daily["Revenue"]
        .rolling(ROLLING_WINDOW)
        .mean()
    )

    daily["RollingStd"] = (
        daily["Revenue"]
        .rolling(ROLLING_WINDOW)
        .std()
    )

    daily["RollingMin"] = (
        daily["Revenue"]
        .rolling(ROLLING_WINDOW)
        .min()
    )

    daily["RollingMax"] = (
        daily["Revenue"]
        .rolling(ROLLING_WINDOW)
        .max()
    )

    daily["RollingMedian"] = (
        daily["Revenue"]
        .rolling(ROLLING_WINDOW)
        .median()
    )

    daily["RevenueGrowth"] = (
        daily["Revenue"]
        .pct_change()
    )

    return daily

# ==========================================================
# Business Summary
# ==========================================================

def create_business_summary(
    df: pd.DataFrame,
    customer: pd.DataFrame,
    products: pd.DataFrame,
) -> dict:
    """
    Generate executive KPIs.
    """

    logger.info("Generating business KPIs...")

    summary = {

        "project": "NeuralRetail",

        "generated_on": str(datetime.now()),

        "total_revenue": float(
            df["Revenue"].sum()
        ),

        "total_orders": int(
            df["InvoiceNo"].nunique()
        ),

        "total_customers": int(
            df["CustomerID"].nunique()
        ),

        "total_products": int(
            df["StockCode"].nunique()
        ),

        "average_order_value": float(
            customer["AverageOrderValue"].mean()
        ),

        "repeat_customer_rate": float(
            (
                customer["InvoiceCount"] > 1
            ).mean()
            * 100
        ),

        "top_product": str(
            products.iloc[0]["Description"]
        ),

        "top_customer_revenue": float(
            customer["TotalRevenue"].max()
        ),
    }

    return summary

# ==========================================================
# Metadata
# ==========================================================

def create_feature_metadata(
    feature_df: pd.DataFrame,
) -> dict:
    """
    Metadata for feature engineering.
    """

    return {

        "generated_on": str(datetime.now()),

        "rows": int(
            feature_df.shape[0]
        ),

        "columns": int(
            feature_df.shape[1]
        ),

        "rolling_window": ROLLING_WINDOW,

        "forecast_horizon": FORECAST_HORIZON,
    }

# ==========================================================
# Customer Lifetime Value
# ==========================================================

def calculate_clv(
    customer: pd.DataFrame,
) -> pd.DataFrame:
    """
    Estimate a simple Customer Lifetime Value (CLV).

    Formula:
        CLV = Average Order Value × Frequency
    """

    logger.info("Calculating customer lifetime value...")

    customer = customer.copy()

    customer["CustomerLifetimeValue"] = (
        customer["AverageOrderValue"]
        * customer["Frequency"]
    )

    total_revenue = customer["TotalRevenue"].sum()

    customer["RevenueContribution"] = (
        customer["TotalRevenue"]
        / total_revenue
    ) * 100

    customer = customer.sort_values(
        "CustomerLifetimeValue",
        ascending=False,
    )

    return customer


# ==========================================================
# Merge Forecast Features
# ==========================================================

def build_feature_dataset(
    transactions: pd.DataFrame,
    daily_sales: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merge transaction data with daily forecasting features.
    """

    logger.info("Building feature dataset...")

    feature_df = transactions.copy()

    feature_df["Date"] = (
        feature_df["InvoiceDate"]
        .dt.normalize()
    )

    feature_df = feature_df.merge(
        daily_sales,
        on="Date",
        how="left",
        suffixes=("", "_Daily"),
    )

    return feature_df

# ==========================================================
# Pipeline
# ==========================================================

@timer
def run_pipeline():
    """
    Execute complete feature engineering pipeline.
    """

    logger.info("=" * 60)
    logger.info("Starting Feature Engineering Pipeline")
    logger.info("=" * 60)

    # ---------------------------------------------
    # Load cleaned data
    # ---------------------------------------------

    df = load_cleaned_data()

    logger.info(
        "Loaded cleaned dataset: %s",
        df.shape,
    )

    # ---------------------------------------------
    # Time Features
    # ---------------------------------------------

    df = create_time_features(df)

    # ---------------------------------------------
    # Product Intelligence
    # ---------------------------------------------

    products = create_product_features(df)

    # ---------------------------------------------
    # Daily Sales
    # ---------------------------------------------

    daily = create_daily_sales(df)

    daily = create_rolling_features(daily)

    # ---------------------------------------------
    # Customer Intelligence
    # ---------------------------------------------

    rfm = create_rfm_table(df)

    customer = create_customer_features(
        df,
        rfm,
    )

    customer = calculate_clv(customer)

    # ---------------------------------------------
    # Feature Dataset
    # ---------------------------------------------

    feature_df = build_feature_dataset(
        df,
        daily,
    )

    # ---------------------------------------------
    # Business KPIs
    # ---------------------------------------------

    summary = create_business_summary(
        df,
        customer,
        products,
    )

    metadata = create_feature_metadata(
        feature_df
    )

    # ---------------------------------------------
    # Save Outputs
    # ---------------------------------------------

    save_csv(
        feature_df,
        FEATURE_OUTPUT,
    )

    save_csv(
        rfm,
        RFM_OUTPUT,
    )

    save_csv(
        customer,
        CUSTOMER_OUTPUT,
    )

    save_csv(
        products,
        PRODUCT_OUTPUT,
    )

    save_csv(
        daily,
        DAILY_OUTPUT,
    )

    save_json(
        summary,
        BUSINESS_OUTPUT,
    )

    save_json(
        metadata,
        METADATA_OUTPUT,
    )

    logger.info("=" * 60)
    logger.info("Feature Engineering Completed Successfully")
    logger.info("=" * 60)

    return (
        feature_df,
        customer,
        products,
        daily,
        summary,
    )

# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    (
        feature_df,
        customer_df,
        product_df,
        daily_df,
        summary,
    ) = run_pipeline()

    print("\n")
    print("=" * 60)
    print("Feature Engineering Complete")
    print("=" * 60)

    print("\nFeature Dataset")
    print(feature_df.head())

    print("\nCustomer Features")
    print(customer_df.head())

    print("\nProduct Features")
    print(product_df.head())

    print("\nDaily Sales")
    print(daily_df.head())

    print("\nBusiness Summary")

    for key, value in summary.items():
        print(f"{key}: {value}")

