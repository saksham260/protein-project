"""Unit tests for calculated metrics engine."""

import pytest
from src.engine.metrics import (
    calculate_cost_per_g_protein,
    calculate_protein_per_pack,
    calculate_protein_density,
    calculate_true_net_carbs,
    compute_all_metrics,
)
from src.models import NutritionPerPack


def test_calculate_cost_per_g_protein_normal():
    # ₹150 for 20g protein = ₹7.50/g
    assert calculate_cost_per_g_protein(150.0, 20.0) == 7.50
    # ₹3000 for 750g protein = ₹4.00/g
    assert calculate_cost_per_g_protein(3000.0, 750.0) == 4.00


def test_calculate_cost_per_g_protein_edge_cases():
    # 0g protein or negative values
    assert calculate_cost_per_g_protein(150.0, 0.0) is None
    assert calculate_cost_per_g_protein(150.0, -5.0) is None
    assert calculate_cost_per_g_protein(-50.0, 20.0) is None
    assert calculate_cost_per_g_protein(0.0, 20.0) == 0.0


def test_calculate_protein_density_normal():
    # 20g protein * 4 = 80 kcal; 80 / 250 kcal * 100 = 32.0%
    assert calculate_protein_density(20.0, 250.0) == 32.00
    # 25g protein in 120 kcal shake = 100 / 120 * 100 = 83.33%
    assert calculate_protein_density(25.0, 120.0) == 83.33


def test_calculate_protein_density_edge_cases():
    assert calculate_protein_density(20.0, 0.0) is None
    assert calculate_protein_density(20.0, -100.0) is None
    assert calculate_protein_density(-5.0, 250.0) is None
    assert calculate_protein_density(0.0, 250.0) == 0.0


def test_calculate_true_net_carbs_normal():
    # 25g total carbs - 10g fiber - 5g erythritol = 10g net carbs
    assert calculate_true_net_carbs(25.0, 10.0, 5.0) == 10.0
    # No fiber, no polyols
    assert calculate_true_net_carbs(30.0, 0.0, 0.0) == 30.0


def test_calculate_true_net_carbs_clamped_at_zero():
    # Fiber + polyols exceeds total carbs
    assert calculate_true_net_carbs(15.0, 12.0, 10.0) == 0.0


def test_compute_all_metrics():
    nutrition = NutritionPerPack(
        calories_kcal=212.0,
        protein_g=20.0,
        total_fat_g=8.0,
        total_carbs_g=20.0,
        dietary_fiber_g=6.0,
        non_glycemic_polyols_g=0.0,
    )
    metrics = compute_all_metrics(mrp_inr=150.0, nutrition=nutrition)
    assert metrics.cost_per_g_protein == 7.50
    # 20 * 4 / 212 * 100 = 37.74%
    assert metrics.protein_density_pct == 37.74
    # 20 - 6 = 14g
    assert metrics.true_net_carbs_g == 14.0
    assert metrics.best_price_inr is None
    assert metrics.best_cost_per_g_protein is None


def test_calculate_protein_per_pack_scales_serving_to_pack():
    # 25g per 31g scoop in a 1kg tub = 806.45g protein
    assert calculate_protein_per_pack(25.0, 1000.0, 31.0) == pytest.approx(806.45, abs=0.01)
    # Single-serve bar: serving is the whole pack
    assert calculate_protein_per_pack(20.0, 52.0, 52.0) == 20.0
    # No pack info -> treated as single serve
    assert calculate_protein_per_pack(20.0) == 20.0


def test_compute_all_metrics_multi_serving_powder():
    # MuscleBlaze Biozyme 1kg: ₹3499 MRP, 25g protein per 31g scoop
    nutrition = NutritionPerPack(calories_kcal=118.0, protein_g=25.0, total_fat_g=1.0, total_carbs_g=2.0)
    metrics = compute_all_metrics(
        mrp_inr=3499.0,
        nutrition=nutrition,
        net_weight_g=1000.0,
        serving_size_g=31.0,
        platform_prices=[3199.0, None, 3249.0],
    )
    # 3499 / 806.45 = ₹4.34/g (was wrongly ₹139.96/g when divided by one scoop)
    assert metrics.cost_per_g_protein == 4.34
    assert metrics.best_price_inr == 3199.0
    assert metrics.best_cost_per_g_protein == 3.97
    # Density is a ratio, so it does not change with pack size
    assert metrics.protein_density_pct == 84.75
