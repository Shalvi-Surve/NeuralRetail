"""
============================================================
NeuralRetail
Inventory Recommendation Engine
============================================================

Author  : Shalvi Surve
Project : NeuralRetail

Description
-----------
Generate inventory recommendations based on
historical sales demand.

Outputs
-------
artifacts/
    inventory_recommendations.csv
    inventory_summary.json
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd

import numpy as np

from utils import (
    ARTIFACTS_DIR,
    get_logger,
    load_csv,
    save_csv,
    save_json,
    timer,
)

from config import (
    SAFETY_STOCK_PERCENT,
)

logger = get_logger(__name__)

# ==========================================================
# Files
# ==========================================================

INPUT_FILE = (
    ARTIFACTS_DIR /
    "product_features.csv"
)

OUTPUT_FILE = (
    ARTIFACTS_DIR /
    "inventory_recommendations.csv"
)

SUMMARY_FILE = (
    ARTIFACTS_DIR /
    "inventory_summary.json"
)

# ==========================================================
# Load Dataset
# ==========================================================

def load_dataset():

    logger.info(
        "Loading product features..."
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
# Calculate Inventory Metrics
# ==========================================================

def calculate_inventory(
    df,
):

    logger.info(
        "Calculating inventory metrics..."
    )

    inventory = df.copy()

    inventory["AverageDailyDemand"] = (

        inventory["QuantitySold"]

        / 604

    )

    inventory["SafetyStock"] = (

        inventory["AverageDailyDemand"]

        * SAFETY_STOCK_PERCENT

    )

    inventory["RecommendedStock"] = (

        inventory["AverageDailyDemand"]

        * 30

    ) + inventory["SafetyStock"]

    return inventory

# ==========================================================
# Inventory Status
# ==========================================================

def assign_status(
    inventory,
):

    logger.info(
        "Assigning inventory status..."
    )

    conditions = [

        inventory["RecommendedStock"] >= 300,

        inventory["RecommendedStock"].between(
            100,
            300,
        ),

        inventory["RecommendedStock"] < 100,

    ]

    choices = [

        "Restock Immediately",

        "Monitor",

        "Sufficient",

    ]

    inventory["InventoryStatus"] = pd.Series(
        pd.Categorical(
            pd.Series(
                pd.Series(index=inventory.index)
            )
        )
    )

    inventory["InventoryStatus"] = pd.Series(
        np.select(
            conditions,
            choices,
            default="Monitor",
        )
    )

    return inventory

# ==========================================================
# Restock Priority
# ==========================================================

def assign_priority(
    inventory,
):
    """
    Assign restocking priority.
    """

    logger.info(
        "Calculating restock priority..."
    )

    inventory = inventory.copy()

    inventory["PriorityScore"] = (

        inventory["TotalRevenue"] * 0.50

        +

        inventory["QuantitySold"] * 0.30

        +

        inventory["CustomerCount"] * 0.20

    )

    inventory = inventory.sort_values(

        "PriorityScore",

        ascending=False,

    )

    inventory = inventory.reset_index(drop=True)

    inventory["PriorityRank"] = inventory.index + 1

    return inventory

# ==========================================================
# Inventory Summary
# ==========================================================

def create_summary(
    inventory,
):
    """
    Generate inventory KPIs.
    """

    summary = {

        "project": "NeuralRetail",

        "generated_on": str(

            datetime.now()

        ),

        "total_products": int(

            inventory.shape[0]

        ),

        "restock_immediately": int(

            (

                inventory["InventoryStatus"]

                == "Restock Immediately"

            ).sum()

        ),

        "monitor_products": int(

            (

                inventory["InventoryStatus"]

                == "Monitor"

            ).sum()

        ),

        "sufficient_stock": int(

            (

                inventory["InventoryStatus"]

                == "Sufficient"

            ).sum()

        ),

        "highest_priority_product": str(

            inventory.iloc[0]["Description"]

        ),

    }

    return summary

# ==========================================================
# Save Outputs
# ==========================================================

def save_outputs(

    inventory,

    summary,

):
    """
    Save inventory artifacts.
    """

    logger.info(
        "Saving inventory outputs..."
    )

    save_csv(

        inventory,

        OUTPUT_FILE,

    )

    save_json(

        summary,

        SUMMARY_FILE,

    )

    logger.info(
        "Inventory artifacts saved."
    )

# ==========================================================
# Pipeline
# ==========================================================

@timer
def run_pipeline():

    logger.info("=" * 60)

    logger.info(
        "Starting Inventory Recommendation Engine"
    )

    logger.info("=" * 60)

    products = load_dataset()

    inventory = calculate_inventory(

        products,

    )

    inventory = assign_status(

        inventory,

    )

    inventory = assign_priority(

        inventory,

    )

    summary = create_summary(

        inventory,

    )

    save_outputs(

        inventory,

        summary,

    )

    logger.info("=" * 60)

    logger.info(
        "Inventory Recommendation Completed"
    )

    logger.info("=" * 60)

    return (

        inventory,

        summary,

    )

# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    (

        inventory,

        summary,

    ) = run_pipeline()

    print("\n")

    print("=" * 60)

    print(
        "Inventory Recommendation Completed"
    )

    print("=" * 60)

    print("\nInventory")

    print(

        inventory.head()

    )

    print("\nSummary")

    for key, value in summary.items():

        print(

            f"{key}: {value}"

        )

