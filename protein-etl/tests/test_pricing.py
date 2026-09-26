"""Unit tests for the Amazon price poller."""

from types import SimpleNamespace
from src.pricing.amazon import AmazonOffer, parse_get_items_response
from src.pricing.poller import best_price_metrics, extract_asin, is_plausible_price, poll_amazon_prices


def test_extract_asin_from_product_urls():
    assert extract_asin("https://www.amazon.in/dp/B07XJ8C8F5") == "B07XJ8C8F5"
    assert extract_asin("https://www.amazon.in/MuscleBlaze-Whey/dp/B07XJ8C8F5/ref=sr_1_1?tag=x") == "B07XJ8C8F5"
    assert extract_asin("https://www.amazon.in/gp/product/B07XJ8C8F5?th=1") == "B07XJ8C8F5"
    assert extract_asin("https://www.amazon.in/s?k=whey+protein") is None


def test_is_plausible_price():
    assert is_plausible_price(None, 2999)
    assert is_plausible_price(3000, 2600)
    assert not is_plausible_price(3000, 1200)  # -60%
    assert not is_plausible_price(3000, 0)
    assert not is_plausible_price(3000, None)


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


def test_best_price_metrics_scales_to_whole_pack():
    # 25g protein per 32g scoop, 1kg tub = 781.25g protein; ₹2899 / 781.25 = ₹3.71/g
    variant = {"protein_g": 25, "net_weight_g": 1000, "serving_size_g": 32}
    metrics = best_price_metrics(variant, [3499, 2899, None])
    assert metrics == {"best_price_inr": 2899.0, "best_cost_per_g_protein": 3.71}


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
