"""Targeted seeder script for Batch 4B products:
- Amul High Protein Milk & High Protein Probiotic Dahi
- Open Secret (6 products: DailyWHEY+, Rusk, 2 Cookies, Oats, Ragi Chips)
- The Butternut Company (7 products: 5 PB & Spreads, Energy Balls, Coffee Caramel)
- Taali Foods (4 products: 2 Protein Puffs, Roasted Makhana, Roasted Peanuts)
"""
import json
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table

ROOT = Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(ROOT / "protein-etl"))

from src.db.supabase_client import SupabaseUploader
from src.models import ProductCreate

console = Console(force_terminal=True)
SEED_FILE = ROOT / "protein-etl" / "data" / "seed_products.json"

BATCH4B_BRANDS = {"Open Secret", "The Butternut Company", "Taali Foods"}
BATCH4B_AMUL_SLUGS = {"amul-high-protein-milk", "amul-high-protein-probiotic-dahi"}

def main():
    with open(SEED_FILE, encoding="utf-8") as f:
        all_products = json.load(f)

    batch4b_products = [
        p for p in all_products 
        if p.get("brand_name") in BATCH4B_BRANDS or p.get("slug") in BATCH4B_AMUL_SLUGS
    ]
    console.print(f"\n[bold green]Seeding Batch 4B to Supabase[/] | Products to upsert: {len(batch4b_products)}\n")

    uploader = SupabaseUploader(dry_run=False)
    console.print(f"Supabase client initialized. supports_is_vegan={uploader.supports_is_vegan}\n")

    table = Table(title="Batch 4B Live Supabase Upload")
    table.add_column("#", justify="center", style="dim")
    table.add_column("Brand", style="cyan")
    table.add_column("Product", style="white")
    table.add_column("Category", style="magenta")
    table.add_column("Vegan", justify="center", style="yellow")
    table.add_column("Variants", justify="center", style="yellow")
    table.add_column("Time (s)", justify="right", style="blue")
    table.add_column("Status", style="green")

    success_count = 0
    t_start = time.time()

    for idx, p_data in enumerate(batch4b_products, 1):
        product = ProductCreate(**p_data)
        t0 = time.time()
        try:
            res = uploader.upsert_product(product)
            elapsed = time.time() - t0
            table.add_row(
                str(idx),
                product.brand_name,
                product.name,
                product.category_slug,
                "Yes" if product.is_vegan else "No",
                str(len(product.variants)),
                f"{elapsed:.1f}s",
                "[bold green]OK[/]"
            )
            success_count += 1
        except Exception as e:
            elapsed = time.time() - t0
            table.add_row(
                str(idx),
                product.brand_name,
                product.name,
                product.category_slug,
                "Yes" if product.is_vegan else "No",
                str(len(product.variants)),
                f"{elapsed:.1f}s",
                f"[bold red]FAIL: {str(e)[:30]}[/]"
            )

    console.print(table)
    total_time = time.time() - t_start
    console.print(f"\n[bold green]Batch 4B Seeding Complete![/] {success_count}/{len(batch4b_products)} uploaded in {total_time:.1f}s\n")

if __name__ == "__main__":
    main()
