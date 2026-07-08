"""
============================================================
NeuralRetail
Demand Forecast Center
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
    forecast_chart,
    histogram,
    line_chart,
)

from components.tables import (
    data_table,
    download_csv,
)


# ==========================================================
# INITIALIZE
# ==========================================================

repo = initialize_dashboard("Demand Forecast")


# ==========================================================
# LOAD DATA
# ==========================================================

forecast = repo.forecast()

metrics = repo.forecast_metrics()


# ==========================================================
# HEADER
# ==========================================================

page_header(

    title="Demand Forecast Center",

    subtitle="Machine Learning Demand Forecasting",

)

st.markdown(
"""
Analyze historical sales trends, evaluate forecast
performance, and monitor future demand using
Machine Learning.
"""
)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# METRICS
# ==========================================================

mae = float(

    metrics.loc[
        metrics["Metric"] == "MAE",
        "Value",
    ].values[0]

)

rmse = float(

    metrics.loc[
        metrics["Metric"] == "RMSE",
        "Value",
    ].values[0]

)

r2 = float(

    metrics.loc[
        metrics["Metric"] == "R2 Score",
        "Value",
    ].values[0]

)


# ==========================================================
# KPI CARDS
# ==========================================================

section_header(
    "📈 Forecast KPIs",
    "Overall forecasting model performance"
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    kpi_card(

        "Forecast Days",

        f"{len(forecast):,}",

        "📅",

    )

with c2:

    kpi_card(

        "MAE",

        f"{mae:,.0f}",

        "📉",

    )

with c3:

    kpi_card(

        "RMSE",

        f"{rmse:,.0f}",

        "📊",

    )

with c4:

    kpi_card(

        "R² Score",

        f"{r2:.3f}",

        "🤖",

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# FORECAST CHART
# ==========================================================

section_header(
    "📈 Actual vs Forecast",
    "Comparison between observed and predicted revenue"
)

forecast_chart(

    df=forecast,

    x="Date",

    actual="Revenue",

    predicted="PredictedRevenue",

)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# REVENUE ANALYSIS
# ==========================================================

section_header(
    "📊 Revenue Analysis",
    "Growth trends and forecast error distribution"
)

left, right = st.columns(
    2,
    gap="large",
)

with left:

    line_chart(

        df=forecast,

        x="Date",

        y="RevenueGrowth",

        title="Revenue Growth",

    )

with right:

    histogram(

        df=forecast,

        column="ForecastError",

        title="Forecast Error Distribution",

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# MODEL PERFORMANCE
# ==========================================================

section_header(
    "🎯 Forecast Performance",
    "Evaluation metrics for the forecasting model"
)

c1, c2, c3 = st.columns(3)

with c1:
    
    status_card(

        "Mean Absolute Error",

        f"{mae:,.2f}"

    )

with c2:
    
    status_card(

        "Root Mean Square Error",

         f"{rmse:,.2f}"

    )

with c3:
    
    status_card(

        "R² Score",

        f"{r2:.3f}"

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# HIGHEST FORECAST ERRORS
# ==========================================================

section_header(
    "⚠️ Highest Forecast Errors",
    "Dates where the model deviated the most"
)

largest_errors = (

    forecast

    .sort_values(

        "AbsoluteError",

        ascending=False,

    )

    .head(15)

)

data_table(

    largest_errors[

        [

            "Date",

            "Revenue",

            "PredictedRevenue",

            "ForecastError",

            "AbsoluteError",

        ]

    ]

)

download_csv(

    largest_errors,

    "forecast_errors.csv",

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# FORECAST SUMMARY TABLE
# ==========================================================

section_header(
    "📋 Forecast Results",
    "Prediction results for every available date"
)

preview = (

    forecast[

        [

            "Date",

            "Revenue",

            "PredictedRevenue",

            "ForecastError",

            "AbsoluteError",

        ]

    ]

)

data_table(

    preview,

)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# FORECAST STATISTICS
# ==========================================================

section_header(
    "📌 Forecast Statistics",
    "Overall revenue and prediction summary"
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    status_card(
        "Average Revenue",
        f"₹ {forecast['Revenue'].mean():,.0f}"
    )

with c2:
    
    status_card(

        "Average Prediction",

        f"₹ {forecast['PredictedRevenue'].mean():,.0f}"

    )

with c3:
    
    status_card(

    "Maximum Revenue",

    f"₹ {forecast['Revenue'].max():,.0f}"

)

with c4:
    
    status_card(

        "Maximum Error",

        f"{forecast['AbsoluteError'].max():,.0f}"

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# AI FORECAST INSIGHTS
# ==========================================================

highest_error = forecast.loc[
    forecast["AbsoluteError"].idxmax()
]

best_day = forecast.loc[
    forecast["Revenue"].idxmax()
]

insight_card(

    "AI Forecast Insights",

    f"""

### 📈 Forecast Summary

• Forecasting model achieved an **R² Score of {r2:.3f}**.

• Mean Absolute Error:
**{mae:,.2f}**

• Root Mean Square Error:
**{rmse:,.2f}**

---

### ⭐ Key Observations

Highest revenue day:

**{best_day['Date']}**

Revenue:

**₹ {best_day['Revenue']:,.0f}**

Largest prediction error:

**{highest_error['Date']}**

Absolute Error:

**₹ {highest_error['AbsoluteError']:,.0f}**

---

### 💡 Business Interpretation

✅ Forecast accuracy is suitable for retail planning.

✅ Demand remains relatively stable.

✅ Monitor periods with unusually high prediction errors.

✅ Combine forecasting with inventory optimization.

"""
)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# FULL FORECAST DATASET
# ==========================================================

with st.expander(

    "📄 View Complete Forecast Dataset",

    expanded=False,

):

    data_table(

        forecast,

        height=500,

    )

    download_csv(

        forecast,

        "demand_forecast.csv",

    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# RECOMMENDATIONS
# ==========================================================

st.subheader("💡 Business Recommendations")

insight_card(

    "Business Recommendations",

    """

✅ Increase inventory before high-demand periods.

✅ Monitor dates with large forecast errors.

✅ Retrain the forecasting model periodically.

✅ Use forecasts for procurement planning.

✅ Combine demand forecasting with inventory optimization.

"""

)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# FOOTER
# ==========================================================

render_footer()

