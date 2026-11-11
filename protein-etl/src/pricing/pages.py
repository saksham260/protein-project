"""Read prices from a brand's product page when the store has no Shopify feed.

Uses the schema.org Product/Offer JSON-LD that most stores embed for search engines
(the same data Google Shopping reads to check prices). One request per product page.
"""

from __future__ import annotations
import json
import time
from dataclasses import dataclass
from typing import Any, Optional, Protocol

import httpx
from bs4 import BeautifulSoup

REQUEST_INTERVAL_S = 1.0
USER_AGENT = "ProteinDiscoveryEngine/0.1 (price check; contact via site)"


class DeadLink(Exception):
    """The product page is gone (404/410): the link itself needs fixing."""


@dataclass
class PageOffer:
    sku: str
    name: str
    price_inr: float
    in_stock: Optional[bool]


class PageReader(Protocol):
    def offers(self, url: str) -> list[PageOffer]: ...


def _types(node: dict) -> list:
    t = node.get("@type")
    return t if isinstance(t, list) else [t]


def parse_offers(html: str) -> list[PageOffer]:
    """Every priced Offer in the page's JSON-LD, with the nearest Product name."""
    soup = BeautifulSoup(html, "html.parser")
    found: list[PageOffer] = []

    def walk(node: Any, name: str) -> None:
        if isinstance(node, list):
            for item in node:
                walk(item, name)
            return
        if not isinstance(node, dict):
            return
        types = _types(node)
        if "Product" in types or "ProductGroup" in types:
            name = str(node.get("name") or name)
        if "Offer" in types or "AggregateOffer" in types:
            raw = node.get("price", node.get("lowPrice"))
            try:
                price = float(str(raw).replace(",", ""))
            except (TypeError, ValueError):
                price = 0.0
            currency = str(node.get("priceCurrency") or "INR").upper()
            if price > 0 and currency == "INR":
                availability = str(node.get("availability") or "")
                found.append(
                    PageOffer(
                        sku=str(node.get("sku") or "").strip(),
                        name=str(node.get("name") or name),
                        price_inr=price,
                        in_stock=("InStock" in availability) if availability else None,
                    )
                )
        for key, value in node.items():
            if key != "@context":
                walk(value, name)

    for script in soup.find_all("script", type="application/ld+json"):
        try:
            walk(json.loads(script.string or ""), "")
        except (json.JSONDecodeError, TypeError):
            continue
    return found


class HttpPageReader:
    """Fetches product pages over HTTP, politely, and parses their JSON-LD offers."""

    def __init__(self, client: Optional[httpx.Client] = None, interval_s: float = REQUEST_INTERVAL_S):
        self._client = client or httpx.Client(
            headers={"User-Agent": USER_AGENT}, timeout=30.0, follow_redirects=True
        )
        self._interval_s = interval_s

    def offers(self, url: str) -> list[PageOffer]:
        time.sleep(self._interval_s)
        response = self._client.get(url)
        if response.status_code in (404, 410):
            raise DeadLink(f"HTTP {response.status_code}")
        response.raise_for_status()
        return parse_offers(response.text)
