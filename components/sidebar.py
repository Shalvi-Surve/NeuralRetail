"""
============================================================
NeuralRetail
Reusable Sidebar
============================================================

Author : Shalvi Surve
Project : NeuralRetail
"""

from __future__ import annotations

import streamlit as st


# ==========================================================
# SIDEBAR
# ==========================================================

def render_sidebar():

    with st.sidebar:

        st.markdown(
            """
# 🧠 NeuralRetail

##### AI Retail Intelligence Platform
"""
        )

        st.divider()

        st.markdown(
            """
### 🚀 Modules

- 📊 Executive Dashboard
- 👥 Customer Intelligence
- 🚨 Churn Prediction
- 📈 Demand Forecasting
- 📦 Inventory Optimization
"""
        )

        st.divider()

        st.markdown(
            """
### 📈 System Status

🟢 **Online**

**Dataset**

UCI Online Retail II

**Customers**

5,678

**Version**

v1.0.0
"""
        )

        st.divider()

        st.caption(
            "© 2026 NeuralRetail\n\nDeveloped by **Shalvi Surve**"
        )