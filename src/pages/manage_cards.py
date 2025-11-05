"""
Manage cards page component
"""

import streamlit as st


def show_manage_cards(storage):
    """Page to manage (edit/delete) cards"""
    st.header("📝 Manage Cards")

    cards = storage.load_cards()

    if not cards:
        st.info("No cards to manage. Add some vocabulary first!")
        return

    # Search and filter
    col_search, col_count = st.columns([3, 1])
    with col_search:
        search_term = st.text_input(
            "🔍 Search cards", placeholder="Search by word, phrase, or definition..."
        )

    with col_count:
        st.write("")  # Spacing
        st.caption(f"**{len(cards)}** total cards")

    # Filter cards
    filtered_cards = cards
    if search_term:
        search_lower = search_term.lower()
        filtered_cards = [
            c
            for c in cards
            if search_lower in c.front.lower()
            or search_lower in c.back.lower()
            or (c.example and search_lower in c.example.lower())
        ]

    if search_term:
        st.caption(f"Showing {len(filtered_cards)} of {len(cards)} cards")

    st.markdown("---")

    # Initialize editing state
    if "editing_card_id" not in st.session_state:
        st.session_state.editing_card_id = None

    # Display cards in a grid layout (card-style, not expanders)
    if filtered_cards:
        # Add CSS to ensure cards have equal heights within rows
        st.markdown(
            """
        <style>
        /* Ensure all columns in a row have equal height */
        div[data-testid="column"] {
            align-self: stretch !important;
        }
        div[data-testid="column"] > div {
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
        }
        div[data-testid="column"] > div > div {
            flex: 1 !important;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        # Calculate number of columns (3 columns for card layout)
        num_cols = 2
        for i in range(0, len(filtered_cards), num_cols):
            cols = st.columns(num_cols, gap="medium")
            for j, col in enumerate(cols):
                if i + j < len(filtered_cards):
                    card = filtered_cards[i + j]
                    with col:
                        # Check if this card is being edited
                        if st.session_state.editing_card_id == card.id:
                            # Show edit form in a container
                            with st.container():
                                st.markdown("#### ✏️ Editing Card")
                                with st.form(f"edit_form_{card.id}"):
                                    edit_front = st.text_input(
                                        "Word or Phrase *",
                                        value=card.front,
                                        key=f"edit_front_{card.id}",
                                    )
                                    edit_category = st.selectbox(
                                        "Category",
                                        [
                                            "vocabulary",
                                            "phrase",
                                            "idiom",
                                            "phrasal verb",
                                            "collocation",
                                            "other",
                                        ],
                                        index=[
                                            "vocabulary",
                                            "phrase",
                                            "idiom",
                                            "phrasal verb",
                                            "collocation",
                                            "other",
                                        ].index(card.category),
                                        key=f"edit_category_{card.id}",
                                    )
                                    edit_back = st.text_area(
                                        "Definition *",
                                        value=card.back,
                                        key=f"edit_back_{card.id}",
                                        height=100,
                                    )
                                    edit_example = st.text_area(
                                        "Example (Optional)",
                                        value=card.example or "",
                                        key=f"edit_example_{card.id}",
                                        height=80,
                                    )

                                    col_save, col_cancel = st.columns(2)
                                    with col_save:
                                        if st.form_submit_button(
                                            "💾 Save", use_container_width=True, type="primary"
                                        ):
                                            if edit_front and edit_back:
                                                card.front = edit_front.strip()
                                                card.back = edit_back.strip()
                                                card.category = edit_category
                                                card.example = (
                                                    edit_example.strip()
                                                    if edit_example.strip()
                                                    else None
                                                )
                                                storage.update_card(card)
                                                st.session_state.editing_card_id = None
                                                st.success("✅ Updated!")
                                                st.rerun()
                                            else:
                                                st.error("Fill required fields.")
                                    with col_cancel:
                                        if st.form_submit_button(
                                            "❌ Cancel", use_container_width=True
                                        ):
                                            st.session_state.editing_card_id = None
                                            st.rerun()
                        else:
                            # Display card using Streamlit components
                            # Wrap in container to ensure consistent height
                            with st.container():
                                st.markdown(f"#### {card.front}")
                                st.caption(f"Category: {card.category}")
                                st.write(
                                    f"**Definition:** {card.back[:100]}{'...' if len(card.back) > 100 else ''}"
                                )
                                if card.example:
                                    st.caption(
                                        f'Example: "{card.example[:80]}{"..." if len(card.example) > 80 else ""}"'
                                    )
                                st.write(
                                    f"📊 {card.repetitions} reviews • ⏰ {card.interval}d interval"
                                )
                                st.write(f"📅 Next: {card.next_review.strftime('%Y-%m-%d')}")
                                st.markdown("---")

                                # Action buttons below card
                                col_edit, col_delete = st.columns(2)
                                with col_edit:
                                    if st.button(
                                        "✏️ Edit", key=f"edit_{card.id}", use_container_width=True
                                    ):
                                        st.session_state.editing_card_id = card.id
                                        st.rerun()
                                with col_delete:
                                    if st.button(
                                        "🗑️ Delete",
                                        key=f"delete_{card.id}",
                                        type="secondary",
                                        use_container_width=True,
                                    ):
                                        storage.delete_card(card.id)
                                        st.success("Card deleted!")
                                        st.rerun()
    else:
        st.info("No cards match your search. Try a different search term.")
