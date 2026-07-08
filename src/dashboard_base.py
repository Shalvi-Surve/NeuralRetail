"""
============================================================
NeuralRetail
Dashboard Base
============================================================

Shared initialization for every dashboard page.

Author : Shalvi Surve
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from src.utils import DataRepository
from components.sidebar import render_sidebar


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ASSETS_DIR = PROJECT_ROOT / "assets"

STYLE_FILE = ASSETS_DIR / "styles.css"


# ==========================================================
# Load Global CSS
# ==========================================================

def load_css():

    if STYLE_FILE.exists():

        with open(

            STYLE_FILE,

            encoding="utf-8"

        ) as css:

            st.markdown(

                f"<style>{css.read()}</style>",

                unsafe_allow_html=True,

            )


# ==========================================================
# Initialize Dashboard
# ==========================================================

def initialize_dashboard(

    page_title: str,

):

    st.set_page_config(

        page_title=f"NeuralRetail | {page_title}",

        page_icon="🧠",

        layout="wide",

        initial_sidebar_state="expanded",

    )

    load_css()

    # render_sidebar()

    return DataRepository()


# ==========================================================
# Footer
# ==========================================================

def render_footer():

    st.divider()

    st.caption(

        "© 2026 NeuralRetail • AI Retail Intelligence Platform • Developed by Shalvi Surve"

    )