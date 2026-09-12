"""Protein Tier Classifier for The Protein Discovery Engine.

Classifies protein products into Tiers 1 through 4 based on:
1. Primary protein source (first protein source in the ingredient deck).
2. Weakest-link rule: overall tier is set by the lowest-quality protein source present in the blend.
3. Amino-spiking override: any free-form amino addition demotes the blend to Tier 4.
"""

from __future__ import annotations
import json
from pathlib import Path

try:
    from src.engine.text_match import find_term_spans, pick_longest_matches
    from src.models import ProteinProfile, RedFlagItem
except (ImportError, ModuleNotFoundError):
    from engine.text_match import find_term_spans, pick_longest_matches
    from models import ProteinProfile, RedFlagItem

SOURCES_PATH = Path(__file__).resolve().parent.parent / "data" / "protein_sources.json"


def load_protein_sources() -> dict:
    """Load curated protein sources and tier definitions from disk."""
    with open(SOURCES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["tier_definitions"]


def classify_protein_profile(
    ingredients: list[str],
    red_flags: list[RedFlagItem] | None = None,
) -> ProteinProfile:
    """Analyze the ingredient deck to determine primary source, free-form aminos, and tier.

    Args:
        ingredients: List of ingredient strings from pack / FSSAI label.
        red_flags: Optional list of previously scanned RedFlagItems.

    Returns:
        ProteinProfile containing primary_protein_source, protein_tier, and has_added_free_form_aminos.
    """
    if not ingredients:
        return ProteinProfile(
            primary_protein_source="Unknown",
            protein_tier="Unknown / Unclassified",
            has_added_free_form_aminos=False,
        )

    tier_defs = load_protein_sources()

    # Format: (deck position, position inside the ingredient, tier rank, canonical name).
    # The inner position orders sources listed together in a blend, e.g.
    # "Protein Blend (Soy Protein Isolate, Whey Protein Concentrate)".
    found_sources: list[tuple[int, int, int, str]] = []

    for ing_idx, raw_ing in enumerate(ingredients):
        ing_clean = raw_ing.lower().strip()
        candidates = []
        for tier_data in tier_defs.values():
            for source_entry in tier_data["sources"]:
                for match_term in source_entry["match"]:
                    for span in find_term_spans(ing_clean, match_term.lower()):
                        candidates.append((span, (tier_data["rank"], source_entry["canonical"])))

        for (start, _), (tier_rank, canonical) in pick_longest_matches(candidates):
            found_sources.append((ing_idx, start, tier_rank, canonical))

    # Check for amino spiking flag
    has_aminos = False
    if red_flags:
        has_aminos = any(f.flag_type == "amino_spiking" for f in red_flags)

    # If no protein sources found
    if not found_sources:
        tier_label = (
            tier_defs["tier_4"]["label"]
            if has_aminos
            else "Unknown / Unclassified"
        )
        return ProteinProfile(
            primary_protein_source="Unknown",
            protein_tier=tier_label,
            has_added_free_form_aminos=has_aminos,
        )

    # Sort by deck position to identify primary protein source (first in descending weight)
    found_sources.sort(key=lambda s: (s[0], s[1]))
    primary_source = found_sources[0][3]

    # Weakest link rule: maximum rank number (4 is lowest quality, 1 is highest)
    max_rank = max(s[2] for s in found_sources)

    # If amino spiked, demote to Tier 4 regardless of protein base
    if has_aminos:
        tier_label = tier_defs["tier_4"]["label"]
    else:
        # Find the label matching max_rank
        tier_label = next(
            data["label"] for data in tier_defs.values() if data["rank"] == max_rank
        )

    return ProteinProfile(
        primary_protein_source=primary_source,
        protein_tier=tier_label,
        has_added_free_form_aminos=has_aminos,
    )
