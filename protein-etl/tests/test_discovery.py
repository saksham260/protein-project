"""Unit tests for product discovery and layered nutrition extraction."""

import json
from bs4 import BeautifulSoup
from src.discovery.facts import LabelFacts, parse_nutrient_value
from src.discovery.gemini import parse_gemini_json
from src.discovery.html_facts import facts_from_html, match_nutrient, parse_json_ld
from src.discovery.open_food_facts import parse_off_product
from src.discovery.pipeline import build_draft, infer_category
from src.models import ProductCreate

FULL_NUTRITION = {"calories_kcal": 120.0, "protein_g": 24.0, "total_fat_g": 1.5, "total_carbs_g": 3.0}


def test_parse_nutrient_value_units():
    assert parse_nutrient_value("calories_kcal", "1650 kJ / 395 kcal") == 395.0
    assert parse_nutrient_value("calories_kcal", "418.4 kJ") == 100.0
    assert parse_nutrient_value("sodium_mg", "0.12 g") == 120.0
    assert parse_nutrient_value("sodium_mg", "95 mg") == 95.0
    assert parse_nutrient_value("protein_g", "24g") == 24.0
    assert parse_nutrient_value("protein_g", "-") is None


def test_match_nutrient_prefers_specific_labels():
    assert match_nutrient("Saturated Fat") == "saturated_fat_g"
    assert match_nutrient("Total Fat") == "total_fat_g"
    assert match_nutrient("of which Added Sugars") == "added_sugars_g"
    assert match_nutrient("Total Sugars") == "total_sugars_g"
    assert match_nutrient("Dietary Fibre") == "dietary_fiber_g"
    assert match_nutrient("Energy (kcal)") == "calories_kcal"


def test_table_uses_per_serving_column():
    html = """
    <table>
      <tr><th>Nutrient</th><th>Per 100g</th><th>Per Serving (30g)</th></tr>
      <tr><td>Energy</td><td>400 kcal</td><td>120 kcal</td></tr>
      <tr><td>Protein</td><td>80 g</td><td>24 g</td></tr>
      <tr><td>Total Fat</td><td>5 g</td><td>1.5 g</td></tr>
      <tr><td>Carbohydrate</td><td>10 g</td><td>3 g</td></tr>
      <tr><td>Sodium</td><td>300 mg</td><td>90 mg</td></tr>
    </table>
    <p>Ingredients: Whey Protein Isolate, Cocoa, Sucralose</p>
    """
    facts = facts_from_html(html)
    assert facts.source == "html_table"
    assert facts.nutrition == {**FULL_NUTRITION, "sodium_mg": 90.0}
    assert facts.serving_size_g == 30.0
    assert facts.ingredients_text == "Whey Protein Isolate, Cocoa, Sucralose"


def test_table_scales_per_100g_when_serving_size_known():
    html = """
    <p>Serving size: 30 g</p>
    <table>
      <tr><th>Nutrient</th><th>Per 100 g</th></tr>
      <tr><td>Energy</td><td>400 kcal</td></tr>
      <tr><td>Protein</td><td>80 g</td></tr>
      <tr><td>Fat</td><td>5 g</td></tr>
      <tr><td>Carbohydrates</td><td>10 g</td></tr>
    </table>
    """
    facts = facts_from_html(html)
    assert facts.nutrition == FULL_NUTRITION
    assert any("per-100g" in n for n in facts.notes)


def test_per_100g_table_without_serving_size_is_rejected():
    html = """
    <table>
      <tr><th>Nutrient</th><th>Per 100 g</th></tr>
      <tr><td>Energy</td><td>400 kcal</td></tr>
      <tr><td>Protein</td><td>80 g</td></tr>
      <tr><td>Fat</td><td>5 g</td></tr>
      <tr><td>Carbohydrates</td><td>10 g</td></tr>
    </table>
    """
    assert facts_from_html(html) is None


def test_json_ld_nutrition():
    html = """<script type="application/ld+json">
    {"@context": "https://schema.org", "@type": "Product", "name": "Bar",
     "nutrition": {"@type": "NutritionInformation", "servingSize": "1 bar (60 g)",
       "calories": "220 calories", "proteinContent": "20 g", "fatContent": "8 g", "carbohydrateContent": "18 g"}}
    </script>"""
    facts = parse_json_ld(BeautifulSoup(html, "html.parser"))
    assert facts.serving_size_g == 60.0
    assert facts.nutrition["calories_kcal"] == 220.0
    assert facts.is_complete


def test_description_text_without_numbers_finds_nothing():
    assert facts_from_html("<p>Enjoy 24g of gut loving protein in every scoop.</p>") is None


def test_open_food_facts_scales_per_100g():
    product = {
        "serving_quantity": "30",
        "nutriments": {"energy-kcal_100g": 400, "proteins_100g": 80, "fat_100g": 5, "carbohydrates_100g": 10, "sodium_100g": 0.3},
        "ingredients_text": "Whey protein",
        "allergens_tags": ["en:milk"],
    }
    facts = parse_off_product(product)
    assert facts.nutrition == {**FULL_NUTRITION, "sodium_mg": 90.0}
    assert facts.allergens == ["milk"]


def test_open_food_facts_incomplete_returns_none():
    assert parse_off_product({"nutriments": {"proteins_100g": 80}}) is None


def test_gemini_json_parsing():
    data = {"found": True, "basis": "per_serving", "serving_size_g": 30, **FULL_NUTRITION, "ingredients_text": "Whey", "allergens": ["Milk"]}
    facts = parse_gemini_json(data)
    assert facts.source == "gemini"
    assert facts.nutrition == FULL_NUTRITION
    assert facts.allergens == ["milk"]
    assert parse_gemini_json({"found": False}) is None


def test_infer_category():
    assert infer_category("Chocolate Fermented Yeast Protein - 500g Jar", "", []) == "protein-powders"
    assert infer_category("NAKPRO GEN-NXT Protein Shake Mix", "Fitness & Nutrition", []) == "protein-powders"
    assert infer_category("Double Cocoa Protein Bar", "", []) == "protein-bars"
    assert infer_category("Protein Chips Peri Peri", "", []) == "savory-snacks"
    assert infer_category("Cold Coffee Protein Shake 200ml", "", []) == "rtd-drinks"
    assert infer_category("OG Muesli - Dark Chocolate", "", []) is None
    assert infer_category("Protein Bar Combo Pack of 6", "", []) is None


def _extract(weight=500.0, weight_source="label"):
    return {
        "title": "Chocolate Whey Protein - 500g",
        "description": "Whey",
        "images": ["https://cdn.shopify.com/a.jpg"],
        "variants": [
            {"variant_name": "Default Title", "price_inr": 1499.0, "mrp_inr": 1799.0, "weight_g": weight,
             "weight_source": weight_source, "sku": "X1", "barcode": None},
        ],
    }


def test_build_draft_ready_validates_as_product():
    facts = LabelFacts("html_table", dict(FULL_NUTRITION), serving_size_g=30.0, ingredients_text="Whey Protein Isolate, Cocoa")
    draft = build_draft(_extract(), "SuperYou", "protein-powders", "https://superyou.in/products/x", facts, ["description"])
    assert draft["status"] == "ready"
    product = ProductCreate(**json.loads(json.dumps(draft["product"])))
    variant = product.variants[0]
    assert variant.variant_name == "Chocolate Whey Protein - 500g"
    assert variant.servings_per_pack == 17
    assert {link.platform for link in variant.redirect_links} == {"d2c", "amazon", "blinkit", "zepto", "instamart"}


def test_build_draft_without_facts_needs_input():
    draft = build_draft(_extract(weight_source="shipping"), "SuperYou", "protein-powders", "https://x/products/y", None, ["description", "product_page"])
    assert draft["status"] == "needs_input"
    assert any("shipping weight" in w for w in draft["warnings"])
    assert any("No nutrition" in w for w in draft["warnings"])


# --- OCR label parsing ---------------------------------------------------------------------------

from src.discovery.compare import ProductComparison, ReaderRun, summarize, values_agree
from src.discovery.label_text import facts_from_label_rows, find_ingredients_in_rows, group_into_rows


def _box(x, y, w=80, h=20):
    return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]


def test_group_into_rows_orders_cells():
    boxes = [_box(200, 101), _box(10, 100), _box(10, 140), _box(200, 139)]
    texts = ["24 g", "Protein", "Energy", "120 kcal"]
    assert group_into_rows(boxes, texts, [0.9] * 4) == [["Protein", "24 g"], ["Energy", "120 kcal"]]


def test_group_into_rows_drops_low_confidence():
    assert group_into_rows([_box(0, 0)], ["??"], [0.2]) == []


def test_label_rows_pick_per_serving_column_and_skip_rda():
    rows = [
        ["Nutritional Information", "Per 100g", "Per Serving (30g)", "%RDA"],
        ["Energy (kcal)", "400", "120", "6%"],
        ["Protein (g)", "80", "24", "48%"],
        ["Total Fat (g)", "5", "1.5"],
        ["Carbohydrate (g)", "10", "3"],
        ["Sodium (mg)", "300", "90"],
        ["Ingredients: Whey Protein Isolate, Cocoa,"],
        ["Sucralose."],
        ["Allergen info: Contains milk"],
    ]
    facts = facts_from_label_rows(rows)
    assert facts.nutrition == {**FULL_NUTRITION, "sodium_mg": 90.0}
    assert facts.serving_size_g == 30.0
    assert facts.ingredients_text == "Whey Protein Isolate, Cocoa, Sucralose."


def test_label_rows_energy_kj_and_kcal():
    rows = [["Per serving"], ["Energy", "502kJ / 120kcal"], ["Protein", "24g"], ["Fat", "1.5g"], ["Carbohydrates", "3g"]]
    assert facts_from_label_rows(rows).nutrition == FULL_NUTRITION


def test_label_rows_per_100g_only_needs_serving_size():
    rows = [["Per 100 g"], ["Energy", "400 kcal"], ["Protein", "80 g"], ["Fat", "5 g"], ["Carbohydrates", "10 g"]]
    assert facts_from_label_rows(rows) is None
    rows.insert(0, ["Serving size: 30 g"])
    assert facts_from_label_rows(rows).nutrition == FULL_NUTRITION


def test_find_ingredients_stops_at_next_section():
    rows = [["INGREDIENTS: Milk Solids, Whey"], ["Protein Concentrate"], ["Storage: cool dry place"]]
    assert find_ingredients_in_rows(rows) == "Milk Solids, Whey Protein Concentrate"


def test_values_agree():
    assert values_agree(24.0, 24.5)
    assert not values_agree(24.0, 2.4)
    assert not values_agree(24.0, None)
    assert values_agree(None, None) is None


def test_summarize_counts_and_agreement():
    good = LabelFacts("ocr", dict(FULL_NUTRITION))
    off = LabelFacts("gemini", {**FULL_NUTRITION, "protein_g": 2.4})
    comparison = ProductComparison("B", "P", "u", 3, {"ocr": ReaderRun(good, 2.0), "gemini": ReaderRun(off, 4.0)})
    summary = summarize([comparison], ["ocr", "gemini"])
    assert summary["ocr"]["complete"] == 1
    assert summary["gemini"]["est_cost_usd"] == 0.02
    assert summary["agreement"] == {"fields_compared": 4, "agree_pct": 75}
