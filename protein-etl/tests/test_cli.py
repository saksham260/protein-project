"""Unit tests for protein-etl CLI."""

import json
from unittest.mock import patch
import pytest
import src.cli as cli
import src.db.supabase_client as supabase_client
from src.cli import main, run_batch, run_check_links


def test_cli_help(capsys):
    with patch("sys.argv", ["protein-etl", "--help"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "The Protein Discovery Engine Ingestion CLI" in captured.out


def test_run_batch_dry_run(tmp_path, monkeypatch):
    # Write exports to a temp folder so the test never overwrites data/dry_run_exports
    exports_dir = tmp_path / "exports"
    monkeypatch.setattr(supabase_client, "EXPORTS_DIR", exports_dir)

    sample_product = {
        "name": "Organic Plant Protein",
        "brand_name": "Plantigo",
        "category_slug": "protein-powders",
        "description": "Clean plant protein blend",
        "variants": [
            {
                "variant_name": "Rich Chocolate 1kg",
                "mrp_inr": 2499.0,
                "net_weight_g": 1000.0,
                "serving_size_g": 35.0,
                "nutrition": {
                    "calories_kcal": 135.0,
                    "protein_g": 24.0,
                    "total_fat_g": 2.0,
                    "total_carbs_g": 5.0,
                    "dietary_fiber_g": 3.0,
                },
                "ingredient_list": [
                    "Organic Pea Protein Isolate",
                    "Organic Brown Rice Protein",
                    "Organic Raw Cocoa",
                    "Stevia Extract",
                ],
                "allergens": [],
                "dietary_tags": ["Vegan", "Organic", "Gluten-Free"],
            }
        ],
    }

    test_file = tmp_path / "sample_product.json"
    with open(test_file, "w", encoding="utf-8") as f:
        json.dump([sample_product], f)

    # Execute batch dry run
    run_batch(str(test_file), dry_run=True)

    exported_file = exports_dir / "plantigo-organic-plant-protein.json"
    assert exported_file.exists()

    with open(exported_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    variant = data["variants"][0]
    assert data["name"] == "Organic Plant Protein"
    # 24g per 35g serving x 1000g tub = 685.7g protein; ₹2499 / 685.7 = ₹3.64/g
    assert variant["computed_metrics"]["cost_per_g_protein"] == 3.64
    assert variant["servings_per_pack"] == 29
    assert "Tier 3" in variant["protein_profile"]["protein_tier"]
    assert len(variant["red_flags"]) == 0


def test_run_check_links_counts_broken(tmp_path, monkeypatch):
    product = {
        "name": "Bar",
        "brand_name": "Brand",
        "image_url": "https://example.com/bad-image.png",
        "variants": [{"redirect_links": [{"platform": "amazon", "url": "https://example.com/ok"}]}],
    }
    test_file = tmp_path / "links.json"
    test_file.write_text(json.dumps([product]), encoding="utf-8")

    monkeypatch.setattr(
        cli, "check_url", lambda url, client: ("broken", 404) if "bad" in url else ("ok", 200)
    )
    assert run_check_links(str(test_file)) == 1
