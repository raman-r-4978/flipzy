"""
Configuration and session state initialization
"""

import streamlit as st

from .storage import Storage


def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Flipzy", page_icon="📚", layout="wide", initial_sidebar_state="expanded"
    )


def initialize_session_state():
    """Initialize session state variables"""
    if "storage" not in st.session_state:
        st.session_state.storage = Storage()
    if "current_card_index" not in st.session_state:
        st.session_state.current_card_index = 0
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False
    if "review_mode" not in st.session_state:
        st.session_state.review_mode = False
