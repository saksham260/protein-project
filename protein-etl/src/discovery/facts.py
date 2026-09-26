"""Label facts found by any extraction layer, normalised to our per-serving units."""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Optional

# Field name -> unit it is stored in (matches NutritionPerPack).
NUTRIENT_UNITS = {
    "calories_kcal": "kcal",
    "protein_g": "g",
    "total_fat_g": "g",
    "saturated_fat_g": "g",
    "trans_fat_g": "g",
    "cholesterol_mg": "mg",
    "total_carbs_g": "g",
    "dietary_fiber_g": "g",
    "total_sugars_g": "g",
    "added_sugars_g": "g",
    "sodium_mg": "mg",
}
REQUIRED_NUTRIENTS = ("calories_kcal", "protein_g", "total_fat_g", "total_carbs_g")

KCAL_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*kcal", re.IGNORECASE)
QUANTITY_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*(kcal|kj|mcg|µg|mg|g)?\b", re.IGNORECASE)
SERVING_SIZE_PATTERNS = [
    re.compile(r"serving\s*size\s*[:\-]?\s*(?:\d+\s*\w+\s*)?\(?\s*(\d+(?:\.\d+)?)\s*(?:g|ml)\b", re.IGNORECASE),
    re.compile(r"per\s*(?:serving|scoop|bar|bottle|sachet)\s*\(\s*(\d+(?:\.\d+)?)\s*(?:g|ml)\s*\)", re.IGNORECASE),
    re.compile(r"1\s*scoop\s*\(\s*(\d+(?:\.\d+)?)\s*(?:g|ml)\s*\)", re.IGNORECASE),
]


@dataclass
class LabelFacts:
    """Nutrition per serving plus whatever else the layer could read."""
    source: str
    nutrition: dict[str, float]
    serving_size_g: Optional[float] = None
    ingredients_text: Optional[str] = None
    allergens: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        return all(self.nutrition.get(k) is not None for k in REQUIRED_NUTRIENTS)


def scale_per_100g(values: dict[str, float], serving_size_g: float) -> dict[str, float]:
    """Convert per-100g label values to one serving."""
    return {k: round(v * serving_size_g / 100.0, 2) for k, v in values.items()}


def parse_nutrient_value(field_name: str, text: str) -> Optional[float]:
    """Read a label cell like '25 g', '0.4g', '120 mg' or '1650 kJ / 395 kcal' in the field's unit."""
    target = NUTRIENT_UNITS[field_name]
    if target == "kcal":
        kcal = KCAL_PATTERN.search(text)
        if kcal:
            return round(float(kcal.group(1)), 2)
    match = QUANTITY_PATTERN.search(text.replace(",", ""))
    if not match:
        return None
    value = float(match.group(1))
    unit = (match.group(2) or "").lower()
    if target == "kcal":
        return round(value / 4.184, 2) if unit == "kj" else round(value, 2)
    if target == "mg":
        return round(value * 1000, 2) if unit == "g" else round(value / 1000, 2) if unit in ("mcg", "µg") else round(value, 2)
    return round(value / 1000, 3) if unit == "mg" else round(value, 2)


def find_serving_size(text: str) -> Optional[float]:
    for pattern in SERVING_SIZE_PATTERNS:
        match = pattern.search(text)
        if match:
            return float(match.group(1))
    return None
