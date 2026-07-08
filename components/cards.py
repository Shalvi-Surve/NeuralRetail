from __future__ import annotations

import streamlit as st

def kpi_card(title: str, value: str, icon="📊", delta=""):

    html = f"""<div class="kpi-card">
<div class="kpi-top">
<div class="kpi-label">{title}</div>
<div class="kpi-icon">{icon}</div>
</div>

<div class="kpi-number">{value}</div>

<div class="kpi-change">{delta}</div>

</div>"""

    st.markdown(html, unsafe_allow_html=True)

def insight_card(title: str, message: str):

    st.markdown(
        f"""
<div class="card">

<div class="insight-heading">
🤖 {title}
</div>

<div class="insight-body">

{message}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


def status_card(title: str, value: str):

    st.markdown(
        f"""
<div class="card">

<div class="status-title">
{title}
</div>

<div class="status-value">
{value}
</div>

</div>
""",
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = ""):

    st.markdown(
        f"""
<div class="section-header">

<div class="section-title">
{title}
</div>

<div class="section-subtitle">
{subtitle}
</div>

</div>
""",
        unsafe_allow_html=True,
    )