"""Data schemas for API request and response validation."""

from dataclasses import dataclass
from typing import List


@dataclass
class ConjugationEntry:
    """Single conjugation with pronoun and verb form."""
    pronoun: str
    form: str


@dataclass
class ConjugationRequest:
    """Request schema for /conjugate endpoint."""
    verb: str


@dataclass
class ConjugationResponse:
    """Response schema for /conjugate endpoint."""
    english: str
    greek: str
    conjugations: List[ConjugationEntry]
    confidence: float
    notes: str
