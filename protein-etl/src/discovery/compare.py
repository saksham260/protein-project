"""Run several label readers (OCR, Gemini) on the same products and report how they compare.

The report has an empty "Correct on pack?" column so a person can score each reader against the real label.
"""

from __future__ import annotations
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
import httpx

try:
    from src.discovery.facts import NUTRIENT_UNITS, REQUIRED_NUTRIENTS, LabelFacts
    from src.discovery.pipeline import LabelReader, fetch_store_catalog, infer_category
    from src.parsers.shopify import parse_shopify_product
except (ImportError, ModuleNotFoundError):
    from discovery.facts import NUTRIENT_UNITS, REQUIRED_NUTRIENTS, LabelFacts
    from discovery.pipeline import LabelReader, fetch_store_catalog, infer_category
    from parsers.shopify import parse_shopify_product

REPO_ROOT = Path(__file__).resolve().parents[3]
REPORTS_DIR = REPO_ROOT / "documentation" / "reader-comparisons"
COMPARE_FIELDS = ["serving_size_g", *NUTRIENT_UNITS]
AGREE_TOLERANCE = 0.05  # values within 5% (or 0.5 units) count as agreeing
GEMINI_COST_PER_CALL_USD = 0.02


@dataclass
class ReaderRun:
    facts: Optional[LabelFacts]
    seconds: float
    error: Optional[str] = None
    cached: bool = False


@dataclass
class ProductComparison:
    brand: str
    title: str
    url: str
    image_count: int
    runs: dict[str, ReaderRun] = field(default_factory=dict)


def field_value(facts: Optional[LabelFacts], name: str) -> Optional[float]:
    if facts is None:
        return None
    return facts.serving_size_g if name == "serving_size_g" else facts.nutrition.get(name)


def values_agree(a: Optional[float], b: Optional[float]) -> Optional[bool]:
    """None when neither reader found the value."""
    if a is None and b is None:
        return None
    if a is None or b is None:
        return False
    return abs(a - b) <= max(0.5, AGREE_TOLERANCE * max(abs(a), abs(b)))


def collect_products(brands: list[dict], client: httpx.Client, limit: int) -> list[tuple[str, dict]]:
    """The first `limit` protein products with photos from each brand."""
    picked: list[tuple[str, dict]] = []
    for brand in brands:
        store_url = brand["store_url"].rstrip("/")
        count = 0
        for raw in fetch_store_catalog(store_url, client):
            if count >= limit:
                break
            if not raw.get("images") or not infer_category(raw.get("title", ""), raw.get("product_type", ""), raw.get("tags", [])):
                continue
            picked.append((brand["brand_name"], parse_shopify_product(raw, f"{store_url}/products/{raw.get('handle')}")))
            count += 1
    return picked


def compare_product(brand: str, extract: dict, readers: list[LabelReader]) -> ProductComparison:
    comparison = ProductComparison(brand, extract["title"], extract["url"], len(extract.get("images", [])))
    for reader in readers:
        start = time.perf_counter()
        try:
            facts = reader.read(extract["images"])
            error = None
        except Exception as e:  # a reader failing must not stop the comparison
            facts, error = None, f"{type(e).__name__}: {e}"[:200]
        comparison.runs[reader.name] = ReaderRun(
            facts=facts,
            seconds=round(time.perf_counter() - start, 1),
            error=error,
            cached=bool(getattr(reader, "last_call_cached", False)),
        )
    return comparison


def summarize(comparisons: list[ProductComparison], reader_names: list[str]) -> dict[str, dict]:
    summary: dict[str, dict] = {}
    for name in reader_names:
        runs = [c.runs[name] for c in comparisons if name in c.runs]
        paid_calls = sum(1 for r in runs if not r.cached and r.error is None) if name == "gemini" else 0
        summary[name] = {
            "products": len(runs),
            "complete": sum(1 for r in runs if r.facts and r.facts.is_complete),
            "partial": sum(1 for r in runs if r.facts and not r.facts.is_complete),
            "nothing": sum(1 for r in runs if r.facts is None and r.error is None),
            "errors": sum(1 for r in runs if r.error),
            "avg_seconds": round(sum(r.seconds for r in runs) / len(runs), 1) if runs else 0.0,
            "est_cost_usd": round(paid_calls * GEMINI_COST_PER_CALL_USD, 2),
        }

    if len(reader_names) == 2:
        a, b = reader_names
        checks = [
            values_agree(field_value(c.runs[a].facts, f), field_value(c.runs[b].facts, f))
            for c in comparisons
            for f in REQUIRED_NUTRIENTS
            if a in c.runs and b in c.runs
        ]
        both_read = [x for x in checks if x is not None]
        summary["agreement"] = {
            "fields_compared": len(both_read),
            "agree_pct": round(100 * sum(both_read) / len(both_read)) if both_read else None,
        }
    return summary


def _fmt(value: Optional[float]) -> str:
    return "—" if value is None else f"{value:g}"


def to_markdown(comparisons: list[ProductComparison], summary: dict[str, dict], reader_names: list[str]) -> str:
    lines = [
        f"# Label Reader Comparison — {datetime.now():%Y-%m-%d %H:%M}",
        "",
        f"Readers: {', '.join(reader_names)} · Products: {len(comparisons)}",
        "",
        "## Summary",
        "",
        "| Reader | Complete | Partial | Nothing | Errors | Avg seconds | Est. cost (USD) |",
        "|---|---|---|---|---|---|---|",
    ]
    for name in reader_names:
        s = summary[name]
        lines.append(
            f"| {name} | {s['complete']}/{s['products']} | {s['partial']} | {s['nothing']} | {s['errors']} | {s['avg_seconds']} | {s['est_cost_usd']} |"
        )
    if "agreement" in summary and summary["agreement"]["agree_pct"] is not None:
        ag = summary["agreement"]
        lines += ["", f"Readers agree on {ag['agree_pct']}% of {ag['fields_compared']} required values both of them read."]
    lines += [
        "",
        "Fill the **Correct on pack?** column (✅ / ❌ per reader) by checking the real label, then decide which reader to keep.",
    ]

    for c in comparisons:
        lines += ["", f"## {c.brand} — {c.title}", "", f"[Product page]({c.url}) · {c.image_count} photos", ""]
        for name, run in c.runs.items():
            status = "error" if run.error else "complete" if run.facts and run.facts.is_complete else "partial" if run.facts else "nothing found"
            lines.append(f"- **{name}**: {status} in {run.seconds}s{' (cached)' if run.cached else ''}{' — ' + run.error if run.error else ''}")
        header = "| Field | " + " | ".join(c.runs) + " | Agree | Correct on pack? |"
        lines += ["", header, "|" + "---|" * (len(c.runs) + 3)]
        names = list(c.runs)
        for f in COMPARE_FIELDS:
            vals = [field_value(c.runs[n].facts, f) for n in names]
            if all(v is None for v in vals):
                continue
            agree = values_agree(vals[0], vals[1]) if len(vals) == 2 else None
            mark = "" if agree is None else "✅" if agree else "⚠️"
            lines.append(f"| {f} | " + " | ".join(_fmt(v) for v in vals) + f" | {mark} |  |")
        for n in names:
            facts = c.runs[n].facts
            if facts and facts.ingredients_text:
                lines.append(f"\n**{n} ingredients:** {facts.ingredients_text[:300]}")
    return "\n".join(lines) + "\n"


def save_report(comparisons: list[ProductComparison], summary: dict[str, dict], reader_names: list[str]) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    path = REPORTS_DIR / f"{stamp}.md"
    path.write_text(to_markdown(comparisons, summary, reader_names), encoding="utf-8")
    raw = {
        "summary": summary,
        "products": [
            {
                "brand": c.brand,
                "title": c.title,
                "url": c.url,
                "runs": {
                    n: {
                        "seconds": r.seconds,
                        "error": r.error,
                        "cached": r.cached,
                        "source": r.facts.source if r.facts else None,
                        "serving_size_g": r.facts.serving_size_g if r.facts else None,
                        "nutrition": r.facts.nutrition if r.facts else None,
                        "ingredients_text": r.facts.ingredients_text if r.facts else None,
                    }
                    for n, r in c.runs.items()
                },
            }
            for c in comparisons
        ],
    }
    path.with_suffix(".json").write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
