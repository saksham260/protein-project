"""Price poller: refresh Amazon prices in Supabase, keep history, and recompute best-price metrics."""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional, Protocol
import httpx

try:
    from src.engine.metrics import calculate_cost_per_g_protein, calculate_protein_per_pack
    from src.pricing.amazon import AmazonOffer
except (ImportError, ModuleNotFoundError):
    from engine.metrics import calculate_cost_per_g_protein, calculate_protein_per_pack
    from pricing.amazon import AmazonOffer

ASIN_PATTERN = re.compile(r"/(?:dp|gp/product)/([A-Z0-9]{10})(?:[/?#]|$)")
MAX_PRICE_CHANGE = 0.5  # a >50% jump between polls is more likely a wrong listing than a real price


class OfferSource(Protocol):
    def get_offers(self, asins: list[str]) -> dict[str, AmazonOffer]: ...


@dataclass
class PollSummary:
    checked: int = 0
    updated: int = 0
    skipped: list[str] = field(default_factory=list)
    variants_recomputed: int = 0


def extract_asin(url: str) -> Optional[str]:
    """Pull the 10-character ASIN out of an amazon.in product URL (not search URLs)."""
    match = ASIN_PATTERN.search(url or "")
    return match.group(1) if match else None


def is_plausible_price(previous: Optional[float], new: Optional[float]) -> bool:
    """Reject non-positive prices and jumps larger than MAX_PRICE_CHANGE versus the last known price."""
    if new is None or new <= 0:
        return False
    if not previous or previous <= 0:
        return True
    return abs(new - previous) / previous <= MAX_PRICE_CHANGE


def best_price_metrics(variant: dict[str, Any], platform_prices: list[Optional[float]]) -> dict[str, Optional[float]]:
    """Lowest known platform price and its ₹/g protein for one variant row."""
    known = [float(p) for p in platform_prices if p is not None and float(p) > 0]
    best_price = min(known) if known else None
    protein_per_pack = calculate_protein_per_pack(
        float(variant["protein_g"]),
        float(variant["net_weight_g"]) if variant.get("net_weight_g") else None,
        float(variant["serving_size_g"]) if variant.get("serving_size_g") else None,
    )
    best_cost = (
        calculate_cost_per_g_protein(best_price, protein_per_pack)
        if best_price is not None and protein_per_pack
        else None
    )
    return {"best_price_inr": best_price, "best_cost_per_g_protein": best_cost}


def poll_amazon_prices(db: Any, amazon: OfferSource, dry_run: bool = False, force: bool = False) -> PollSummary:
    """Fetch current Amazon prices for every Amazon redirect link and write them back.

    Args:
        db: Supabase client (service role).
        amazon: Anything with get_offers(asins) -> {asin: AmazonOffer}.
        dry_run: Read and report only; no writes.
        force: Accept price changes larger than MAX_PRICE_CHANGE.
    """
    summary = PollSummary()
    links = (
        db.table("redirect_links")
        .select("id, variant_id, url, external_id, platform_price_inr")
        .eq("platform", "amazon")
        .execute()
        .data
    )

    link_asins: list[tuple[dict, str]] = []
    for link in links:
        asin = link.get("external_id") or extract_asin(link["url"])
        if asin:
            link_asins.append((link, asin))
        else:
            summary.skipped.append(f"{link['variant_id']}: no ASIN in {link['url']}")

    offers = amazon.get_offers([asin for _, asin in link_asins]) if link_asins else {}
    now_iso = datetime.now(timezone.utc).isoformat()
    touched_variants: set[str] = set()

    for link, asin in link_asins:
        summary.checked += 1
        offer = offers.get(asin)
        if offer is None:
            summary.skipped.append(f"{asin}: not returned by Amazon")
            continue

        previous = link.get("platform_price_inr")
        price = offer.price_inr
        if price is not None and not force and not is_plausible_price(previous, price):
            summary.skipped.append(f"{asin}: implausible change ₹{previous} → ₹{price} (use --force)")
            continue

        summary.updated += 1
        if dry_run:
            continue

        update = {"in_stock": offer.in_stock, "price_last_checked": now_iso, "external_id": asin}
        if price is not None:
            update["platform_price_inr"] = price
        db.table("redirect_links").update(update).eq("id", link["id"]).execute()
        db.table("price_history").insert(
            {
                "variant_id": link["variant_id"],
                "platform": "amazon",
                "price_inr": price,
                "in_stock": offer.in_stock,
                "recorded_at": now_iso,
            }
        ).execute()
        touched_variants.add(link["variant_id"])

    for variant_id in touched_variants:
        variant = (
            db.table("product_variants")
            .select("protein_g, net_weight_g, serving_size_g")
            .eq("id", variant_id)
            .single()
            .execute()
            .data
        )
        prices = [
            row["platform_price_inr"]
            for row in db.table("redirect_links").select("platform_price_inr").eq("variant_id", variant_id).execute().data
        ]
        db.table("product_variants").update(best_price_metrics(variant, prices)).eq("id", variant_id).execute()
        summary.variants_recomputed += 1

    return summary


def trigger_revalidate(url: str, secret: str) -> bool:
    """Ask the website to rebuild its cached pages. Returns True on success."""
    try:
        response = httpx.post(url, headers={"Authorization": f"Bearer {secret}"}, timeout=15.0)
    except httpx.HTTPError:
        return False
    return response.status_code == 200
