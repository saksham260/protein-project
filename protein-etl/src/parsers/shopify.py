"""Shopify /products.json product data extractor."""

from __future__ import annotations
import re
from typing import Optional
from urllib.parse import urlparse
import httpx
from bs4 import BeautifulSoup

# "1kg", "500 g", "1.5 Kg", "200ml", "2 lbs" -> grams (ml treated as g for drinks)
WEIGHT_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*(kgs?|lbs?|grams?|gms?|g|ml|l)\b", re.IGNORECASE)
UNIT_TO_GRAMS = {"kg": 1000.0, "kgs": 1000.0, "l": 1000.0, "lb": 453.6, "lbs": 453.6}


def parse_shopify_url(url: str) -> tuple[str, str]:
    """Extract domain base URL and product handle from a Shopify product link."""
    parsed = urlparse(url.strip())
    domain = f"{parsed.scheme}://{parsed.netloc}"

    # Path pattern: /products/<handle>
    match = re.search(r"/products/([^/?#]+)", parsed.path)
    if not match:
        raise ValueError(f"Could not extract Shopify product handle from URL: {url}")

    handle = match.group(1)
    return domain, handle


def clean_html_text(html_content: str) -> str:
    """Extract clean text content from Shopify HTML description."""
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    # Clean up whitespace
    text = soup.get_text(separator=" ", strip=True)
    return re.sub(r"\s+", " ", text)


def parse_weight_g(text: str | None) -> Optional[float]:
    """Read a pack weight like '1kg' or '52 g' out of a title, in grams."""
    match = WEIGHT_PATTERN.search(text or "")
    if not match:
        return None
    value = float(match.group(1))
    return round(value * UNIT_TO_GRAMS.get(match.group(2).lower(), 1.0), 2)


def _parse_price(raw) -> Optional[float]:
    try:
        return float(raw) if raw not in (None, "") else None
    except (ValueError, TypeError):
        return None


def extract_shopify_product_url(url: str, client: httpx.Client | None = None) -> dict:
    """Alias for extract_shopify_product to match spec."""
    return extract_shopify_product(url, client)


def extract_shopify_product(url: str, client: httpx.Client | None = None) -> dict:
    """Fetch and parse product metadata from a Shopify /products/{handle}.json endpoint.

    Args:
        url: Full Shopify product page URL.
        client: Optional httpx.Client instance for testing / reuse.

    Returns:
        Structured dict containing title, brand, description, images, and variants.
        Each variant has `mrp_inr` (compare-at price when the item is on sale),
        `price_inr` (current selling price), and `weight_g` with `weight_source`
        ("label" when read from the title, "shipping" when it fell back to Shopify's
        shipping weight and must be checked by hand).
    """
    domain, handle = parse_shopify_url(url)
    endpoint = f"{domain}/products/{handle}.json"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }

    should_close = False
    if client is None:
        client = httpx.Client(timeout=10.0)
        should_close = True

    try:
        response = client.get(endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()
    finally:
        if should_close:
            client.close()

    raw_product = data.get("product", {})
    if not raw_product:
        raise ValueError(f"No 'product' key in response from {endpoint}")
    return parse_shopify_product(raw_product, url)


def parse_shopify_product(raw_product: dict, url: str) -> dict:
    """Turn one raw Shopify product (from /products/{handle}.json or /products.json) into our extract dict."""
    handle = raw_product.get("handle") or url.rstrip("/").split("/")[-1].split("?")[0]

    body_html = raw_product.get("body_html") or ""
    plain_description = clean_html_text(body_html)

    # Images
    images = [img.get("src") for img in raw_product.get("images", []) if img.get("src")]

    # Parse variants
    raw_variants = raw_product.get("variants", [])
    parsed_variants = []
    for var in raw_variants:
        price = _parse_price(var.get("price")) or 0.0
        compare_at = _parse_price(var.get("compare_at_price"))
        mrp = compare_at if compare_at and compare_at > price else price

        # Shopify "grams" is the shipping weight (packaging included), so prefer the size in the title.
        label_weight = parse_weight_g(var.get("title"))
        if label_weight is None and len(raw_variants) == 1:
            label_weight = parse_weight_g(raw_product.get("title"))
        shipping_weight = float(var["grams"]) if var.get("grams") else None

        if label_weight is not None:
            weight_g, weight_source = label_weight, "label"
        elif shipping_weight is not None:
            weight_g, weight_source = shipping_weight, "shipping"
        else:
            weight_g, weight_source = None, None

        parsed_variants.append({
            "variant_name": var.get("title", "Default Variant"),
            "price_inr": price,
            "mrp_inr": mrp,
            "weight_g": weight_g,
            "weight_source": weight_source,
            "shipping_weight_g": shipping_weight,
            "sku": var.get("sku"),
            "barcode": var.get("barcode"),
        })

    return {
        "source": "shopify",
        "url": url,
        "title": raw_product.get("title", ""),
        "brand_name": raw_product.get("vendor", ""),
        "handle": handle,
        "description": plain_description,
        "tags": raw_product.get("tags", []),
        "product_type": raw_product.get("product_type", ""),
        "body_html": body_html,
        "images": images,
        "variants": parsed_variants,
    }
