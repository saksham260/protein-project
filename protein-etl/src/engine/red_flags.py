"""Red-Flag Detection Engine for The Protein Discovery Engine.

Scans normalized ingredient lists against a curated alias dictionary with
FSSAI-mandated INS numbers and canonical flag metadata.
"""

from __future__ import annotations
import json
import re
from pathlib import Path
from src.models import RedFlagItem

DICT_PATH = Path(__file__).resolve().parent.parent / "data" / "red_flag_dictionary.json"


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
        List of RedFlagItem objects.
    """
    if not ingredients:
        return []

    dictionary = load_red_flag_dictionary()
    detected_flags: list[RedFlagItem] = []
    seen_keys: set[tuple[str, str]] = set()
    seen_flag_types: set[str] = set()

    # Pre-normalize all input ingredients
    normalized_ingredients = [normalize_ingredient_token(ing) for ing in ingredients]
    full_deck_text = " , ".join(normalized_ingredients)

    for flag_type, flag_meta in dictionary.items():
        severity = flag_meta["severity"]
        badge_label = flag_meta["badge_label"]
        tooltip = flag_meta["tooltip"]

        for pattern_entry in flag_meta.get("patterns", []):
            canonical = pattern_entry["canonical"]
            ins_code = pattern_entry.get("ins")
            match_variants = pattern_entry.get("match", [])
            pattern_matched = False

            for variant in match_variants:
                var_norm = normalize_ingredient_token(variant)
                escaped_var = re.escape(var_norm)
                regex_pattern = rf"(?:\b|\W){escaped_var}(?:\b|\W)"

                if re.search(regex_pattern, f" {full_deck_text} "):
                    key = (flag_type, canonical)
                    if key not in seen_keys:
                        seen_keys.add(key)
                        detected_flags.append(
                            RedFlagItem(
                                flag_type=flag_type,
                                flag_severity=severity,
                                flag_label=badge_label,
                                flag_description=tooltip,
                                matched_ingredient=canonical,
                                ins_number=ins_code,
                            )
                        )
                        pattern_matched = True
                        seen_flag_types.add(flag_type)
                    break

            # For single-substance alerts like maltitol_alert, once matched we don't need redundant sub-patterns
            if pattern_matched and flag_type == "maltitol_alert":
                break

    return detected_flags
