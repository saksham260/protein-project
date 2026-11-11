"""The catalog only uses brand pack shots: no stock photos, retailer hotlinks or web pages."""

import pytest
from src.image_policy import image_problem


@pytest.mark.parametrize(
    "url",
    [
        "https://images.unsplash.com/photo-1599490659213-e2b9527bd087?auto=format",
        "https://img4.hkrtcdn.com/32384/prd_3238333-Fuel-One-Whey-Protein_o.jpg",
        "https://rukminim2.flixcart.com/image/850/1000/x.jpeg",
        "https://cdn.grofers.com/cdn-cgi/image/x.png",
        "https://www.protinex.com/images/products/protinex_original_400g.png",  # returns a web page
        "http://cdn.shopify.com/s/files/1/x.jpg",
    ],
)
def test_refused(url):
    assert image_problem(url)


@pytest.mark.parametrize(
    "url",
    [
        None,
        "",
        "/images/products/whey-protein-tub.jpg",
        "https://cdn.shopify.com/s/files/1/0902/2590/1858/files/FOPcopy2.jpg?v=1",
        "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/x.webp",
    ],
)
def test_allowed(url):
    assert image_problem(url) is None
