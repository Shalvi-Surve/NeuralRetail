"""
===========================================================
NeuralRetail
Project Configuration
===========================================================

Central configuration used throughout the project.

Author : Shalvi Surve
"""

# ==========================================================
# Project Information
# ==========================================================

PROJECT_NAME = "NeuralRetail"

VERSION = "1.0.0"

AUTHOR = "Shalvi Surve"

# ==========================================================
# Random Seed
# ==========================================================

RANDOM_STATE = 42

# ==========================================================
# Customer Churn
# ==========================================================

CHURN_THRESHOLD = 90

# ==========================================================
# Demand Forecasting
# ==========================================================

ROLLING_WINDOW = 7

FORECAST_HORIZON = 30

# ==========================================================
# Inventory Management
# ==========================================================

SAFETY_STOCK_PERCENT = 0.20

# ==========================================================
# Customer Segmentation
# ==========================================================

MIN_CLUSTERS = 2

MAX_CLUSTERS = 8

# ==========================================================
# Dashboard Configuration
# ==========================================================

TOP_CUSTOMERS = 10

TOP_PRODUCTS = 10

TOP_COUNTRIES = 10

# ==========================================================
# Plot Configuration
# ==========================================================

PLOT_WIDTH = 1000

PLOT_HEIGHT = 600

# ==========================================================
# Date Formats
# ==========================================================

DATE_FORMAT = "%Y-%m-%d"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# ==========================================================
# File Names
# ==========================================================

RAW_DATA_FILE = "retail.csv"

CLEANED_DATA_FILE = "cleaned_data.csv"

FEATURE_DATA_FILE = "feature_data.csv"

CUSTOMER_FEATURES_FILE = "customer_features.csv"

PRODUCT_FEATURES_FILE = "product_features.csv"

DAILY_SALES_FILE = "daily_sales.csv"

CUSTOMER_SEGMENTS_FILE = "customer_segments.csv"

CHURN_PREDICTIONS_FILE = "customer_churn_predictions.csv"