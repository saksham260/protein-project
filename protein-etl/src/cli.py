"""Dual-mode Interactive CLI and Batch Ingestion Tool for The Protein Discovery Engine."""

from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path
import httpx
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from pydantic import ValidationError

# Ensure protein-etl package root is in sys.path
_pkg_root = str(Path(__file__).resolve().parent.parent)
if _pkg_root not in sys.path:
    sys.path.insert(0, _pkg_root)

try:
    from src.db.supabase_client import SupabaseUploader
    from src.engine.metrics import compute_all_metrics
    from src.engine.protein_tier import classify_protein_profile
    from src.engine.red_flags import scan_ingredients_for_red_flags
    from src.links import BROWSER_USER_AGENT, check_url
    from src.models import ProductCreate, VariantCreate
    from src.parsers.manual import prompt_manual_entry
    from src.parsers.shopify import extract_shopify_product
    from src.discovery.compare import collect_products, compare_product, save_report, summarize
    from src.discovery.gemini import GeminiLabelReader
    from src.discovery.ocr import OcrLabelReader
    from src.discovery.pipeline import DRAFTS_DIR, discover_brand, http_client
    from src.pricing.amazon import AmazonCreatorsClient
    from src.pricing.poller import poll_amazon_prices, trigger_revalidate
except (ImportError, ModuleNotFoundError):
    from db.supabase_client import SupabaseUploader
    from engine.metrics import compute_all_metrics
    from engine.protein_tier import classify_protein_profile
    from engine.red_flags import scan_ingredients_for_red_flags
    from links import BROWSER_USER_AGENT, check_url
    from models import ProductCreate, VariantCreate
    from parsers.manual import prompt_manual_entry
    from parsers.shopify import extract_shopify_product
    from discovery.compare import collect_products, compare_product, save_report, summarize
    from discovery.gemini import GeminiLabelReader
    from discovery.ocr import OcrLabelReader
    from discovery.pipeline import DRAFTS_DIR, discover_brand, http_client
    from pricing.amazon import AmazonCreatorsClient
    from pricing.poller import poll_amazon_prices, trigger_revalidate

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

        table = Table(
            title=f"Variant #{i}: {var.variant_name} (₹{var.mrp_inr} | {var.net_weight_g}g | {var.servings_per_pack} servings)"
        )
        table.add_column("Category", style="cyan", no_wrap=True)
        table.add_column("Metric / Value", style="white")

        # Metrics
        cost = v_metrics.cost_per_g_protein if v_metrics else None
        best_price = v_metrics.best_price_inr if v_metrics else None
        best_cost = v_metrics.best_cost_per_g_protein if v_metrics else None
        density = v_metrics.protein_density_pct if v_metrics else None
        net_carbs = v_metrics.true_net_carbs_g if v_metrics else None

        cost_str = f"₹{cost:.2f}/g" if cost is not None else "N/A"
        best_str = f"₹{best_price:g} → ₹{best_cost:.2f}/g" if best_price is not None and best_cost is not None else "N/A (no platform price)"
        density_str = f"{density:.1f}%" if density is not None else "N/A"
        net_carbs_str = f"{net_carbs:.1f}g" if net_carbs is not None else "N/A"

        table.add_row("Efficiency at MRP (₹/g)", cost_str)
        table.add_row("Best Known Price", best_str)
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


def run_check_links(path_str: str) -> int:
    """Check every redirect and image URL in a JSON file or folder. Returns the number of broken links."""
    target_path = Path(path_str)
    if not target_path.exists():
        console.print(f"[red]Error: Path '{path_str}' does not exist.[/]")
        sys.exit(1)

    files = [target_path] if target_path.is_file() else sorted(target_path.glob("*.json"))
    to_check: list[tuple[str, str, str]] = []  # (product, kind, url)
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_json = json.load(f)
        for item in raw_json if isinstance(raw_json, list) else [raw_json]:
            label = f"{item.get('brand_name', '?')} – {item.get('name', '?')}"
            if item.get("image_url"):
                to_check.append((label, "image", item["image_url"]))
            for var in item.get("variants", []):
                if var.get("image_url"):
                    to_check.append((label, "image", var["image_url"]))
                for link in var.get("redirect_links", []):
                    to_check.append((label, link.get("platform", "?"), link["url"]))

    results_table = Table(title=f"Link Check ({len(to_check)} URLs)")
    results_table.add_column("Product", style="cyan")
    results_table.add_column("Kind", style="magenta")
    results_table.add_column("Status")
    results_table.add_column("URL", style="dim", overflow="fold")

    status_styles = {"ok": "green", "broken": "bold red", "blocked": "yellow", "unreachable": "yellow"}
    broken = 0
    with httpx.Client(timeout=10.0, headers={"User-Agent": BROWSER_USER_AGENT}) as client:
        for label, kind, url in to_check:
            status, code = check_url(url, client)
            broken += status == "broken"
            status_text = f"{status} ({code})" if code else status
            results_table.add_row(label, kind, f"[{status_styles[status]}]{status_text}[/]", url)

    console.print(results_table)
    console.print(f"[bold]{broken} broken[/] link(s). 'blocked'/'unreachable' usually means bot protection — open those by hand.")
    return broken


def run_poll_prices(dry_run: bool = False, force: bool = False) -> int:
    """Refresh Amazon prices in Supabase. Returns a process exit code."""
    supabase_url = os.getenv("SUPABASE_URL", "").strip()
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY", "").strip()
    if not supabase_url or not supabase_key:
        console.print("[red]SUPABASE_URL and SUPABASE_SERVICE_KEY are required (the poller reads links from the database).[/]")
        return 1

    amazon = AmazonCreatorsClient.from_env()
    if amazon is None:
        console.print(
            "[red]Amazon Creators API credentials missing.[/] Set AMAZON_CREATORS_CLIENT_ID, "
            "AMAZON_CREATORS_CLIENT_SECRET and AMAZON_PARTNER_TAG."
        )
        return 1

    from supabase import create_client

    db = create_client(supabase_url, supabase_key)
    console.print(f"[bold green]Polling Amazon prices[/] | Mode: {'DRY-RUN' if dry_run else 'LIVE'}")
    summary = poll_amazon_prices(db, amazon, dry_run=dry_run, force=force)

    console.print(
        f"Checked {summary.checked} link(s), updated {summary.updated}, "
        f"recomputed {summary.variants_recomputed} variant(s), skipped {len(summary.skipped)}."
    )
    for reason in summary.skipped:
        console.print(f"  [yellow]skipped[/] {reason}")

    revalidate_url = os.getenv("REVALIDATE_URL", "").strip()
    revalidate_secret = os.getenv("REVALIDATE_SECRET", "").strip()
    if not dry_run and summary.updated and revalidate_url and revalidate_secret:
        ok = trigger_revalidate(revalidate_url, revalidate_secret)
        console.print("[green]Website pages refreshed.[/]" if ok else "[yellow]Website refresh request failed.[/]")
    return 0


def load_brands(brands_file: str, only_brand: str | None) -> list[dict] | None:
    """Brands from the JSON file, optionally just one. None (after printing why) when the brand is unknown."""
    with open(brands_file, "r", encoding="utf-8") as f:
        brands = json.load(f)
    if only_brand:
        brands = [b for b in brands if b["brand_name"].lower() == only_brand.lower()]
        if not brands:
            console.print(f"[red]Brand '{only_brand}' is not in {brands_file}.[/]")
            return None
    return brands


def build_readers(names: str, use_ai: bool = True) -> list:
    """Label-photo readers in the requested order, skipping (with a note) any that are not set up."""
    readers = []
    for name in [n.strip().lower() for n in names.split(",") if n.strip()]:
        if name == "ocr":
            reader = OcrLabelReader.from_env()
            if reader is None:
                console.print('[yellow]OCR skipped: install it with pip install -e ".[ocr]"[/]')
        elif name == "gemini":
            if not use_ai:
                continue
            reader = GeminiLabelReader.from_env()
            if reader is None:
                console.print("[yellow]Gemini skipped: GEMINI_API_KEY is not set.[/]")
        else:
            console.print(f"[yellow]Unknown reader '{name}' (use ocr, gemini).[/]")
            reader = None
        if reader:
            readers.append(reader)
    return readers


def run_discover(brands_file: str, only_brand: str | None, readers_arg: str, use_ai: bool, refresh: bool, limit: int | None) -> int:
    """Crawl brand Shopify stores and write review drafts to data/drafts/."""
    brands = load_brands(brands_file, only_brand)
    if brands is None:
        return 1

    readers = build_readers(readers_arg, use_ai)
    console.print(
        f"[bold green]Discovering products[/] from {len(brands)} brand(s) | "
        f"Label-photo readers: {', '.join(r.name for r in readers) or 'none'}"
    )

    status_styles = {"ready": "green", "needs_input": "yellow", "skipped": "dim", "exists": "dim"}
    with http_client() as client:
        for brand in brands:
            table = Table(title=brand["brand_name"])
            table.add_column("Product", style="cyan", overflow="fold")
            table.add_column("Status")
            table.add_column("Detail", style="dim")
            try:
                rows = discover_brand(brand["brand_name"], brand["store_url"], client, readers, refresh=refresh, limit=limit)
            except httpx.HTTPError as e:
                console.print(f"[red]{brand['brand_name']}: store not reachable ({e}).[/]")
                continue
            for row in rows:
                if row.status in ("ready", "needs_input"):
                    table.add_row(row.title, f"[{status_styles[row.status]}]{row.status}[/]", row.detail)
            skipped = sum(r.status in ("skipped", "exists") for r in rows)
            console.print(table)
            console.print(f"[dim]{skipped} product(s) skipped (not protein, bundles, or already seen).[/]\n")

    console.print(f"Drafts are in [bold]{DRAFTS_DIR}[/]. Next: [bold]python src/cli.py review[/]")
    return 0


def run_compare_readers(brands_file: str, only_brand: str | None, readers_arg: str, limit: int) -> int:
    """Run every reader on the same products and write a side-by-side report to documentation/."""
    brands = load_brands(brands_file, only_brand)
    if brands is None:
        return 1
    readers = build_readers(readers_arg)
    if not readers:
        console.print("[red]No readers available to compare.[/]")
        return 1

    with http_client() as client:
        console.print(f"[bold green]Collecting up to {limit} product(s) per brand...[/]")
        products = collect_products(brands, client, limit)
    if not products:
        console.print("[yellow]No protein products with photos found.[/]")
        return 0

    names = [r.name for r in readers]
    comparisons = []
    for i, (brand, extract) in enumerate(products, 1):
        console.print(f"[{i}/{len(products)}] {brand} — {extract['title']}")
        comparisons.append(compare_product(brand, extract, readers))

    summary = summarize(comparisons, names)
    table = Table(title="Label Reader Comparison")
    for column in ("Reader", "Complete", "Partial", "Nothing", "Errors", "Avg s", "Est. $"):
        table.add_column(column)
    for name in names:
        s = summary[name]
        table.add_row(name, f"{s['complete']}/{s['products']}", str(s["partial"]), str(s["nothing"]),
                      str(s["errors"]), str(s["avg_seconds"]), str(s["est_cost_usd"]))
    console.print(table)
    if summary.get("agreement", {}).get("agree_pct") is not None:
        ag = summary["agreement"]
        console.print(f"Readers agree on {ag['agree_pct']}% of {ag['fields_compared']} required values both read.")

    report = save_report(comparisons, summary, names)
    console.print(f"Report: [bold]{report}[/] — tick 'Correct on pack?' against the real labels.")
    return 0


def run_review(dry_run: bool = False) -> int:
    """Walk through drafts: approve (upload), skip, or reject each one."""
    drafts = sorted(DRAFTS_DIR.glob("*.json"))
    if not drafts:
        console.print("[yellow]No drafts to review. Run 'discover' first.[/]")
        return 0

    uploader = SupabaseUploader(dry_run=dry_run)
    console.print(f"[bold green]Reviewing {len(drafts)} draft(s)[/] | Mode: {'DRY-RUN' if uploader.dry_run else 'LIVE'}\n")
    approved = 0

    for path in drafts:
        draft = json.loads(path.read_text(encoding="utf-8"))
        console.print(
            Panel(
                f"[bold]{path.name}[/]\nSource: {draft.get('source_url')}\n"
                f"Nutrition from: {draft.get('nutrition_source') or 'nowhere yet'} "
                f"(tried: {', '.join(draft.get('layers_tried', [])) or '-'})",
                title=f"Draft · {draft.get('status')}",
            )
        )
        for warning in draft.get("warnings", []):
            console.print(f"  [yellow]⚠ {warning}[/]")

        product = None
        try:
            product = uploader.process_and_enrich_product(ProductCreate(**draft["product"]))
            render_preview(product)
        except ValidationError as e:
            console.print("[red]Not ready to upload — fix these fields in the JSON file:[/]")
            for err in e.errors():
                console.print(f"  [red]•[/] {'.'.join(str(x) for x in err['loc'])}: {err['msg']}")

        choices = (["Approve & upload"] if product else []) + ["Skip for now", "Reject (never suggest again)", "Quit"]
        choice = questionary.select("What do you want to do?", choices=choices).ask()
        if choice is None or choice == "Quit":
            break
        if choice == "Approve & upload":
            result = uploader.upsert_product(product)
            (DRAFTS_DIR / "approved").mkdir(exist_ok=True)
            path.replace(DRAFTS_DIR / "approved" / path.name)
            approved += 1
            console.print(f"[green]✅ Uploaded ({result['mode']}).[/]\n")
        elif choice.startswith("Reject"):
            (DRAFTS_DIR / "rejected").mkdir(exist_ok=True)
            path.replace(DRAFTS_DIR / "rejected" / path.name)
            console.print("[dim]Rejected.[/]\n")
        else:
            console.print(f"[dim]Skipped. Edit {path} and run review again.[/]\n")

    revalidate_url = os.getenv("REVALIDATE_URL", "").strip()
    revalidate_secret = os.getenv("REVALIDATE_SECRET", "").strip()
    if approved and not uploader.dry_run and revalidate_url and revalidate_secret:
        ok = trigger_revalidate(revalidate_url, revalidate_secret)
        console.print("[green]Website pages refreshed.[/]" if ok else "[yellow]Website refresh request failed.[/]")
    console.print(f"[bold]{approved} product(s) approved.[/]")
    return 0


def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(description="The Protein Discovery Engine Ingestion CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Interactive subparser
    subparsers.add_parser("interactive", help="Run interactive single-product wizard")

    # Batch subparser
    batch_parser = subparsers.add_parser("batch", help="Batch ingest JSON file or folder")
    batch_parser.add_argument("path", help="Path to JSON file or folder of JSON files")

    # Link-check subparser
    links_parser = subparsers.add_parser("check-links", help="Check redirect and image URLs in a JSON file or folder")
    links_parser.add_argument("path", help="Path to JSON file or folder of JSON files")

    # Price poller subparser
    poll_parser = subparsers.add_parser("poll-prices", help="Refresh Amazon prices in Supabase via the Creators API")
    poll_parser.add_argument("--force", action="store_true", help="Accept price changes larger than 50%%")

    # Discovery subparsers
    discover_parser = subparsers.add_parser("discover", help="Find protein products on brand Shopify stores and draft them")
    discover_parser.add_argument("--brands", default=str(Path(_pkg_root) / "data" / "brands.json"), help="Brands JSON file")
    discover_parser.add_argument("--brand", help="Only this brand name from the file")
    discover_parser.add_argument("--readers", default="ocr,gemini", help="Label-photo readers in order (default: ocr,gemini)")
    discover_parser.add_argument("--no-ai", action="store_true", help="Never call Gemini, even if GEMINI_API_KEY is set")
    discover_parser.add_argument("--refresh", action="store_true", help="Re-draft products seen before")
    discover_parser.add_argument("--limit", type=int, help="Max new drafts per brand")
    subparsers.add_parser("review", help="Approve, skip or reject discovered drafts")
    compare_parser = subparsers.add_parser("compare-readers", help="Run OCR and Gemini on the same products and report")
    compare_parser.add_argument("--brands", default=str(Path(_pkg_root) / "data" / "brands.json"), help="Brands JSON file")
    compare_parser.add_argument("--brand", help="Only this brand name from the file")
    compare_parser.add_argument("--readers", default="ocr,gemini", help="Readers to compare (default: ocr,gemini)")
    compare_parser.add_argument("--limit", type=int, default=3, help="Products per brand (default: 3)")

    # Global flags
    parser.add_argument("--dry-run", action="store_true", help="Force dry-run mode without live DB upload")

    args = parser.parse_args()

    if args.command == "batch":
        run_batch(args.path, dry_run=args.dry_run)
    elif args.command == "check-links":
        sys.exit(1 if run_check_links(args.path) else 0)
    elif args.command == "poll-prices":
        sys.exit(run_poll_prices(dry_run=args.dry_run, force=args.force))
    elif args.command == "discover":
        sys.exit(run_discover(args.brands, args.brand, args.readers, not args.no_ai, args.refresh, args.limit))
    elif args.command == "compare-readers":
        sys.exit(run_compare_readers(args.brands, args.brand, args.readers, args.limit))
    elif args.command == "review":
        sys.exit(run_review(dry_run=args.dry_run))
    elif args.command == "interactive":
        run_interactive(dry_run=args.dry_run)
    else:
        # If no command provided, default to interactive
        run_interactive(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
