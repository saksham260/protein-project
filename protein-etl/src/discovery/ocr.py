"""Layer 4a: read nutrition labels from product photos with free, local OCR (RapidOCR / PaddleOCR models).

Install with `pip install -e ".[ocr]"`. Runs on the CPU; the first run downloads the OCR models.
"""

from __future__ import annotations
import os
from typing import Any, Optional
import httpx

try:
    from src.discovery.facts import LabelFacts
    from src.discovery.images import download_image, pick_label_images
    from src.discovery.label_text import facts_from_label_rows, find_ingredients_in_rows, group_into_rows
except (ImportError, ModuleNotFoundError):
    from discovery.facts import LabelFacts
    from discovery.images import download_image, pick_label_images
    from discovery.label_text import facts_from_label_rows, find_ingredients_in_rows, group_into_rows

DEFAULT_MAX_IMAGES = 6


class OcrLabelReader:
    name = "ocr"

    def __init__(self, engine: Any, max_images: int = DEFAULT_MAX_IMAGES, http: Optional[httpx.Client] = None):
        self.engine = engine
        self.max_images = max_images
        self.http = http or httpx.Client(timeout=60.0, follow_redirects=True)

    @classmethod
    def from_env(cls) -> Optional[OcrLabelReader]:
        """None when RapidOCR is not installed."""
        try:
            from rapidocr import RapidOCR
        except ImportError:
            return None
        return cls(RapidOCR(), max_images=int(os.getenv("OCR_MAX_IMAGES", "").strip() or DEFAULT_MAX_IMAGES))

    def image_rows(self, content: bytes) -> list[list[str]]:
        result = self.engine(content)
        if result is None or not getattr(result, "txts", None):
            return []
        return group_into_rows(result.boxes, result.txts, result.scores)

    def read(self, image_urls: list[str]) -> Optional[LabelFacts]:
        """OCR photos from the back of the gallery forward; stop at the first complete nutrition panel."""
        ingredients: Optional[str] = None
        partial: Optional[LabelFacts] = None
        for url in reversed(pick_label_images(image_urls, self.max_images)):
            image = download_image(url, self.http)
            if not image:
                continue
            rows = self.image_rows(image[0])
            ingredients = ingredients or find_ingredients_in_rows(rows)
            facts = facts_from_label_rows(rows, source="ocr")
            if facts and facts.is_complete:
                facts.ingredients_text = facts.ingredients_text or ingredients
                return facts
            if facts and (partial is None or len(facts.nutrition) > len(partial.nutrition)):
                partial = facts
        if partial:
            partial.ingredients_text = partial.ingredients_text or ingredients
        return partial
