"""
============================================================
NeuralRetail
Customer Churn Prediction Engine
============================================================

Author  : Shalvi Surve
Project : NeuralRetail

Description
-----------
Predict customer churn using supervised machine learning.

Outputs
-------
artifacts/
    customer_churn_predictions.csv
    classification_report.csv

models/
    churn_classifier.pkl
    churn_scaler.pkl
    churn_metadata.json
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

from xgboost import XGBClassifier

from config import (
    RANDOM_STATE,
    CHURN_THRESHOLD,
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

logger = get_logger(__name__)

# ==========================================================
# Project Files
# ==========================================================

INPUT_FILE = (
    ARTIFACTS_DIR /
    "customer_features.csv"
)

PREDICTION_OUTPUT = (
    ARTIFACTS_DIR /
    "customer_churn_predictions.csv"
)

REPORT_OUTPUT = (
    ARTIFACTS_DIR /
    "classification_report.csv"
)

MODEL_FILE = "churn_classifier.pkl"

SCALER_FILE = "churn_scaler.pkl"

METADATA_FILE = "churn_metadata.json"


# ==========================================================
# Features
# ==========================================================

FEATURE_COLUMNS = [

    "Frequency",

    "Monetary",

    "TotalRevenue",

    "InvoiceCount",

    "ProductVariety",

    "AverageOrderValue",

    "CustomerLifetimeValue",

    "RevenueContribution",

]

# ==========================================================
# Load Dataset
# ==========================================================

def load_dataset():

    logger.info(
        "Loading customer dataset..."
    )

    df = load_csv(
        INPUT_FILE
    )

    logger.info(
        "Shape : %s",
        df.shape,
    )

    return df

# ==========================================================
# Create Churn Labels
# ==========================================================

def generate_labels(df):

    logger.info(
        "Generating churn labels..."
    )

    df = df.copy()

    df["Churn"] = (

        df["Recency"] > 90

    ).astype(int)

    return df

# ==========================================================
# Feature Selection
# ==========================================================

def prepare_dataset(df):

    logger.info(
        "Preparing dataset..."
    )

    X = df[
        FEATURE_COLUMNS
    ]

    y = df[
        "Churn"
    ]

    return X, y

# ==========================================================
# Train Test Split
# ==========================================================

def split_dataset(
    X,
    y,
):

    logger.info(
        "Splitting dataset..."
    )

    return train_test_split(

        X,

        y,

        test_size=0.20,

        random_state=RANDOM_STATE,

        stratify=y,

    )

# ==========================================================
# Feature Scaling
# ==========================================================

def scale_dataset(

    X_train,

    X_test,

):

    logger.info(
        "Scaling dataset..."
    )

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(
        X_train
    )

    X_test_scaled = scaler.transform(
        X_test
    )

    return (

        X_train_scaled,

        X_test_scaled,

        scaler,

    )

# ==========================================================
# Train Logistic Regression
# ==========================================================

def train_logistic_regression(
    X_train,
    y_train,
):

    logger.info(
        "Training Logistic Regression..."
    )

    model = LogisticRegression(
        random_state=RANDOM_STATE,
        max_iter=1000,
    )

    model.fit(
        X_train,
        y_train,
    )

    return model

# ==========================================================
# Train Random Forest
# ==========================================================

def train_random_forest(
    X_train,
    y_train,
):

    logger.info(
        "Training Random Forest..."
    )

    model = RandomForestClassifier(

        n_estimators=300,

        max_depth=10,

        random_state=RANDOM_STATE,

    )

    model.fit(
        X_train,
        y_train,
    )

    return model

# ==========================================================
# Train XGBoost
# ==========================================================

def train_xgboost(
    X_train,
    y_train,
):

    logger.info(
        "Training XGBoost..."
    )

    model = XGBClassifier(

        random_state=RANDOM_STATE,

        learning_rate=0.05,

        n_estimators=300,

        max_depth=6,

        subsample=0.9,

        colsample_bytree=0.9,

        eval_metric="logloss",

    )

    model.fit(

        X_train,

        y_train,

    )

    return model

# ==========================================================
# Evaluate Model
# ==========================================================

def evaluate_model(

    model,

    X_test,

    y_test,

):

    predictions = model.predict(
        X_test
    )

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    metrics = {

        "Accuracy": accuracy_score(

            y_test,

            predictions,

        ),

        "Precision": precision_score(

            y_test,

            predictions,

            zero_division=0,

        ),

        "Recall": recall_score(

            y_test,

            predictions,

            zero_division=0,

        ),

        "F1": f1_score(

            y_test,

            predictions,

            zero_division=0,

        ),

        "ROC_AUC": roc_auc_score(

            y_test,

            probabilities,

        ),

    }

    return metrics

# ==========================================================
# Compare Models
# ==========================================================

def compare_models(

    X_train,

    y_train,

    X_test,

    y_test,

):

    logger.info(
        "Comparing machine learning models..."
    )

    models = {

        "Logistic Regression":

        train_logistic_regression(

            X_train,

            y_train,

        ),

        "Random Forest":

        train_random_forest(

            X_train,

            y_train,

        ),

        "XGBoost":

        train_xgboost(

            X_train,

            y_train,

        ),

    }

    results = []

    best_model = None

    best_name = None

    best_score = -1

    for name, model in models.items():

        metrics = evaluate_model(

            model,

            X_test,

            y_test,

        )

        metrics["Model"] = name

        results.append(metrics)

        logger.info(

            "%s | F1 = %.4f",

            name,

            metrics["F1"],

        )

        if metrics["F1"] > best_score:

            best_score = metrics["F1"]

            best_model = model

            best_name = name

    report = pd.DataFrame(results)

    logger.info(

        "Best Model : %s",

        best_name,

    )

    return (

        best_model,

        best_name,

        report,

    )

# ==========================================================
# Predict Entire Dataset
# ==========================================================

def predict_all_customers(

    model,

    scaler,

    df,

):

    logger.info(
        "Predicting churn probabilities..."
    )

    features = df[
        FEATURE_COLUMNS
    ]

    scaled = scaler.transform(
        features
    )

    probabilities = model.predict_proba(
        scaled
    )[:, 1]

    predictions = model.predict(
        scaled
    )

    output = df.copy()

    output["ChurnProbability"] = probabilities

    output["PredictedChurn"] = predictions

    output["RiskLevel"] = pd.cut(

        output["ChurnProbability"],

        bins=[

            -0.01,

            0.30,

            0.60,

            1.00,

        ],

        labels=[

            "Low",

            "Medium",

            "High",

        ],

    )

    return output

# ==========================================================
# Create Metadata
# ==========================================================

def create_metadata(
    model_name: str,
    report: pd.DataFrame,
):
    """
    Create metadata for the selected churn model.
    """

    metrics = report[
        report["Model"] == model_name
    ].iloc[0]

    metadata = {

        "project": "NeuralRetail",

        "generated_on": str(
            datetime.now()
        ),

        "best_model": model_name,

        "accuracy": round(
            float(metrics["Accuracy"]),
            4,
        ),

        "precision": round(
            float(metrics["Precision"]),
            4,
        ),

        "recall": round(
            float(metrics["Recall"]),
            4,
        ),

        "f1_score": round(
            float(metrics["F1"]),
            4,
        ),

        "roc_auc": round(
            float(metrics["ROC_AUC"]),
            4,
        ),

    }

    return metadata

# ==========================================================
# Save Outputs
# ==========================================================

def save_outputs(

    model,

    scaler,

    predictions,

    report,

    metadata,

):

    logger.info(
        "Saving churn prediction artifacts..."
    )

    save_model(
        model,
        MODEL_FILE,
    )

    save_model(
        scaler,
        SCALER_FILE,
    )

    save_csv(
        predictions,
        PREDICTION_OUTPUT,
    )

    save_csv(
        report,
        REPORT_OUTPUT,
    )

    save_json(
        metadata,
        METADATA_FILE,
    )

    logger.info(
        "Artifacts saved successfully."
    )

# ==========================================================
# Pipeline
# ==========================================================

@timer
def run_pipeline():

    logger.info("=" * 60)
    logger.info(
        "Starting Churn Prediction Pipeline"
    )
    logger.info("=" * 60)

    # ---------------------------------
    # Load Dataset
    # ---------------------------------

    df = load_dataset()

    df = generate_labels(df)

    # ---------------------------------
    # Features
    # ---------------------------------

    X, y = prepare_dataset(df)

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = split_dataset(
        X,
        y,
    )

    (
        X_train_scaled,
        X_test_scaled,
        scaler,
    ) = scale_dataset(

        X_train,

        X_test,

    )

    # ---------------------------------
    # Train Models
    # ---------------------------------

    (
        best_model,
        best_name,
        report,
    ) = compare_models(

        X_train_scaled,

        y_train,

        X_test_scaled,

        y_test,

    )

    # ---------------------------------
    # Predict Entire Dataset
    # ---------------------------------

    predictions = predict_all_customers(

        best_model,

        scaler,

        df,

    )

    # ---------------------------------
    # Metadata
    # ---------------------------------

    metadata = create_metadata(

        best_name,

        report,

    )

    # ---------------------------------
    # Save Outputs
    # ---------------------------------

    save_outputs(

        best_model,

        scaler,

        predictions,

        report,

        metadata,

    )

    logger.info("=" * 60)
    logger.info(
        "Churn Prediction Completed"
    )
    logger.info("=" * 60)

    return (

        predictions,

        report,

        metadata,

    )

# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    (
        predictions,
        report,
        metadata,
    ) = run_pipeline()

    print("\n")

    print("=" * 60)
    print("Churn Prediction Completed")
    print("=" * 60)

    print("\nPredictions")

    print(
        predictions.head()
    )

    print("\nModel Comparison")

    print(report)

    print("\nMetadata")

    for key, value in metadata.items():

        print(f"{key}: {value}")

