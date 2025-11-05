"""
Review page component with spaced repetition
"""

import streamlit as st


def show_review(storage, sr):
    """Review page with spaced repetition"""
    st.header("📖 Review Cards")

    cards = storage.load_cards()
    due_cards = sr.get_due_cards(cards)

    if not due_cards:
        st.info(
            "🎉 Great job! No cards due for review right now. Check back later or add more cards!"
        )
        return

    # Reset state if no current card
    if (
        "current_review_card" not in st.session_state
        or st.session_state.current_review_card is None
    ):
        st.session_state.current_review_card = due_cards[0]
        st.session_state.show_answer = False

    current_card = st.session_state.current_review_card

    st.progress(
        len(due_cards) - due_cards.index(current_card) if current_card in due_cards else 0,
        text=f"Cards remaining: {len(due_cards)}",
    )

    # Card display
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"### {current_card.front}")
        st.markdown(f"**Category:** {current_card.category}")

        if st.button("Show Answer", disabled=st.session_state.show_answer):
            st.session_state.show_answer = True

        if st.session_state.show_answer:
            st.markdown("---")
            st.markdown("### Answer")
            st.success(f"**{current_card.back}**")

            if current_card.example:
                st.markdown("---")
                st.markdown("### Example")
                st.info(f"**{current_card.example}**")

            st.markdown("---")
            st.markdown("### How well did you remember?")

            col_a, col_b, col_c, col_d, col_e, col_f = st.columns(6)

            with col_a:
                if st.button("0 - Wrong", use_container_width=True, type="primary"):
                    rate_card(storage, sr, current_card, 0)
            with col_b:
                if st.button("1 - Hard", use_container_width=True):
                    rate_card(storage, sr, current_card, 1)
            with col_c:
                if st.button("2 - Good", use_container_width=True):
                    rate_card(storage, sr, current_card, 2)
            with col_d:
                if st.button("3 - Easy", use_container_width=True):
                    rate_card(storage, sr, current_card, 3)
            with col_e:
                if st.button("4 - Very Easy", use_container_width=True):
                    rate_card(storage, sr, current_card, 4)
            with col_f:
                if st.button("5 - Perfect", use_container_width=True):
                    rate_card(storage, sr, current_card, 5)

            st.caption("💡 Tip: Be honest! The algorithm adjusts based on your responses.")

    with col2:
        st.markdown("### Card Info")
        st.write(f"**Repetitions:** {current_card.repetitions}")
        st.write(f"**Interval:** {current_card.interval} days")
        st.write(f"**Ease Factor:** {current_card.ease_factor:.2f}")
        if current_card.last_reviewed:
            st.write(f"**Last Reviewed:** {current_card.last_reviewed.strftime('%Y-%m-%d')}")
        else:
            st.write("**Last Reviewed:** Never")


def rate_card(storage, sr, card, quality):
    """Rate a card and update it"""
    updated_card = sr.calculate_next_review(card, quality)
    storage.update_card(updated_card)

    # Move to next card
    cards = storage.load_cards()
    due_cards = sr.get_due_cards(cards)

    if due_cards:
        # Remove current card from due list if it's no longer due
        remaining_due = [c for c in due_cards if c.id != card.id]
        if remaining_due:
            st.session_state.current_review_card = remaining_due[0]
        else:
            st.session_state.current_review_card = None
    else:
        st.session_state.current_review_card = None

    st.session_state.show_answer = False
    st.rerun()
