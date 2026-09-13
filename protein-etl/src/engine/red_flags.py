"""Red-Flag Detection Engine for The Protein Discovery Engine.

Scans normalized ingredient lists against a curated alias dictionary with
FSSAI-mandated INS numbers and canonical flag metadata.
"""

from __future__ import annotations
import json
import re
from pathlib import Path

try:
    from src.engine.text_match import find_term_spans, pick_longest_matches
    from src.models import RedFlagItem
except (ImportError, ModuleNotFoundError):
    from engine.text_match import find_term_spans, pick_longest_matches
    from models import RedFlagItem

DICT_PATH = Path(__file__).resolve().parent.parent / "data" / "red_flag_dictionary.json"

# Flag types that show a single badge no matter how many of their patterns match.
SINGLE_BADGE_FLAGS = {"maltitol_alert"}


def load_red_flag_dictionary() -> dict:
    """Load the curated red-flag dictionary from disk."""
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_ingredient_token(text: str) -> str:
    """Normalize ingredient string for robust token matching."""
    text = text.lower().strip()
    text = text.replace("–", "-").replace("—", "-").replace("'", "").replace('"', "")
    text = re.sub(r"\s+", " ", text)
    return text


def scan_ingredients_for_red_flags(ingredients: list[str]) -> list[RedFlagItem]:
    """Scan an ingredient list and return all identified red flags without duplicates.

    Args:
        ingredients: List of ingredient strings from pack / FSSAI label.

    Returns:
        List of RedFlagItem objects, in dictionary order.
    """
    if not ingredients:
        return []

    dictionary = load_red_flag_dictionary()
    full_deck_text = " , ".join(normalize_ingredient_token(ing) for ing in ingredients)

    # Collect every alias hit, then keep only the longest non-overlapping ones.
    candidates = []
    for flag_order, (flag_type, flag_meta) in enumerate(dictionary.items()):
        for pattern_order, pattern_entry in enumerate(flag_meta.get("patterns", [])):
            for variant in pattern_entry.get("match", []):
                for span in find_term_spans(full_deck_text, normalize_ingredient_token(variant)):
                    candidates.append((span, (flag_order, pattern_order, flag_type, pattern_entry)))

    hits: dict[tuple[int, int], tuple[str, dict]] = {}
    for _, (flag_order, pattern_order, flag_type, pattern_entry) in pick_longest_matches(candidates):
        hits.setdefault((flag_order, pattern_order), (flag_type, pattern_entry))

    detected_flags: list[RedFlagItem] = []
    badged: set[str] = set()
    for _, (flag_type, pattern_entry) in sorted(hits.items()):
        if flag_type in SINGLE_BADGE_FLAGS:
            if flag_type in badged:
                continue
            badged.add(flag_type)

        flag_meta = dictionary[flag_type]
        detected_flags.append(
            RedFlagItem(
                flag_type=flag_type,
                flag_severity=flag_meta["severity"],
                flag_label=flag_meta["badge_label"],
                flag_description=flag_meta["tooltip"],
                matched_ingredient=pattern_entry["canonical"],
                ins_number=pattern_entry.get("ins"),
            )
        )

    return detected_flags
