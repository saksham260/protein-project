"""Unit tests for SupabaseUploader in offline dry-run and enrichment — Suite 10."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from src.db.supabase_client import SupabaseUploader
from src.models import (
    NutritionPerPack,
    ProductCreate,
    RedirectLinkItem,
    VariantCreate,
)


@pytest.fixture
def sample_product():
    nutrition = NutritionPerPack(
        calories_kcal=212.0,
        protein_g=20.0,
        total_fat_g=8.0,
        total_carbs_g=20.0,
        dietary_fiber_g=6.0,
    )
    variant = VariantCreate(
        variant_name="Double Cocoa Bar",
        mrp_inr=150.0,
        net_weight_g=52.0,
        serving_size_g=52.0,
        nutrition=nutrition,
        ingredient_list=["Whey Protein Isolate", "Almonds", "Maltitol"],
        redirect_links=[
            RedirectLinkItem(platform="amazon", url="https://amazon.in/dp/B1", platform_price_inr=140.0)
        ],
    )
    return ProductCreate(
        name="Double Cocoa Protein Bar",
        brand_name="The Whole Truth",
        category_slug="protein-bars",
        variants=[variant],
    )


def test_uploader_auto_dry_run_without_env():
    with patch.dict("os.environ", {}, clear=True):
        uploader = SupabaseUploader()
        assert uploader.dry_run is True
        assert uploader.client is None


def test_process_and_enrich_product(sample_product):
    uploader = SupabaseUploader(dry_run=True)
    enriched = uploader.process_and_enrich_product(sample_product)
    v = enriched.variants[0]

    # Metrics computed
    assert v.computed_metrics is not None
    assert v.computed_metrics.cost_per_g_protein == 7.50
    assert v.computed_metrics.best_price_inr == 140.0
    assert v.computed_metrics.best_cost_per_g_protein == 7.0

    # Red flags scanned
    assert len(v.red_flags) == 1
    assert v.red_flags[0].flag_type == "maltitol_alert"

    # Protein tier classified
    assert v.protein_profile is not None
    assert v.protein_profile.primary_protein_source == "Whey Protein Isolate"
    assert "Tier 1" in v.protein_profile.protein_tier


def test_dry_run_export_writes_json(sample_product, tmp_path):
    with patch("src.db.supabase_client.EXPORTS_DIR", tmp_path):
        uploader = SupabaseUploader(dry_run=True)
        res = uploader.upsert_product(sample_product)

        assert res["mode"] == "dry-run"
        assert res["status"] == "success"
        assert res["variants_count"] == 1
        assert res["product_id"] is not None

        export_path = Path(res["export_file"])
        assert export_path.exists()

        with open(export_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["slug"] == sample_product.slug
        assert data["variants"][0]["computed_metrics"]["cost_per_g_protein"] == 7.50
