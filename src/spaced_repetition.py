"""
Spaced Repetition System using SM-2 algorithm
Based on SuperMemo 2 algorithm for optimal learning intervals
"""

from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field


class Card(BaseModel):
    """Represents a vocabulary or phrase card"""

    id: str
    front: str  # Word or phrase
    back: str  # Definition, translation, or explanation
    category: str = "general"  # e.g., "vocabulary", "phrase", "idiom"
    example: Optional[str] = None  # Example sentence
    created_at: datetime = Field(default_factory=datetime.now)

    # Spaced repetition fields
    ease_factor: float = 2.5  # EF starts at 2.5
    interval: int = 1  # Days until next review
    repetitions: int = 0  # Number of successful reviews
    next_review: datetime = Field(default_factory=datetime.now)
    last_reviewed: Optional[datetime] = None


class SpacedRepetition:
    """Implements SM-2 spaced repetition algorithm"""

    @staticmethod
    def calculate_next_review(card: Card, quality: int) -> Card:
        """
        Calculate next review date based on SM-2 algorithm

        Quality scale:
        0 - Complete blackout (incorrect response)
        1 - Incorrect response, but remembered with difficulty
        2 - Incorrect response, but correct after hesitation
        3 - Correct response, but with difficulty
        4 - Correct response after some hesitation
        5 - Perfect response (immediate recall)
        """
        now = datetime.now()
        card.last_reviewed = now

        if quality < 3:
            # Incorrect or difficult - reset
            card.repetitions = 0
            card.interval = 1
        else:
            # Correct response
            if card.repetitions == 0:
                card.interval = 1
            elif card.repetitions == 1:
                card.interval = 6
            else:
                card.interval = int(card.interval * card.ease_factor)

            card.repetitions += 1

            # Update ease factor
            card.ease_factor = max(
                1.3, card.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            )

        card.next_review = now + timedelta(days=card.interval)
        return card

    @staticmethod
    def get_due_cards(cards: list[Card]) -> list[Card]:
        """Get all cards that are due for review"""
        now = datetime.now()
        return [card for card in cards if card.next_review <= now]

    @staticmethod
    def get_stats(cards: list[Card]) -> dict:
        """Get statistics about the learning progress"""
        total = len(cards)
        due = len(SpacedRepetition.get_due_cards(cards))
        mastered = len([c for c in cards if c.repetitions >= 5 and c.interval >= 30])
        new = len([c for c in cards if c.repetitions == 0])

        return {
            "total_cards": total,
            "due_for_review": due,
            "mastered": mastered,
            "new_cards": new,
            "in_progress": total - new - mastered,
        }
