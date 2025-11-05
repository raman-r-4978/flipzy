"""
Statistics page component
"""

import streamlit as st


def show_statistics(storage, sr):
    """Statistics page"""
    st.header("📊 Learning Statistics")

    cards = storage.load_cards()
    stats = sr.get_stats(cards)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Cards", stats["total_cards"])
        st.metric("Due for Review", stats["due_for_review"])
        st.metric("New Cards", stats["new_cards"])

    with col2:
        st.metric("Mastered", stats["mastered"])
        st.metric("In Progress", stats["in_progress"])

    st.markdown("---")

    # Category breakdown
    if cards:
        st.subheader("📚 Cards by Category")
        categories = {}
        for card in cards:
            categories[card.category] = categories.get(card.category, 0) + 1

        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            st.write(f"**{category.capitalize()}:** {count}")

        st.markdown("---")

        # Recent activity
        st.subheader("📅 Recent Activity")
        recent_cards = sorted(
            [c for c in cards if c.last_reviewed], key=lambda x: x.last_reviewed, reverse=True
        )[:10]
        if recent_cards:
            for card in recent_cards:
                st.write(
                    f"**{card.front}** - Last reviewed: {card.last_reviewed.strftime('%Y-%m-%d %H:%M')} "
                    f"(Repetitions: {card.repetitions}, Interval: {card.interval} days)"
                )
        else:
            st.info("No cards reviewed yet. Start reviewing to see your activity here!")
