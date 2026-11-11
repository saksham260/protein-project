"""Brand-store (D2C) price poller: read each brand's public Shopify product feed and refresh prices in Supabase.

Only the brand's own public `/products.json` is read - one request per store, one second apart.
Stores without that feed fall back to the schema.org price data on each product page (src/pricing/pages.py).

Variants are matched by the store's variant ID once known (saved in redirect_links.external_id after the
first confident match), then SKU, then variant name and pack size within the same product page.
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
    from src.pricing.pages import DeadLink, PageOffer, PageReader
    from src.pricing.poller import is_plausible_price, recompute_best_prices, write_price
except (ImportError, ModuleNotFoundError):
    from pricing.pages import DeadLink, PageOffer, PageReader
    from pricing.poller import is_plausible_price, recompute_best_prices, write_price

REQUEST_INTERVAL_S = 1.0
PAGE_LIMIT = 250
MAX_PAGES = 6  # 1,500 products per store is far more than any brand here
MAX_FAILED_STORE_SHARE = 0.3  # the run is reported as failed when more stores than this are unreachable
USER_AGENT = "ProteinDiscoveryEngine/0.1 (price check; contact via site)"


@dataclass
class StoreVariant:
    """One variant as listed on the brand's own store.

    is_group marks a match to several store variants that all cost the same (e.g. every flavour
    of a 1kg pouch): the price is certain, but not which flavour, so stock is unknown and no ID is saved.
    """
    product_handle: str
    sku: str
    title: str
    price_inr: float
    in_stock: Optional[bool]
    variant_id: str = ""
    is_group: bool = False


class StoreFeed(Protocol):
    def fetch(self, host: str) -> list[StoreVariant]: ...


@dataclass
class D2CSummary:
    stores: int = 0
    failed_stores: list[str] = field(default_factory=list)
    dead_links: list[str] = field(default_factory=list)
    ids_saved: int = 0
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
                    variant_id=str(variant.get("id") or ""),
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


_SIZE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(kgs?|kilograms?|grams?|gms?|gm|g|ml|ltrs?|litres?|liters?|l|lbs?)\b", re.IGNORECASE
)
_SIZE_FACTOR = {"kg": 1000, "kgs": 1000, "kilogram": 1000, "kilograms": 1000, "g": 1, "gm": 1, "gms": 1,
                "gram": 1, "grams": 1, "ml": 1, "l": 1000, "ltr": 1000, "ltrs": 1000, "litre": 1000,
                "litres": 1000, "liter": 1000, "liters": 1000, "lb": 453.6, "lbs": 453.6}


def _canon_size(match: re.Match) -> str:
    grams = float(match.group(1)) * _SIZE_FACTOR[match.group(2).lower()]
    return f" {round(grams)}g "


def _normalize(text: str) -> str:
    """Lowercase words, with pack sizes written one way ("1 Kg", "1kg", "1000gm" -> "1000g")."""
    text = _SIZE.sub(_canon_size, (text or "").lower())
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _sizes(text: str) -> set[str]:
    return {w for w in _normalize(text).split() if re.fullmatch(r"\d+g", w)}


def _size_conflict(variant_name: Optional[str], store_title: str) -> bool:
    """Both name a pack size and they differ: an SKU or ID match pointing there is a data error, not a match."""
    ours, theirs = _sizes(variant_name or ""), _sizes(store_title)
    return bool(ours and theirs and ours != theirs)


def product_handle_from_url(url: str) -> str:
    match = re.search(r"/products?/([^/?#]+)", url or "")
    return match.group(1) if match else ""


def _same_price_group(candidates: list[StoreVariant]) -> Optional[StoreVariant]:
    """Several candidates that all cost the same: the price is certain even if the exact variant isn't."""
    if len(candidates) < 2 or len({round(v.price_inr, 2) for v in candidates}) != 1:
        return None
    stock = {v.in_stock for v in candidates}
    return StoreVariant(
        product_handle=candidates[0].product_handle,
        sku="",
        title=" | ".join(sorted({v.title for v in candidates}))[:120],
        price_inr=candidates[0].price_inr,
        in_stock=stock.pop() if len(stock) == 1 else None,
        is_group=True,
    )


def match_variant(
    link_url: str,
    sku: Optional[str],
    variant_name: Optional[str],
    store_variants: list[StoreVariant],
    variant_id: Optional[str] = None,
) -> Optional[StoreVariant]:
    """Find the store's listing for one of our variants.

    Order: saved store variant ID -> SKU -> only variant on the linked page -> variant name ->
    pack size -> a group of same-priced variants. Returns None rather than guess.
    """
    handle = product_handle_from_url(link_url)

    if variant_id:
        by_id = [v for v in store_variants if v.variant_id == variant_id]
        # an ID saved for an older URL must not price a different product
        if (
            len(by_id) == 1
            and (not handle or by_id[0].product_handle == handle)
            and not _size_conflict(variant_name, by_id[0].title)
        ):
            return by_id[0]

    sku = (sku or "").strip()
    if sku:
        by_sku = [v for v in store_variants if v.sku == sku]
        # catalog SKUs have been copied onto the wrong pack size; trust the size in the name over them
        if len(by_sku) == 1 and not _size_conflict(variant_name, by_sku[0].title):
            return by_sku[0]

    on_page = [v for v in store_variants if v.product_handle == handle] if handle else []
    if len(on_page) == 1:
        return on_page[0]

    wanted = _normalize(variant_name or "")
    if wanted:
        exact = [v for v in on_page if _normalize(v.title) == wanted]
        if len(exact) == 1:
            return exact[0]
        # our names look like "Chocolate 1kg Jar" / "Pack of 8 x 50g" while the store says "Chocolate / 1 Kg"
        wanted_words = set(wanted.split())
        contained = [v for v in on_page if v.title and set(_normalize(v.title).split()) <= wanted_words]
        if len(contained) == 1:
            return contained[0]

        # same pack size: the linked page is already the right product (and usually the right flavour)
        wanted_sizes = _sizes(variant_name or "")
        if wanted_sizes:
            same_size = [v for v in on_page if _sizes(v.title) == wanted_sizes]
            if len(same_size) == 1:
                return same_size[0]
            if same_size:
                return _same_price_group(same_size)

    return _same_price_group(on_page)


def match_page_offer(
    offers: list[PageOffer], sku: Optional[str], variant_name: Optional[str], handle: str
) -> Optional[StoreVariant]:
    """Pick our variant's price from a product page's offers: SKU, a single price, then name and size."""
    if not offers:
        return None
    as_variants = [StoreVariant(handle, o.sku, o.name, o.price_inr, o.in_stock) for o in offers]
    sku = (sku or "").strip()
    if sku:
        by_sku = [v for v in as_variants if v.sku == sku]
        if len(by_sku) == 1 and not _size_conflict(variant_name, by_sku[0].title):
            return by_sku[0]
    if len(as_variants) == 1:
        return as_variants[0]
    wanted_sizes = _sizes(variant_name or "")
    if wanted_sizes:
        same_size = [v for v in as_variants if _sizes(v.title) == wanted_sizes]
        if len(same_size) == 1:
            return same_size[0]
        if same_size:
            return _same_price_group(same_size)
    return _same_price_group(as_variants)


def poll_d2c_prices(
    db: Any,
    feed: StoreFeed,
    dry_run: bool = False,
    force: bool = False,
    page_reader: Optional[PageReader] = None,
) -> D2CSummary:
    """Refresh the price and stock of every D2C redirect link from the brand's own store.

    Args:
        db: Supabase client (service role).
        feed: Anything with fetch(host) -> list[StoreVariant].
        page_reader: Reads schema.org prices from product pages for stores without a feed (None: such stores fail).
        dry_run: Read and report only; no writes.
        force: Accept price changes larger than 50%.
    """
    summary = D2CSummary()
    links = (
        db.table("redirect_links")
        .select("id, variant_id, url, external_id, platform_price_inr, in_stock, product_variants(sku, variant_name)")
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
        matches: list[tuple[dict, dict, StoreVariant]] = []
        try:
            store_variants = feed.fetch(host)
        except (httpx.HTTPError, ValueError) as exc:
            if page_reader is None:
                summary.failed_stores.append(f"{host}: {exc}")
                continue
            # No Shopify feed: read each product page's schema.org price data instead.
            if not _match_from_pages(host, host_links, page_reader, summary, matches):
                summary.failed_stores.append(f"{host}: no product feed, and no product page could be read ({exc})")
                continue
        else:
            for link in host_links:
                summary.checked += 1
                ours = link.get("product_variants") or {}
                found = match_variant(
                    link["url"], ours.get("sku"), ours.get("variant_name"), store_variants, link.get("external_id")
                )
                if found is None:
                    summary.skipped.append(f"{host}: no match for {ours.get('variant_name') or link['variant_id']} ({link['url']})")
                else:
                    matches.append((link, ours, found))

        # If two of our variants point at the same store listing (e.g. a SKU copied between variants),
        # at least one of them would get the wrong price - skip all of them. A same-price group is
        # exempt: every variant in it costs the same, so sharing it can't give a wrong price.
        claimed_by: dict[tuple, set] = {}
        for link, _, found in matches:
            if not found.is_group:
                claimed_by.setdefault((found.product_handle, found.sku, found.title), set()).add(link["variant_id"])

        for link, ours, found in matches:
            if not found.is_group and len(claimed_by[(found.product_handle, found.sku, found.title)]) > 1:
                summary.skipped.append(f"{host}: {ours.get('variant_name')} shares a store listing with another variant ({link['url']})")
                continue

            previous = link.get("platform_price_inr")
            previous_f = float(previous) if previous is not None else None
            if not force and not is_plausible_price(previous_f, found.price_inr):
                summary.skipped.append(f"{host}: implausible change ₹{previous} → ₹{found.price_inr} for {link['url']} (use --force)")
                continue

            changed = previous_f is None or abs(previous_f - found.price_inr) > 0.005 or link.get("in_stock") != found.in_stock
            stock_text = {True: "in stock", False: "out of stock", None: "stock unknown"}[found.in_stock]
            if changed:
                summary.changed += 1
                summary.changes.append(f"{host}: {ours.get('variant_name')} ₹{previous} → ₹{found.price_inr} ({stock_text})")

            # Remember the store's variant ID after a confident match, so later runs match on it directly.
            extra = {}
            if found.variant_id and not found.is_group and link.get("external_id") != found.variant_id:
                extra["external_id"] = found.variant_id
                summary.ids_saved += 1
            if dry_run:
                continue

            # Always stamp "checked just now"; only add history rows when something actually changed.
            write_price(db, link, "d2c", found.price_inr, found.in_stock, now_iso, extra=extra, record_history=changed)
            if changed:
                touched_variants.add(link["variant_id"])

    if not dry_run:
        summary.variants_recomputed = recompute_best_prices(db, touched_variants)
    return summary


def _match_from_pages(
    host: str,
    host_links: list[dict],
    page_reader: PageReader,
    summary: D2CSummary,
    matches: list[tuple[dict, dict, StoreVariant]],
) -> bool:
    """Price a store's links from their product pages. Returns False if no page could be read at all."""
    any_read = False
    for link in host_links:
        summary.checked += 1
        ours = link.get("product_variants") or {}
        label = ours.get("variant_name") or link["variant_id"]
        try:
            offers = page_reader.offers(link["url"])
        except DeadLink as exc:
            any_read = True  # the store answered; this one link is broken
            summary.dead_links.append(f"{host}: {label} ({link['url']}) {exc}")
            continue
        except (httpx.HTTPError, ValueError) as exc:
            summary.skipped.append(f"{host}: page not readable for {label} ({link['url']}): {exc.__class__.__name__}")
            continue
        any_read = True
        if not offers:
            summary.skipped.append(f"{host}: page has no price data for {label} ({link['url']})")
            continue
        found = match_page_offer(offers, ours.get("sku"), ours.get("variant_name"), product_handle_from_url(link["url"]))
        if found is None:
            summary.skipped.append(f"{host}: no match on page for {label} ({link['url']})")
        else:
            matches.append((link, ours, found))
    return any_read
