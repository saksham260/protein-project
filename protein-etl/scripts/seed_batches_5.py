"""Seed runner script to upload Batches 5A–5G (98 new products) to live Supabase."""

from __future__ import annotations
import json
import sys
import time
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

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "protein-etl"))

from src.db.supabase_client import SupabaseUploader
from src.models import ProductCreate

console = Console(force_terminal=True, legacy_windows=False)
SEED_FILE = ROOT / "protein-etl" / "data" / "seed_products.json"


def main():
    if not SEED_FILE.exists():
        console.print(f"[bold red]Error:[/] Seed file not found at {SEED_FILE}")
        sys.exit(1)

    with open(SEED_FILE, "r", encoding="utf-8") as f:
        all_products = json.load(f)

    # Batches 5A through 5G: products at index 280 onwards (98 products)
    batch5_products = all_products[280:]
    console.print(
        f"\n[bold green]Uploading Catalog Expansion (Batches 5A–5G) to Live Supabase[/]\n"
        f"Total products to upsert: [bold cyan]{len(batch5_products)}[/]\n"
    )

    uploader = SupabaseUploader(dry_run=False)

    table = Table(title="Live Supabase Batch 5 Ingestion")
    table.add_column("#", justify="center", style="dim", width=4)
    table.add_column("Brand", style="cyan", width=22)
    table.add_column("Product", style="white", width=36)
    table.add_column("Category", style="magenta", width=18)
    table.add_column("Variants", justify="center", style="yellow", width=8)
    table.add_column("Time (s)", justify="right", style="blue", width=8)
    table.add_column("Status", style="green", width=10)

    success_count = 0
    error_count = 0
    t_start = time.time()

    for idx, p_data in enumerate(batch5_products, 1):
        product = ProductCreate(**p_data)
        t0 = time.time()
        try:
            res = uploader.upsert_product(product)
            elapsed = time.time() - t0
            table.add_row(
                str(idx),
                product.brand_name[:20],
                product.name[:34],
                product.category_slug,
                str(len(product.variants)),
                f"{elapsed:.2f}",
                "[green]OK[/]",
            )
            success_count += 1
        except Exception as e:
            elapsed = time.time() - t0
            table.add_row(
                str(idx),
                product.brand_name[:20],
                product.name[:34],
                product.category_slug,
                str(len(product.variants)),
                f"{elapsed:.2f}",
                f"[red]FAIL: {str(e)[:15]}[/]",
            )
            error_count += 1
            console.print(f"[bold red]Error on {product.slug}:[/] {e}")

    total_time = time.time() - t_start
    console.print(table)
    console.print(
        f"\n[bold]Upload Complete in {total_time:.1f}s[/]: "
        f"[green]{success_count} succeeded[/], "
        f"[red]{error_count} failed[/].\n"
    )

    # Verify live counts
    client = uploader.client
    res_p = client.table("products").select("id", count="exact").execute()
    res_b = client.table("brands").select("id", count="exact").execute()
    res_v = client.table("product_variants").select("id", count="exact").execute()
    res_c = client.table("categories").select("id", count="exact").execute()

    console.print("[bold cyan]=== Live Supabase Database Verification ===[/]")
    console.print(f"Total Products:  [bold white]{res_p.count}[/]")
    console.print(f"Total Brands:    [bold white]{res_b.count}[/]")
    console.print(f"Total Variants:  [bold white]{res_v.count}[/]")
    console.print(f"Total Categories:[bold white]{res_c.count}[/]")


if __name__ == "__main__":
    main()
