"""
Flipzy - Spaced Repetition App
A Streamlit app to help learn English vocabulary and phrases
"""
import streamlit as st
from src.config import configure_page, initialize_session_state
from src.sidebar import render_sidebar
from src.spaced_repetition import SpacedRepetition
from src.pages import (
    show_home,
    show_add_vocabulary,
    show_review,
    show_statistics,
    show_manage_cards
)


def main():
    """Main application entry point"""
    st.title("📚 Flipzy")
    st.markdown("---")
    
    storage = st.session_state.storage
    sr = SpacedRepetition()
    cards = storage.load_cards()
    stats = sr.get_stats(cards)
    
    # Render sidebar and get selected page
    page = render_sidebar(storage, stats)
    
    # Route to appropriate page
    if page == "🏠 Home":
        show_home(storage, stats)
    elif page == "➕ Add Vocabulary":
        show_add_vocabulary(storage)
    elif page == "📖 Review":
        show_review(storage, sr)
    elif page == "📊 Statistics":
        show_statistics(storage, sr)
    elif page == "📝 Manage Cards":
        show_manage_cards(storage)


if __name__ == "__main__":
    configure_page()
    initialize_session_state()
    main()
