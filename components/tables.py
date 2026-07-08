"""
============================================================
NeuralRetail
Reusable Table Components
============================================================

Author : Shalvi Surve
Project : NeuralRetail
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


# ==========================================================
# TABLE CARD
# ==========================================================

def data_table(

    df: pd.DataFrame,

    height: int = 420,

):

    st.markdown(
        '<div class="table-card">',
        unsafe_allow_html=True,
    )

    st.dataframe(

        df,

        height=height,

        width="stretch",

        hide_index=True,

    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ==========================================================
# TOP N TABLE
# ==========================================================

def top_table(

    df: pd.DataFrame,

    n: int = 10,

):

    data_table(

        df.head(n),

        height=390,

    )


# ==========================================================
# DOWNLOAD BUTTON
# ==========================================================

def download_csv(

    df: pd.DataFrame,

    filename: str,

    label: str = "📥 Download CSV",

):

    csv = df.to_csv(

        index=False,

    ).encode("utf-8")

    st.download_button(

        label=label,

        data=csv,

        file_name=filename,

        mime="text/csv",

        width="stretch",

    )