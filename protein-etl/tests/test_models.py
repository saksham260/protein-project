"""Unit tests for Pydantic models, slugify, pack-math, and redirect validation — Suite 5."""

import pytest
from pydantic import ValidationError
from src.models import (
    NutritionPerPack,
    ProductCreate,
    RedirectLinkItem,
    VariantCreate,
    slugify,
)

NUTRITION = {
    "calories_kcal": 135.0,
    "protein_g": 24.0,
    "total_fat_g": 2.0,
    "total_carbs_g": 5.0,
}


def make_variant(**overrides) -> VariantCreate:
    fields = {
        "variant_name": "Chocolate 1kg",
        "mrp_inr": 2499.0,
        "net_weight_g": 1000.0,
        "serving_size_g": 35.0,
        "nutrition": NUTRITION,
    }
    fields.update(overrides)
    return VariantCreate(**fields)


# ==========================================
# 5.1 slugify
# ==========================================

def test_slugify_normal_text():
    assert slugify("The Whole Truth Protein Bar") == "the-whole-truth-protein-bar"


def test_slugify_special_characters():
    assert slugify("MuscleBlaze Biozyme (1kg)") == "muscleblaze-biozyme-1kg"


def test_slugify_multiple_spaces_dashes():
    assert slugify("Nakpro  Gold -- Whey") == "nakpro-gold-whey"


def test_slugify_leading_trailing():
    assert slugify("  Test  ") == "test"


# ==========================================
# 5.2 NutritionPerPack
# ==========================================

def test_nutrition_per_pack_valid():
    nut = NutritionPerPack(
        calories_kcal=200.0,
        protein_g=25.0,
        total_fat_g=5.0,
        total_carbs_g=10.0,
    )
    assert nut.protein_g == 25.0
    assert nut.saturated_fat_g == 0.0  # default field
    assert nut.dietary_fiber_g == 0.0


def test_nutrition_per_pack_negative_calories():
    with pytest.raises(ValidationError):
        NutritionPerPack(
            calories_kcal=-10.0,
            protein_g=20.0,
            total_fat_g=2.0,
            total_carbs_g=5.0,
        )


def test_nutrition_per_pack_missing_required():
    with pytest.raises(ValidationError):
        NutritionPerPack(
            protein_g=20.0,
            total_fat_g=2.0,
            total_carbs_g=5.0,
        )


def test_nutrition_per_pack_zero_protein():
    nut = NutritionPerPack(
        calories_kcal=100.0,
        protein_g=0.0,
        total_fat_g=2.0,
        total_carbs_g=5.0,
    )
    assert nut.protein_g == 0.0


# ==========================================
# 5.3 VariantCreate
# ==========================================

def test_variant_auto_slugify():
    v = make_variant(variant_name="Double Rich Choc (1kg)")
    assert v.slug == "double-rich-choc-1kg"


def test_variant_explicit_slug_preserved():
    v = make_variant(slug="custom-slug")
    assert v.slug == "custom-slug"


def test_servings_per_pack_derived_when_missing():
    assert make_variant().servings_per_pack == 29
    assert make_variant(net_weight_g=52.0, serving_size_g=52.0).servings_per_pack == 1
    # 1000g / 31.25g = 32
    assert make_variant(net_weight_g=1000.0, serving_size_g=31.25).servings_per_pack == 32


def test_servings_per_pack_that_does_not_match_weight_is_rejected():
    with pytest.raises(ValidationError):
        make_variant(servings_per_pack=1)


def test_serving_larger_than_pack_is_rejected():
    with pytest.raises(ValidationError):
        make_variant(net_weight_g=52.0, serving_size_g=100.0)


def test_pack_math_within_tolerance():
    # 1000g tub with 30 servings of 35g = 1050g (5% diff, within 25% tolerance)
    v = make_variant(net_weight_g=1000.0, serving_size_g=35.0, servings_per_pack=30)
    assert v.servings_per_pack == 30


def test_duplicate_platform_links_are_rejected():
    links = [
        {"platform": "amazon", "url": "https://www.amazon.in/s?k=a"},
        {"platform": "amazon", "url": "https://www.amazon.in/s?k=b"},
    ]
    with pytest.raises(ValidationError):
        make_variant(redirect_links=links)


def test_unique_platform_links_accepted():
    links = [
        {"platform": "amazon", "url": "https://www.amazon.in/dp/B1"},
        {"platform": "blinkit", "url": "https://blinkit.com/prn/1"},
    ]
    v = make_variant(redirect_links=links)
    assert len(v.redirect_links) == 2


def test_variant_invalid_mrp():
    with pytest.raises(ValidationError):
        make_variant(mrp_inr=0.0)
    with pytest.raises(ValidationError):
        make_variant(mrp_inr=-10.0)


def test_variant_invalid_weight():
    with pytest.raises(ValidationError):
        make_variant(net_weight_g=0.0)


# ==========================================
# 5.4 ProductCreate
# ==========================================

def test_product_auto_slugify():
    prod = ProductCreate(
        name="Biozyme Performance Whey",
        brand_name="MuscleBlaze",
        category_slug="protein-powders",
    )
    assert prod.slug == "muscleblaze-biozyme-performance-whey"


def test_product_explicit_slug():
    prod = ProductCreate(
        name="Biozyme Performance Whey",
        brand_name="MuscleBlaze",
        category_slug="protein-powders",
        slug="custom-mb-biozyme",
    )
    assert prod.slug == "custom-mb-biozyme"


def test_product_empty_variants_allowed():
    prod = ProductCreate(
        name="Bar",
        brand_name="Brand",
        category_slug="protein-bars",
    )
    assert prod.variants == []
