"""
Sidebar component with navigation and quick stats
"""

import random
from datetime import datetime

import streamlit as st


def render_sidebar(storage, stats):
    """Render the sidebar with stats, navigation, and quick actions"""
    with st.sidebar:
        st.markdown("### 🎯 Quick Stats")

        # Stats cards in sidebar
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", stats["total_cards"], delta=None)
        with col2:
            st.metric(
                "Due",
                stats["due_for_review"],
                delta=f"{stats['due_for_review']} ready" if stats["due_for_review"] > 0 else None,
                delta_color="normal" if stats["due_for_review"] > 0 else "off",
            )

        col3, col4 = st.columns(2)
        with col3:
            st.metric("Mastered", stats["mastered"])
        with col4:
            st.metric("In Progress", stats["in_progress"])

        st.markdown("---")

        # Progress indicator
        if stats["total_cards"] > 0:
            mastery_rate = (stats["mastered"] / stats["total_cards"]) * 100
            st.markdown("#### 📈 Mastery Progress")
            st.progress(mastery_rate / 100)
            st.caption(f"{mastery_rate:.1f}% mastered")
        else:
            st.info("📝 Add your first card to start learning!")

        st.markdown("---")

        # Navigation
        st.markdown("### 🧭 Navigation")
        page = st.radio(
            "Choose a page",
            ["🏠 Home", "➕ Add Vocabulary", "📖 Review", "📊 Statistics", "📝 Manage Cards"],
            label_visibility="collapsed",
        )

        st.markdown("---")

        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("💾 Create Backup", use_container_width=True):
            backup_path = storage.backup_now()
            if backup_path:
                st.success("✅ Backup created!")
                st.caption(f"📁 {backup_path.split('/')[-1]}")
            else:
                st.warning("No data to backup.")

        st.markdown("---")

        # Learning tip
        st.markdown("### 💡 Learning Tip")
        tips = [
            "Review cards daily for best results!",
            "Be honest with your ratings - it helps the algorithm.",
            "Add example sentences to remember better.",
            "Focus on quality over quantity.",
            "Consistency is key to language learning!",
        ]
        st.info(f"💬 {random.choice(tips)}")

        st.markdown("---")

        # Recent activity preview
        cards = storage.load_cards()
        if cards:
            recent_reviewed = sorted(
                [c for c in cards if c.last_reviewed], key=lambda x: x.last_reviewed, reverse=True
            )[:3]
            if recent_reviewed:
                st.markdown("#### 🕐 Recent Activity")
                for card in recent_reviewed:
                    days_ago = (datetime.now() - card.last_reviewed).days
                    if days_ago == 0:
                        time_str = "Today"
                    elif days_ago == 1:
                        time_str = "Yesterday"
                    else:
                        time_str = f"{days_ago} days ago"
                    st.caption(f"📌 {card.front}")
                    st.caption(f"   {time_str} • {card.repetitions}x reviewed")

    return page
