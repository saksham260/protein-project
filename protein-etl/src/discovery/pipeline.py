"""Discover products from brand Shopify stores and turn them into review drafts.

Nutrition layers, cheapest and most exact first; the first complete result wins:
  1. Open Food Facts by barcode
  2. Text in the Shopify description (tables / 'Protein: 25g' lines)
  3. The live product page (schema.org JSON-LD, tables, text)
  4. Label-photo readers, in the order given (free local OCR, then Gemini)
Anything still missing is left for a human in `review`.
"""

from __future__ import annotations
import json
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Protocol
import httpx

try:
    from src.discovery.facts import REQUIRED_NUTRIENTS, LabelFacts
    from src.discovery.html_facts import facts_from_html
    from src.discovery.open_food_facts import lookup_barcode
    from src.links import BROWSER_USER_AGENT, SEARCH_URL_TEMPLATES, build_search_url
    from src.models import slugify
    from src.parsers.manual import parse_raw_ingredient_deck
    from src.parsers.shopify import parse_shopify_product
except (ImportError, ModuleNotFoundError):
    from discovery.facts import REQUIRED_NUTRIENTS, LabelFacts
    from discovery.html_facts import facts_from_html
    from discovery.open_food_facts import lookup_barcode
    from links import BROWSER_USER_AGENT, SEARCH_URL_TEMPLATES, build_search_url
    from models import slugify
    from parsers.manual import parse_raw_ingredient_deck
    from parsers.shopify import parse_shopify_product

DRAFTS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "drafts"
PAGE_SIZE = 250
MAX_PAGES = 20
REQUEST_DELAY_S = 1.0  # be polite to brand stores
SINGLE_SERVE_CATEGORIES = {"protein-bars", "rtd-drinks"}

PROTEIN_WORDS = re.compile(r"protein|whey|casein|isolate", re.I)
BUNDLE_WORDS = re.compile(r"combo|bundle|\bpack of\b|\bx\s*\d+\b|\d+\s*x\b|gift|trial", re.I)
CATEGORY_RULES = [
    ("protein-powders", re.compile(r"powder|whey|isolate|shake mix|\bmix\b|\bjar\b|\btub\b|scoop", re.I)),
    ("protein-bars", re.compile(r"\bbars?\b", re.I)),
    ("savory-snacks", re.compile(r"chips|puffs|crisps|namkeen|makhana|cookies?|snack|nachos|wafers?", re.I)),
    ("rtd-drinks", re.compile(r"shake|smoothie|drink|milk|lassi|coffee|\brtd\b|bottle|\d+\s*ml\b", re.I)),
]


class LabelReader(Protocol):
    """Reads nutrition from product photos (OcrLabelReader, GeminiLabelReader)."""
    name: str

    def read(self, image_urls: list[str]) -> Optional[LabelFacts]: ...


@dataclass
class DiscoveryRow:
    """One line of the discover summary table."""
    title: str
    status: str  # ready / needs_input / skipped / exists
    detail: str


def infer_category(title: str, product_type: str, tags: list[str] | str) -> Optional[str]:
    """Map a Shopify product to one of our categories, or None when it isn't a protein product we list."""
    tag_text = " ".join(tags) if isinstance(tags, list) else str(tags or "")
    text = f"{title} {product_type} {tag_text}"
    if not PROTEIN_WORDS.search(text) or BUNDLE_WORDS.search(title):
        return None
    for category, pattern in CATEGORY_RULES:
        if pattern.search(text):
            return category
    return None


def fetch_store_catalog(store_url: str, client: httpx.Client) -> list[dict]:
    """Every product in a Shopify store via the public /products.json feed."""
    store_url = store_url.rstrip("/")
    products: list[dict] = []
    for page in range(1, MAX_PAGES + 1):
        response = client.get(f"{store_url}/products.json", params={"limit": PAGE_SIZE, "page": page})
        response.raise_for_status()
        batch = response.json().get("products", [])
        products.extend(batch)
        if len(batch) < PAGE_SIZE:
            break
        time.sleep(REQUEST_DELAY_S)
    return products


def find_label_facts(
    extract: dict,
    product_url: str,
    client: httpx.Client,
    readers: list[LabelReader],
) -> tuple[Optional[LabelFacts], list[str]]:
    """Run the layers in order. Returns (facts or None, names of layers tried)."""
    tried: list[str] = []

    for barcode in dict.fromkeys(v["barcode"] for v in extract["variants"] if v.get("barcode")):
        tried.append("open_food_facts")
        if (facts := lookup_barcode(barcode, client)) and facts.is_complete:
            return facts, tried

    tried.append("description")
    if (facts := facts_from_html(extract.get("body_html", ""))) is not None:
        return facts, tried

    tried.append("product_page")
    try:
        time.sleep(REQUEST_DELAY_S)
        page = client.get(product_url)
        if page.status_code == 200 and (facts := facts_from_html(page.text)) is not None:
            return facts, tried
    except httpx.HTTPError:
        pass

    best_partial: Optional[LabelFacts] = None
    for reader in readers if extract.get("images") else []:
        tried.append(reader.name)
        try:
            facts = reader.read(extract["images"])
        except (httpx.HTTPError, KeyError, ValueError) as e:
            tried[-1] = f"{reader.name} (failed: {type(e).__name__})"
            continue
        if facts and facts.is_complete:
            return facts, tried
        if facts and (best_partial is None or len(facts.nutrition) > len(best_partial.nutrition)):
            best_partial = facts

    # A partial read still saves typing; review shows which fields are missing.
    return best_partial, tried


def build_draft(
    extract: dict,
    brand_name: str,
    category: str,
    product_url: str,
    facts: Optional[LabelFacts],
    tried: list[str],
) -> dict:
    """Shape a draft whose `product` matches ProductCreate, plus review metadata."""
    warnings = list(facts.notes) if facts else ["No nutrition found automatically — enter it from the pack"]
    if facts and not facts.is_complete:
        missing = [k for k in REQUIRED_NUTRIENTS if k not in facts.nutrition]
        warnings.append(f"Partial label read — missing {', '.join(missing)}")
    ingredient_list = parse_raw_ingredient_deck(facts.ingredients_text) if facts and facts.ingredients_text else []
    if not ingredient_list:
        warnings.append("No ingredient list found — ingredient red flags and protein tier need it")

    variants = []
    for v in extract["variants"]:
        if not v.get("mrp_inr"):
            warnings.append(f"Variant '{v['variant_name']}' skipped: no price")
            continue
        name = extract["title"] if v["variant_name"] == "Default Title" else v["variant_name"]
        if v.get("weight_source") == "shipping":
            warnings.append(f"'{name}': weight is Shopify's shipping weight — check the net weight on the pack")
        serving = facts.serving_size_g if facts else None
        if serving is None and category in SINGLE_SERVE_CATEGORIES:
            serving = v.get("weight_g")

        links = [{"platform": "d2c", "url": product_url, "platform_price_inr": v.get("price_inr")}]
        query = f"{brand_name} {extract['title']}"
        links += [{"platform": p, "url": build_search_url(p, query)} for p in SEARCH_URL_TEMPLATES]

        variants.append(
            {
                "variant_name": name,
                "sku": v.get("sku") or None,
                "barcode_ean": v.get("barcode") or None,
                "mrp_inr": v["mrp_inr"],
                "net_weight_g": v.get("weight_g"),
                "serving_size_g": serving,
                "nutrition": dict(facts.nutrition) if facts else {},
                "ingredient_list": ingredient_list,
                "ingredient_deck_raw": [{"name": i} for i in ingredient_list],
                "allergens": facts.allergens if facts else [],
                "dietary_tags": [],
                "image_url": None,
                "redirect_links": links,
            }
        )
    if len(variants) > 1 and facts:
        warnings.append(f"Same nutrition applied to all {len(variants)} variants — check flavours differ")

    complete = bool(facts and facts.is_complete) and all(
        v["net_weight_g"] and v["serving_size_g"] for v in variants
    )
    return {
        "status": "ready" if complete and variants else "needs_input",
        "nutrition_source": facts.source if facts else None,
        "layers_tried": tried,
        "warnings": warnings,
        "source_url": product_url,
        "discovered_at": datetime.now(timezone.utc).isoformat(),
        "product": {
            "name": extract["title"],
            "brand_name": brand_name,
            "category_slug": category,
            "description": extract.get("description") or None,
            "image_url": (extract.get("images") or [None])[0],
            "variants": variants,
        },
    }


def draft_path(slug: str) -> Path:
    return DRAFTS_DIR / f"{slug}.json"


def already_seen(slug: str) -> bool:
    """True when this product was drafted, approved or rejected before."""
    return any((DRAFTS_DIR / sub / f"{slug}.json").exists() for sub in ("", "approved", "rejected"))


def discover_brand(
    brand_name: str,
    store_url: str,
    client: httpx.Client,
    readers: list[LabelReader],
    refresh: bool = False,
    limit: Optional[int] = None,
) -> list[DiscoveryRow]:
    """Crawl one store and write a draft per new protein product."""
    rows: list[DiscoveryRow] = []
    store_url = store_url.rstrip("/")
    new_count = 0
    for raw in fetch_store_catalog(store_url, client):
        if limit is not None and new_count >= limit:
            break
        title = raw.get("title", "")
        category = infer_category(title, raw.get("product_type", ""), raw.get("tags", []))
        if not category:
            rows.append(DiscoveryRow(title, "skipped", "not a single protein product"))
            continue

        slug = slugify(f"{brand_name}-{title}")
        if not refresh and already_seen(slug):
            rows.append(DiscoveryRow(title, "exists", "already drafted/reviewed"))
            continue

        product_url = f"{store_url}/products/{raw.get('handle')}"
        extract = parse_shopify_product(raw, product_url)
        facts, tried = find_label_facts(extract, product_url, client, readers)
        draft = build_draft(extract, brand_name, category, product_url, facts, tried)

        DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
        draft_path(slug).write_text(json.dumps(draft, indent=2, ensure_ascii=False), encoding="utf-8")
        new_count += 1
        rows.append(DiscoveryRow(title, draft["status"], f"{category} · nutrition: {draft['nutrition_source'] or 'none'}"))
    return rows


def http_client() -> httpx.Client:
    return httpx.Client(timeout=20.0, follow_redirects=True, headers={"User-Agent": BROWSER_USER_AGENT})
