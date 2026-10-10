"""Find each picked product's nutrition-label and ingredient photos, and refresh the store snapshot.

For every line in data/demo_catalog/picks.txt this script:
  1. fetches https://<store>/products/<handle>.json (the brand's public Shopify product feed),
  2. updates data/demo_catalog/store_snapshot.json (prices, variants, first image),
  3. runs RapidOCR (free, local) over the product photos, newest first, and saves the photo that looks most like a
     nutrition table as labels/NNN_n.jpg and the best ingredient photo as labels/NNN_i.jpg,
  4. always saves labels/NNN_sheet.jpg, a numbered contact sheet of all photos, for when OCR picks the wrong one.

NNN is the product's line number in picks.txt (= "i" in readings.jsonl). The labels/ folder is git-ignored.

Usage (from protein-etl/):
  pip install -e ".[ocr]"
  python scripts/find_label_photos.py                    # all products
  python scripts/find_label_photos.py --only 5,12,40     # just these
  python scripts/find_label_photos.py --snapshot-only    # refresh prices only (fast, no OCR)
  python scripts/find_label_photos.py --photo 12 3       # save photo #3 of product 12 full-size (labels/012_x3.jpg)
"""

from __future__ import annotations
import argparse
import io
import json
import sys
import time
from pathlib import Path

import httpx
from PIL import Image, ImageDraw

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "demo_catalog"
LABELS_DIR = DATA_DIR / "labels"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"}
NUTRITION_WORDS = ["energy", "protein", "carbohydrate", "fat", "sodium", "sugar", "kcal", "serving", "100g", "100 g", "nutrition"]
MAX_PHOTOS = 20  # some stores have 100+ photos per product
OCR_SIZE = 850  # OCR a smaller copy; the saved photo stays full size


def load_picks() -> list[tuple[int, str, str, str, str]]:
    lines = [l for l in (DATA_DIR / "picks.txt").read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]
    return [(i, *l.split("|")) for i, l in enumerate(lines, 1)]


def fetch_product(client: httpx.Client, store: str, handle: str) -> dict | None:
    response = client.get(f"https://{store}/products/{handle}.json")
    if response.status_code != 200:
        return None
    return response.json()["product"]


def photo(client: httpx.Client, src: str, width: int = 1400) -> Image.Image:
    data = client.get(f"{src.split('?')[0]}?width={width}").content
    return Image.open(io.BytesIO(data)).convert("RGB")


def contact_sheet(client: httpx.Client, srcs: list[str], path: Path) -> None:
    tile, cols = 300, 4
    rows = max(1, (len(srcs) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * tile, rows * tile), "white")
    draw = ImageDraw.Draw(sheet)
    for k, src in enumerate(srcs):
        x, y = (k % cols) * tile, (k // cols) * tile
        try:
            im = photo(client, src, 400)
            im.thumbnail((tile - 6, tile - 6))
            sheet.paste(im, (x + 3, y + 3))
        except Exception:
            pass
        draw.rectangle([x, y, x + 34, y + 26], fill="red")
        draw.text((x + 6, y + 6), str(k), fill="white")
    sheet.save(path, quality=80)


def find_labels(client: httpx.Client, ocr, i: int, srcs: list[str]) -> dict:
    best_n: tuple[int, Image.Image | None] = (0, None)
    best_i: tuple[int, Image.Image | None] = (0, None)
    for src in list(reversed(srcs))[:MAX_PHOTOS]:
        try:
            im = photo(client, src)
            small = im.copy()
            small.thumbnail((OCR_SIZE, OCR_SIZE))
            buf = io.BytesIO()
            small.save(buf, "JPEG", quality=90)
            result = ocr(buf.getvalue())
            text = " ".join(result.txts or []).lower() if result and result.txts else ""
        except Exception:
            continue
        score = sum(1 for word in NUTRITION_WORDS if word in text)
        if score > best_n[0]:
            best_n = (score, im)
        if "ingredient" in text and len(text) > best_i[0]:
            best_i = (len(text), im)
        if best_n[0] >= 6 and best_i[1] is not None:
            break
    found = {"nutrition": None, "ingredients": None}
    if best_n[0] >= 3:
        best_n[1].save(LABELS_DIR / f"{i:03d}_n.jpg", quality=88)
        found["nutrition"] = f"{i:03d}_n.jpg"
    if best_i[1] is not None and best_i[1] is not best_n[1]:
        best_i[1].save(LABELS_DIR / f"{i:03d}_i.jpg", quality=88)
        found["ingredients"] = f"{i:03d}_i.jpg"
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", help="Comma-separated product numbers (picks.txt line numbers)")
    parser.add_argument("--snapshot-only", action="store_true", help="Refresh store_snapshot.json without OCR")
    parser.add_argument("--photo", nargs=2, type=int, metavar=("N", "K"), help="Save photo K of product N full size")
    args = parser.parse_args()

    LABELS_DIR.mkdir(parents=True, exist_ok=True)
    picks = load_picks()
    client = httpx.Client(headers=HEADERS, timeout=30, follow_redirects=True)

    if args.photo:
        n, k = args.photo
        _, store, handle, _, _ = picks[n - 1]
        product = fetch_product(client, store, handle)
        path = LABELS_DIR / f"{n:03d}_x{k}.jpg"
        photo(client, product["images"][k]["src"], 2000).save(path, quality=90)
        print(path)
        return 0

    only = {int(x) for x in args.only.split(",")} if args.only else None
    ocr = None
    if not args.snapshot_only:
        try:
            from rapidocr import RapidOCR
        except ImportError:
            print('OCR is not installed: pip install -e ".[ocr]"  (or use --snapshot-only)')
            return 1
        ocr = RapidOCR()

    snapshot_path = DATA_DIR / "store_snapshot.json"
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8")) if snapshot_path.exists() else {}
    for i, store, handle, category, brand in picks:
        if only and i not in only:
            continue
        start = time.time()
        product = fetch_product(client, store, handle)
        if product is None:
            print(f"[{i:03d}] {brand} | {handle} | NOT FOUND (removed from store?)", flush=True)
            continue
        entry = {
            "handle": product["handle"],
            "title": product["title"],
            "images": [{"src": im["src"]} for im in product.get("images", [])[:1]],
            "variants": [{k: v.get(k) for k in ("title", "price", "compare_at_price", "sku", "available")} for v in product["variants"]],
        }
        items = [x for x in snapshot.setdefault(store, []) if x["handle"] != handle]
        snapshot[store] = items + [entry]
        if args.snapshot_only:
            print(f"[{i:03d}] {brand} | {product['title'][:50]} | {entry['variants'][0]['price']}", flush=True)
            continue
        srcs = [im["src"] for im in product.get("images", [])]
        contact_sheet(client, srcs, LABELS_DIR / f"{i:03d}_sheet.jpg")
        found = find_labels(client, ocr, i, srcs)
        print(
            f"[{i:03d}] {brand} | {product['title'][:50]} | label={found['nutrition'] or 'NOT FOUND'} "
            f"ingredients={found['ingredients'] or '-'} | {time.time() - start:.0f}s",
            flush=True,
        )
        snapshot_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=1), encoding="utf-8")
    snapshot_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
