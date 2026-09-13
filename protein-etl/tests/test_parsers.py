"""Unit tests for Shopify and manual parsers."""

import pytest
from unittest.mock import MagicMock
from src.parsers.manual import parse_raw_ingredient_deck
from src.parsers.shopify import parse_shopify_url, extract_shopify_product, parse_weight_g


def test_parse_shopify_url_valid():
    url = "https://thewholetruthfoods.com/products/dark-chocolate-protein-bar?variant=400123"
    domain, handle = parse_shopify_url(url)
    assert domain == "https://thewholetruthfoods.com"
    assert handle == "dark-chocolate-protein-bar"


def test_parse_shopify_url_invalid():
    with pytest.raises(ValueError):
        parse_shopify_url("https://thewholetruthfoods.com/collections/all")


def test_extract_shopify_product_with_mock():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "product": {
            "title": "Double Cocoa Bar",
            "vendor": "The Whole Truth",
            "body_html": "<p>Made with <strong>100% natural</strong> ingredients.</p>",
            "tags": ["Protein Bar", "Gluten Free"],
            "images": [{"src": "https://cdn.shopify.com/image.jpg"}],
            "variants": [
                {
                    "title": "Box of 6",
                    "price": "900.00",
                    "grams": 312,
                    "sku": "TWT-DCB-6",
                }
            ],
        }
    }
    mock_client.get.return_value = mock_response

    result = extract_shopify_product(
        "https://thewholetruthfoods.com/products/double-cocoa-bar",
        client=mock_client,
    )

    assert result["title"] == "Double Cocoa Bar"
    assert result["brand_name"] == "The Whole Truth"
    assert "100% natural" in result["description"]
    assert len(result["variants"]) == 1
    assert result["variants"][0]["price_inr"] == 900.0
    assert result["variants"][0]["mrp_inr"] == 900.0
    # No size in the title, so it falls back to the shipping weight and says so
    assert result["variants"][0]["weight_g"] == 312.0
    assert result["variants"][0]["weight_source"] == "shipping"


def test_extract_shopify_reads_mrp_and_label_weight():
    mock_client = MagicMock()
    mock_client.get.return_value.json.return_value = {
        "product": {
            "title": "Biozyme Whey Isolate",
            "vendor": "MuscleBlaze",
            "variants": [
                {"title": "Rich Chocolate / 1kg", "price": "2999.00", "compare_at_price": "3499.00", "grams": 1250},
            ],
        }
    }

    variant = extract_shopify_product(
        "https://example-store.com/products/biozyme-whey-isolate", client=mock_client
    )["variants"][0]

    assert variant["mrp_inr"] == 3499.0
    assert variant["price_inr"] == 2999.0
    assert variant["weight_g"] == 1000.0
    assert variant["weight_source"] == "label"
    assert variant["shipping_weight_g"] == 1250.0


def test_parse_weight_g():
    assert parse_weight_g("1kg") == 1000.0
    assert parse_weight_g("Chocolate 500 g") == 500.0
    assert parse_weight_g("1.5 Kg tub") == 1500.0
    assert parse_weight_g("Rose 200ml") == 200.0
    assert parse_weight_g("Box of 6") is None
    assert parse_weight_g(None) is None


def test_parse_raw_ingredient_deck_simple():
    text = "Whey Protein Isolate, Cocoa Powder, Almonds, Stevia"
    tokens = parse_raw_ingredient_deck(text)
    assert tokens == ["Whey Protein Isolate", "Cocoa Powder", "Almonds", "Stevia"]


def test_parse_raw_ingredient_deck_with_parentheses():
    text = "Whey Protein Isolate (Milk), Dark Chocolate (Cocoa Mass, Sugar, Cocoa Butter), Roasted Almonds, Sea Salt."
    tokens = parse_raw_ingredient_deck(text)
    assert len(tokens) == 4
    assert tokens[0] == "Whey Protein Isolate (Milk)"
    assert tokens[1] == "Dark Chocolate (Cocoa Mass, Sugar, Cocoa Butter)"
    assert tokens[2] == "Roasted Almonds"
    assert tokens[3] == "Sea Salt"


def test_parse_raw_ingredient_deck_bullets_and_newlines():
    text = """
    • Whey Protein Concentrate
    • Cocoa Solids
    • INS 965(ii) Maltitol Syrup
    """
    tokens = parse_raw_ingredient_deck(text)
    assert len(tokens) == 3
    assert tokens[0] == "Whey Protein Concentrate"
    assert tokens[1] == "Cocoa Solids"
    assert tokens[2] == "INS 965(ii) Maltitol Syrup"
