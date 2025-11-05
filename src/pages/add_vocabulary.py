"""
Add vocabulary page component
"""

import uuid

import streamlit as st

from src.spaced_repetition import Card


def show_add_vocabulary(storage):
    """Page to add new vocabulary/phrases"""
    st.header("➕ Add New Vocabulary or Phrase")

    with st.form("add_card_form"):
        col1, col2 = st.columns(2)

        with col1:
            front = st.text_input("Word or Phrase *", placeholder="e.g., Break the ice")
            category = st.selectbox(
                "Category",
                ["vocabulary", "phrase", "idiom", "phrasal verb", "collocation", "other"],
            )

        with col2:
            back = st.text_area(
                "Definition/Translation/Explanation *",
                placeholder="e.g., To start a conversation in a friendly way",
            )
            example = st.text_area(
                "Example Sentence (Optional)",
                placeholder="e.g., He broke the ice by telling a joke.",
            )

        submitted = st.form_submit_button("Add Card", use_container_width=True)

        if submitted:
            if front and back:
                card = Card(
                    id=str(uuid.uuid4()),
                    front=front.strip(),
                    back=back.strip(),
                    category=category,
                    example=example.strip() if example else None,
                )
                storage.add_card(card)
                st.success(f"✅ Added: '{front}' - '{back}'")
                st.rerun()
            else:
                st.error("Please fill in at least the Word/Phrase and Definition fields.")

    # Show recent cards
    st.markdown("---")
    st.subheader("📋 Recent Cards")
    cards = storage.load_cards()
    if cards:
        recent_cards = sorted(cards, key=lambda x: x.created_at, reverse=True)[:10]
        for card in recent_cards:
            with st.expander(f"{card.front} ({card.category})"):
                st.write(f"**Definition:** {card.back}")
                if card.example:
                    st.write(f"**Example:** {card.example}")
                st.caption(f"Created: {card.created_at.strftime('%Y-%m-%d %H:%M')}")
    else:
        st.info("No cards yet. Add your first vocabulary word above!")
