"""
============================================================
NeuralRetail
Business Metrics
============================================================

Author : Shalvi Surve
Project : NeuralRetail
"""

from __future__ import annotations

import pandas as pd


# ==========================================================
# Revenue Metrics
# ==========================================================

def total_revenue(df: pd.DataFrame) -> float:
    return float(df["Revenue"].sum())


def average_order_value(df: pd.DataFrame) -> float:
    return float(df["Revenue"].mean())


def total_orders(df: pd.DataFrame) -> int:
    return int(df["InvoiceNo"].nunique())


# ==========================================================
# Customer Metrics
# ==========================================================

def total_customers(df: pd.DataFrame) -> int:
    return int(df["CustomerID"].nunique())


def repeat_customer_rate(df: pd.DataFrame) -> float:

    customer_orders = (

        df.groupby("CustomerID")["InvoiceNo"]

        .nunique()

    )

    repeat = (

        customer_orders > 1

    ).sum()

    return (

        repeat

        / len(customer_orders)

    ) * 100


# ==========================================================
# Product Metrics
# ==========================================================

def total_products(df: pd.DataFrame) -> int:
    return int(df["StockCode"].nunique())


def top_product(df: pd.DataFrame):

    top = (

        df.groupby("Description")["Revenue"]

        .sum()

        .idxmax()

    )

    return top


# ==========================================================
# Churn Metrics
# ==========================================================

def churn_rate(churn_df):

    churned = (

        churn_df["PredictedChurn"] == 1

    ).sum()

    return (

        churned

        / len(churn_df)

    ) * 100


# ==========================================================
# Forecast Metrics
# ==========================================================

def forecast_accuracy(metrics_df):

    value = metrics_df.loc[

        metrics_df["Metric"] == "R2 Score",

        "Value",

    ].iloc[0]

    return value * 100


# ==========================================================
# Inventory Metrics
# ==========================================================

def inventory_health(summary):

    safe = summary["sufficient_stock"]

    total = summary["total_products"]

    return (

        safe

        / total

    ) * 100