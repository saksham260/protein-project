"""Check the demo catalogue's data quality and write a report to documentation/data-quality/<date>.md.

Automatic checks on every product (readings.jsonl + store_snapshot.json):
  - label maths: calories ≈ 4×protein + 4×carbs + 9×fat (+2.4×polyols); sub-values not bigger than their totals
  - physical limits: protein (and protein+carbs+fat) not more than the serving weight
  - pack claims: "26g protein" / "28% protein" in the store title matches the label reading
  - category sanity: protein density inside the normal range for its category
  - live prices (--live): today's store price vs the snapshot used in the catalogue
Plus a random spot-check list: open each product page, compare with the real label, tick ✅ / ❌.

Usage (from protein-etl/):
  python scripts/verify_demo_catalog.py              # offline checks + spot-check list of 10
  python scripts/verify_demo_catalog.py --live       # also re-fetch prices from the stores
  python scripts/verify_demo_catalog.py --sample 20  # bigger spot check
Exit code 1 when any ERROR is found.
"""

from __future__ import annotations
import argparse
import json
import random
import re
import sys
from datetime import date
from pathlib import Path

import httpx

ETL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ETL_DIR / "data" / "demo_catalog"
REPORT_DIR = ETL_DIR.parent / "documentation" / "data-quality"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"}
KEYS = ["kcal", "protein", "carbs", "fat", "sat_fat", "trans_fat", "cholesterol_mg", "fibre", "sugar", "added_sugar", "sodium_mg"]
# Protein as % of serving weight that is normal for each category (outside = WARN, check the label)
DENSITY_RANGE = {
    "protein-powders": (55, 100),
    "protein-bars": (12, 45),
    "savory-snacks": (5, 40),
    "rtd-drinks": (4, 15),  # per ml of drink
    "protein-spreads": (15, 40),
    "breakfast-cereals": (15, 45),
    "dairy": (4, 35),
    "cookies-baked": (10, 45),
}


def load() -> tuple[list, list, dict]:
    picks = [l.split("|") for l in (DATA_DIR / "picks.txt").read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]
    readings = [json.loads(l) for l in (DATA_DIR / "readings.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    snapshot = json.loads((DATA_DIR / "store_snapshot.json").read_text(encoding="utf-8"))
    return picks, readings, snapshot


def snapshot_product(snapshot: dict, store: str, handle: str) -> dict | None:
    return next((p for p in snapshot.get(store, []) if p["handle"] == handle), None)


def check(r: dict, pick: list, product: dict | None) -> list[tuple[str, str]]:
    """(level, message) pairs; level is ERROR or WARN."""
    store, handle, category, brand = pick
    n = dict(zip(KEYS, r["n"]))
    serv = r["serv"]
    issues: list[tuple[str, str]] = []

    def val(key: str) -> float:
        return n.get(key) or 0.0

    fiber = val("fibre")
    poly = r.get("poly") or 0
    est = 4 * val("protein") + 4 * val("carbs") + 9 * val("fat") - 1.6 * poly
    est_net = 4 * val("protein") + 4 * max(0.0, val("carbs") - fiber) + 9 * val("fat") - 1.6 * poly
    diff = min(abs(est - val("kcal")), abs(est_net - val("kcal")))
    if diff > max(25, 0.2 * val("kcal")):
        issues.append(("ERROR", f"calories {val('kcal'):g} but macros give ~{est:.0f} kcal"))
    if val("protein") > serv:
        issues.append(("ERROR", f"protein {val('protein'):g} g is more than the {serv:g} g serving"))
    if category not in ("rtd-drinks", "dairy") and val("protein") + val("carbs") + val("fat") > serv * 1.05:
        issues.append(("ERROR", "protein + carbs + fat is more than the serving weight"))
    for part, whole in (("sat_fat", "fat"), ("sugar", "carbs"), ("added_sugar", "sugar")):
        if n.get(part) is not None and n.get(whole) is not None and n[part] > n[whole] + 0.05:
            issues.append(("ERROR", f"{part} ({n[part]:g}) is bigger than {whole} ({n[whole]:g})"))
    if val("sodium_mg") > 1500:
        issues.append(("WARN", f"sodium {val('sodium_mg'):g} mg per serving is very high"))
    if r["net"] < serv:
        issues.append(("ERROR", f"pack ({r['net']:g}) is smaller than one serving ({serv:g})"))

    density = 100 * val("protein") / serv
    low, high = DENSITY_RANGE.get(category, (0, 100))
    if not low <= density <= high:
        issues.append(("WARN", f"protein density {density:.0f}% is unusual for {category} ({low}-{high}%)"))

    title = (product or {}).get("title", "")
    grams = re.search(r"(\d+(?:\.\d+)?)\s?g(?:m|ms)?\s+protein", title, re.I)
    if grams and " per pack" not in title.lower() and "grams protein" not in title.lower():
        claim = float(grams.group(1))
        per_100 = 100 * val("protein") / serv
        if abs(claim - val("protein")) > 0.15 * claim and abs(claim - per_100) > 0.15 * claim:
            issues.append(("WARN", f"title says {claim:g} g protein, label reading is {val('protein'):g} g per serving"))
    pct = re.search(r"(\d+(?:\.\d+)?)\s?%\s+protein", title, re.I)
    if pct:
        claim = float(pct.group(1))
        if abs(claim - density) > 4:
            issues.append(("WARN", f"title says {claim:g}% protein, label reading gives {density:.0f}%"))
    if not r.get("ing") and not r.get("protein_source"):
        issues.append(("WARN", "no ingredient list (red flags and protein tier can't be checked)"))
    if product is None:
        issues.append(("ERROR", "product missing from store_snapshot.json"))
    return issues


def live_price_issues(picks: list, readings: list, snapshot: dict) -> list[tuple[int, str]]:
    out = []
    with httpx.Client(headers=HEADERS, timeout=30, follow_redirects=True) as client:
        for r in readings:
            store, handle, _, brand = picks[r["i"] - 1]
            saved = snapshot_product(snapshot, store, handle)
            try:
                resp = client.get(f"https://{store}/products/{handle}.json")
            except httpx.HTTPError:
                out.append((r["i"], "store unreachable"))
                continue
            if resp.status_code != 200:
                out.append((r["i"], f"product page gone (HTTP {resp.status_code})"))
                continue
            live = resp.json()["product"]["variants"]
            v = r.get("v", 0)
            if not saved or v >= len(live) or v >= len(saved["variants"]):
                out.append((r["i"], "variant list changed — re-run find_label_photos.py --snapshot-only"))
                continue
            old, new = float(saved["variants"][v]["price"]), float(live[v]["price"])
            if abs(old - new) > 0.5:
                out.append((r["i"], f"price changed ₹{old:g} → ₹{new:g}"))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--live", action="store_true", help="Re-fetch prices from the brand stores")
    parser.add_argument("--sample", type=int, default=10, help="Products in the manual spot check (default 10)")
    args = parser.parse_args()

    picks, readings, snapshot = load()
    rows = []
    for r in readings:
        pick = picks[r["i"] - 1]
        rows.append((r, pick, check(r, pick, snapshot_product(snapshot, pick[0], pick[1]))))
    errors = sum(1 for *_, issues in rows for level, _ in issues if level == "ERROR")
    warns = sum(1 for *_, issues in rows for level, _ in issues if level == "WARN")
    prices = live_price_issues(picks, readings, snapshot) if args.live else None

    rng = random.Random(date.today().isoformat())
    sample = rng.sample(rows, min(args.sample, len(rows)))

    lines = [
        f"# Data Quality Report — {date.today().isoformat()}",
        "",
        f"Products: {len(rows)} · Errors: {errors} · Warnings: {warns}" + (f" · Price changes: {len(prices)}" if prices is not None else ""),
        "",
        "## Automatic checks",
        "",
        "| # | Brand | Product | Level | Issue |",
        "|---|---|---|---|---|",
    ]
    for r, pick, issues in rows:
        for level, msg in issues:
            lines.append(f"| {r['i']} | {pick[3]} | {r['name']} | {level} | {msg} |")
    if not errors and not warns:
        lines.append("| – | – | – | – | all checks passed |")
    if prices is not None:
        lines += ["", "## Live price check", "", "| # | Product | Change |", "|---|---|---|"]
        lines += [f"| {i} | {readings_by_i(readings)[i]['name']} | {msg} |" for i, msg in prices] or ["| – | – | no changes |"]
    lines += [
        "",
        "## Manual spot check",
        "",
        "Open each product page, find the nutrition-label photo, and compare. Tick **Correct?** ✅ or ❌.",
        "If more than 1 in 10 is wrong, re-read that brand's labels.",
        "",
        "| # | Product | Serving | kcal | Protein | Carbs | Fat | Sugar | Sodium | Correct? |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r, pick, _ in sample:
        n = dict(zip(KEYS, r["n"]))
        url = f"https://{pick[0]}/products/{pick[1]}"
        lines.append(
            f"| {r['i']} | [{pick[3]} {r['name']}]({url}) | {r['serv']:g} g | {n['kcal']:g} | {n['protein']:g} | "
            f"{n['carbs']:g} | {n['fat']:g} | {n['sugar'] if n['sugar'] is not None else '–'} | {n['sodium_mg'] if n['sodium_mg'] is not None else '–'} |  |"
        )
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = REPORT_DIR / f"{date.today().isoformat()}.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Products: {len(rows)} | errors: {errors} | warnings: {warns}" + (f" | price changes: {len(prices)}" if prices is not None else ""))
    for r, pick, issues in rows:
        for level, msg in issues:
            if level == "ERROR":
                print(f"  ERROR #{r['i']} {pick[3]} {r['name']}: {msg}")
    print(f"Report: {report}")
    return 1 if errors else 0


def readings_by_i(readings: list) -> dict:
    return {r["i"]: r for r in readings}


if __name__ == "__main__":
    sys.exit(main())
