"""Retire products from the live site safely: by slug, reversibly, with a backup.

Replaces the old batch scripts that hard-deleted products from lists that were never committed.

    python scripts/retire_products.py data/retirements/2026-11-xx-duplicates.json            # dry run
    python scripts/retire_products.py data/retirements/2026-11-xx-duplicates.json --apply    # live

The list file is a JSON array of {"slug": ..., "reason": ..., "kept_instead": optional slug}.
Commit it with the change so every removal can be traced.

What --apply does:
  1. Saves the full product, variant, red-flag and link rows to data/retirements/backups/.
  2. Sets is_active = false on the product and its variants. Nothing is deleted, so a product
     can be brought back with:  update products set is_active = true where slug = '...';
"""

from __future__ import annotations
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

ETL = Path(__file__).resolve().parents[1]
BACKUP_DIR = ETL / "data" / "retirements" / "backups"
REASON_MIN_LEN = 10


def load_retirements(path: Path) -> list[dict]:
    """Read and validate the retirement list. Every entry needs a slug and a real reason."""
    entries = json.loads(path.read_text(encoding="utf-8"))
    problems = []
    seen = set()
    for i, e in enumerate(entries):
        slug, reason = e.get("slug"), (e.get("reason") or "").strip()
        if not slug:
            problems.append(f"entry {i}: no slug")
        elif slug in seen:
            problems.append(f"{slug}: listed twice")
        seen.add(slug)
        if len(reason) < REASON_MIN_LEN:
            problems.append(f"{slug}: give a reason (duplicate of X / product does not exist / ...)")
        if e.get("kept_instead") == slug:
            problems.append(f"{slug}: kept_instead points at itself")
    if problems:
        raise SystemExit("Retirement list rejected:\n  " + "\n  ".join(problems))
    return entries


def snapshot(client, slug: str) -> dict | None:
    rows = client.table("products").select("*").eq("slug", slug).execute().data
    if not rows:
        return None
    product = rows[0]
    variants = client.table("product_variants").select("*").eq("product_id", product["id"]).execute().data
    ids = [v["id"] for v in variants]
    links = client.table("redirect_links").select("*").in_("variant_id", ids).execute().data if ids else []
    flags = client.table("variant_red_flags").select("*").in_("variant_id", ids).execute().data if ids else []
    return {"product": product, "variants": variants, "redirect_links": links, "variant_red_flags": flags}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("list_file", type=Path)
    parser.add_argument("--apply", action="store_true", help="Write to live Supabase (default is a dry run)")
    args = parser.parse_args()

    entries = load_retirements(args.list_file)
    kept = {e["kept_instead"] for e in entries if e.get("kept_instead")}
    retiring = {e["slug"] for e in entries}
    if kept & retiring:
        raise SystemExit(f"These are both retired and named as the product kept instead: {sorted(kept & retiring)}")

    load_dotenv(ETL / ".env")
    from supabase import create_client  # imported late so the validation above works offline

    client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])

    for slug in sorted(kept):
        alive = client.table("products").select("id").eq("slug", slug).eq("is_active", True).execute().data
        if not alive:
            raise SystemExit(f"'{slug}' is named as the product kept instead, but it is not live. Stopping.")

    snapshots = {}
    for e in entries:
        snap = snapshot(client, e["slug"])
        print(f"{'RETIRE' if snap else 'NOT LIVE'}  {e['slug']}  ({e['reason']})")
        if snap:
            snapshots[e["slug"]] = snap

    if not args.apply:
        print(f"\nDry run: {len(snapshots)} live products would be hidden. Re-run with --apply.")
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = BACKUP_DIR / f"{stamp}-{args.list_file.stem}.json"
    backup.write_text(json.dumps({"list": entries, "rows": snapshots}, indent=2, default=str), encoding="utf-8")
    print(f"Backup written: {backup}")

    for slug, snap in snapshots.items():
        client.table("product_variants").update({"is_active": False}).eq("product_id", snap["product"]["id"]).execute()
        client.table("products").update({"is_active": False}).eq("id", snap["product"]["id"]).execute()
    print(f"Hidden {len(snapshots)} products. Commit {args.list_file} and the backup with this change.")


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    main()
