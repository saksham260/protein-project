"""Unit tests for the Red-Flag detection engine — covering Suite 3 test cases."""

import pytest
from src.engine.red_flags import (
    normalize_ingredient_token,
    scan_ingredients_for_red_flags,
)


# ==========================================
# 3.1 normalize_ingredient_token
# ==========================================

def test_normalize_token_lowering_and_strip():
    assert normalize_ingredient_token("  Maltitol Syrup  ") == "maltitol syrup"


def test_normalize_token_dashes():
    assert normalize_ingredient_token("Sugar–Free") == "sugar-free"
    assert normalize_ingredient_token("Sugar—Free") == "sugar-free"


def test_normalize_token_quotes():
    assert normalize_ingredient_token('"Corn Syrup"') == "corn syrup"
    assert normalize_ingredient_token("'Corn Syrup'") == "corn syrup"


def test_normalize_token_whitespace():
    assert normalize_ingredient_token("Palm   Oil") == "palm oil"


# ==========================================
# 3.2 scan_ingredients_for_red_flags
# ==========================================

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


def test_maltitol_single_badge_deduplication():
    # Both maltitol and maltitol syrup should collapse to 1 single badge because of SINGLE_BADGE_FLAGS
    deck = ["Maltitol", "Maltitol Syrup", "Whey Protein"]
    flags = scan_ingredients_for_red_flags(deck)
    maltitol_flags = [f for f in flags if f.flag_type == "maltitol_alert"]
    assert len(maltitol_flags) == 1


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
    matched_ingredients = [f.matched_ingredient for f in flags]
    assert "Glycine" in matched_ingredients
    assert "Taurine" in matched_ingredients


def test_amino_spiking_glutamine():
    deck = ["Whey Protein", "L-Glutamine"]
    flags = scan_ingredients_for_red_flags(deck)
    assert any(f.flag_type == "amino_spiking" for f in flags)


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


def test_vanaspati_detection():
    deck = ["Vanaspati Ghee", "Whey Protein"]
    flags = scan_ingredients_for_red_flags(deck)
    assert any(f.flag_type == "fat_quality" for f in flags)


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


def test_corn_syrup_detection():
    deck = ["Corn Syrup", "Soy Protein"]
    flags = scan_ingredients_for_red_flags(deck)
    assert any(f.flag_type == "hidden_sugars" for f in flags)


def test_multiple_red_flags_combined():
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
    flags = scan_ingredients_for_red_flags(["Whey Protein Isolate", "Hydrogenated Glucose Syrup"])
    assert [f.flag_type for f in flags] == ["maltitol_alert"]


def test_hfcs_is_not_also_reported_as_corn_syrup():
    flags = scan_ingredients_for_red_flags(["High Fructose Corn Syrup"])
    assert [f.matched_ingredient for f in flags] == ["High Fructose Corn Syrup"]


def test_ins_and_e_number_matching():
    flags_ins = scan_ingredients_for_red_flags(["INS 965"])
    assert any(f.flag_type == "maltitol_alert" for f in flags_ins)

    flags_e = scan_ingredients_for_red_flags(["Sweetener E965"])
    assert any(f.flag_type == "maltitol_alert" for f in flags_e)


def test_empty_ingredient_deck():
    assert scan_ingredients_for_red_flags([]) == []


def test_case_insensitivity_matching():
    flags = scan_ingredients_for_red_flags(["PALM OIL"])
    assert any(f.flag_type == "fat_quality" for f in flags)


def test_bare_number_1400_is_not_flagged():
    assert scan_ingredients_for_red_flags(["Whey Protein Isolate", "Batch 1400"]) == []
