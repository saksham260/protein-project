"""Shopify /products.json product data extractor."""

from __future__ import annotations
import re
from urllib.parse import urlparse
import httpx
from bs4 import BeautifulSoup


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

    body_html = raw_product.get("body_html", "")
    plain_description = clean_html_text(body_html)

    # Images
    images = [img.get("src") for img in raw_product.get("images", []) if img.get("src")]

    # Parse variants
    parsed_variants = []
    for var in raw_product.get("variants", []):
        price_str = var.get("price", "0")
        try:
            mrp = float(price_str)
        except (ValueError, TypeError):
            mrp = 0.0

        grams = var.get("grams")
        weight_g = float(grams) if grams else 0.0

        parsed_variants.append({
            "variant_name": var.get("title", "Default Variant"),
            "price_inr": mrp,
            "weight_g": weight_g,
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
        "images": images,
        "variants": parsed_variants,
    }
