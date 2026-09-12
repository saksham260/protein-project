"""Shared term-matching helpers for the ingredient scanners."""

from __future__ import annotations
import re
from typing import Any

Span = tuple[int, int]


def find_term_spans(text: str, term: str) -> list[Span]:
    """Return (start, end) spans where `term` appears in `text` as a whole word or phrase."""
    pattern = rf"(?<!\w){re.escape(term)}(?!\w)"
    return [(m.start(), m.end()) for m in re.finditer(pattern, text)]


def pick_longest_matches(candidates: list[tuple[Span, Any]]) -> list[tuple[Span, Any]]:
    """Keep the longest non-overlapping matches, returned in text order.

    Stops a short alias from double-counting text already claimed by a longer one,
    e.g. "glucose syrup" inside "hydrogenated glucose syrup".
    """
    chosen: list[tuple[Span, Any]] = []
    for span, payload in sorted(candidates, key=lambda c: (c[0][0] - c[0][1], c[0][0])):
        start, end = span
        if all(end <= c_start or start >= c_end for (c_start, c_end), _ in chosen):
            chosen.append((span, payload))
    return sorted(chosen, key=lambda c: c[0][0])
