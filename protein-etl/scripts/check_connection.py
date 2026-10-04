"""Connection verification script for protein-etl.
Validates SUPABASE_URL and SUPABASE_SERVICE_KEY against the live Supabase instance.
"""

from __future__ import annotations
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

console = Console(force_terminal=True, legacy_windows=False)

# Load protein-etl/.env
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    load_dotenv()

PLACEHOLDERS = {"", "https://your-project.supabase.co", "your-service-role-key", "your-project"}


def main():
    console.print("\n[bold cyan]=== Supabase ETL Connection Pre-Flight Check ===[/]\n")

    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_SERVICE_KEY", "").strip()

    if not url or url in PLACEHOLDERS or "placeholder" in url.lower():
        console.print("[bold red]❌ SUPABASE_URL is missing or contains placeholder values.[/]")
        console.print(f"   Current value: '{url}'")
        console.print(f"   Please update [bold]{ENV_FILE}[/]")
        sys.exit(1)

    if not key or key in PLACEHOLDERS or "placeholder" in key.lower():
        console.print("[bold red]❌ SUPABASE_SERVICE_KEY is missing or contains placeholder values.[/]")
        console.print(f"   Please update [bold]{ENV_FILE}[/]")
        sys.exit(1)

    masked_key = key[:10] + "..." + key[-4:] if len(key) > 14 else "***"
    console.print(f"Target URL: [green]{url}[/]")
    console.print(f"Service Key: [dim]{masked_key}[/]\n")

    try:
        from supabase import create_client
        client = create_client(url, key)
    except Exception as e:
        console.print(f"[bold red]❌ Failed to initialize Supabase client:[/] {e}")
        sys.exit(1)

    table = Table(title="Supabase Database Accessibility")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Details", style="dim")

    has_errors = False

    # Check 1: Read categories
    try:
        res = client.table("categories").select("count", count="exact").execute()
        count = res.count if res.count is not None else len(res.data or [])
        table.add_row("Read categories", "[green]✅ PASS[/]", f"{count} rows found")
    except Exception as e:
        has_errors = True
        table.add_row("Read categories", "[red]❌ FAIL[/]", str(e))

    # Check 2: Read products
    try:
        res = client.table("products").select("count", count="exact").execute()
        count = res.count if res.count is not None else len(res.data or [])
        table.add_row("Read products", "[green]✅ PASS[/]", f"{count} rows found")
    except Exception as e:
        has_errors = True
        table.add_row("Read products", "[red]❌ FAIL[/]", str(e))

    # Check 3: Read product_variants
    try:
        res = client.table("product_variants").select("count", count="exact").execute()
        count = res.count if res.count is not None else len(res.data or [])
        table.add_row("Read product_variants", "[green]✅ PASS[/]", f"{count} rows found")
    except Exception as e:
        has_errors = True
        table.add_row("Read product_variants", "[red]❌ FAIL[/]", str(e))

    # Check 4: Read redirect_links
    try:
        res = client.table("redirect_links").select("count", count="exact").execute()
        count = res.count if res.count is not None else len(res.data or [])
        table.add_row("Read redirect_links", "[green]✅ PASS[/]", f"{count} rows found")
    except Exception as e:
        has_errors = True
        table.add_row("Read redirect_links", "[red]❌ FAIL[/]", str(e))

    # Check 5: Read availability_reports
    try:
        res = client.table("availability_reports").select("count", count="exact").execute()
        count = res.count if res.count is not None else len(res.data or [])
        table.add_row("Read availability_reports", "[green]✅ PASS[/]", f"{count} rows found")
    except Exception as e:
        has_errors = True
        table.add_row("Read availability_reports", "[red]❌ FAIL[/]", str(e))

    # Check 6: Write & Delete Permission (Test Brand)
    test_slug = "__test_conn_check__"
    try:
        insert_res = client.table("brands").insert({
            "name": "Connection Test Temporary Brand",
            "slug": test_slug,
            "description": "Pre-flight connection test row; deleted immediately.",
        }).execute()
        
        # Verify inserted
        if insert_res.data:
            # Delete test brand
            client.table("brands").delete().eq("slug", test_slug).execute()
            table.add_row("Write/Delete (service_role)", "[green]✅ PASS[/]", "Inserted and cleaned up test brand")
        else:
            has_errors = True
            table.add_row("Write/Delete (service_role)", "[red]❌ FAIL[/]", "Insert returned no data")
    except Exception as e:
        has_errors = True
        table.add_row("Write/Delete (service_role)", "[red]❌ FAIL[/]", str(e))

    console.print(table)

    if has_errors:
        console.print("\n[bold red]Connection pre-flight check failed.[/] Review the errors above.")
        sys.exit(1)
    else:
        console.print("\n[bold green]All checks passed![/] Supabase is configured and ready for live seeding.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
