"""Which product image URLs the catalog may use.

A product image must be the brand's own pack shot (or our copy of it in Supabase Storage).
Stock photos and pictures hotlinked from retailers are refused, and so are URLs that were
found to return a web page instead of an image (kept in data/image_url_blocklist.json,
refreshed by scripts/audit_image_urls.py).
"""

from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

BLOCKLIST_FILE = Path(__file__).resolve().parents[1] / "data" / "image_url_blocklist.json"

# host suffix -> why it is refused
REFUSED_HOSTS = {
    "unsplash.com": "stock photo, not the product",
    "pexels.com": "stock photo, not the product",
    "hkrtcdn.com": "copied from HealthKart, not the brand",
    "flixcart.com": "copied from Flipkart, not the brand",
    "grofers.com": "copied from Blinkit, not the brand",
    "media-amazon.com": "copied from Amazon, not the brand",
    "nykaa.com": "copied from a retailer, not the brand",
}


@lru_cache(maxsize=1)
def _blocklist() -> dict[str, str]:
    if not BLOCKLIST_FILE.exists():
        return {}
    return {e["url"]: e["reason"] for e in json.loads(BLOCKLIST_FILE.read_text(encoding="utf-8"))}


def image_problem(url: Optional[str]) -> Optional[str]:
    """Why this image URL may not be used, or None if it is fine (an empty URL is fine: the site shows a placeholder)."""
    if not url:
        return None
    if url.startswith("/"):
        return None  # file served by the website itself
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        return "not an https URL"
    host = parsed.netloc.lower()
    for suffix, reason in REFUSED_HOSTS.items():
        if host == suffix or host.endswith("." + suffix):
            return reason
    return _blocklist().get(url)
