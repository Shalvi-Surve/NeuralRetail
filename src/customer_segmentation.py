"""
============================================================
NeuralRetail
Customer Segmentation Engine
============================================================

Author  : Shalvi Surve
Project : NeuralRetail

Description
-----------
Performs customer segmentation using K-Means clustering
on engineered customer features.

Pipeline
--------
1. Load customer features
2. Validate dataset
3. Select clustering features
4. Standardize data
5. Find optimal number of clusters
6. Train KMeans model
7. Generate customer segments
8. Create business summaries
9. Save artifacts

Outputs
-------
artifacts/
    customer_segments.csv
    cluster_summary.csv

models/
    customer_clusters.pkl
    customer_scaler.pkl
    cluster_profile.json
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from config import (
    RANDOM_STATE,
    MIN_CLUSTERS,
    MAX_CLUSTERS,
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

INPUT_FILE = ARTIFACTS_DIR / "customer_features.csv"

SEGMENT_OUTPUT = (
    ARTIFACTS_DIR /
    "customer_segments.csv"
)

SUMMARY_OUTPUT = (
    ARTIFACTS_DIR /
    "cluster_summary.csv"
)

MODEL_FILE = "customer_clusters.pkl"

SCALER_FILE = "customer_scaler.pkl"

PROFILE_FILE = "cluster_profile.json"


# ==========================================================
# Required Features
# ==========================================================

FEATURE_COLUMNS = [

    "Recency",

    "Frequency",

    "Monetary",

    "AverageOrderValue",

    "InvoiceCount",

    "ProductVariety",

    "CustomerLifetimeValue",

    "RevenueContribution",
]

# ==========================================================
# Load Customer Dataset
# ==========================================================

def load_customer_data() -> pd.DataFrame:
    """
    Load engineered customer dataset.
    """

    logger.info(
        "Loading customer features..."
    )

    df = load_csv(INPUT_FILE)

    logger.info(
        "Customer Shape : %s",
        df.shape,
    )

    return df


# ==========================================================
# Dataset Validation
# ==========================================================

def validate_dataset(
    df: pd.DataFrame,
):
    """
    Validate required columns.
    """

    missing = [

        column

        for column in FEATURE_COLUMNS

        if column not in df.columns

    ]

    if missing:

        raise ValueError(

            f"Missing columns: {missing}"

        )

    logger.info(
        "Dataset validation successful."
    )

# ==========================================================
# Feature Selection
# ==========================================================

def select_features(
    df: pd.DataFrame,
):
    """
    Select numerical features used for clustering.
    """

    logger.info(
        "Selecting clustering features..."
    )

    x = df[
        FEATURE_COLUMNS
    ].copy()

    return x


# ==========================================================
# Feature Scaling
# ==========================================================

def scale_features(
    features: pd.DataFrame,
):
    """
    Standardize feature values.
    """

    logger.info(
        "Scaling features..."
    )

    scaler = StandardScaler()

    scaled = scaler.fit_transform(
        features
    )

    logger.info(
        "Scaling completed."
    )

    return scaled, scaler

# ==========================================================
# Find Optimal K
# ==========================================================

def find_best_clusters(
    data,
):
    """
    Determine optimal number of clusters
    using Silhouette Score.
    """

    logger.info(
        "Searching for optimal K..."
    )

    best_k = 2

    best_score = -1

    scores = []

    for k in range(
        MIN_CLUSTERS,
        MAX_CLUSTERS + 1,
    ):

        model = KMeans(

            n_clusters=k,

            random_state=RANDOM_STATE,

            n_init=20,

        )

        labels = model.fit_predict(
            data
        )

        score = silhouette_score(

            data,

            labels,

        )

        scores.append(

            {

                "k": k,

                "score": score,

            }

        )

        logger.info(

            "k=%d | silhouette=%.4f",

            k,

            score,

        )

        if score > best_score:

            best_score = score

            best_k = k

    logger.info(

        "Best Cluster Count : %d",

        best_k,

    )

    return (

        best_k,

        best_score,

        scores,

    )

# ==========================================================
# Train KMeans Model
# ==========================================================

def train_model(
    data,
    n_clusters: int,
):
    """
    Train final KMeans model.
    """

    logger.info(
        "Training final KMeans model..."
    )

    model = KMeans(
        n_clusters=n_clusters,
        random_state=RANDOM_STATE,
        n_init=20,
    )

    labels = model.fit_predict(data)

    logger.info(
        "Model training completed."
    )

    return model, labels

# ==========================================================
# Attach Cluster Labels
# ==========================================================

def assign_clusters(
    df: pd.DataFrame,
    labels,
):
    """
    Add cluster labels to customer dataset.
    """

    logger.info(
        "Assigning cluster labels..."
    )

    segmented = df.copy()

    segmented["Cluster"] = labels

    return segmented

# ==========================================================
# Cluster Statistics
# ==========================================================

def create_cluster_summary(
    segmented: pd.DataFrame,
):
    """
    Create cluster level summary.
    """

    logger.info(
        "Generating cluster summary..."
    )

    summary = (

        segmented

        .groupby("Cluster")

        .agg(

            Customers=("CustomerID", "count"),

            AverageRevenue=(

                "TotalRevenue",

                "mean",

            ),

            AverageCLV=(

                "CustomerLifetimeValue",

                "mean",

            ),

            AverageRecency=(

                "Recency",

                "mean",

            ),

            AverageFrequency=(

                "Frequency",

                "mean",

            ),

        )

        .reset_index()

    )

    return summary

# ==========================================================
# Business Segment Names
# ==========================================================

def assign_segment_names(
    segmented: pd.DataFrame,
    summary: pd.DataFrame,
):
    """
    Convert Cluster IDs into business names.
    """

    logger.info(
        "Assigning business segment names..."
    )

    ranking = (

        summary

        .sort_values(

            "AverageCLV",

            ascending=False,

        )

        ["Cluster"]

        .tolist()

    )

    names = [

        "VIP Customers",

        "High Value Customers",

        "Loyal Customers",

        "Potential Loyalists",

        "Regular Customers",

        "At Risk Customers",

        "Dormant Customers",

    ]

    mapping = {}

    for cluster, name in zip(
        ranking,
        names,
    ):

        mapping[cluster] = name

    segmented["Segment"] = (

        segmented["Cluster"]

        .map(mapping)

    )

    summary["Segment"] = (

        summary["Cluster"]

        .map(mapping)

    )

    return segmented, summary

# ==========================================================
# Segment Ranking
# ==========================================================

def assign_segment_rank(
    segmented: pd.DataFrame,
):
    """
    Rank customers inside every segment.
    """

    logger.info(
        "Ranking customers..."
    )

    segmented = segmented.sort_values(

        [

            "CustomerLifetimeValue",

            "TotalRevenue",

        ],

        ascending=False,

    )

    segmented["SegmentRank"] = (

        segmented

        .groupby("Segment")

        .cumcount()

        + 1

    )

    return segmented

# ==========================================================
# Cluster Profile Metadata
# ==========================================================

def create_cluster_profile(
    n_clusters: int,
    score: float,
):
    """
    Create metadata describing
    the clustering model.
    """
    from config import PROJECT_NAME, VERSION

    profile = {
        "project": PROJECT_NAME,
        
        "version": VERSION,

        "algorithm": "KMeans",

        "clusters": n_clusters,

        "silhouette_score": round(

            score,

            4,

        ),

        "generated_on": str(

            datetime.now()

        ),

        "features_used": FEATURE_COLUMNS,

    }

    return profile

# ==========================================================
# Save Outputs
# ==========================================================

def save_outputs(
    model,
    scaler,
    segmented: pd.DataFrame,
    summary: pd.DataFrame,
    profile: dict,
):
    """
    Save all segmentation artifacts.
    """

    logger.info(
        "Saving segmentation artifacts..."
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
        segmented,
        SEGMENT_OUTPUT,
    )

    save_csv(
        summary,
        SUMMARY_OUTPUT,
    )

    save_json(
        profile,
        PROFILE_FILE,
    )

    logger.info(
        "Artifacts saved successfully."
    )

# ==========================================================
# Pipeline
# ==========================================================

@timer
def run_pipeline():
    """
    Execute complete customer
    segmentation pipeline.
    """

    logger.info("=" * 60)
    logger.info(
        "Starting Customer Segmentation"
    )
    logger.info("=" * 60)

    # ---------------------------------
    # Load Dataset
    # ---------------------------------

    df = load_customer_data()

    validate_dataset(df)

    # ---------------------------------
    # Feature Selection
    # ---------------------------------

    features = select_features(df)

    scaled_data, scaler = scale_features(
        features
    )

    # ---------------------------------
    # Optimal K
    # ---------------------------------

    (
        best_k,
        best_score,
        scores,
    ) = find_best_clusters(
        scaled_data
    )

    # ---------------------------------
    # Train Model
    # ---------------------------------

    model, labels = train_model(

        scaled_data,

        best_k,

    )

    segmented = assign_clusters(

        df,

        labels,

    )

    # ---------------------------------
    # Cluster Summary
    # ---------------------------------

    summary = create_cluster_summary(

        segmented,

    )

    segmented, summary = assign_segment_names(

        segmented,

        summary,

    )

    segmented = assign_segment_rank(

        segmented,

    )

    # ---------------------------------
    # Metadata
    # ---------------------------------

    profile = create_cluster_profile(

        best_k,

        best_score,

    )

    profile["cluster_scores"] = scores

    # ---------------------------------
    # Save Everything
    # ---------------------------------

    save_outputs(

        model,

        scaler,

        segmented,

        summary,

        profile,

    )

    logger.info("=" * 60)
    logger.info(
        "Customer Segmentation Completed"
    )
    logger.info("=" * 60)

    return (

        segmented,

        summary,

        profile,

    )

# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    (
        customer_segments,
        cluster_summary,
        cluster_profile,
    ) = run_pipeline()

    print("\n")

    print("=" * 60)
    print("Customer Segmentation Completed")
    print("=" * 60)

    print("\nCustomer Segments")

    print(customer_segments.head())

    print("\nCluster Summary")

    print(cluster_summary)

    print("\nCluster Profile")

    for key, value in cluster_profile.items():

        print(f"{key}: {value}")

