"""Layers 2–3: nutrition written as text on the brand's page (schema.org JSON-LD, HTML tables, 'Protein: 25g' lines)."""

from __future__ import annotations
import json
import re
from typing import Any, Iterator, Optional
from bs4 import BeautifulSoup

try:
    from src.discovery.facts import LabelFacts, find_serving_size, parse_nutrient_value, scale_per_100g
except (ImportError, ModuleNotFoundError):
    from discovery.facts import LabelFacts, find_serving_size, parse_nutrient_value, scale_per_100g

# Checked in order: more specific labels first ("saturated fat" before "fat", "added sugar" before "sugar").
NUTRIENT_LABELS = [
    ("saturated_fat_g", re.compile(r"saturated|saturates", re.I)),
    ("trans_fat_g", re.compile(r"\btrans\b", re.I)),
    ("total_fat_g", re.compile(r"\bfats?\b", re.I)),
    ("added_sugars_g", re.compile(r"added\s+sugars?", re.I)),
    ("total_sugars_g", re.compile(r"\bsugars?\b", re.I)),
    ("dietary_fiber_g", re.compile(r"fib(?:re|er)", re.I)),
    ("total_carbs_g", re.compile(r"carbohydrates?|\bcarbs?\b", re.I)),
    ("protein_g", re.compile(r"\bproteins?\b", re.I)),
    ("cholesterol_mg", re.compile(r"cholesterol", re.I)),
    ("sodium_mg", re.compile(r"sodium", re.I)),
    ("calories_kcal", re.compile(r"energy|calories?|\bkcal\b", re.I)),
]
PER_SERVING = re.compile(r"serv|scoop|per\s*(?:bar|bottle|pack|sachet|piece)", re.I)
PER_100 = re.compile(r"100\s*(?:g|ml)", re.I)
GRAMS = re.compile(r"(\d+(?:\.\d+)?)\s*(?:g|ml)", re.I)
INGREDIENTS = re.compile(r"^\s*ingredients?\s*[:\-]\s*(.{10,})$", re.I | re.M)
# schema.org NutritionInformation property -> our field
JSON_LD_FIELDS = {
    "calories": "calories_kcal",
    "proteinContent": "protein_g",
    "fatContent": "total_fat_g",
    "saturatedFatContent": "saturated_fat_g",
    "transFatContent": "trans_fat_g",
    "cholesterolContent": "cholesterol_mg",
    "carbohydrateContent": "total_carbs_g",
    "fiberContent": "dietary_fiber_g",
    "sugarContent": "total_sugars_g",
    "sodiumContent": "sodium_mg",
}


def match_nutrient(label: str) -> Optional[str]:
    for field_name, pattern in NUTRIENT_LABELS:
        if pattern.search(label):
            return field_name
    return None


def _walk(node: Any) -> Iterator[dict]:
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from _walk(value)
    elif isinstance(node, list):
        for item in node:
            yield from _walk(item)


def parse_json_ld(soup: BeautifulSoup) -> Optional[LabelFacts]:
    """schema.org nutrition is per `servingSize` by definition."""
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
        except json.JSONDecodeError:
            continue
        for node in _walk(data):
            info = node.get("nutrition")
            if not isinstance(info, dict):
                continue
            nutrition = {}
            for key, field_name in JSON_LD_FIELDS.items():
                if info.get(key) is not None:
                    value = parse_nutrient_value(field_name, str(info[key]))
                    if value is not None:
                        nutrition[field_name] = value
            if nutrition:
                grams = GRAMS.search(str(info.get("servingSize") or ""))
                serving = float(grams.group(1)) if grams else None
                return LabelFacts(source="json_ld", nutrition=nutrition, serving_size_g=serving)
    return None


def _table_rows(table) -> list[list[str]]:
    return [
        [cell.get_text(" ", strip=True) for cell in tr.find_all(["td", "th"])]
        for tr in table.find_all("tr")
    ]


def _pick_column(rows: list[list[str]]) -> tuple[Optional[int], Optional[str]]:
    """Find the per-serving column (preferred) or the per-100g column from the header row."""
    for row in rows:
        serving_col = next((i for i, c in enumerate(row) if i > 0 and PER_SERVING.search(c)), None)
        per100_col = next((i for i, c in enumerate(row) if i > 0 and PER_100.search(c)), None)
        if serving_col is not None:
            return serving_col, "serving"
        if per100_col is not None:
            return per100_col, "per_100g"
    return None, None


def _finish(source: str, values: dict[str, float], basis: Optional[str], page_text: str) -> Optional[LabelFacts]:
    if not values:
        return None
    serving = find_serving_size(page_text)
    notes: list[str] = []
    if basis == "per_100g":
        if not serving:
            return None  # can't turn per-100g values into a serving without the serving size
        values = scale_per_100g(values, serving)
        notes.append(f"Scaled from per-100g column using {serving:g}g serving")
    elif basis is None:
        notes.append("Label column (per serving vs per 100g) not stated — check on the pack")
    return LabelFacts(source=source, nutrition=values, serving_size_g=serving, notes=notes)


def parse_tables(soup: BeautifulSoup, page_text: str) -> Optional[LabelFacts]:
    for table in soup.find_all("table"):
        rows = _table_rows(table)
        col, basis = _pick_column(rows)
        values: dict[str, float] = {}
        for row in rows:
            if len(row) < 2:
                continue
            field_name = match_nutrient(row[0])
            if not field_name or field_name in values:
                continue
            cell = row[col] if col is not None and col < len(row) else row[1]
            value = parse_nutrient_value(field_name, cell)
            if value is not None:
                values[field_name] = value
        facts = _finish("html_table", values, basis, page_text)
        if facts and facts.is_complete:
            return facts
    return None


def parse_text_lines(page_text: str) -> Optional[LabelFacts]:
    """'Protein: 25g' style lines. Only trusted when the text says the values are per serving."""
    if not PER_SERVING.search(page_text) or PER_100.search(page_text):
        return None
    values: dict[str, float] = {}
    for line in page_text.splitlines():
        match = re.match(r"\s*([A-Za-z ()]{3,40}?)\s*[:\-–]\s*(\d[\d.,]*\s*(?:kcal|kj|mg|g)\b.*)", line, re.I)
        if not match:
            continue
        field_name = match_nutrient(match.group(1))
        if field_name and field_name not in values:
            value = parse_nutrient_value(field_name, match.group(2))
            if value is not None:
                values[field_name] = value
    facts = _finish("html_text", values, "serving", page_text)
    return facts if facts and facts.is_complete else None


def find_ingredients(page_text: str) -> Optional[str]:
    match = INGREDIENTS.search(page_text)
    return match.group(1).strip() if match else None


def facts_from_html(html: str) -> Optional[LabelFacts]:
    """Try JSON-LD, then tables, then text lines. Returns the first complete result."""
    soup = BeautifulSoup(html or "", "html.parser")
    page_text = soup.get_text("\n", strip=True)
    for facts in (parse_json_ld(soup), parse_tables(soup, page_text), parse_text_lines(page_text)):
        if facts and facts.is_complete:
            facts.ingredients_text = facts.ingredients_text or find_ingredients(page_text)
            return facts
    return None
