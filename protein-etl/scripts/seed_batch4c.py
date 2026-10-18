"""Targeted seeder script for Batch 4C products:
- Fuel One (4 products: Whey Max Powder, Whey Iso-Max, Whey Protein, Impact Whey Protein)
- Kapiva (1 product: Testofuel Shilajit Whey Protein)
- Bolt Nutrition (5 products: Whey 5lb, Whey Isolate 2lb, Fermented Yeast, Biozyme Plant, Protein Bar)
- XLR8 Sports Nutrition (4 products: Whey 4lbs, Whey 2lbs, Classic Whey 1kg, Whey Sachets)
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

BATCH4C_BRANDS = {"Fuel One", "Kapiva", "Bolt Nutrition", "XLR8 Sports Nutrition"}

def main():
    with open(SEED_FILE, encoding="utf-8") as f:
        all_products = json.load(f)

    batch4c_products = [
        p for p in all_products 
        if p.get("brand_name") in BATCH4C_BRANDS
    ]
    console.print(f"\n[bold green]Seeding Batch 4C to Supabase[/] | Products to upsert: {len(batch4c_products)}\n")

    uploader = SupabaseUploader(dry_run=False)
    console.print(f"Supabase client initialized. supports_is_vegan={uploader.supports_is_vegan}\n")

    table = Table(title="Batch 4C Live Supabase Upload")
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

    for idx, p_data in enumerate(batch4c_products, 1):
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
                f"[bold red]FAIL: {e}[/]"
            )
            console.print(f"[bold red]Error upserting {product.brand_name} {product.name}: {e}[/]")

    total_time = time.time() - t_start
    console.print(table)
    console.print(f"\n[bold]{'SUCCESS' if success_count == len(batch4c_products) else 'PARTIAL'}:[/] Seeded {success_count}/{len(batch4c_products)} products to Supabase in {total_time:.1f}s.\n")

if __name__ == "__main__":
    main()
