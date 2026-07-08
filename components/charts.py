"""
============================================================
NeuralRetail
Chart Components
============================================================

Author : Shalvi Surve

Reusable Plotly charts used across the application.
"""

from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from contextlib import contextmanager

PRIMARY = "#4F46E5"
SECONDARY = "#7C3AED"
ACCENT = "#06B6D4"

SUCCESS = "#22C55E"
WARNING = "#F59E0B"
DANGER = "#EF4444"

PLOT_COLORS = [
    PRIMARY,
    SECONDARY,
    ACCENT,
    SUCCESS,
    WARNING,
    "#F97316",
    "#14B8A6",
    "#EC4899",
]

opacity = 0.75
size_max = 25

# ==========================================================
# Chart Card
# ==========================================================

@contextmanager
def chart_card(title: str):

    st.markdown(
        f"""
<div class="chart-card">

<div class="chart-title">

{title}

</div>

""",
        unsafe_allow_html=True,
    )

    yield

    st.markdown(

        "</div>",

        unsafe_allow_html=True,

    )

# ==========================================================
# Default Layout
# ==========================================================

def _style(fig):

    fig.update_layout(

        template="plotly_white",

        height=430,

        margin=dict(
            l=15,
            r=15,
            t=65,
            b=15,
        ),

        font=dict(
            family="Inter",
            size=14,
            color="#334155",
        ),

        title=dict(

            x=0.03,

            font=dict(

                family="Inter",

                size=22,

                color="#0F172A",

            ),

        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        hovermode="x unified",

        legend=dict(

            orientation="h",

            y=1.08,

            x=0,

            bgcolor="rgba(255,255,255,.6)",

        ),

    )

    fig.update_xaxes(

        showgrid=False,

        showline=True,

        linecolor="#CBD5E1",

        tickfont=dict(

            color="#475569",

            family="Inter",

        ),

        title_font=dict(

            family="Inter",

            color="#334155",

        ),

    )

    fig.update_yaxes(

        showgrid=True,

        gridcolor="#E2E8F0",

        gridwidth=1,

        zeroline=False,

        tickfont=dict(

            color="#475569",

            family="Inter",

        ),

        title_font=dict(

            family="Inter",

            color="#334155",

        ),

    )

    return fig

# ==========================================================
# Line Chart
# ==========================================================

def line_chart(
    df,
    x,
    y,
    title,
    color="#6366F1",
):

    fig = px.line(

        df,

        x=x,

        y=y,

        markers=True,

        title=title,

    )

    fig.update_traces(

        line=dict(width=3, color=color),

        marker=dict(
            size=8,
            color = color,

            line=dict(
                width=2,
                color="white",
            ),
        )

    )

    st.plotly_chart(

        _style(fig),

        width="stretch",

    )


# ==========================================================
# Bar Chart
# ==========================================================

def bar_chart(
    df,
    x,
    y,
    title,
    orientation="v",
):

    fig = px.bar(

        df,

        x=x,

        y=y,

        title=title,

        orientation=orientation,

        text_auto=".2s",

    )

    fig.update_traces(

        marker_color=PRIMARY,
        marker_line_color="white",
        marker_line_width=.6,
        opacity = .92,
    )

    st.plotly_chart(

        _style(fig),

        width="stretch",

    )


# ==========================================================
# Donut Chart
# ==========================================================

def donut_chart(
    df,
    names,
    values,
    title,
):

    fig = px.pie(

        df,

        names=names,

        values=values,

        hole=0.65,

        title=title,

    )

    fig.update_traces(

        textinfo="percent",

        textfont_size=14,

        marker=dict(

            colors=PLOT_COLORS,

            line=dict(

                color="white",

                width=2,

            ),
        ),
    )

    st.plotly_chart(

        _style(fig),

        width="stretch",

    )


# ==========================================================
# Scatter Plot
# ==========================================================

def scatter_chart(
    df,
    x,
    y,
    color,
    title,
):

    fig = px.scatter(

        df,

        x=x,

        y=y,

        color=color,

        title=title,

        size_max=28,

        color_discrete_sequence=PLOT_COLORS,
    )

    st.plotly_chart(

        _style(fig),

        width="stretch",

    )


# ==========================================================
# Histogram
# ==========================================================

def histogram(
    df,
    column,
    title,
):

    fig = px.histogram(

        df,

        x=column,

        nbins=30,

        title=title,

        color_discrete_sequence=[PRIMARY],

    )

    st.plotly_chart(

        _style(fig),

        width="stretch",

    )


# ==========================================================
# Area Chart
# ==========================================================

def area_chart(
    df,
    x,
    y,
    title,
):

    fig = px.area(

        df,

        x=x,

        y=y,

        title=title,

    )

    fig.update_traces(

        line=dict(
            
            width=3,
            
            color=PRIMARY,

        ),

    )

    st.plotly_chart(

        _style(fig),

        width="stretch",

    )


# ==========================================================
# Gauge Chart
# ==========================================================

def gauge_chart(
    value,
    title,
):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=value,

            number={

                "suffix":"%",

                "font":{

                    "size":40,

                },

            },

            title={

                "text":title,

                "font":{

                    "size":20,

                },

            },

            gauge={

                "axis":{

                    "range":[0,100],

                },

                "bar":{

                    "color":PRIMARY,

                },

                "bgcolor":"#F8FAFC",

                "borderwidth":0,

                "steps":[

                    {

                        "range":[0,40],

                        "color":"#DCFCE7",

                    },

                    {

                        "range":[40,70],

                        "color":"#FEF3C7",

                    },

                    {

                        "range":[70,100],

                        "color":"#FEE2E2",

                    },

                ],

            },

        )

    )

    fig.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        height=350,

    )

    st.plotly_chart(

        fig,

        width="stretch",

    )

# ==========================================================
# Forecast Chart
# ==========================================================

def forecast_chart(
    df,
    x,
    actual,
    predicted,
):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df[x],

            y=df[actual],

            mode="lines",

            name="Actual",

        )

    )

    fig.add_trace(

        go.Scatter(

            x=df[x],

            y=df[predicted],

            mode="lines",

            name="Forecast",

        )

    )

    fig.update_layout(

        title="Demand Forecast",

        template="plotly_white",

        height=430,

    )

    st.plotly_chart(

        fig,

        width="stretch",

    )