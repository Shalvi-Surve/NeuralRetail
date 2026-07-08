from __future__ import annotations

from datetime import datetime
import streamlit as st


def page_header(title: str, subtitle: str):

    today = datetime.now().strftime("%d %B %Y")

    st.markdown(
        f"""
<div class="dashboard-header">

<div class="header-left">

<div class="dashboard-title">
🧠 {title}
</div>

<div class="dashboard-subtitle">
{subtitle}
</div>

</div>

<div class="header-right">

<div class="header-date">
📅 {today}
</div>

<div class="header-status">
🟢 System Healthy
</div>

</div>

</div>
""",
        unsafe_allow_html=True,
    )


def welcome_message():

    hour = datetime.now().hour

    if hour < 12:
        greeting = "Good Morning"
    elif hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    st.markdown(
        f"""
<div class="welcome-card">

<div class="welcome-title">
{greeting} 👋
</div>

<div class="welcome-text">

Welcome back to <b>NeuralRetail</b>.

Explore customer intelligence,
demand forecasting,
inventory optimization,
churn prediction,
and AI-powered retail insights.

</div>

</div>
""",
        unsafe_allow_html=True,
    )