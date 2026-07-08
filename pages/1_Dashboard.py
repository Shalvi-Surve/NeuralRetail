"""
============================================================
NeuralRetail
Executive Dashboard
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
    welcome_message,
)

from components.cards import (
    kpi_card,
    insight_card,
    section_header,
    status_card,
)

from components.charts import (
    line_chart,
    bar_chart,
    donut_chart,
)


# ==========================================================
# INITIALIZE
# ==========================================================

repo = initialize_dashboard("Executive Dashboard")


# ==========================================================
# LOAD DATA
# ==========================================================

summary = repo.business_summary()

daily_sales = repo.daily_sales()

customers = repo.customers()

products = repo.products()

segments = repo.segments()


# ==========================================================
# HEADER
# ==========================================================

page_header(

    title="Executive Dashboard",

    subtitle="AI Retail Intelligence Platform",

)

welcome_message()




# ==========================================================
# KPI SECTION
# ==========================================================

section_header(
    "📊 Executive KPIs",
    "Key business performance indicators"
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    kpi_card(

        "Revenue",

        f"₹ {summary['total_revenue']:,.0f}",

        "💰",

        "+12.8%",

    )

with c2:

    kpi_card(

        "Customers",

        f"{summary['total_customers']:,}",

        "👥",

        "+6.3%",

    )

with c3:

    kpi_card(

        "Orders",

        f"{summary['total_orders']:,}",

        "🛒",

        "+8.1%",

    )

with c4:

    kpi_card(

        "Products",

        f"{summary['total_products']:,}",

        "📦",

        "+2.5%",

    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# BUSINESS VISUALIZATIONS
# ==========================================================

left, right = st.columns(

    [1.8,1.2],

    gap="large",
)

with left:

    line_chart(

        daily_sales,

        x="Date",

        y="Revenue",

        title="Revenue Trend",

    )

with right:

    segment_counts = (

        segments

        .groupby("Segment")

        .size()

        .reset_index(name="Customers")

    )

    donut_chart(

        segment_counts,

        names="Segment",

        values="Customers",

        title="Customer Segments",

    )


st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# PRODUCT & CUSTOMER ANALYTICS
# ==========================================================

left, right = st.columns(
    2,
    gap="large"
)

with left:

    top_products = (

        products

        .sort_values(

            "TotalRevenue",

            ascending=False,

        )

        .head(10)

    )

    bar_chart(

        top_products,

        x="TotalRevenue",

        y="Description",

        title="Top Products",

        orientation="h",

    )

with right:

    top_customers = (

        customers

        .sort_values(

            "TotalRevenue",

            ascending=False,

        )

        .head(10)

    )

    bar_chart(

        top_customers,

        x="TotalRevenue",

        y="CustomerID",

        title="Top Customers",

        orientation="h",

    )


st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# AI EXECUTIVE SUMMARY
# ==========================================================

insight_card(

    "Executive Summary",

    f"""

### 📈 Performance Highlights

• Revenue generated: **₹ {summary['total_revenue']:,.0f}**

• Customers served: **{summary['total_customers']:,}**

• Orders processed: **{summary['total_orders']:,}**

• Repeat customer rate:
**{summary['repeat_customer_rate']:.1f}%**

• Best-selling product:
**{summary['top_product']}**

---

### 🤖 AI Interpretation

NeuralRetail indicates healthy business growth with
strong customer retention and consistent purchasing
patterns. Revenue concentration remains stable and
customer engagement is above average.

""",
)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# BUSINESS SNAPSHOT
# ==========================================================

section_header(
    "📌 Business Snapshot",
    "Quick overview of important retail metrics"
)

m1, m2, m3 = st.columns(3)

with m1:

    status_card(

        "Average Order Value",

        f"₹ {summary['average_order_value']:.2f}",

    )

with m2:

    status_card(

        "Repeat Customers",

        f"{summary['repeat_customer_rate']:.1f}%",

    )

with m3:

    status_card(

        "Top Product",

        summary["top_product"][:28],

    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# DATA PREVIEW
# ==========================================================

section_header(
    "🏆 Highest Revenue Customers"
)

from components.tables import data_table

data_table(top_customers)

section_header(
    "📦 Best Selling Products"
)

data_table(top_products)

# ==========================================================
# FOOTER
# ==========================================================

render_footer()