"""
Data storage and persistence for vocabulary cards
"""

import json
import os
import shutil
from datetime import datetime
from typing import List, Optional

from .spaced_repetition import Card


class Storage:
    """Handles persistence of vocabulary cards"""

    def __init__(self, file_path: str = "data/vocabulary_cards.json"):
        # Ensure data directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.file_path = file_path
        self.backup_dir = "data/backups"
        os.makedirs(self.backup_dir, exist_ok=True)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create the storage file if it doesn't exist"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def load_cards(self) -> List[Card]:
        """Load all cards from storage"""
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                cards = []
                for item in data:
                    # Parse datetime fields
                    if "created_at" in item:
                        item["created_at"] = datetime.fromisoformat(item["created_at"])
                    if "next_review" in item:
                        item["next_review"] = datetime.fromisoformat(item["next_review"])
                    if "last_reviewed" in item and item["last_reviewed"]:
                        item["last_reviewed"] = datetime.fromisoformat(item["last_reviewed"])
                    cards.append(Card(**item))
                return cards
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_cards(self, cards: List[Card]):
        """Save all cards to storage"""
        with open(self.file_path, "w") as f:
            # Convert cards to dicts with serialized datetimes
            data = []
            for card in cards:
                card_dict = card.model_dump()
                card_dict["created_at"] = card.created_at.isoformat()
                card_dict["next_review"] = card.next_review.isoformat()
                if card.last_reviewed:
                    card_dict["last_reviewed"] = card.last_reviewed.isoformat()
                else:
                    card_dict["last_reviewed"] = None
                data.append(card_dict)
            json.dump(data, f, indent=2)

    def add_card(self, card: Card):
        """Add a new card"""
        cards = self.load_cards()
        cards.append(card)
        self.save_cards(cards)

    def update_card(self, updated_card: Card):
        """Update an existing card"""
        cards = self.load_cards()
        for i, card in enumerate(cards):
            if card.id == updated_card.id:
                cards[i] = updated_card
                break
        self.save_cards(cards)

    def delete_card(self, card_id: str):
        """Delete a card"""
        cards = self.load_cards()
        cards = [c for c in cards if c.id != card_id]
        self.save_cards(cards)

    def get_card_by_id(self, card_id: str) -> Optional[Card]:
        """Get a card by its ID"""
        cards = self.load_cards()
        for card in cards:
            if card.id == card_id:
                return card
        return None

    def backup_now(self) -> str:
        """Create a backup of the current data file"""
        if not os.path.exists(self.file_path):
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"vocabulary_cards_backup_{timestamp}.json"
        backup_path = os.path.join(self.backup_dir, backup_filename)

        shutil.copy2(self.file_path, backup_path)
        return backup_path
