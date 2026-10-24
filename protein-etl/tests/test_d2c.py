"""Unit tests for the brand-store (D2C) price poller."""

import httpx
from src.pricing.d2c import (
    StoreVariant,
    match_variant,
    parse_products_json,
    poll_d2c_prices,
    product_handle_from_url,
)
from tests.test_pricing import FakeDb


def sv(handle="whey", sku="SKU-1", title="Chocolate", price=1000.0, in_stock=True):
    return StoreVariant(handle, sku, title, price, in_stock)


class FakeFeed:
    def __init__(self, stores):
        self.stores = stores

    def fetch(self, host):
        result = self.stores[host]
        if isinstance(result, Exception):
            raise result
        return result


def make_db(price=1000.0, sku="SKU-1"):
    return FakeDb(
        {
            "redirect_links": [
                {
                    "id": "l1",
                    "variant_id": "v1",
                    "platform": "d2c",
                    "url": "https://brand.in/products/whey",
                    "platform_price_inr": price,
                    "in_stock": True,
                    "product_variants": {"sku": sku, "variant_name": "Chocolate 1kg"},
                },
            ],
            "product_variants": [{"id": "v1", "protein_g": 25, "net_weight_g": 1000, "serving_size_g": 32}],
            "price_history": [],
        }
    )


# ---- parsing & matching ----

def test_parse_products_json_flattens_variants_and_skips_unpriced():
    payload = {
        "products": [
            {
                "handle": "whey",
                "variants": [
                    {"sku": " A ", "title": "Choc", "price": "1499.00", "available": True},
                    {"sku": "B", "title": "Vanilla", "price": "0.00", "available": True},
                    {"sku": "C", "title": "Mango", "price": None},
                    {"sku": "D", "title": "Out", "price": "999", "available": False},
                ],
            }
        ]
    }
    assert parse_products_json(payload) == [
        StoreVariant("whey", "A", "Choc", 1499.0, True),
        StoreVariant("whey", "D", "Out", 999.0, False),
    ]


def test_product_handle_from_url():
    assert product_handle_from_url("https://brand.in/products/whey-1?variant=1") == "whey-1"
    assert product_handle_from_url("https://brand.in/") == ""


def test_match_by_sku_first():
    variants = [sv(sku="A", title="x"), sv(sku="B", title="y")]
    assert match_variant("https://brand.in/products/whey", "B", "anything", variants).sku == "B"


def test_match_single_variant_product_without_sku():
    variants = [sv(handle="whey", sku="", title="Default Title"), sv(handle="other", sku="", title="Default Title")]
    assert match_variant("https://brand.in/products/whey", None, "Jar", variants).product_handle == "whey"


def test_match_by_name_within_product_page():
    variants = [sv(sku="", title="Pack of 8"), sv(sku="", title="Pack of 12"), sv(sku="", title="Pack of 18")]
    assert match_variant("https://brand.in/products/whey", None, "Pack of 12 x 50g", variants).title == "Pack of 12"


def test_match_returns_none_when_ambiguous():
    variants = [sv(sku="", title="A"), sv(sku="", title="B")]
    assert match_variant("https://brand.in/products/whey", None, "Something else", variants) is None


# ---- polling ----

def test_poll_updates_price_history_and_best_metrics():
    db = make_db(price=1000.0)
    summary = poll_d2c_prices(db, FakeFeed({"brand.in": [sv(price=1100.0)]}))
    assert (summary.checked, summary.changed, summary.variants_recomputed) == (1, 1, 1)
    link = db.rows["redirect_links"][0]
    assert link["platform_price_inr"] == 1100.0
    assert db.rows["price_history"][0]["platform"] == "d2c"
    assert db.rows["product_variants"][0]["best_price_inr"] == 1100.0


def test_poll_unchanged_price_only_refreshes_checked_time():
    db = make_db(price=1000.0)
    summary = poll_d2c_prices(db, FakeFeed({"brand.in": [sv(price=1000.0)]}))
    assert summary.changed == 0
    assert db.rows["price_history"] == []
    assert db.rows["redirect_links"][0]["price_last_checked"]


def test_poll_dry_run_writes_nothing():
    db = make_db(price=1000.0)
    summary = poll_d2c_prices(db, FakeFeed({"brand.in": [sv(price=1100.0)]}), dry_run=True)
    assert summary.changed == 1
    assert db.rows["redirect_links"][0]["platform_price_inr"] == 1000.0
    assert db.rows["price_history"] == []


def test_poll_rejects_implausible_jump_unless_forced():
    db = make_db(price=1000.0)
    summary = poll_d2c_prices(db, FakeFeed({"brand.in": [sv(price=3000.0)]}))
    assert summary.changed == 0 and len(summary.skipped) == 1
    assert db.rows["redirect_links"][0]["platform_price_inr"] == 1000.0

    forced = poll_d2c_prices(db, FakeFeed({"brand.in": [sv(price=3000.0)]}), force=True)
    assert forced.changed == 1
    assert db.rows["redirect_links"][0]["platform_price_inr"] == 3000.0


def test_poll_unmatched_variant_is_skipped_and_price_kept():
    db = make_db(price=1000.0, sku="MISSING")
    summary = poll_d2c_prices(db, FakeFeed({"brand.in": [sv(sku="A", title="x"), sv(sku="B", title="y")]}))
    assert summary.changed == 0 and "no match" in summary.skipped[0]
    assert db.rows["redirect_links"][0]["platform_price_inr"] == 1000.0


def test_poll_failed_store_is_reported_without_stopping_the_run():
    db = make_db()
    summary = poll_d2c_prices(db, FakeFeed({"brand.in": httpx.ConnectError("boom")}))
    assert summary.stores == 1 and len(summary.failed_stores) == 1
    assert summary.too_many_stores_failed
    assert db.rows["redirect_links"][0]["platform_price_inr"] == 1000.0


def test_poll_skips_variants_that_share_one_store_listing():
    db = make_db(price=1000.0)
    db.rows["redirect_links"].append(
        {
            "id": "l2",
            "variant_id": "v2",
            "platform": "d2c",
            "url": "https://brand.in/products/whey",
            "platform_price_inr": 1800.0,
            "in_stock": True,
            "product_variants": {"sku": "SKU-1", "variant_name": "Chocolate 1kg (30 Servings)"},
        }
    )
    summary = poll_d2c_prices(db, FakeFeed({"brand.in": [sv(sku="SKU-1", price=1100.0)]}))
    assert summary.changed == 0 and len(summary.skipped) == 2
    assert [l["platform_price_inr"] for l in db.rows["redirect_links"]] == [1000.0, 1800.0]
