"""Check every product image URL in the catalog really returns an image.

    python scripts/audit_image_urls.py            # report only
    python scripts/audit_image_urls.py --update   # also add failures to data/image_url_blocklist.json

URLs on refused hosts (stock photos, retailer hotlinks) are reported without being fetched.
The build (scripts/build_demo_catalog.py) drops any image the policy refuses.
"""

from __future__ import annotations
import argparse
import json
import sys
from datetime import date
from pathlib import Path
import httpx

ETL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ETL))
from src.image_policy import BLOCKLIST_FILE, image_problem  # noqa: E402

CATALOG = ETL.parent / "protein-web" / "src" / "data" / "seedCatalog.json"


def catalog_image_urls() -> dict[str, list[str]]:
    """url -> slugs using it (product and variant images)."""
    out: dict[str, list[str]] = {}
    for p in json.loads(CATALOG.read_text(encoding="utf-8")):
        for url in [p.get("image_url")] + [v.get("image_url") for v in p.get("variants", [])]:
            if url and url.startswith("http"):
                out.setdefault(url, []).append(p["slug"])
    return out


def fetch_problem(client: httpx.Client, url: str) -> str | None:
    try:
        r = client.get(url)
    except httpx.HTTPError as exc:
        return f"request failed: {exc.__class__.__name__}"
    if r.status_code != 200:
        return f"HTTP {r.status_code}"
    content_type = r.headers.get("content-type", "")
    if not content_type.startswith("image/"):
        return f"returns {content_type or 'no content type'}, not an image"
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Add failing URLs to the blocklist")
    args = parser.parse_args()

    urls = catalog_image_urls()
    failures: dict[str, str] = {}
    with httpx.Client(timeout=20, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}) as client:
        for url in sorted(urls):
            problem = image_problem(url) or fetch_problem(client, url)
            if problem:
                failures[url] = problem
                print(f"BAD  {problem:<45} {', '.join(sorted(set(urls[url])))}  {url}")

    print(f"\n{len(failures)} of {len(urls)} image URLs fail.")
    if args.update and failures:
        existing = json.loads(BLOCKLIST_FILE.read_text(encoding="utf-8")) if BLOCKLIST_FILE.exists() else []
        known = {e["url"] for e in existing}
        today = date.today().isoformat()
        for url, problem in failures.items():
            if url not in known and not image_problem(url):
                existing.append({"url": url, "reason": f"{problem} - checked {today}"})
        BLOCKLIST_FILE.write_text(json.dumps(existing, indent=2), encoding="utf-8")
        print(f"Blocklist now has {len(existing)} URLs. Rebuild the catalog to drop them.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
