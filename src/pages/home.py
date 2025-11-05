"""
Home page component
"""

import streamlit as st


def show_home(storage, stats):
    """Home page with overview"""
    st.header("Welcome to Flipzy! 🎯")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Cards", stats["total_cards"])
    with col2:
        st.metric("Due for Review", stats["due_for_review"])
    with col3:
        st.metric("Mastered", stats["mastered"])
    with col4:
        st.metric("In Progress", stats["in_progress"])

    st.markdown("---")

    if stats["due_for_review"] > 0:
        st.success(
            f"🎉 You have {stats['due_for_review']} cards ready for review! Go to the Review page to continue learning."
        )
    else:
        st.info("✨ Great job! No cards due for review. Add more vocabulary or check back later.")

    st.markdown("### 🎓 How to Use This App")
    st.markdown(
        """
    1. **Add Vocabulary**: Start by adding new words and phrases you want to learn
    2. **Review**: Use the spaced repetition system to review cards regularly
    3. **Rate Your Recall**: When reviewing, rate how well you remembered (0-5)
    4. **Track Progress**: Monitor your learning statistics
    5. **Manage Cards**: Edit or delete cards as needed
    
    **Tip**: Review cards daily for best results! The app will automatically schedule cards based on how well you remember them.
    """
    )
