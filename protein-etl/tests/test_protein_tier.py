"""Unit tests for the Protein Tier Classifier — covering Suite 4 test cases."""

import pytest
from src.engine.protein_tier import classify_protein_profile
from src.models import RedFlagItem


def test_pure_isolate_is_tier_1():
    deck = [
        "Whey Protein Isolate",
        "Cocoa Powder",
        "Sunflower Lecithin",
        "Stevia Extract",
    ]
    profile = classify_protein_profile(deck)
    assert profile.primary_protein_source == "Whey Protein Isolate"
    assert "Tier 1" in profile.protein_tier
    assert not profile.has_added_free_form_aminos


def test_wpc_only_is_tier_2():
    deck = ["Whey Protein Concentrate", "Sugar"]
    profile = classify_protein_profile(deck)
    assert profile.primary_protein_source == "Whey Protein Concentrate"
    assert "Tier 2" in profile.protein_tier


def test_isolate_and_concentrate_blend_is_tier_2():
    deck = [
        "Whey Protein Isolate",
        "Whey Protein Concentrate",
        "Natural Vanilla Flavor",
    ]
    profile = classify_protein_profile(deck)
    assert profile.primary_protein_source == "Whey Protein Isolate"
    assert "Tier 2" in profile.protein_tier


def test_isolate_with_collagen_is_tier_4():
    deck = [
        "Whey Protein Isolate (70%)",
        "Almond Butter",
        "Hydrolyzed Collagen Peptides (15%)",
        "Cocoa Butter",
    ]
    profile = classify_protein_profile(deck)
    assert profile.primary_protein_source == "Whey Protein Isolate"
    assert "Tier 4" in profile.protein_tier


def test_plant_blend_is_tier_3():
    deck = [
        "Organic Pea Protein Isolate",
        "Sprouted Brown Rice Protein",
        "Cocoa",
        "Monk Fruit Extract",
    ]
    profile = classify_protein_profile(deck)
    assert profile.primary_protein_source == "Pea Protein Isolate"
    assert "Tier 3" in profile.protein_tier


def test_amino_spiked_product_forced_to_tier_4():
    deck = [
        "Whey Protein Isolate",
        "Natural Chocolate Flavor",
    ]
    flags = [
        RedFlagItem(
            flag_type="amino_spiking",
            flag_severity="amber",
            flag_label="Added Aminos Detected",
            flag_description="Free-form glycine added",
            matched_ingredient="Glycine",
        )
    ]
    profile = classify_protein_profile(deck, red_flags=flags)
    assert profile.primary_protein_source == "Whey Protein Isolate"
    assert profile.has_added_free_form_aminos is True
    assert "Tier 4" in profile.protein_tier


def test_blend_order_primary_source():
    deck = ["Pea Protein Isolate", "Whey Protein Concentrate"]
    profile = classify_protein_profile(deck)
    assert profile.primary_protein_source == "Pea Protein Isolate"


def test_primary_source_follows_label_order_inside_blend():
    deck = [
        "Protein Blend (Soy Protein Isolate, Whey Protein Concentrate, Calcium Caseinate)",
        "Cocoa Powder",
    ]
    profile = classify_protein_profile(deck)
    assert profile.primary_protein_source == "Soy Protein Isolate"
    assert "Tier 3" in profile.protein_tier


def test_casein_tier_2():
    profile = classify_protein_profile(["Micellar Casein", "Cocoa"])
    assert profile.primary_protein_source == "Micellar Casein"
    assert "Tier 2" in profile.protein_tier


def test_egg_white_protein_tier_2():
    profile = classify_protein_profile(["Egg White Protein", "Almonds"])
    assert "Tier 2" in profile.protein_tier


def test_soy_protein_isolate_tier_3():
    profile = classify_protein_profile(["Soy Protein Isolate"])
    assert "Tier 3" in profile.protein_tier


def test_wheat_gluten_tier_4():
    profile = classify_protein_profile(["Wheat Gluten"])
    assert "Tier 4" in profile.protein_tier


def test_caseinate_matches_its_own_source_not_micellar_casein():
    profile = classify_protein_profile(["Calcium Caseinate", "Cocoa"])
    assert profile.primary_protein_source == "Calcium Caseinate"


def test_empty_deck():
    profile = classify_protein_profile([])
    assert profile.primary_protein_source == "Unknown"
    assert "Unknown" in profile.protein_tier
    assert profile.has_added_free_form_aminos is False


def test_unrecognized_deck():
    profile = classify_protein_profile(["Apples", "Water", "Sugar"])
    assert profile.primary_protein_source == "Unknown"
    assert "Unknown" in profile.protein_tier


def test_no_protein_with_amino_spiking():
    flags = [
        RedFlagItem(
            flag_type="amino_spiking",
            flag_severity="amber",
            flag_label="Added Aminos Detected",
            flag_description="Glycine",
            matched_ingredient="Glycine",
        )
    ]
    profile = classify_protein_profile(["Sugar", "Glycine"], red_flags=flags)
    assert profile.primary_protein_source == "Unknown"
    assert "Tier 4" in profile.protein_tier
