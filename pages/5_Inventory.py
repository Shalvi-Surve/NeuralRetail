"""
============================================================
NeuralRetail
Inventory Command Center
============================================================

Author : Shalvi Surve
Project : NeuralRetail
"""

from __future__ import annotations

import streamlit as st

from src.dashboard_base import (
    initialize_dashboard,
    render_footer,
)

from components.header import (
    page_header,
)

from components.cards import (
    kpi_card,
    insight_card,
    status_card,
    section_header,
)

from components.charts import (
    donut_chart,
    bar_chart,
)

from components.tables import (
    data_table,
    download_csv,
)


# ==========================================================
# INITIALIZE
# ==========================================================

repo = initialize_dashboard("Inventory Command Center")


# ==========================================================
# LOAD DATA
# ==========================================================

inventory = repo.inventory()

summary = repo.inventory_summary()


# ==========================================================
# HEADER
# ==========================================================

page_header(

    title="Inventory Command Center",

    subtitle="AI-powered Inventory Optimization",

)

st.markdown(
"""
Monitor inventory health, identify products requiring
immediate restocking, and prioritize inventory decisions
using Machine Learning recommendations.
"""
)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# KPI CARDS
# ==========================================================

section_header(
    "📦 Inventory KPIs",
    "Current inventory health across the business"
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    kpi_card(

        "Products",

        f"{summary['total_products']:,}",

        "📦",

    )

with c2:

    kpi_card(

        "Restock Now",

        f"{summary['restock_immediately']:,}",

        "🚨",

    )

with c3:

    kpi_card(

        "Monitor",

        f"{summary['monitor_products']:,}",

        "👀",

    )

with c4:

    kpi_card(

        "Healthy Stock",

        f"{summary['sufficient_stock']:,}",

        "✅",

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# INVENTORY STATUS
# ==========================================================

left, right = st.columns(
    [1,2],
    gap="large",
)

with left:

    status = (

        inventory

        .groupby("InventoryStatus")

        .size()

        .reset_index(name="Products")

    )

    donut_chart(

        status,

        names="InventoryStatus",

        values="Products",

        title="Inventory Status",

    )

with right:

    highest_priority = (

        inventory

        .sort_values(

            "PriorityRank"

        )

        .head(10)

    )

    bar_chart(

        highest_priority,

        x="PriorityRank",

        y="Description",

        title="Highest Priority Products",

        orientation="h",

    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# RESTOCK RECOMMENDATIONS
# ==========================================================

section_header(
    "🚨 Immediate Restock",
    "Products that require urgent replenishment"
)

restock = (

    inventory

    .query("InventoryStatus == 'Restock Immediately'")

    .sort_values(

        "PriorityRank"

    )

)

st.caption(
    f"Displaying {len(restock)} products requiring immediate replenishment."
)

data_table(

    restock[

        [

            "StockCode",

            "Description",

            "PriorityRank",

            "InventoryStatus",

            "PopularityScore",

        ]

    ]

)

download_csv(

    restock,

    "restock_recommendations.csv",

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# POPULAR PRODUCTS
# ==========================================================

section_header(
    "🔥 Popular Products",
    "Products driving the highest customer demand"
)

popular = (

    inventory

    .sort_values(

        "PopularityScore",

        ascending=False,

    )

    .head(15)

)

bar_chart(

    popular,

    x="PopularityScore",

    y="Description",

    title="Popularity Ranking",

    orientation="h",

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# INVENTORY SUMMARY
# ==========================================================

section_header(
    "📊 Inventory Status",
    "Overall stock health and restocking priorities"
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    
    status_card(

        "Total Products",

        f"{summary['total_products']:,}"

    )

with c2:
    
    status_card(

        "Immediate Restock",

        f"{summary['restock_immediately']:,}"

    )

with c3:
    
    status_card(

        "Monitor Products",

        f"{summary['monitor_products']:,}"

    )

with c4:
    
    status_card(

        "Healthy Stock",

        f"{summary['sufficient_stock']:,}"

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# AI INVENTORY INSIGHTS
# ==========================================================

highest = inventory.loc[
    inventory["PriorityRank"].idxmin()
]

insight_card(

    "AI Inventory Insights",

    f"""

### 📦 Inventory Overview

• NeuralRetail currently manages **{summary['total_products']:,} products**.

• **{summary['restock_immediately']:,} products** require immediate replenishment.

• **{summary['monitor_products']:,} products** should be monitored closely.

• **{summary['sufficient_stock']:,} products** currently have healthy inventory levels.

---

### ⭐ Highest Priority Product

**{highest['Description']}**

Stock Code:
**{highest['StockCode']}**

Priority Rank:
**#{int(highest['PriorityRank'])}**

---

### 💡 Recommendations

✅ Restock high-priority products immediately.

✅ Increase procurement for popular products.

✅ Reduce excess inventory of slow-moving products.

✅ Combine inventory planning with demand forecasting.

"""
)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# COMPLETE INVENTORY DATA
# ==========================================================

with st.expander(

    "📄 View Complete Inventory Dataset",

    expanded=False,

):

    data_table(

        inventory,

        height=500,

    )

    download_csv(

        inventory,

        "inventory_recommendations.csv",

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# BUSINESS ACTIONS
# ==========================================================

section_header(
    "📊 Inventory Statistics",
    "Quick operational inventory overview"
)

insight_card(

    "Business Recommendations",

    """

✅ Restock products marked as *Restock Immediately.*

✅ Review Monitor products weekly.

✅ Combine inventory planning with demand forecasts.

✅ Increase stock before seasonal demand.

✅ Continuously monitor inventory health.

"""

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# FOOTER
# ==========================================================

render_footer() 

