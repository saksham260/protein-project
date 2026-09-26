"""Layer 1: Open Food Facts (free, open data, ODbL licence — credit Open Food Facts on the site)."""

from __future__ import annotations
import os
from typing import Optional
import httpx

try:
    from src.discovery.facts import LabelFacts, REQUIRED_NUTRIENTS, scale_per_100g
except (ImportError, ModuleNotFoundError):
    from discovery.facts import LabelFacts, REQUIRED_NUTRIENTS, scale_per_100g

OFF_PRODUCT_URL = "https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
OFF_FIELDS = "nutriments,serving_quantity,ingredients_text,allergens_tags"
# Open Food Facts asks every client to identify itself.
OFF_USER_AGENT = os.getenv("OFF_USER_AGENT", "ProteinDiscoveryEngine/0.1 (protein-etl)")

# OFF nutriment key -> (our field, multiplier from OFF's unit). OFF stores sodium/cholesterol in grams.
OFF_NUTRIENTS = {
    "energy-kcal": ("calories_kcal", 1),
    "proteins": ("protein_g", 1),
    "fat": ("total_fat_g", 1),
    "saturated-fat": ("saturated_fat_g", 1),
    "trans-fat": ("trans_fat_g", 1),
    "cholesterol": ("cholesterol_mg", 1000),
    "carbohydrates": ("total_carbs_g", 1),
    "fiber": ("dietary_fiber_g", 1),
    "sugars": ("total_sugars_g", 1),
    "added-sugars": ("added_sugars_g", 1),
    "sodium": ("sodium_mg", 1000),
}


def _number(value) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_off_product(product: dict) -> Optional[LabelFacts]:
    """Build per-serving facts from an OFF product; None when neither basis has the required nutrients."""
    nutriments = product.get("nutriments") or {}
    serving = _number(product.get("serving_quantity"))
    per_serving: dict[str, float] = {}
    per_100g: dict[str, float] = {}
    for key, (field_name, multiplier) in OFF_NUTRIENTS.items():
        if (value := _number(nutriments.get(f"{key}_serving"))) is not None:
            per_serving[field_name] = round(value * multiplier, 2)
        if (value := _number(nutriments.get(f"{key}_100g"))) is not None:
            per_100g[field_name] = round(value * multiplier, 2)

    if all(k in per_serving for k in REQUIRED_NUTRIENTS):
        nutrition = per_serving
    elif serving and all(k in per_100g for k in REQUIRED_NUTRIENTS):
        nutrition = scale_per_100g(per_100g, serving)
    else:
        return None

    return LabelFacts(
        source="open_food_facts",
        nutrition=nutrition,
        serving_size_g=serving,
        ingredients_text=product.get("ingredients_text") or None,
        allergens=[tag.split(":", 1)[-1] for tag in product.get("allergens_tags") or []],
    )


def lookup_barcode(barcode: str, client: httpx.Client) -> Optional[LabelFacts]:
    """Look a barcode up on Open Food Facts; None when unknown or incomplete."""
    try:
        response = client.get(
            OFF_PRODUCT_URL.format(barcode=barcode),
            params={"fields": OFF_FIELDS},
            headers={"User-Agent": OFF_USER_AGENT},
        )
    except httpx.HTTPError:
        return None
    if response.status_code != 200:
        return None
    body = response.json()
    if body.get("status") != 1 or not body.get("product"):
        return None
    return parse_off_product(body["product"])
