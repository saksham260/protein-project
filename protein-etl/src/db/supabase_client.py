"""Supabase uploader with offline dry-run support for The Protein Discovery Engine."""

from __future__ import annotations
import json
import os
import uuid
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from rich.console import Console

from src.engine.metrics import compute_all_metrics
from src.engine.protein_tier import classify_protein_profile
from src.engine.red_flags import scan_ingredients_for_red_flags
from src.models import ProductCreate, slugify

# Load .env if present
load_dotenv()

console = Console()
EXPORTS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "dry_run_exports"


class SupabaseUploader:
    """Handles product upload to Supabase or offline local export."""

    def __init__(self, dry_run: bool = False):
        self.supabase_url = os.getenv("SUPABASE_URL", "").strip()
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY", "").strip()

        # If credentials are missing or dry_run is requested, fallback to offline dry-run
        if dry_run or not self.supabase_url or not self.supabase_key:
            self.dry_run = True
            self.client = None
        else:
            self.dry_run = False
            from supabase import create_client
            self.client = create_client(self.supabase_url, self.supabase_key)

    def process_and_enrich_product(self, product: ProductCreate) -> ProductCreate:
        """Enrich all product variants with computed metrics, red flags, and protein tiers."""
        for variant in product.variants:
            # 1. Computed Metrics
            variant.computed_metrics = compute_all_metrics(
                mrp_inr=variant.mrp_inr,
                nutrition=variant.nutrition,
            )

            # 2. Red-Flag Scanning
            variant.red_flags = scan_ingredients_for_red_flags(variant.ingredient_list)

            # 3. Protein Tier Profile
            variant.protein_profile = classify_protein_profile(
                ingredients=variant.ingredient_list,
                red_flags=variant.red_flags,
            )

        return product

    def upsert_product(self, product: ProductCreate) -> dict[str, Any]:
        """Upload product or export locally in dry-run mode."""
        # Ensure all metrics and flags are computed
        product = self.process_and_enrich_product(product)

        if self.dry_run:
            return self._dry_run_export(product)
        else:
            return self._live_upsert(product)

    def upsert_product_variant(self, product: ProductCreate) -> dict[str, Any]:
        """Alias for upsert_product to match spec."""
        return self.upsert_product(product)

    def _dry_run_export(self, product: ProductCreate) -> dict[str, Any]:
        """Validate and write enriched product payload to disk without live database."""
        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
        export_file = EXPORTS_DIR / f"{product.slug}.json"

        payload = product.model_dump(mode="json")
        with open(export_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        mock_product_id = str(uuid.uuid4())
        mock_variant_ids = [str(uuid.uuid4()) for _ in product.variants]

        return {
            "mode": "dry-run",
            "export_file": str(export_file),
            "brand_slug": slugify(product.brand_name),
            "product_id": mock_product_id,
            "variant_ids": mock_variant_ids,
            "variants_count": len(product.variants),
            "status": "success",
        }

    def _live_upsert(self, product: ProductCreate) -> dict[str, Any]:
        """Upsert product and variants to live Supabase PostgreSQL."""
        if not self.client:
            raise RuntimeError("Supabase client is not initialized.")

        brand_slug = slugify(product.brand_name)

        # 1. Upsert Brand
        brand_res = self.client.table("brands").upsert(
            {
                "name": product.brand_name,
                "slug": brand_slug,
            },
            on_conflict="slug",
        ).execute()
        brand_id = brand_res.data[0]["id"]

        # 2. Get Category ID
        cat_res = self.client.table("categories").select("id").eq(
            "slug", product.category_slug
        ).execute()
        if not cat_res.data:
            # Create category if not existing
            cat_insert = self.client.table("categories").insert({
                "name": product.category_slug.replace("-", " ").title(),
                "slug": product.category_slug,
            }).execute()
            category_id = cat_insert.data[0]["id"]
        else:
            category_id = cat_res.data[0]["id"]

        # 3. Upsert Product
        prod_res = self.client.table("products").upsert(
            {
                "brand_id": brand_id,
                "category_id": category_id,
                "name": product.name,
                "slug": product.slug,
                "description": product.description,
                "image_url": product.image_url,
                "is_active": True,
            },
            on_conflict="slug",
        ).execute()
        product_id = prod_res.data[0]["id"]

        uploaded_variant_ids = []

        # 4. Upsert Variants
        for variant in product.variants:
            v_metrics = variant.computed_metrics
            v_profile = variant.protein_profile

            var_payload = {
                "product_id": product_id,
                "variant_name": variant.variant_name,
                "slug": f"{product.slug}-{variant.slug}",
                "sku": variant.sku,
                "barcode_ean": variant.barcode_ean,
                "mrp_inr": variant.mrp_inr,
                "net_weight_g": variant.net_weight_g,
                "serving_size_g": variant.serving_size_g,
                "servings_per_pack": variant.servings_per_pack,
                "calories_kcal": variant.nutrition.calories_kcal,
                "protein_g": variant.nutrition.protein_g,
                "total_fat_g": variant.nutrition.total_fat_g,
                "saturated_fat_g": variant.nutrition.saturated_fat_g,
                "trans_fat_g": variant.nutrition.trans_fat_g,
                "cholesterol_mg": variant.nutrition.cholesterol_mg,
                "total_carbs_g": variant.nutrition.total_carbs_g,
                "dietary_fiber_g": variant.nutrition.dietary_fiber_g,
                "total_sugars_g": variant.nutrition.total_sugars_g,
                "added_sugars_g": variant.nutrition.added_sugars_g,
                "sodium_mg": variant.nutrition.sodium_mg,
                "ingredient_list": variant.ingredient_list,
                "ingredient_deck_raw": variant.ingredient_deck_raw,
                "allergens": variant.allergens,
                "dietary_tags": variant.dietary_tags,
                "primary_protein_source": v_profile.primary_protein_source if v_profile else None,
                "protein_tier": v_profile.protein_tier if v_profile else None,
                "has_added_free_form_aminos": v_profile.has_added_free_form_aminos if v_profile else False,
                "cost_per_g_protein": v_metrics.cost_per_g_protein if v_metrics else None,
                "protein_density_pct": v_metrics.protein_density_pct if v_metrics else None,
                "true_net_carbs_g": v_metrics.true_net_carbs_g if v_metrics else None,
                "image_url": variant.image_url,
                "is_active": True,
            }

            var_res = self.client.table("product_variants").upsert(
                var_payload,
                on_conflict="slug",
            ).execute()
            variant_id = var_res.data[0]["id"]
            uploaded_variant_ids.append(variant_id)

            # 5. Insert Red Flags
            self.client.table("variant_red_flags").delete().eq("variant_id", variant_id).execute()
            if variant.red_flags:
                flag_rows = [
                    {
                        "variant_id": variant_id,
                        "flag_type": f.flag_type,
                        "flag_severity": f.flag_severity,
                        "flag_label": f.flag_label,
                        "flag_description": f.flag_description,
                        "matched_ingredient": f.matched_ingredient,
                        "ins_number": f.ins_number,
                    }
                    for f in variant.red_flags
                ]
                self.client.table("variant_red_flags").insert(flag_rows).execute()

            # 6. Upsert Redirect Links
            if variant.redirect_links:
                for link in variant.redirect_links:
                    self.client.table("redirect_links").insert({
                        "variant_id": variant_id,
                        "platform": link.platform,
                        "url": link.url,
                        "platform_price_inr": link.platform_price_inr,
                    }).execute()

        return {
            "mode": "live",
            "product_id": product_id,
            "variant_ids": uploaded_variant_ids,
            "variants_count": len(uploaded_variant_ids),
            "status": "success",
        }
