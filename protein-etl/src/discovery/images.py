"""Product-image helpers shared by the label readers (OCR, Gemini)."""

from __future__ import annotations
from typing import Optional
import httpx

IMAGE_WIDTH_PX = 1200


def pick_label_images(image_urls: list[str], max_images: int) -> list[str]:
    """Back-of-pack shots (nutrition panel) are usually at the end of a gallery, so keep the last N."""
    return image_urls if len(image_urls) <= max_images else image_urls[-max_images:]


def sized_url(url: str) -> str:
    """Ask Shopify's image CDN for a 1200px copy (fewer tokens for Gemini, faster OCR)."""
    if "shopify" in url or "/cdn/shop/" in url:
        return str(httpx.URL(url).copy_merge_params({"width": IMAGE_WIDTH_PX}))
    return url


def download_image(url: str, http: httpx.Client) -> Optional[tuple[bytes, str]]:
    """Return (bytes, mime type), or None when the image can't be fetched."""
    try:
        response = http.get(sized_url(url))
    except httpx.HTTPError:
        return None
    if response.status_code != 200:
        return None
    return response.content, response.headers.get("content-type", "image/jpeg").split(";")[0]
