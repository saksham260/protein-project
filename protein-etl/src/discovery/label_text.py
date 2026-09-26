"""Turn OCR text boxes from a label photo into rows, then into per-serving nutrition facts."""

from __future__ import annotations
import re
from statistics import median
from typing import Optional, Sequence

try:
    from src.discovery.facts import LabelFacts, find_serving_size, parse_nutrient_value, scale_per_100g
    from src.discovery.html_facts import match_nutrient
except (ImportError, ModuleNotFoundError):
    from discovery.facts import LabelFacts, find_serving_size, parse_nutrient_value, scale_per_100g
    from discovery.html_facts import match_nutrient

MIN_OCR_SCORE = 0.5
# Header words that name a value column, in the order they appear across the header row.
COLUMN_KINDS = re.compile(
    r"(per\s*serv\w*|serving|per\s*(?:scoop|bar|bottle|sachet|pack)|100\s*(?:g|ml)|%\s*rda|rda|%\s*dv|daily\s*value)",
    re.I,
)
SERVING_LINE = re.compile(r"serving\s*size|servings\s*per", re.I)
QUANTITY_TOKEN = re.compile(r"\d+(?:[.,]\d+)?\s*(?:kcal|kj|mcg|µg|mg|g|%)?", re.I)
INGREDIENTS_START = re.compile(r"^\s*ingredients?\s*[:\-.]?\s*(.*)$", re.I)
INGREDIENTS_STOP = re.compile(
    r"^\s*(allergen|contains|nutrition|storage|store\s|manufactured|marketed|mfd|best\s*before|net\s*(?:wt|weight|qty)|batch|directions|how\s*to)",
    re.I,
)
MAX_INGREDIENT_ROWS = 10


def group_into_rows(boxes: Sequence, texts: Sequence[str], scores: Sequence[float]) -> list[list[str]]:
    """Group OCR boxes (4 corner points each) into text rows, top to bottom, cells left to right."""
    items = []
    for box, text, score in zip(boxes, texts, scores):
        if score < MIN_OCR_SCORE or not text.strip():
            continue
        ys = [float(p[1]) for p in box]
        xs = [float(p[0]) for p in box]
        items.append(((min(ys) + max(ys)) / 2, max(ys) - min(ys), min(xs), text.strip()))
    if not items:
        return []

    tolerance = median(h for _, h, _, _ in items) * 0.6
    items.sort(key=lambda it: it[0])
    rows: list[list[tuple[float, str]]] = []
    row_y: Optional[float] = None
    for y, _, x, text in items:
        if row_y is None or y - row_y > tolerance:
            rows.append([])
            row_y = y
        rows[-1].append((x, text))
    return [[text for _, text in sorted(row)] for row in rows]


def _column_kind(token: str) -> str:
    token = token.lower()
    if "100" in token:
        return "per_100g"
    if "rda" in token or "dv" in token or "daily" in token:
        return "rda"
    return "serving"


def _split_label(row_text: str) -> tuple[str, str]:
    """'Protein (g) 80 24' -> ('Protein (g)', '80 24'). The label is everything before the first number."""
    match = re.search(r"\d", row_text)
    if not match:
        return row_text, ""
    return row_text[: match.start()].strip(), row_text[match.start() :]


def _row_values(field_name: str, label: str, rest: str) -> list[str]:
    tokens = [t.strip().replace(",", ".") for t in QUANTITY_TOKEN.findall(rest)]
    tokens = [t for t in tokens if not t.endswith("%")]  # %RDA columns
    if field_name == "calories_kcal":
        kcal = [t for t in tokens if t.lower().endswith("kcal")]
        if kcal:
            return kcal
        if "kj" in label.lower():
            return [t if t.lower().endswith("kj") else f"{t} kJ" for t in tokens]
    return tokens


def facts_from_label_rows(rows: list[list[str]], source: str = "ocr") -> Optional[LabelFacts]:
    """Read nutrient rows, choosing the per-serving column when the header names one."""
    columns: list[str] = []
    values: dict[str, float] = {}
    for row in rows:
        row_text = " ".join(row)
        label, rest = _split_label(row_text)
        field_name = match_nutrient(label) if label else None

        if field_name is None or not rest:
            if SERVING_LINE.search(row_text):
                continue  # "Serving size: 30g" is not a column header
            kinds = [_column_kind(k) for k in COLUMN_KINDS.findall(row_text)]
            if kinds and not values:
                columns = kinds  # header row (before any nutrient rows)
            continue
        if field_name in values:
            continue

        tokens = _row_values(field_name, label, rest)
        value_columns = [c for c in columns if c != "rda"]
        if "serving" in value_columns:
            index = value_columns.index("serving")
        elif "per_100g" in value_columns:
            index = value_columns.index("per_100g")
        else:
            index = 0
        if index < len(tokens):
            unit_hint = re.search(r"\((kcal|kj|mg|g)\)", label, re.I)
            token = tokens[index]
            if unit_hint and not re.search(r"[a-z]", token, re.I):
                token = f"{token} {unit_hint.group(1)}"
            value = parse_nutrient_value(field_name, token)
            if value is not None:
                values[field_name] = value

    if not values:
        return None

    full_text = "\n".join(" ".join(r) for r in rows)
    serving = find_serving_size(full_text)
    notes = ["Read from label photo by OCR — check every number against the pack"]
    value_columns = [c for c in columns if c != "rda"]
    if "serving" not in value_columns and "per_100g" in value_columns:
        if not serving:
            return None
        values = scale_per_100g(values, serving)
        notes.append(f"Scaled from per-100g column using {serving:g}g serving")
    elif not value_columns:
        notes.append("Label column (per serving vs per 100g) not detected — check on the pack")

    return LabelFacts(
        source=source,
        nutrition=values,
        serving_size_g=serving,
        ingredients_text=find_ingredients_in_rows(rows),
        notes=notes,
    )


def find_ingredients_in_rows(rows: list[list[str]]) -> Optional[str]:
    """Collect the ingredient paragraph: from the 'Ingredients:' row until the next section heading."""
    collected: list[str] = []
    for row in rows:
        row_text = " ".join(row)
        if not collected:
            match = INGREDIENTS_START.match(row_text)
            if match:
                collected.append(match.group(1))
            continue
        if INGREDIENTS_STOP.match(row_text) or len(collected) >= MAX_INGREDIENT_ROWS:
            break
        collected.append(row_text)
    text = " ".join(c for c in collected if c).strip()
    return text or None
