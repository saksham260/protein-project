"""Unit tests for the brand-store (D2C) price poller."""

import httpx
from src.pricing.d2c import (
    StoreVariant,
    match_page_offer,
    match_variant,
    parse_products_json,
    poll_d2c_prices,
    product_handle_from_url,
)
from src.pricing.pages import DeadLink, PageOffer, parse_offers
from tests.test_pricing import FakeDb


def sv(handle="whey", sku="SKU-1", title="Chocolate", price=1000.0, in_stock=True, variant_id=""):
    return StoreVariant(handle, sku, title, price, in_stock, variant_id)


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
    variants = [sv(sku="", title="A", price=1000.0), sv(sku="", title="B", price=1200.0)]
    assert match_variant("https://brand.in/products/whey", None, "Something else", variants) is None


# ---- store variant IDs, pack sizes, same-price groups ----

def test_match_by_saved_store_variant_id_first():
    variants = [sv(sku="A", title="x", variant_id="111"), sv(sku="B", title="y", variant_id="222")]
    assert match_variant("https://brand.in/products/whey", "A", "x", variants, variant_id="222").sku == "B"


def test_saved_id_ignored_when_it_belongs_to_another_product():
    variants = [sv(handle="old", sku="", title="x", variant_id="111"), sv(handle="whey", sku="", title="Default")]
    found = match_variant("https://brand.in/products/whey", None, "Jar", variants, variant_id="111")
    assert found.product_handle == "whey"


def test_pack_sizes_match_across_spellings():
    variants = [sv(sku="", title="1 Kg", price=2199.0), sv(sku="", title="Assorted Pack (2 of each)", price=999.0)]
    assert match_variant("https://brand.in/products/whey", None, "Cold Coffee 1kg", variants).title == "1 Kg"
    variants = [sv(sku="", title="500gm", price=599.0), sv(sku="", title="1kg", price=999.0)]
    assert match_variant("https://brand.in/products/whey", None, "500g Pouch", variants).price_inr == 599.0


def test_sku_pointing_at_another_pack_size_is_not_trusted():
    # real case: catalog SKU for "Light Cocoa 1kg" was the store's 2 kg SKU
    variants = [sv(sku="F2", title="Pack of 2 KG", price=8219.0), sv(sku="F1", title="Pack of 1 KG", price=4119.0)]
    assert match_variant("https://brand.in/products/whey", "F2", "Light Cocoa 1kg", variants).price_inr == 4119.0
    offers = [PageOffer("F2", "Pack of 2 KG", 8219.0, True), PageOffer("F1", "Pack of 1 KG", 4119.0, True)]
    assert match_page_offer(offers, "F2", "Light Cocoa 1kg", "whey").price_inr == 4119.0


def test_saved_id_with_wrong_pack_size_is_not_trusted():
    variants = [sv(sku="", title="2kg", price=3000.0, variant_id="9"), sv(sku="", title="1kg", price=1700.0, variant_id="8")]
    assert match_variant("https://brand.in/products/whey", None, "Choc 1kg", variants, variant_id="9").price_inr == 1700.0


def test_flavour_and_size_in_store_title():
    variants = [sv(sku="", title="Cafe latte / 1kg", price=1999.0), sv(sku="", title="Mango Fusion / 1kg", price=2099.0)]
    assert match_variant("https://brand.in/products/whey", None, "Mango Fusion 1 Kg Pouch", variants).price_inr == 2099.0


def test_same_priced_flavours_give_a_certain_price_but_unknown_stock():
    variants = [
        sv(sku="", title="Cafe latte / 1kg", price=1999.0, in_stock=True, variant_id="1"),
        sv(sku="", title="Mango Fusion / 1kg", price=1999.0, in_stock=False, variant_id="2"),
        sv(sku="", title="Mango Fusion / 2kg", price=3599.0, variant_id="3"),
    ]
    found = match_variant("https://brand.in/products/whey", None, "1kg Pouch", variants)
    assert found.is_group and found.price_inr == 1999.0 and found.in_stock is None and found.variant_id == ""


def test_differently_priced_flavours_of_one_size_are_not_guessed():
    variants = [sv(sku="", title="Cafe latte / 1kg", price=1999.0), sv(sku="", title="Mango / 1kg", price=2099.0)]
    assert match_variant("https://brand.in/products/whey", None, "1kg Pouch", variants) is None


def test_poll_saves_store_variant_id_after_confident_match():
    db = make_db(price=1000.0)
    summary = poll_d2c_prices(db, FakeFeed({"brand.in": [sv(price=1000.0, variant_id="4455")]}))
    assert summary.ids_saved == 1
    assert db.rows["redirect_links"][0]["external_id"] == "4455"

    again = poll_d2c_prices(db, FakeFeed({"brand.in": [sv(price=1000.0, variant_id="4455")]}))
    assert again.ids_saved == 0


def test_poll_dry_run_counts_ids_but_saves_nothing():
    db = make_db(price=1000.0)
    summary = poll_d2c_prices(db, FakeFeed({"brand.in": [sv(price=1000.0, variant_id="4455")]}), dry_run=True)
    assert summary.ids_saved == 1 and "external_id" not in db.rows["redirect_links"][0]


def test_poll_prices_two_variants_sharing_a_same_price_group():
    db = make_db(price=1000.0, sku="")
    db.rows["redirect_links"][0]["product_variants"] = {"sku": "", "variant_name": "1kg Pouch"}
    db.rows["redirect_links"].append(
        {"id": "l2", "variant_id": "v2", "platform": "d2c", "url": "https://brand.in/products/whey",
         "platform_price_inr": 1000.0, "in_stock": True,
         "product_variants": {"sku": "", "variant_name": "1kg Pouch (Pack of 1)"}}
    )
    db.rows["product_variants"].append({"id": "v2", "protein_g": 25, "net_weight_g": 1000, "serving_size_g": 32})
    feed = FakeFeed({"brand.in": [sv(sku="", title="Choc / 1kg", price=1050.0, variant_id="1"),
                                  sv(sku="", title="Vanilla / 1kg", price=1050.0, variant_id="2")]})
    summary = poll_d2c_prices(db, feed)
    assert summary.changed == 2 and summary.ids_saved == 0
    assert [l["platform_price_inr"] for l in db.rows["redirect_links"]] == [1050.0, 1050.0]


# ---- stores without a Shopify feed: product-page price data ----

class FakePages:
    def __init__(self, pages):
        self.pages = pages

    def offers(self, url):
        result = self.pages[url]
        if isinstance(result, Exception):
            raise result
        return result


def test_parse_offers_reads_schema_org_json_ld():
    html = """<html><head><script type="application/ld+json">
    {"@context": "https://schema.org", "@type": "Product", "name": "Whey 1kg",
     "offers": [{"@type": "Offer", "sku": "W1", "price": "2,499.00", "priceCurrency": "INR",
                 "availability": "https://schema.org/InStock"},
                {"@type": "Offer", "sku": "W2", "price": "0", "priceCurrency": "INR"},
                {"@type": "Offer", "sku": "W3", "price": "30", "priceCurrency": "USD"}]}
    </script></head></html>"""
    assert parse_offers(html) == [PageOffer("W1", "Whey 1kg", 2499.0, True)]


def test_poll_falls_back_to_product_pages_when_store_has_no_feed():
    db = make_db(price=1000.0)
    pages = FakePages({"https://brand.in/products/whey": [PageOffer("SKU-1", "Whey", 1100.0, False)]})
    summary = poll_d2c_prices(db, FakeFeed({"brand.in": httpx.ConnectError("404")}), page_reader=pages)
    assert summary.failed_stores == [] and summary.changed == 1
    link = db.rows["redirect_links"][0]
    assert link["platform_price_inr"] == 1100.0 and link["in_stock"] is False


def test_poll_reports_dead_product_pages():
    db = make_db(price=1000.0)
    pages = FakePages({"https://brand.in/products/whey": DeadLink("HTTP 404")})
    summary = poll_d2c_prices(db, FakeFeed({"brand.in": httpx.ConnectError("404")}), page_reader=pages)
    assert len(summary.dead_links) == 1 and summary.failed_stores == []
    assert db.rows["redirect_links"][0]["platform_price_inr"] == 1000.0


def test_page_without_price_data_is_skipped_not_failed():
    db = make_db(price=1000.0)
    pages = FakePages({"https://brand.in/products/whey": []})
    summary = poll_d2c_prices(db, FakeFeed({"brand.in": httpx.ConnectError("404")}), page_reader=pages)
    assert "no price data" in summary.skipped[0] and summary.failed_stores == []


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
    summary = poll_d2c_prices(db, FakeFeed({"brand.in": [sv(sku="A", title="x", price=900.0), sv(sku="B", title="y")]}))
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
