"""Dual-mode Interactive CLI and Batch Ingestion Tool for The Protein Discovery Engine."""

from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Ensure protein-etl package root is in sys.path
_pkg_root = str(Path(__file__).resolve().parent.parent)
if _pkg_root not in sys.path:
    sys.path.insert(0, _pkg_root)

try:
    from src.db.supabase_client import SupabaseUploader
    from src.engine.metrics import compute_all_metrics
    from src.engine.protein_tier import classify_protein_profile
    from src.engine.red_flags import scan_ingredients_for_red_flags
    from src.models import ProductCreate, VariantCreate
    from src.parsers.manual import prompt_manual_entry
    from src.parsers.shopify import extract_shopify_product
except (ImportError, ModuleNotFoundError):
    from db.supabase_client import SupabaseUploader
    from engine.metrics import compute_all_metrics
    from engine.protein_tier import classify_protein_profile
    from engine.red_flags import scan_ingredients_for_red_flags
    from models import ProductCreate, VariantCreate
    from parsers.manual import prompt_manual_entry
    from parsers.shopify import extract_shopify_product

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

console = Console(force_terminal=True, legacy_windows=False)


def render_preview(product: ProductCreate):
    """Render rich terminal preview for a product and its variants."""
    console.print(Panel(f"[bold cyan]{product.brand_name}[/] - [bold white]{product.name}[/] ({product.category_slug})", title="Product Preview"))

    for i, var in enumerate(product.variants, 1):
        v_metrics = var.computed_metrics
        v_profile = var.protein_profile

        table = Table(title=f"Variant #{i}: {var.variant_name} (₹{var.mrp_inr} | {var.net_weight_g}g)")
        table.add_column("Category", style="cyan", no_wrap=True)
        table.add_column("Metric / Value", style="white")

        # Metrics
        cost_str = f"₹{v_metrics.cost_per_g_protein:.2f}/g" if v_metrics and v_metrics.cost_per_g_protein else "N/A"
        density_str = f"{v_metrics.protein_density_pct:.1f}%" if v_metrics and v_metrics.protein_density_pct else "N/A"
        net_carbs_str = f"{v_metrics.true_net_carbs_g:.1f}g" if v_metrics and v_metrics.true_net_carbs_g is not None else "N/A"

        table.add_row("Efficiency (₹/g)", cost_str)
        table.add_row("Protein Density (%)", density_str)
        table.add_row("True Net Carbs", net_carbs_str)

        # Protein Profile
        primary = v_profile.primary_protein_source if v_profile else "Unknown"
        tier = v_profile.protein_tier if v_profile else "Unclassified"
        spiked = "⚠️ YES (Added Aminos)" if v_profile and v_profile.has_added_free_form_aminos else "✅ No (Intact Protein)"

        table.add_row("Primary Protein Source", primary)
        table.add_row("Protein Tier", tier)
        table.add_row("Amino Spiking", spiked)

        # Red Flags
        if var.red_flags:
            flags_str = "\n".join(
                f"[bold red]🔴 {f.flag_label}[/] ({f.matched_ingredient or 'INS ' + str(f.ins_number)})"
                if f.flag_severity == "high"
                else f"[bold yellow]🟠 {f.flag_label}[/] ({f.matched_ingredient or ''})"
                for f in var.red_flags
            )
            table.add_row("Red Flags", flags_str)
        else:
            table.add_row("Red Flags", "[bold green]✅ Zero Red Flags Detected[/]")

        console.print(table)


def run_interactive(dry_run: bool = False):
    """Run interactive single-product wizard."""
    console.print("\n[bold green]═══ The Protein Discovery Engine: Interactive CLI ═══[/]\n")

    source_choice = questionary.select(
        "How do you want to add this product?",
        choices=[
            "[1] Shopify URL (auto-extract from /products.json)",
            "[2] Manual entry (guided interactive prompts)",
        ],
    ).ask()

    if not source_choice:
        console.print("[yellow]Operation cancelled.[/]")
        return

    product_data = None
    if "[1]" in source_choice:
        url = questionary.text("Enter Shopify Product URL:").ask()
        if url and url.strip():
            try:
                with console.status("Fetching from Shopify endpoint..."):
                    extracted = extract_shopify_product(url.strip())
                console.print(f"[green]Found:[/] {extracted['title']} ({extracted['brand_name']})")
                product_data = prompt_manual_entry(initial_data=extracted)
            except Exception as e:
                console.print(f"[red]Failed to extract Shopify URL: {e}[/]")
                if questionary.confirm("Fallback to manual entry?").ask():
                    product_data = prompt_manual_entry()
                else:
                    return
    else:
        product_data = prompt_manual_entry()

    if not product_data:
        return

    uploader = SupabaseUploader(dry_run=dry_run)
    enriched_product = uploader.process_and_enrich_product(product_data)
    render_preview(enriched_product)

    confirm_upload = questionary.confirm(
        f"Proceed with upload to Supabase? (mode: {'DRY-RUN' if uploader.dry_run else 'LIVE'})",
        default=True,
    ).ask()

    if confirm_upload:
        with console.status("Uploading product data..."):
            result = uploader.upsert_product(enriched_product)
        console.print(f"[bold green]✅ Upload Complete![/] Mode: {result['mode']} | Product ID: {result.get('product_id')}")
    else:
        console.print("[yellow]Upload cancelled by user.[/]")


def run_batch(path_str: str, dry_run: bool = False):
    """Ingest JSON product file or directory of JSON files in bulk."""
    target_path = Path(path_str)
    if not target_path.exists():
        console.print(f"[red]Error: Path '{path_str}' does not exist.[/]")
        sys.exit(1)

    files_to_process = []
    if target_path.is_file():
        files_to_process.append(target_path)
    else:
        files_to_process.extend(target_path.glob("*.json"))

    if not files_to_process:
        console.print(f"[yellow]No JSON files found at '{path_str}'.[/]")
        return

    uploader = SupabaseUploader(dry_run=dry_run)
    console.print(f"[bold green]Starting Batch Ingestion:[/] {len(files_to_process)} file(s) | Mode: {'DRY-RUN' if uploader.dry_run else 'LIVE'}\n")

    summary_table = Table(title="Batch Ingestion Results")
    summary_table.add_column("File", style="cyan")
    summary_table.add_column("Brand", style="white")
    summary_table.add_column("Product", style="white")
    summary_table.add_column("Variants", justify="center")
    summary_table.add_column("Status", style="green")

    for file_path in files_to_process:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_json = json.load(f)

            # Support single product dict or list of products
            items = raw_json if isinstance(raw_json, list) else [raw_json]
            for item in items:
                prod = ProductCreate(**item)
                res = uploader.upsert_product(prod)
                summary_table.add_row(
                    file_path.name,
                    prod.brand_name,
                    prod.name,
                    str(len(prod.variants)),
                    f"✅ {res['status']}",
                )
        except Exception as e:
            summary_table.add_row(
                file_path.name,
                "Error",
                str(e),
                "-",
                "[red]❌ Failed[/]",
            )

    console.print(summary_table)


def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(description="The Protein Discovery Engine Ingestion CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Interactive subparser
    subparsers.add_parser("interactive", help="Run interactive single-product wizard")

    # Batch subparser
    batch_parser = subparsers.add_parser("batch", help="Batch ingest JSON file or folder")
    batch_parser.add_argument("path", help="Path to JSON file or folder of JSON files")

    # Global flags
    parser.add_argument("--dry-run", action="store_true", help="Force dry-run mode without live DB upload")

    args = parser.parse_args()

    if args.command == "batch":
        run_batch(args.path, dry_run=args.dry_run)
    elif args.command == "interactive":
        run_interactive(dry_run=args.dry_run)
    else:
        # If no command provided, default to interactive
        run_interactive(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
