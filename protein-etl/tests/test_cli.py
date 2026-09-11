"""Unit tests for protein-etl CLI."""

import json
from pathlib import Path
from unittest.mock import patch
import pytest
from src.cli import main, run_batch


def test_cli_help(capsys):
    with patch("sys.argv", ["protein-etl", "--help"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "The Protein Discovery Engine Ingestion CLI" in captured.out


def test_run_batch_dry_run(tmp_path):
    # Create sample product JSON file
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

    # Check export was generated
    export_dir = Path("protein-etl/data/dry_run_exports")
    assert export_dir.exists()
    exported_file = export_dir / "plantigo-organic-plant-protein.json"
    assert exported_file.exists()

    with open(exported_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["name"] == "Organic Plant Protein"
    assert data["variants"][0]["computed_metrics"]["cost_per_g_protein"] == 104.12
    assert "Tier 3" in data["variants"][0]["protein_profile"]["protein_tier"]
    assert len(data["variants"][0]["red_flags"]) == 0
