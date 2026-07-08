"""
============================================================
NeuralRetail
Demand Forecasting Engine
============================================================

Author  : Shalvi Surve
Project : NeuralRetail

Description
-----------
Forecast future daily revenue using machine learning.

Outputs
-------
artifacts/
    demand_forecast.csv
    forecast_metrics.csv

models/
    demand_forecast.pkl
    forecast_metadata.json
"""

from __future__ import annotations

from datetime import datetime

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from utils import (
    ARTIFACTS_DIR,
    get_logger,
    load_csv,
    save_csv,
    save_json,
    save_model,
    timer,
)

from config import (
    RANDOM_STATE,
)

logger = get_logger(__name__)

# ==========================================================
# Files
# ==========================================================

INPUT_FILE = (
    ARTIFACTS_DIR /
    "daily_sales.csv"
)

FORECAST_OUTPUT = (
    ARTIFACTS_DIR /
    "demand_forecast.csv"
)

METRICS_OUTPUT = (
    ARTIFACTS_DIR /
    "forecast_metrics.csv"
)

MODEL_FILE = "demand_forecast.pkl"

METADATA_FILE = "forecast_metadata.json"

# ==========================================================
# Load Dataset
# ==========================================================

def load_dataset():

    logger.info(
        "Loading daily sales..."
    )

    df = load_csv(
        INPUT_FILE,
        parse_dates=["Date"],
    )

    logger.info(
        "Shape : %s",
        df.shape,
    )

    return df

# ==========================================================
# Feature Preparation
# ==========================================================

def prepare_dataset(df):

    logger.info(
        "Preparing forecasting dataset..."
    )

    df = df.copy()

    df = df.dropna()

    FEATURES = [

        "Lag1",

        "Lag7",

        "Lag30",

        "RollingMean",

        "RollingStd",

        "RollingMin",

        "RollingMax",

        "RollingMedian",

    ]

    X = df[
        FEATURES
    ]

    y = df[
        "Revenue"
    ]

    return (

        X,

        y,

        df,

    )

# ==========================================================
# Train/Test Split
# ==========================================================

def split_dataset(
    X,
    y,
):

    split = int(
        len(X) * 0.80
    )

    X_train = X.iloc[:split]

    X_test = X.iloc[split:]

    y_train = y.iloc[:split]

    y_test = y.iloc[split:]

    return (

        X_train,

        X_test,

        y_train,

        y_test,

    )

# ==========================================================
# Train Model
# ==========================================================

def train_model(

    X_train,

    y_train,

):

    logger.info(
        "Training Random Forest Regressor..."
    )

    model = RandomForestRegressor(

        n_estimators=300,

        random_state=RANDOM_STATE,

    )

    model.fit(

        X_train,

        y_train,

    )

    return model

# ==========================================================
# Model Prediction
# ==========================================================

def predict(
    model,
    X_test,
):

    logger.info(
        "Generating predictions..."
    )

    predictions = model.predict(
        X_test
    )

    return predictions

# ==========================================================
# Model Evaluation
# ==========================================================

def evaluate_model(

    y_test,

    predictions,

):

    logger.info(
        "Evaluating forecasting model..."
    )

    mae = mean_absolute_error(

        y_test,

        predictions,

    )

    mse = mean_squared_error(

        y_test,

        predictions,

    )

    rmse = np.sqrt(mse)

    r2 = r2_score(

        y_test,

        predictions,

    )

    metrics = pd.DataFrame(

        {

            "Metric": [

                "MAE",

                "RMSE",

                "R2 Score",

            ],

            "Value": [

                mae,

                rmse,

                r2,

            ],

        }

    )

    return metrics

# ==========================================================
# Forecast Entire Dataset
# ==========================================================

def forecast_dataset(

    model,

    df,

):

    logger.info(
        "Forecasting historical demand..."
    )

    feature_columns = [

        "Lag1",

        "Lag7",

        "Lag30",

        "RollingMean",

        "RollingStd",

        "RollingMin",

        "RollingMax",

        "RollingMedian",

    ]

    forecast = df.copy()

    forecast["PredictedRevenue"] = model.predict(

        forecast[feature_columns]

    )

    forecast["ForecastError"] = (

        forecast["Revenue"]

        - forecast["PredictedRevenue"]

    )

    forecast["AbsoluteError"] = (

        forecast["ForecastError"]

        .abs()

    )

    return forecast

# ==========================================================
# Feature Importance
# ==========================================================

def feature_importance(

    model,

):

    importance = pd.DataFrame(

        {

            "Feature": [

                "Lag1",

                "Lag7",

                "Lag30",

                "RollingMean",

                "RollingStd",

                "RollingMin",

                "RollingMax",

                "RollingMedian",

            ],

            "Importance": model.feature_importances_,

        }

    )

    return importance.sort_values(

        "Importance",

        ascending=False,

    )

# ==========================================================
# Metadata
# ==========================================================

def create_metadata(

    metrics,

):

    metadata = {

        "project": "NeuralRetail",

        "generated_on": str(

            datetime.now()

        ),

        "algorithm": "RandomForestRegressor",

        "mae": float(

            metrics.loc[
                metrics["Metric"] == "MAE",
                "Value",
            ].iloc[0]
        ),

        "rmse": float(

            metrics.loc[
                metrics["Metric"] == "RMSE",
                "Value",
            ].iloc[0]
        ),

        "r2_score": float(

            metrics.loc[
                metrics["Metric"] == "R2 Score",
                "Value",
            ].iloc[0]
        ),

    }

    return metadata

# ==========================================================
# Save Outputs
# ==========================================================

def save_outputs(

    model,

    forecast,

    metrics,

    metadata,

):

    logger.info(
        "Saving forecasting artifacts..."
    )

    save_model(

        model,

        MODEL_FILE,

    )

    save_csv(

        forecast,

        FORECAST_OUTPUT,

    )

    save_csv(

        metrics,

        METRICS_OUTPUT,

    )

    save_json(

        metadata,

        METADATA_FILE,

    )

    logger.info(
        "Forecast artifacts saved."
    )

# ==========================================================
# Pipeline
# ==========================================================

@timer
def run_pipeline():

    logger.info("=" * 60)

    logger.info(
        "Starting Demand Forecasting Pipeline"
    )

    logger.info("=" * 60)

    df = load_dataset()

    X, y, cleaned = prepare_dataset(
        df
    )

    (

        X_train,

        X_test,

        y_train,

        y_test,

    ) = split_dataset(
        X,
        y,
    )

    model = train_model(

        X_train,

        y_train,

    )

    predictions = predict(

        model,

        X_test,

    )

    metrics = evaluate_model(

        y_test,

        predictions,

    )

    forecast = forecast_dataset(

        model,

        cleaned,

    )

    metadata = create_metadata(
        metrics
    )

    save_outputs(

        model,

        forecast,

        metrics,

        metadata,

    )

    logger.info("=" * 60)

    logger.info(
        "Demand Forecasting Completed"
    )

    logger.info("=" * 60)

    return (

        forecast,

        metrics,

        metadata,

    )

# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    (

        forecast,

        metrics,

        metadata,

    ) = run_pipeline()

    print("\n")

    print("=" * 60)

    print(
        "Demand Forecasting Completed"
    )

    print("=" * 60)

    print("\nForecast")

    print(forecast.head())

    print("\nMetrics")

    print(metrics)

    print("\nMetadata")

    for key, value in metadata.items():

        print(f"{key}: {value}")