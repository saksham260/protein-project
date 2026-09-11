"""Unit tests for Shopify and manual parsers."""

import pytest
from unittest.mock import MagicMock
from src.parsers.manual import parse_raw_ingredient_deck
from src.parsers.shopify import parse_shopify_url, extract_shopify_product


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
    assert result["variants"][0]["weight_g"] == 312.0


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
