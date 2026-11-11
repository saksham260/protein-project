"""Seed runner script to load the curated 15 Indian protein products into Supabase."""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from src.db.supabase_client import SupabaseUploader
    from src.models import ProductCreate
except (ImportError, ModuleNotFoundError):
    from db.supabase_client import SupabaseUploader
    from models import ProductCreate

console = Console(force_terminal=True, legacy_windows=False)
SEED_FILE = Path(__file__).resolve().parent.parent / "data" / "seed_products.json"


def select_by_slug(products_data: list[dict], slugs: list[str] | None) -> list[dict]:
    """Pick products by slug, never by position in the file (positions shift whenever the file is rebuilt).

    Stops if a slug is missing or appears twice, so a re-run can never touch the wrong product.
    """
    if not slugs:
        return products_data
    by_slug: dict[str, list[dict]] = {}
    for item in products_data:
        by_slug.setdefault(item.get("slug"), []).append(item)
    missing = [s for s in slugs if s not in by_slug]
    doubled = [s for s in slugs if len(by_slug.get(s, [])) > 1]
    if missing or doubled:
        raise SystemExit(f"Refusing to seed. Not in seed file: {missing}. Listed more than once: {doubled}.")
    return [by_slug[s][0] for s in dict.fromkeys(slugs)]


def run_seed(dry_run: bool = False, slugs: list[str] | None = None):
    """Execute seeding from seed_products.json (all products, or only the given slugs)."""
    if not SEED_FILE.exists():
        console.print(f"[bold red]Error:[/] Seed file not found at {SEED_FILE}")
        sys.exit(1)

    with open(SEED_FILE, "r", encoding="utf-8") as f:
        products_data = select_by_slug(json.load(f), slugs)

    uploader = SupabaseUploader(dry_run=dry_run)
    mode_text = "[yellow]DRY-RUN (Local)[/]" if uploader.dry_run else "[green]LIVE (Supabase)[/]"
    console.print(f"\n[bold green]Seeding Indian Protein Catalog[/] | Mode: {mode_text} | Products: {len(products_data)}\n")

    summary_table = Table(title="Seeded Product Catalog")
    summary_table.add_column("#", justify="center", style="dim")
    summary_table.add_column("Brand", style="cyan", no_wrap=True)
    summary_table.add_column("Product", style="white")
    summary_table.add_column("Category", style="magenta")
    summary_table.add_column("₹ / g Protein", justify="right", style="green")
    summary_table.add_column("Density %", justify="right", style="blue")
    summary_table.add_column("Protein Tier", style="yellow")
    summary_table.add_column("Red Flags", style="red")

    for i, item in enumerate(products_data, 1):
        product = ProductCreate(**item)
        result = uploader.upsert_product(product)

        # Extract enriched variant details from first variant
        v = product.variants[0]
        v_metrics = v.computed_metrics
        v_profile = v.protein_profile

        cost_str = f"₹{v_metrics.cost_per_g_protein:.2f}" if v_metrics and v_metrics.cost_per_g_protein else "N/A"
        density_str = f"{v_metrics.protein_density_pct:.1f}%" if v_metrics and v_metrics.protein_density_pct else "N/A"
        tier_str = v_profile.protein_tier.split("–")[0].strip() if v_profile and v_profile.protein_tier else "Unknown"

        if v.red_flags:
            flags_str = f"{len(v.red_flags)} Flags (" + ", ".join(f.flag_type.replace('_alert', '') for f in v.red_flags) + ")"
        else:
            flags_str = "[bold green]Clean (0)[/]"

        summary_table.add_row(
            str(i),
            product.brand_name,
            product.name,
            product.category_slug,
            cost_str,
            density_str,
            tier_str,
            flags_str,
        )

    console.print(summary_table)
    console.print(f"\n[bold green]Seeding completed successfully![/] Total products: {len(products_data)}\n")


def main():
    parser = argparse.ArgumentParser(description="Seed initial Indian protein products into Supabase")
    parser.add_argument("--dry-run", action="store_true", help="Run without uploading to live Supabase")
    parser.add_argument("--slug", action="append", default=[], help="Only seed this product slug (repeatable)")
    parser.add_argument("--slugs-file", type=Path, help="JSON list of product slugs to seed (commit it with the change)")
    args = parser.parse_args()
    slugs = list(args.slug)
    if args.slugs_file:
        slugs += json.loads(args.slugs_file.read_text(encoding="utf-8"))
    run_seed(dry_run=args.dry_run, slugs=slugs or None)


if __name__ == "__main__":
    main()
