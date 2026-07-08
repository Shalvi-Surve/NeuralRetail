"""
============================================================
NeuralRetail
Customer Intelligence Center
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
    scatter_chart,
    histogram,
)

from components.tables import (
    data_table,
    download_csv,
)


# ==========================================================
# INITIALIZE
# ==========================================================

repo = initialize_dashboard("Customer Intelligence")


# ==========================================================
# LOAD DATA
# ==========================================================

customers = repo.customers()

segments = repo.segments()

rfm = repo.rfm()


# ==========================================================
# HEADER
# ==========================================================

page_header(

    title="Customer Intelligence",

    subtitle="AI-powered Customer Analytics",

)

st.markdown(
"""
Understand customer behaviour, identify your highest-value
customers, analyze lifetime value, and explore customer
segments generated using Machine Learning.
"""
)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# SEARCH CUSTOMER
# ==========================================================

customer_ids = sorted(
    customers["CustomerID"].astype(int).unique()
)

selected_customer = st.selectbox(

    "🔍 Search Customer",

    customer_ids,

)

customer = customers[
    customers["CustomerID"] == selected_customer
].iloc[0]


# ==========================================================
# KPI CARDS
# ==========================================================

section_header(
    "📊 Customer Profile",
    "Complete overview of the selected customer"
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    kpi_card(

        "Lifetime Value",

        f"₹ {customer['CustomerLifetimeValue']:,.0f}",

        "💰",

    )

with c2:

    kpi_card(

        "Revenue",

        f"₹ {customer['TotalRevenue']:,.0f}",

        "📈",

    )

with c3:

    kpi_card(

        "Orders",

        f"{int(customer['InvoiceCount'])}",

        "🛒",

    )

with c4:

    kpi_card(

        "Products",

        f"{int(customer['ProductVariety'])}",

        "📦",

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# CUSTOMER DETAILS
# ==========================================================

section_header(
    "👤 Customer Overview",
    "Detailed customer behaviour metrics"
)

left, right = st.columns([1,1])

with left:

    status_card(

        "Average Order Value",

        f"₹ {customer['AverageOrderValue']:.2f}"

    )

    status_card(

        "Average Quantity",

        f"{customer['AverageQuantity']:.2f}"

    )

    status_card(

        "Revenue Contribution",

        f"{customer['RevenueContribution']:.2f}%"

    )

with right:

    status_card(

        "Recency",

        int(customer["Recency"])

    )

    status_card(

        "Frequency",

        int(customer["Frequency"])

    )

    status_card(

        "Monetary",

        f"₹ {customer['Monetary']:,.0f}"

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# SEGMENT DISTRIBUTION
# ==========================================================

left, right = st.columns(
    [1.2,1.8],
    gap="large",
)

with left:

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

        title="Top Revenue Customers",

        orientation="h",

    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# CUSTOMER VALUE ANALYSIS
# ==========================================================

section_header(

    "📈 Customer Value Analysis",

    "Relationships between purchasing behaviour and customer value"

)

left, right = st.columns(
    2,
    gap="large",
)

with left:

    scatter_chart(

        df=customers,

        x="Frequency",

        y="Monetary",

        color="RevenueContribution",

        title="Frequency vs Monetary Value",

    )

with right:

    scatter_chart(

        df=customers,

        x="CustomerLifetimeValue",

        y="TotalRevenue",

        color="RevenueContribution",

        title="Customer Lifetime Value",

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# CUSTOMER DISTRIBUTIONS
# ==========================================================

section_header(

    "📊 Customer Distributions",

    "Revenue and lifetime value spread"

)

left, right = st.columns(
    2,
    gap="large",
)

with left:

    histogram(

        df=customers,

        column="TotalRevenue",

        title="Revenue Distribution",

    )

with right:

    histogram(

        df=customers,

        column="CustomerLifetimeValue",

        title="Lifetime Value Distribution",

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# RFM ANALYSIS
# ==========================================================

section_header(

    "🎯 RFM Analysis",

    "Recency • Frequency • Monetary scoring"

)

rfm_preview = (

    rfm

    .sort_values(

        "Monetary",

        ascending=False,

    )

    .head(15)

)

data_table(

    rfm_preview,

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# TOP CUSTOMERS TABLE
# ==========================================================

section_header(

    "🏆 Highest Revenue Customers"

)

top20 = (

    customers

    .sort_values(

        "TotalRevenue",

        ascending=False,

    )

    .head(20)

)

data_table(

    top20,

)

download_csv(

    top20,

    "top_customers.csv",

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# CUSTOMER SEGMENT SUMMARY
# ==========================================================

section_header(

    "👥 Customer Segment Summary"

)

segment_summary = (

    segments

    .groupby("Segment")

    .agg(

        Customers=("CustomerID", "count"),

        Revenue=("TotalRevenue", "sum"),

        AvgRevenue=("TotalRevenue", "mean"),

        AvgOrders=("InvoiceCount", "mean"),

    )

    .reset_index()

)

data_table(

    segment_summary,

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# CUSTOMER LEADERBOARD
# ==========================================================

section_header(

    "🥇 Customer Leaderboard"

)

leaderboard = (

    customers

    .sort_values(

        [

            "CustomerLifetimeValue",

            "TotalRevenue",

        ],

        ascending=False,

    )[

        [

            "CustomerID",

            "CustomerLifetimeValue",

            "TotalRevenue",

            "InvoiceCount",

            "RevenueContribution",

        ]

    ]

    .head(15)

)

data_table(

    leaderboard,

)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# CUSTOMER STATISTICS
# ==========================================================

st.subheader("📈 Customer Statistics")

c1, c2, c3, c4 = st.columns(4)

with c1:

    status_card (
        
        "Total Customers",
    
        f"{len(customers):,}",
    
    )

with c2:

    status_card (

        "VIP Customers",

        f"{len(segments[segments['Segment']=='VIP Customers']):,}"

    )

with c3:
    
    status_card(

        "Average Revenue",

        f"₹ {customers['TotalRevenue'].mean():,.0f}"

    )

with c4:
    
    status_card(

        "Average CLV",

        f"₹ {customers['CustomerLifetimeValue'].mean():,.0f}"

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# AI CUSTOMER INSIGHTS
# ==========================================================

vip_count = len(

    segments[

        segments["Segment"] == "VIP Customers"

    ]

)

high_value = len(

    segments[

        segments["Segment"] == "High Value Customers"

    ]

)

top_customer = customers.loc[

    customers["TotalRevenue"].idxmax()

]

insight_card(

    "AI Customer Insights",

    f"""

### Customer Intelligence Summary

• NeuralRetail currently manages **{len(customers):,} customers**.

• Machine Learning identified **{vip_count} VIP Customers**
who generate the highest business value.

• **{high_value:,} customers** belong to the High Value segment.

• The highest revenue customer is **Customer {int(top_customer['CustomerID'])}**
with lifetime revenue of **₹ {top_customer['TotalRevenue']:,.0f}**.

• Customer Lifetime Value distribution indicates that
a small percentage of customers contribute a significant
portion of total revenue.

### Recommendations

✅ Reward VIP customers with exclusive loyalty benefits.

✅ Target High Value customers with premium offers.

✅ Increase engagement for low-frequency customers.

✅ Use churn predictions to retain valuable customers.

""",

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# COMPLETE CUSTOMER DATA
# ==========================================================

with st.expander(

    "📄 View Complete Customer Dataset",

    expanded=False,

):

    data_table(

        customers,

        height=500,

    )

    download_csv(

        customers,

        "customer_features.csv",

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# BUSINESS RECOMMENDATIONS
# ==========================================================

section_header(
    
    "💡 Recommended Business Actions"

)

insight_card(

    "Business Recommendations",

    """

✅ Prioritize VIP customers for premium campaigns.

✅ Reward loyal customers.

✅ Increase engagement for low-frequency customers.

✅ Use churn prediction to retain valuable customers.

✅ Promote cross-selling for high-value customers.

"""

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# PAGE FOOTER
# ==========================================================

render_footer()