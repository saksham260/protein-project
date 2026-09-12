"""Unit tests for variant pack-math and redirect validation."""

import pytest
from pydantic import ValidationError
from src.models import VariantCreate

NUTRITION = {"calories_kcal": 135.0, "protein_g": 24.0, "total_fat_g": 2.0, "total_carbs_g": 5.0}


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


def test_servings_per_pack_derived_when_missing():
    assert make_variant().servings_per_pack == 29
    assert make_variant(net_weight_g=52.0, serving_size_g=52.0).servings_per_pack == 1


def test_servings_per_pack_that_does_not_match_weight_is_rejected():
    # A 1kg tub cannot be a single 35g serving
    with pytest.raises(ValidationError):
        make_variant(servings_per_pack=1)


def test_serving_larger_than_pack_is_rejected():
    with pytest.raises(ValidationError):
        make_variant(net_weight_g=52.0, serving_size_g=100.0)


def test_duplicate_platform_links_are_rejected():
    links = [
        {"platform": "amazon", "url": "https://www.amazon.in/s?k=a"},
        {"platform": "amazon", "url": "https://www.amazon.in/s?k=b"},
    ]
    with pytest.raises(ValidationError):
        make_variant(redirect_links=links)
