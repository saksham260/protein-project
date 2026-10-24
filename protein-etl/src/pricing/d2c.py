"""Brand-store (D2C) price poller: read each brand's public Shopify product feed and refresh prices in Supabase.

Only the brand's own public `/products.json` is read - one request per store, one second apart.
Variants are matched by SKU first, then by variant name within the same product page.
"""

from __future__ import annotations
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional, Protocol
from urllib.parse import urlparse
import httpx

try:
    from src.pricing.poller import is_plausible_price, recompute_best_prices, write_price
except (ImportError, ModuleNotFoundError):
    from pricing.poller import is_plausible_price, recompute_best_prices, write_price

REQUEST_INTERVAL_S = 1.0
PAGE_LIMIT = 250
MAX_PAGES = 6  # 1,500 products per store is far more than any brand here
MAX_FAILED_STORE_SHARE = 0.3  # the run is reported as failed when more stores than this are unreachable
USER_AGENT = "ProteinDiscoveryEngine/0.1 (price check; contact via site)"


@dataclass
class StoreVariant:
    """One variant as listed on the brand's own store."""
    product_handle: str
    sku: str
    title: str
    price_inr: float
    in_stock: bool


class StoreFeed(Protocol):
    def fetch(self, host: str) -> list[StoreVariant]: ...


@dataclass
class D2CSummary:
    stores: int = 0
    failed_stores: list[str] = field(default_factory=list)
    checked: int = 0
    changed: int = 0
    skipped: list[str] = field(default_factory=list)
    changes: list[str] = field(default_factory=list)
    variants_recomputed: int = 0

    @property
    def too_many_stores_failed(self) -> bool:
        return self.stores > 0 and len(self.failed_stores) / self.stores > MAX_FAILED_STORE_SHARE


def parse_products_json(payload: dict) -> list[StoreVariant]:
    """Flatten a Shopify products.json page into StoreVariant rows (skipping variants with no usable price)."""
    out: list[StoreVariant] = []
    for product in payload.get("products", []):
        for variant in product.get("variants", []):
            try:
                price = float(variant.get("price"))
            except (TypeError, ValueError):
                continue
            if price <= 0:
                continue
            out.append(
                StoreVariant(
                    product_handle=product.get("handle", ""),
                    sku=(variant.get("sku") or "").strip(),
                    title=(variant.get("title") or "").strip(),
                    price_inr=price,
                    in_stock=bool(variant.get("available", True)),
                )
            )
    return out


class HttpStoreFeed:
    """Reads https://<host>/products.json over HTTP, politely."""

    def __init__(self, client: Optional[httpx.Client] = None, interval_s: float = REQUEST_INTERVAL_S):
        self._client = client or httpx.Client(
            headers={"User-Agent": USER_AGENT}, timeout=30.0, follow_redirects=True
        )
        self._interval_s = interval_s

    def fetch(self, host: str) -> list[StoreVariant]:
        variants: list[StoreVariant] = []
        for page in range(1, MAX_PAGES + 1):
            time.sleep(self._interval_s)
            response = self._client.get(f"https://{host}/products.json", params={"limit": PAGE_LIMIT, "page": page})
            response.raise_for_status()
            payload = response.json()
            variants.extend(parse_products_json(payload))
            if len(payload.get("products", [])) < PAGE_LIMIT:
                break
        return variants


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def product_handle_from_url(url: str) -> str:
    match = re.search(r"/products/([^/?#]+)", url or "")
    return match.group(1) if match else ""


def match_variant(
    link_url: str, sku: Optional[str], variant_name: Optional[str], store_variants: list[StoreVariant]
) -> Optional[StoreVariant]:
    """Find the store's listing for one of our variants: SKU first, then name within the linked product page."""
    sku = (sku or "").strip()
    if sku:
        by_sku = [v for v in store_variants if v.sku == sku]
        if len(by_sku) == 1:
            return by_sku[0]

    handle = product_handle_from_url(link_url)
    on_page = [v for v in store_variants if v.product_handle == handle] if handle else []
    if len(on_page) == 1:
        return on_page[0]

    wanted = _normalize(variant_name or "")
    if wanted:
        exact = [v for v in on_page if _normalize(v.title) == wanted]
        if len(exact) == 1:
            return exact[0]
        # our names look like "Chocolate 1kg Jar" / "Pack of 8 x 50g" while the store says "Chocolate / 1kg"
        wanted_words = set(wanted.split())
        contained = [v for v in on_page if v.title and set(_normalize(v.title).split()) <= wanted_words]
        if len(contained) == 1:
            return contained[0]
    return None


def poll_d2c_prices(db: Any, feed: StoreFeed, dry_run: bool = False, force: bool = False) -> D2CSummary:
    """Refresh the price and stock of every D2C redirect link from the brand's own store.

    Args:
        db: Supabase client (service role).
        feed: Anything with fetch(host) -> list[StoreVariant].
        dry_run: Read and report only; no writes.
        force: Accept price changes larger than 50%.
    """
    summary = D2CSummary()
    links = (
        db.table("redirect_links")
        .select("id, variant_id, url, platform_price_inr, in_stock, product_variants(sku, variant_name)")
        .eq("platform", "d2c")
        .execute()
        .data
    )

    by_host: dict[str, list[dict]] = {}
    for link in links:
        host = urlparse(link["url"]).netloc
        if host:
            by_host.setdefault(host, []).append(link)
    summary.stores = len(by_host)

    now_iso = datetime.now(timezone.utc).isoformat()
    touched_variants: set[str] = set()

    for host, host_links in by_host.items():
        try:
            store_variants = feed.fetch(host)
        except (httpx.HTTPError, ValueError) as exc:
            summary.failed_stores.append(f"{host}: {exc}")
            continue

        matches: list[tuple[dict, dict, StoreVariant]] = []
        for link in host_links:
            summary.checked += 1
            ours = link.get("product_variants") or {}
            found = match_variant(link["url"], ours.get("sku"), ours.get("variant_name"), store_variants)
            if found is None:
                summary.skipped.append(f"{host}: no match for {ours.get('variant_name') or link['variant_id']} ({link['url']})")
            else:
                matches.append((link, ours, found))

        # If two of our variants point at the same store listing (e.g. a SKU copied between variants),
        # at least one of them would get the wrong price - skip all of them.
        claimed_by: dict[tuple, set] = {}
        for link, _, found in matches:
            claimed_by.setdefault((found.product_handle, found.sku, found.title), set()).add(link["variant_id"])

        for link, ours, found in matches:
            if len(claimed_by[(found.product_handle, found.sku, found.title)]) > 1:
                summary.skipped.append(f"{host}: {ours.get('variant_name')} shares a store listing with another variant ({link['url']})")
                continue

            previous = link.get("platform_price_inr")
            previous_f = float(previous) if previous is not None else None
            if not force and not is_plausible_price(previous_f, found.price_inr):
                summary.skipped.append(f"{host}: implausible change ₹{previous} → ₹{found.price_inr} for {link['url']} (use --force)")
                continue

            changed = previous_f is None or abs(previous_f - found.price_inr) > 0.005 or link.get("in_stock") != found.in_stock
            if changed:
                summary.changed += 1
                summary.changes.append(f"{host}: {ours.get('variant_name')} ₹{previous} → ₹{found.price_inr} ({'in stock' if found.in_stock else 'out of stock'})")
            if dry_run:
                continue

            # Always stamp "checked just now"; only add history rows when something actually changed.
            write_price(db, link, "d2c", found.price_inr, found.in_stock, now_iso, record_history=changed)
            if changed:
                touched_variants.add(link["variant_id"])

    if not dry_run:
        summary.variants_recomputed = recompute_best_prices(db, touched_variants)
    return summary
