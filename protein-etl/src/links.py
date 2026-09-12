"""Outbound link helpers: platform search URLs and link-health checks."""

from __future__ import annotations
from urllib.parse import quote_plus
import httpx

BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Search pages always resolve, and quick-commerce apps pick the user's location themselves.
SEARCH_URL_TEMPLATES = {
    "amazon": "https://www.amazon.in/s?k={query}",
    "blinkit": "https://blinkit.com/s/?q={query}",
    "zepto": "https://www.zeptonow.com/search?query={query}",
    "instamart": "https://www.swiggy.com/instamart/search?query={query}",
}


def build_search_url(platform: str, query: str) -> str:
    """Build a platform search URL for a product query."""
    return SEARCH_URL_TEMPLATES[platform].format(query=quote_plus(query))


def check_url(url: str, client: httpx.Client) -> tuple[str, int | None]:
    """Fetch a URL and classify it as ok / broken / blocked / unreachable."""
    try:
        response = client.get(url, follow_redirects=True)
    except httpx.HTTPError:
        return "unreachable", None
    if response.status_code in (404, 410):
        return "broken", response.status_code
    if response.status_code >= 400:
        # 403/429/503 are usually bot protection rather than a dead page.
        return "blocked", response.status_code
    return "ok", response.status_code
