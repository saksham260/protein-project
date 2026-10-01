"""Unit tests for src/links.py — Suite 7."""

import pytest
from unittest.mock import MagicMock
import httpx
from src.links import build_search_url, check_url


# ==========================================
# 7.1 build_search_url
# ==========================================

def test_build_search_url_amazon():
    assert build_search_url("amazon", "Nakpro Gold Whey") == "https://www.amazon.in/s?k=Nakpro+Gold+Whey"


def test_build_search_url_blinkit():
    assert build_search_url("blinkit", "Yoga Bar") == "https://blinkit.com/s/?q=Yoga+Bar"


def test_build_search_url_zepto():
    assert build_search_url("zepto", "Whey Protein") == "https://www.zeptonow.com/search?query=Whey+Protein"


def test_build_search_url_instamart():
    assert build_search_url("instamart", "Protein Shake") == "https://www.swiggy.com/instamart/search?query=Protein+Shake"


def test_build_search_url_special_characters():
    url = build_search_url("amazon", "Whey 100% (Chocolate & Vanilla)")
    assert "100%25" in url or "%28" in url or "%26" in url


def test_build_search_url_unknown_platform():
    with pytest.raises(KeyError):
        build_search_url("unknown_platform", "Query")


# ==========================================
# 7.2 check_url
# ==========================================

def test_check_url_ok():
    client = MagicMock()
    resp = MagicMock(status_code=200)
    client.get.return_value = resp
    status, code = check_url("https://example.com/ok", client)
    assert status == "ok"
    assert code == 200


def test_check_url_broken_404():
    client = MagicMock()
    resp = MagicMock(status_code=404)
    client.get.return_value = resp
    status, code = check_url("https://example.com/missing", client)
    assert status == "broken"
    assert code == 404


def test_check_url_broken_410():
    client = MagicMock()
    resp = MagicMock(status_code=410)
    client.get.return_value = resp
    status, code = check_url("https://example.com/gone", client)
    assert status == "broken"
    assert code == 410


def test_check_url_blocked_403():
    client = MagicMock()
    resp = MagicMock(status_code=403)
    client.get.return_value = resp
    status, code = check_url("https://example.com/blocked", client)
    assert status == "blocked"
    assert code == 403


def test_check_url_unreachable():
    client = MagicMock()
    client.get.side_effect = httpx.ConnectError("Connection failed")
    status, code = check_url("https://example.com/error", client)
    assert status == "unreachable"
    assert code is None
