"""
============================================================
NeuralRetail
Customer Churn Prediction Center
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
    gauge_chart,
    donut_chart,
    histogram,
    bar_chart,
)

from components.tables import (
    data_table,
    download_csv,
)


# ==========================================================
# INITIALIZE
# ==========================================================

repo = initialize_dashboard("Customer Churn Center")


# ==========================================================
# LOAD DATA
# ==========================================================

customers = repo.customers()

segments = repo.segments()

churn = repo.churn()

classification = repo.classification_report()

churn = churn.merge(

    segments[
        [
            "CustomerID",
            "Segment",
        ]
    ],

    on="CustomerID",

    how="left",

)


# ==========================================================
# HEADER
# ==========================================================

page_header(

    title="Customer Churn Center",

    subtitle="AI-powered Churn Risk Monitoring",

)

st.markdown(
"""
Monitor customer churn risk, identify high-risk customers,
analyze prediction confidence, and prioritize retention
strategies using Machine Learning.
"""
)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_customers = len(churn)

high_risk = len(

    churn[
        churn["PredictedChurn"] == 1
    ]

)

safe_customers = total_customers - high_risk

risk_percent = (

    high_risk / total_customers

) * 100

avg_probability = (

    churn["ChurnProbability"]

    .mean()

    * 100

)


# ==========================================================
# KPI SECTION
# ==========================================================

section_header(
    "🚨 Churn KPIs",
    "Overall churn risk across the customer base"
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    kpi_card(

        "Customers",

        f"{total_customers:,}",

        "👥",

    )

with c2:

    kpi_card(

        "High Risk",

        f"{high_risk:,}",

        "🚨",

    )

with c3:

    kpi_card(

        "Safe Customers",

        f"{safe_customers:,}",

        "✅",

    )

with c4:

    kpi_card(

        "Average Risk",

        f"{avg_probability:.1f}%",

        "📉",

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# CUSTOMER SEARCH
# ==========================================================

customer_ids = sorted(

    churn["CustomerID"]

    .astype(int)

    .unique()

)

selected_customer = st.selectbox(

    "🔍 Search Customer",

    customer_ids,

)

profile = churn[
    churn["CustomerID"] == selected_customer
].iloc[0]


# ==========================================================
# CUSTOMER PROFILE
# ==========================================================

section_header(
    "👤 Customer Risk Profile",
    "Detailed risk assessment for the selected customer"
)

left, right = st.columns(
    [1.1, 1.3],
    gap="large",
)

with left:

    status_card(

        "Customer",

        int(profile["CustomerID"])

    )

    status_card(

        "Revenue",

        f"₹ {profile['TotalRevenue']:,.0f}"

    )

    status_card(

        "Orders",

        int(profile["InvoiceCount"])

    )

    status_card(

        "Segment",

        profile["Segment"]

    )

with right:

    gauge_chart(

        value=profile["ChurnProbability"] * 100,

        title="Churn Probability",

    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# CHURN DISTRIBUTION
# ==========================================================

section_header(
    "📊 Churn Distribution",
    "Current customer retention vs churn predictions"
)

left, right = st.columns(
    2,
    gap="large",
)

with left:

    churn_counts = (

        churn

        .groupby("PredictedChurn")

        .size()

        .reset_index(name="Customers")

    )

    churn_counts["Status"] = churn_counts["PredictedChurn"].map({

        0: "Retained",

        1: "Likely to Churn",

    })

    donut_chart(

        churn_counts,

        names="Status",

        values="Customers",

        title="Customer Status",

    )

with right:

    histogram(

        df=churn,

        column="ChurnProbability",

        title="Prediction Probability Distribution",

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# SEGMENT RISK ANALYSIS
# ==========================================================

section_header(
    "📈 Segment Risk Analysis",
    "Average churn probability across customer segments"
)

segment_risk = (

    churn

    .groupby("Segment")

    .agg(

        Customers=("CustomerID", "count"),

        HighRisk=("PredictedChurn", "sum"),

        AvgProbability=("ChurnProbability", "mean"),

    )

    .reset_index()

)

segment_risk["AvgProbability"] *= 100

bar_chart(

    segment_risk,

    x="AvgProbability",

    y="Segment",

    title="Average Churn Probability",

    orientation="h",

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# HIGH RISK CUSTOMERS
# ==========================================================

section_header(
    "🚨 High Risk Customers",
    "Customers requiring immediate retention efforts"
)

high_risk_customers = (

    churn

    .sort_values(

        "ChurnProbability",

        ascending=False,

    )

    .head(20)

)

data_table(

    high_risk_customers[

        [

            "CustomerID",

            "Segment",

            "ChurnProbability",

            "TotalRevenue",

            "CustomerLifetimeValue",

            "InvoiceCount",

        ]

    ]

)

download_csv(

    high_risk_customers,

    "high_risk_customers.csv",

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# MODEL PERFORMANCE
# ==========================================================

section_header(
    "🤖 Classification Report",
    "Performance metrics of the churn prediction model"
)

data_table(

    classification,

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# BUSINESS METRICS
# ==========================================================

section_header(
    "📌 Churn Statistics",
    "Overall business churn indicators"
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    
    status_card(

        "Overall Risk",

        f"{risk_percent:.1f}%"

    )

with m2:
    
    status_card(

    "Average Probability",

    f"{avg_probability:.1f}%"

)

with m3:
    
    status_card(

    "Highest Probability",

    f"{churn['ChurnProbability'].max()*100:.1f}%"

)

with m4:
    
    status_card(

    "Lowest Probability",

    f"{churn['ChurnProbability'].min()*100:.1f}%"

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# AI INSIGHTS
# ==========================================================

highest = high_risk_customers.iloc[0]

insight_card(

    "AI Churn Insights",

    f"""

### 🚨 Churn Summary

• Total customers analysed:
**{total_customers:,}**

• High-risk customers:
**{high_risk:,}**

• Overall churn risk:
**{risk_percent:.1f}%**

• Average churn probability:
**{avg_probability:.1f}%**

---

### ⭐ Highest Risk Customer

Customer **{int(highest['CustomerID'])}**

Probability:
**{highest['ChurnProbability']*100:.1f}%**

Revenue:
**₹ {highest['TotalRevenue']:,.0f}**

---

### 💡 Recommended Actions

✅ Launch personalised retention campaigns.

✅ Reward loyal VIP customers.

✅ Re-engage inactive buyers.

✅ Monitor declining purchase frequency.

"""
)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# COMPLETE PREDICTIONS
# ==========================================================

with st.expander(

    "📄 View Complete Prediction Dataset",

    expanded=False,

):

    data_table(

        churn,

        height=500,

    )

    download_csv(

        churn,

        "customer_churn_predictions.csv",

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# RETENTION STRATEGY
# ==========================================================

st.subheader("💡 Recommended Retention Strategy")

insight_card(

    "Retention Strategy",

    """

✅ Prioritize high-value customers.

✅ Contact customers with churn probability above 80%.

✅ Offer loyalty rewards.

✅ Personalize promotions.

✅ Monitor customer activity weekly.

"""

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# FOOTER
# ==========================================================

render_footer()