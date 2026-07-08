"""
============================================================
NeuralRetail
Business Insights Generator
============================================================

Author : Shalvi Surve
Project : NeuralRetail
"""

from __future__ import annotations


# ==========================================================
# Dashboard Insights
# ==========================================================

def generate_business_insights(summary: dict) -> str:

    return f"""
### 📊 Business Overview

NeuralRetail processed **{summary['total_orders']:,} completed orders**
from **{summary['total_customers']:,} customers**.

The business generated a total revenue of
**₹{summary['total_revenue']:,.2f}**.

Average Order Value (AOV) stands at
**₹{summary['average_order_value']:.2f}**.

Approximately
**{summary['repeat_customer_rate']:.1f}%**
of customers are repeat buyers.

The highest-selling product is

**{summary['top_product']}**

Overall business performance appears healthy
with strong customer retention and consistent sales.
"""


# ==========================================================
# Customer Insights
# ==========================================================

def generate_customer_insights(customer_df):

    total = len(customer_df)

    vip = customer_df[
        customer_df["Segment"] == "VIP Customers"
    ].shape[0]

    loyal = customer_df[
        customer_df["Segment"] == "Loyal Customers"
    ].shape[0]

    return f"""
### 👥 Customer Intelligence

The business currently manages
**{total:,} customers**.

VIP Customers :

**{vip:,}**

Loyal Customers :

**{loyal:,}**

High-value customers contribute a significant
portion of overall revenue.

Customer retention campaigns should target
medium-value customers for maximum impact.
"""


# ==========================================================
# Churn Insights
# ==========================================================

def generate_churn_insights(churn_df):

    high = (
        churn_df["RiskLevel"] == "High"
    ).sum()

    medium = (
        churn_df["RiskLevel"] == "Medium"
    ).sum()

    low = (
        churn_df["RiskLevel"] == "Low"
    ).sum()

    return f"""
### 🚨 Customer Churn

High Risk Customers :

**{high}**

Medium Risk Customers :

**{medium}**

Low Risk Customers :

**{low}**

High-risk customers should receive
personalized offers and loyalty campaigns
to improve retention.
"""


# ==========================================================
# Forecast Insights
# ==========================================================

def generate_forecast_insights(metrics):

    rmse = metrics.loc[
        metrics["Metric"] == "RMSE",
        "Value",
    ].iloc[0]

    r2 = metrics.loc[
        metrics["Metric"] == "R2 Score",
        "Value",
    ].iloc[0]

    return f"""
### 📈 Demand Forecast

Forecast Accuracy (R²)

**{r2:.3f}**

RMSE

**{rmse:.2f}**

The forecasting model captures
overall demand patterns reasonably well
and can support inventory planning.
"""


# ==========================================================
# Inventory Insights
# ==========================================================

def generate_inventory_insights(summary):

    return f"""
### 📦 Inventory

Products requiring immediate restocking

**{summary['restock_immediately']}**

Products under monitoring

**{summary['monitor_products']}**

Products with sufficient inventory

**{summary['sufficient_stock']}**

Highest Priority Product

**{summary['highest_priority_product']}**
"""