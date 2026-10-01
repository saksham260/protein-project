"""Unit tests for the Amazon Creators API and price poller — Suites 8 & 9."""

import os
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
import httpx
import pytest
from src.pricing.amazon import (
    AmazonCreatorsClient,
    AmazonOffer,
    parse_get_items_response,
)
from src.pricing.poller import (
    best_price_metrics,
    extract_asin,
    is_plausible_price,
    poll_amazon_prices,
    trigger_revalidate,
)


# ==========================================
# Suite 8: Amazon Creators API
# ==========================================

def test_parse_get_items_response_reads_first_listing():
    payload = {
        "itemResults": {
            "items": [
                {
                    "asin": "B000000001",
                    "offersV2": {
                        "listings": [
                            {
                                "price": {"money": {"amount": 2899.0, "currency": "INR"}},
                                "availability": {"type": "IN_STOCK"},
                            }
                        ]
                    },
                },
                {"asin": "B000000002", "offersV2": {"listings": []}},
            ]
        }
    }
    offers = parse_get_items_response(payload)
    assert offers["B000000001"] == AmazonOffer("B000000001", 2899.0, True)
    assert offers["B000000002"] == AmazonOffer("B000000002", None, None)


def test_parse_get_items_response_out_of_stock():
    payload = {
        "itemResults": {
            "items": [
                {
                    "asin": "B000000003",
                    "offersV2": {
                        "listings": [
                            {
                                "price": {"money": {"amount": 1500.0, "currency": "INR"}},
                                "availability": {"type": "OUT_OF_STOCK"},
                            }
                        ]
                    },
                }
            ]
        }
    }
    offers = parse_get_items_response(payload)
    assert offers["B000000003"] == AmazonOffer("B000000003", 1500.0, False)


def test_parse_get_items_response_pascal_case():
    payload = {
        "ItemsResult": {
            "Items": [
                {
                    "Asin": "B000000004",
                    "OffersV2": {
                        "Listings": [
                            {
                                "Price": {"Money": {"Amount": 2000.0}},
                                "Availability": {"Type": "IN_STOCK"},
                            }
                        ]
                    },
                }
            ]
        }
    }
    offers = parse_get_items_response(payload)
    assert offers["B000000004"] == AmazonOffer("B000000004", 2000.0, True)


def test_parse_get_items_empty_or_missing_amount():
    assert parse_get_items_response({}) == {}
    payload = {
        "itemResults": {
            "items": [
                {
                    "asin": "B000000005",
                    "offersV2": {"listings": [{"price": {}}]},
                }
            ]
        }
    }
    offers = parse_get_items_response(payload)
    assert offers["B000000005"].price_inr is None


def test_amazon_client_from_env_all_and_missing():
    with patch.dict(os.environ, {}, clear=True):
        assert AmazonCreatorsClient.from_env() is None

    env = {
        "AMAZON_CREATORS_CLIENT_ID": "cid",
        "AMAZON_CREATORS_CLIENT_SECRET": "csec",
        "AMAZON_PARTNER_TAG": "tag",
    }
    with patch.dict(os.environ, env, clear=True):
        client = AmazonCreatorsClient.from_env()
        assert client is not None
        assert client.client_id == "cid"
        assert client.partner_tag == "tag"
        assert client.credential_version == "2.2"


def test_amazon_client_auth_header_versions():
    mock_http = MagicMock()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"access_token": "token123", "expires_in": 3600}
    mock_http.post.return_value = mock_resp

    # Version 2.2
    c2 = AmazonCreatorsClient("id", "sec", "2.2", "tag", http=mock_http)
    assert c2._auth_header() == "Bearer token123, Version 2.2"

    # Version 3.0
    c3 = AmazonCreatorsClient("id", "sec", "3.0", "tag", http=mock_http)
    c3._token = "token123"
    c3._token_expires_at = 9999999999.0
    assert c3._auth_header() == "Bearer token123"


# ==========================================
# Suite 9: Price Poller
# ==========================================

def test_extract_asin_from_product_urls():
    assert extract_asin("https://www.amazon.in/dp/B07XJ8C8F5") == "B07XJ8C8F5"
    assert extract_asin("https://www.amazon.in/MuscleBlaze-Whey/dp/B07XJ8C8F5/ref=sr_1_1?tag=x") == "B07XJ8C8F5"
    assert extract_asin("https://www.amazon.in/gp/product/B07XJ8C8F5?th=1") == "B07XJ8C8F5"
    assert extract_asin("https://www.amazon.in/s?k=whey+protein") is None
    assert extract_asin(None) is None
    assert extract_asin("") is None


def test_is_plausible_price():
    assert is_plausible_price(None, 2999)
    assert is_plausible_price(0, 500)
    assert is_plausible_price(1000, 1100)  # +10%
    assert is_plausible_price(1000, 1500)  # +50% (boundary)
    assert not is_plausible_price(1000, 1600)  # +60%
    assert not is_plausible_price(1000, 400)  # -60%
    assert not is_plausible_price(1000, 0)
    assert not is_plausible_price(1000, -50)
    assert not is_plausible_price(1000, None)


def test_best_price_metrics_scales_to_whole_pack():
    variant = {"protein_g": 25, "net_weight_g": 1000, "serving_size_g": 32}
    metrics = best_price_metrics(variant, [3499, 2899, None])
    assert metrics == {"best_price_inr": 2899.0, "best_cost_per_g_protein": 3.71}


def test_best_price_metrics_all_none_or_zeros():
    variant = {"protein_g": 20, "net_weight_g": 50, "serving_size_g": 50}
    assert best_price_metrics(variant, [None, 0, -10]) == {
        "best_price_inr": None,
        "best_cost_per_g_protein": None,
    }


def test_trigger_revalidate():
    with patch("httpx.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=200)
        assert trigger_revalidate("https://example.com/api/revalidate", "secret") is True

        mock_post.return_value = MagicMock(status_code=401)
        assert trigger_revalidate("https://example.com/api/revalidate", "wrong") is False

        mock_post.side_effect = httpx.ConnectError("fail")
        assert trigger_revalidate("https://example.com/api/revalidate", "secret") is False


class FakeQuery:
    def __init__(self, db, table):
        self.db, self.table, self.filters, self.op, self.payload = db, table, {}, "select", None

    def select(self, *_):
        return self

    def eq(self, column, value):
        self.filters[column] = value
        return self

    def single(self):
        self.op = "single"
        return self

    def update(self, payload):
        self.op, self.payload = "update", payload
        return self

    def insert(self, payload):
        self.op, self.payload = "insert", payload
        return self

    def execute(self):
        rows = [r for r in self.db.rows[self.table] if all(r.get(k) == v for k, v in self.filters.items())]
        if self.op == "update":
            for r in rows:
                r.update(self.payload)
        elif self.op == "insert":
            self.db.rows[self.table].append(dict(self.payload))
        return SimpleNamespace(data=rows[0] if self.op == "single" else rows)


class FakeDb:
    def __init__(self, rows):
        self.rows = rows

    def table(self, name):
        return FakeQuery(self, name)


class FakeAmazon:
    def __init__(self, offers):
        self.offers = offers

    def get_offers(self, asins):
        return {a: self.offers[a] for a in asins if a in self.offers}


def make_db():
    return FakeDb(
        {
            "redirect_links": [
                {"id": "l1", "variant_id": "v1", "platform": "amazon", "url": "https://www.amazon.in/dp/B000000001", "external_id": None, "platform_price_inr": 3499},
                {"id": "l2", "variant_id": "v1", "platform": "d2c", "url": "https://brand.in/x", "platform_price_inr": 3299},
                {"id": "l3", "variant_id": "v2", "platform": "amazon", "url": "https://www.amazon.in/dp/B000000002", "external_id": None, "platform_price_inr": 1000},
                {"id": "l4", "variant_id": "v3", "platform": "amazon", "url": "https://www.amazon.in/s?k=bar", "external_id": None, "platform_price_inr": None},
            ],
            "product_variants": [
                {"id": "v1", "protein_g": 25, "net_weight_g": 1000, "serving_size_g": 32},
                {"id": "v2", "protein_g": 20, "net_weight_g": 60, "serving_size_g": 60},
            ],
            "price_history": [],
        }
    )


def test_poll_updates_prices_history_and_best_metrics():
    db = make_db()
    amazon = FakeAmazon(
        {
            "B000000001": AmazonOffer("B000000001", 2899.0, True),
            "B000000002": AmazonOffer("B000000002", 300.0, True),  # -70%: rejected
        }
    )
    summary = poll_amazon_prices(db, amazon)

    links = {r["id"]: r for r in db.rows["redirect_links"]}
    assert links["l1"]["platform_price_inr"] == 2899.0
    assert links["l1"]["external_id"] == "B000000001"
    assert links["l3"]["platform_price_inr"] == 1000  # untouched
    assert len(db.rows["price_history"]) == 1
    assert db.rows["product_variants"][0]["best_price_inr"] == 2899.0
    assert (summary.checked, summary.updated, summary.variants_recomputed) == (2, 1, 1)
    assert len(summary.skipped) == 2  # search URL without ASIN + implausible jump


def test_poll_dry_run_writes_nothing():
    db = make_db()
    summary = poll_amazon_prices(db, FakeAmazon({"B000000001": AmazonOffer("B000000001", 2899.0, True)}), dry_run=True)
    assert summary.updated == 1
    assert db.rows["redirect_links"][0]["platform_price_inr"] == 3499
    assert db.rows["price_history"] == []


def test_poll_force_accepts_large_jump():
    db = make_db()
    poll_amazon_prices(db, FakeAmazon({"B000000002": AmazonOffer("B000000002", 300.0, True)}), force=True)
    assert db.rows["redirect_links"][2]["platform_price_inr"] == 300.0
