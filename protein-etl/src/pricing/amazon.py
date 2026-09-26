"""Amazon Creators API client — the official replacement for PA-API 5 — used to read live amazon.in prices.

Access needs an Amazon Associates account with 10 qualifying sales in the last 30 days.
Endpoints are configurable via env because Amazon issues them per credential version/region;
confirm them against the Creators API docs shown when the credentials are created.
"""

from __future__ import annotations
import os
import time
from dataclasses import dataclass
from typing import Any, Iterable, Optional
import httpx

DEFAULT_TOKEN_URL = "https://creatorsapi.auth.eu-south-2.amazoncognito.com/oauth2/token"
DEFAULT_API_URL = "https://creatorsapi.amazon/catalog/v1/getItems"
DEFAULT_SCOPE = "creatorsapi/default"
MARKETPLACE = "www.amazon.in"
MAX_ITEMS_PER_REQUEST = 10
REQUEST_INTERVAL_S = 1.0  # stay under the 1 request/second starting quota
RESOURCES = ["offersV2.listings.price", "offersV2.listings.availability"]


@dataclass
class AmazonOffer:
    """Price and stock for one ASIN. price_inr is None when Amazon lists no buyable offer."""
    asin: str
    price_inr: Optional[float]
    in_stock: Optional[bool]


def _field(obj: Any, name: str) -> Any:
    """Read a lowerCamel key, falling back to its PascalCase spelling (PA-API style)."""
    if not isinstance(obj, dict):
        return None
    if name in obj:
        return obj[name]
    return obj.get(name[0].upper() + name[1:])


def parse_get_items_response(payload: dict) -> dict[str, AmazonOffer]:
    """Map a getItems response to {asin: AmazonOffer}, using the first (featured) listing."""
    result = _field(payload, "itemResults") or _field(payload, "itemsResult") or {}
    offers: dict[str, AmazonOffer] = {}
    for item in _field(result, "items") or []:
        asin = _field(item, "asin")
        if not asin:
            continue
        listings = _field(_field(item, "offersV2"), "listings") or []
        listing = listings[0] if listings else {}
        amount = _field(_field(_field(listing, "price"), "money"), "amount")
        availability = _field(_field(listing, "availability"), "type")
        offers[asin] = AmazonOffer(
            asin=asin,
            price_inr=float(amount) if amount is not None else None,
            in_stock=None if availability is None else availability == "IN_STOCK",
        )
    return offers


class AmazonCreatorsClient:
    """Minimal Creators API client: OAuth client-credentials token + batched getItems."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        credential_version: str,
        partner_tag: str,
        token_url: str = DEFAULT_TOKEN_URL,
        api_url: str = DEFAULT_API_URL,
        scope: str = DEFAULT_SCOPE,
        http: Optional[httpx.Client] = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.credential_version = credential_version
        self.partner_tag = partner_tag
        self.token_url = token_url
        self.api_url = api_url
        self.scope = scope
        self.http = http or httpx.Client(timeout=15.0)
        self._token: Optional[str] = None
        self._token_expires_at = 0.0

    @classmethod
    def from_env(cls) -> Optional[AmazonCreatorsClient]:
        """Build a client from AMAZON_* env vars, or None when credentials are not set yet."""
        client_id = os.getenv("AMAZON_CREATORS_CLIENT_ID", "").strip()
        client_secret = os.getenv("AMAZON_CREATORS_CLIENT_SECRET", "").strip()
        partner_tag = os.getenv("AMAZON_PARTNER_TAG", "").strip()
        if not client_id or not client_secret or not partner_tag:
            return None
        return cls(
            client_id=client_id,
            client_secret=client_secret,
            credential_version=(os.getenv("AMAZON_CREATORS_CREDENTIAL_VERSION", "").strip() or "2.2"),
            partner_tag=partner_tag,
            token_url=(os.getenv("AMAZON_CREATORS_TOKEN_URL", "").strip() or DEFAULT_TOKEN_URL),
            api_url=(os.getenv("AMAZON_CREATORS_API_URL", "").strip() or DEFAULT_API_URL),
            scope=(os.getenv("AMAZON_CREATORS_SCOPE", "").strip() or DEFAULT_SCOPE),
        )

    def _access_token(self) -> str:
        if self._token and time.time() < self._token_expires_at:
            return self._token
        response = self.http.post(
            self.token_url,
            data={"grant_type": "client_credentials", "scope": self.scope},
            auth=(self.client_id, self.client_secret),
        )
        response.raise_for_status()
        body = response.json()
        self._token = body["access_token"]
        # Refresh a minute early so a batch never runs on an expiring token.
        self._token_expires_at = time.time() + int(body.get("expires_in", 3600)) - 60
        return self._token

    def _auth_header(self) -> str:
        token = self._access_token()
        # v2.x credentials must name their version; v3.x (Login with Amazon) must not.
        if self.credential_version.startswith("2"):
            return f"Bearer {token}, Version {self.credential_version}"
        return f"Bearer {token}"

    def get_offers(self, asins: Iterable[str]) -> dict[str, AmazonOffer]:
        """Fetch offers for any number of ASINs, 10 per request."""
        unique = list(dict.fromkeys(asins))
        offers: dict[str, AmazonOffer] = {}
        for start in range(0, len(unique), MAX_ITEMS_PER_REQUEST):
            if start:
                time.sleep(REQUEST_INTERVAL_S)
            batch = unique[start : start + MAX_ITEMS_PER_REQUEST]
            response = self.http.post(
                self.api_url,
                json={
                    "itemIds": batch,
                    "itemIdType": "ASIN",
                    "marketplace": MARKETPLACE,
                    "partnerTag": self.partner_tag,
                    "resources": RESOURCES,
                },
                headers={"Authorization": self._auth_header(), "x-marketplace": MARKETPLACE},
            )
            response.raise_for_status()
            offers.update(parse_get_items_response(response.json()))
        return offers
