"""Layer 4 (optional): read nutrition labels from product photos with Gemini.

Only runs when GEMINI_API_KEY is set and --no-ai is not passed. Results are cached per image set,
so a product is never paid for twice.
"""

from __future__ import annotations
import base64
import hashlib
import json
import os
from pathlib import Path
from typing import Optional
import httpx

try:
    from src.discovery.facts import NUTRIENT_UNITS, LabelFacts, scale_per_100g
    from src.discovery.images import download_image, pick_label_images
except (ImportError, ModuleNotFoundError):
    from discovery.facts import NUTRIENT_UNITS, LabelFacts, scale_per_100g
    from discovery.images import download_image, pick_label_images

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DEFAULT_MODEL = "gemini-3.5-flash"
DEFAULT_MAX_IMAGES = 6
CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "cache" / "gemini"

PROMPT = f"""These are product photos of one Indian packaged protein food. Find the nutrition information panel
and the ingredient list, and copy them exactly as printed.

Return JSON only, with this shape:
{{
  "found": true,
  "basis": "per_serving" or "per_100g",
  "serving_size_g": number or null,
  {", ".join(f'"{k}": number or null' for k in NUTRIENT_UNITS)},
  "ingredients_text": string or null,
  "allergens": [string]
}}

Rules:
- Prefer the per-serving column. Use "per_100g" only when no per-serving column is printed.
- Energy in kcal (if only kJ is printed, divide by 4.184). Sodium and cholesterol in mg; everything else in g.
- Use null for anything not printed. Never guess or estimate.
- If no nutrition panel is visible in any photo, return {{"found": false}}.
"""


def parse_gemini_json(data: dict) -> Optional[LabelFacts]:
    """Turn the model's JSON answer into per-serving facts."""
    if not data.get("found"):
        return None
    nutrition = {k: float(data[k]) for k in NUTRIENT_UNITS if isinstance(data.get(k), (int, float))}
    serving = data.get("serving_size_g") if isinstance(data.get("serving_size_g"), (int, float)) else None
    notes = ["Read from label photos by AI — check every number against the pack"]
    if data.get("basis") == "per_100g":
        if not serving:
            return None
        nutrition = scale_per_100g(nutrition, serving)
        notes.append(f"Scaled from per-100g column using {serving:g}g serving")
    return LabelFacts(
        source="gemini",
        nutrition=nutrition,
        serving_size_g=float(serving) if serving else None,
        ingredients_text=data.get("ingredients_text") or None,
        allergens=[a.lower() for a in data.get("allergens") or [] if isinstance(a, str)],
        notes=notes,
    )


class GeminiLabelReader:
    name = "gemini"

    def __init__(self, api_key: str, model: str = DEFAULT_MODEL, max_images: int = DEFAULT_MAX_IMAGES, http: Optional[httpx.Client] = None):
        self.api_key = api_key
        self.model = model
        self.max_images = max_images
        self.http = http or httpx.Client(timeout=60.0, follow_redirects=True)

    @classmethod
    def from_env(cls) -> Optional[GeminiLabelReader]:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            return None
        return cls(
            api_key=api_key,
            model=os.getenv("GEMINI_MODEL", "").strip() or DEFAULT_MODEL,
            max_images=int(os.getenv("GEMINI_MAX_IMAGES", "").strip() or DEFAULT_MAX_IMAGES),
        )

    def read(self, image_urls: list[str]) -> Optional[LabelFacts]:
        self.last_call_cached = False
        images = pick_label_images(image_urls, self.max_images)
        if not images:
            return None

        cache_key = hashlib.sha1("|".join([self.model, *images]).encode()).hexdigest()
        cache_file = CACHE_DIR / f"{cache_key}.json"
        if cache_file.exists():
            self.last_call_cached = True
            return parse_gemini_json(json.loads(cache_file.read_text(encoding="utf-8")))

        parts: list[dict] = [{"text": PROMPT}]
        for url in images:
            image = download_image(url, self.http)
            if image:
                content, mime = image
                parts.append({"inline_data": {"mime_type": mime, "data": base64.b64encode(content).decode()}})
        if len(parts) == 1:
            return None

        response = self.http.post(
            GEMINI_URL.format(model=self.model),
            headers={"x-goog-api-key": self.api_key},
            json={
                "contents": [{"parts": parts}],
                "generationConfig": {"responseMimeType": "application/json", "temperature": 0},
            },
        )
        response.raise_for_status()
        answer_parts = response.json()["candidates"][0]["content"]["parts"]
        data = json.loads("".join(p.get("text", "") for p in answer_parts if not p.get("thought")))

        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return parse_gemini_json(data)
