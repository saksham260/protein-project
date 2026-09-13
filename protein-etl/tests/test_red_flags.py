"""Unit tests for the Red-Flag detection engine."""

import pytest
from src.engine.red_flags import scan_ingredients_for_red_flags


def test_clean_ingredient_deck_has_zero_flags():
    clean_ingredients = [
        "Whey Protein Isolate",
        "Raw Almonds",
        "Chicory Root Fiber",
        "Cocoa Butter",
        "Dark Chocolate (Cocoa Mass)",
        "Stevia Leaf Extract",
    ]
    flags = scan_ingredients_for_red_flags(clean_ingredients)
    assert len(flags) == 0


def test_maltitol_detection_with_ins():
    deck = [
        "Soy Protein Isolate",
        "Maltitol Syrup (INS 965(ii))",
        "Cocoa Powder",
        "Sunflower Lecithin",
    ]
    flags = scan_ingredients_for_red_flags(deck)
    assert len(flags) == 1
    assert flags[0].flag_type == "maltitol_alert"
    assert flags[0].flag_severity == "high"
    assert "Maltitol" in flags[0].flag_label
    assert flags[0].ins_number in ["INS 965(i)", "INS 965(ii)"]


def test_amino_spiking_detection():
    deck = [
        "Whey Protein Concentrate",
        "Added L-Glycine",
        "Taurine",
        "Natural Flavors",
    ]
    flags = scan_ingredients_for_red_flags(deck)
    flag_types = [f.flag_type for f in flags]
    assert "amino_spiking" in flag_types
    # Both Glycine and Taurine should be detected as patterns under amino_spiking
    matched_ingredients = [f.matched_ingredient for f in flags]
    assert "Glycine" in matched_ingredients
    assert "Taurine" in matched_ingredients


def test_palm_oil_and_hydrogenated_fat_detection():
    deck = [
        "Rolled Oats",
        "Refined Palmolein Oil",
        "Interesterified Vegetable Fat",
        "Peanut Butter",
    ]
    flags = scan_ingredients_for_red_flags(deck)
    flag_types = [f.flag_type for f in flags]
    assert "fat_quality" in flag_types
    matched = [f.matched_ingredient for f in flags]
    assert "Palm Oil" in matched or "Hydrogenated Fat" in matched


def test_hidden_sugars_detection():
    deck = [
        "Whey Protein Concentrate",
        "Maltodextrin (INS 1400)",
        "Dextrose Monohydrate",
        "Artificial Vanilla Flavor",
    ]
    flags = scan_ingredients_for_red_flags(deck)
    flag_types = [f.flag_type for f in flags]
    assert "hidden_sugars" in flag_types
    matched = [f.matched_ingredient for f in flags]
    assert "Maltodextrin" in matched
    assert "Dextrose" in matched


def test_multiple_red_flags_combined():
    # A heavily deceptive protein bar
    dirty_deck = [
        "Soy Protein Isolate",
        "Maltitol",
        "Palm Oil",
        "L-Glycine",
        "High Fructose Corn Syrup",
    ]
    flags = scan_ingredients_for_red_flags(dirty_deck)
    flag_types = {f.flag_type for f in flags}
    assert flag_types == {"maltitol_alert", "amino_spiking", "fat_quality", "hidden_sugars"}


def test_hydrogenated_glucose_syrup_is_only_a_maltitol_flag():
    # "glucose syrup" (hidden sugar) sits inside "hydrogenated glucose syrup" (maltitol alias)
    flags = scan_ingredients_for_red_flags(["Whey Protein Isolate", "Hydrogenated Glucose Syrup"])
    assert [f.flag_type for f in flags] == ["maltitol_alert"]


def test_hfcs_is_not_also_reported_as_corn_syrup():
    flags = scan_ingredients_for_red_flags(["High Fructose Corn Syrup"])
    assert [f.matched_ingredient for f in flags] == ["High Fructose Corn Syrup"]


def test_bare_number_1400_is_not_flagged():
    assert scan_ingredients_for_red_flags(["Whey Protein Isolate", "Batch 1400"]) == []
