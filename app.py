"""
============================================================
NeuralRetail
Landing Page
============================================================

Author : Shalvi Surve
Project : NeuralRetail
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="NeuralRetail",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# HERO
# ==========================================================

st.markdown(
"""
<div class="landing-hero">

<div class="landing-title">

🧠 NeuralRetail

</div>

<div class="landing-subtitle">

AI-Powered Retail Intelligence Platform

</div>

<div class="landing-text">

Transform millions of retail transactions into actionable business
insights using Machine Learning, Data Analytics, Forecasting,
Customer Intelligence and Inventory Optimization.

</div>

</div>
""",
unsafe_allow_html=True,
)

st.markdown("")

# ==========================================================
# QUICK STATS
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Revenue", "₹8.67 M")
c2.metric("👥 Customers", "5,678")
c3.metric("🛒 Orders", "33,301")
c4.metric("📦 Products", "4,585")

st.divider()

# ==========================================================
# MODULES
# ==========================================================

st.markdown("## 🚀 AI Modules")

a, b = st.columns(2)

with a:

    st.markdown(
"""
<div class="card">

### 📊 Executive Dashboard

Business KPIs, revenue analytics and executive insights.

</div>
""",
unsafe_allow_html=True,
)

    st.markdown(
"""
<div class="card">

### 👥 Customer Intelligence

Customer segmentation, CLV analysis and behavioral analytics.

</div>
""",
unsafe_allow_html=True,
)

    st.markdown(
"""
<div class="card">

### 🚨 Customer Churn Prediction

Identify customers likely to churn using Machine Learning.

</div>
""",
unsafe_allow_html=True,
)

with b:

    st.markdown(
"""
<div class="card">

### 📈 Demand Forecasting

Forecast future sales using predictive analytics.

</div>
""",
unsafe_allow_html=True,
)

    st.markdown(
"""
<div class="card">

### 📦 Inventory Optimization

AI-driven inventory recommendations and stock monitoring.

</div>
""",
unsafe_allow_html=True,
)

    st.markdown(
"""
<div class="card">

### 🤖 Business Intelligence

Interactive dashboards with real-time analytics.

</div>
""",
unsafe_allow_html=True,
)

st.divider()

# ==========================================================
# TECH STACK
# ==========================================================

st.markdown("## 💻 Technology Stack")

tech1, tech2, tech3 = st.columns(3)

tech1.info(
"""
### 🐍 Backend

• Python

• Pandas

• NumPy

• Scikit-Learn

• XGBoost
"""
)

tech2.info(
"""
### 📊 Visualization

• Streamlit

• Plotly

• HTML/CSS

• Interactive Dashboards
"""
)

tech3.info(
"""
### 🤖 Machine Learning

• Customer Segmentation

• Churn Prediction

• Demand Forecasting

• Inventory Optimization
"""
)

st.divider()

# ==========================================================
# DATASET
# ==========================================================

st.markdown("## 📁 Dataset")

st.success(
"""
**UCI Online Retail II**

• ~1.06 Million Transactions

• 5,678 Customers

• 4,500+ Products

• Real-world Retail Dataset
"""
)

st.divider()

# ==========================================================
# DEVELOPER
# ==========================================================

st.markdown("## 👩‍💻 Developer")

st.markdown(
"""
### Shalvi Surve

B.Tech Computer Science & Engineering

VIT Vellore

NeuralRetail was built as an end-to-end AI-powered retail analytics
platform demonstrating machine learning, business intelligence,
predictive analytics and interactive visualization.
"""
)

st.divider()

st.caption("© 2026 NeuralRetail • AI Retail Intelligence Platform")