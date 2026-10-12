"""Unit tests for calculated metrics engine — covering Suite 1 test cases and edge cases."""

import pytest
from src.engine.metrics import (
    calculate_cost_per_g_protein,
    calculate_protein_per_pack,
    calculate_protein_density,
    calculate_true_net_carbs,
    compute_all_metrics,
)
from src.models import NutritionPerPack


# ==========================================
# 1.1 calculate_protein_per_pack
# ==========================================

def test_protein_per_pack_single_serve():
    assert calculate_protein_per_pack(20.0, 52.0, 52.0) == 20.0


def test_protein_per_pack_multi_serve():
    assert calculate_protein_per_pack(25.0, 1000.0, 31.25) == 800.0


def test_protein_per_pack_rtd_bottle():
    assert calculate_protein_per_pack(30.0, 330.0, 330.0) == 30.0


def test_protein_per_pack_missing_net_weight():
    assert calculate_protein_per_pack(20.0, None, 52.0) == 20.0


def test_protein_per_pack_missing_serving_size():
    assert calculate_protein_per_pack(20.0, 1000.0, None) == 20.0


def test_protein_per_pack_both_omitted():
    assert calculate_protein_per_pack(15.0) == 15.0


def test_protein_per_pack_none_protein():
    assert calculate_protein_per_pack(None, 1000.0, 30.0) is None


def test_protein_per_pack_negative_protein():
    assert calculate_protein_per_pack(-5.0, 1000.0, 30.0) is None


def test_protein_per_pack_zero_protein():
    assert calculate_protein_per_pack(0.0, 100.0, 30.0) == 0.0


def test_protein_per_pack_zero_net_weight():
    assert calculate_protein_per_pack(25.0, 0.0, 30.0) == 25.0


def test_protein_per_pack_zero_serving_size():
    assert calculate_protein_per_pack(25.0, 1000.0, 0.0) == 25.0


def test_protein_per_pack_large_tub():
    assert calculate_protein_per_pack(25.0, 2000.0, 30.0) == pytest.approx(1666.67, abs=0.01)


def test_protein_per_pack_string_coercion():
    assert calculate_protein_per_pack("25", "1000", "31.25") == 800.0


# ==========================================
# 1.2 calculate_cost_per_g_protein
# ==========================================

def test_cost_per_g_normal_bar():
    assert calculate_cost_per_g_protein(150.0, 20.0) == 7.50


def test_cost_per_g_powder_tub():
    assert calculate_cost_per_g_protein(3499.0, 800.0) == 4.37


def test_cost_per_g_zero_protein():
    assert calculate_cost_per_g_protein(150.0, 0.0) is None


def test_cost_per_g_negative_protein():
    assert calculate_cost_per_g_protein(150.0, -10.0) is None


def test_cost_per_g_none_protein():
    assert calculate_cost_per_g_protein(150.0, None) is None


def test_cost_per_g_none_mrp():
    assert calculate_cost_per_g_protein(None, 20.0) is None


def test_cost_per_g_negative_mrp():
    assert calculate_cost_per_g_protein(-50.0, 20.0) is None


def test_cost_per_g_zero_mrp():
    assert calculate_cost_per_g_protein(0.0, 20.0) == 0.0


def test_cost_per_g_high_price():
    assert calculate_cost_per_g_protein(600.0, 5.0) == 120.00


# ==========================================
# 1.3 calculate_protein_density
# ==========================================

def test_protein_density_normal_bar():
    assert calculate_protein_density(20.0, 212.0) == 37.74


def test_protein_density_pure_isolate():
    assert calculate_protein_density(25.0, 100.0) == 100.0


def test_protein_density_zero_calories():
    assert calculate_protein_density(20.0, 0.0) is None


def test_protein_density_negative_calories():
    assert calculate_protein_density(20.0, -50.0) is None


def test_protein_density_zero_protein():
    assert calculate_protein_density(0.0, 200.0) == 0.0


def test_protein_density_none_protein():
    assert calculate_protein_density(None, 200.0) is None


def test_protein_density_negative_protein():
    assert calculate_protein_density(-5.0, 200.0) is None


def test_protein_density_both_none():
    assert calculate_protein_density(None, None) is None


def test_protein_density_over_100():
    assert calculate_protein_density(30.0, 100.0) == 120.0


# ==========================================
# 1.4 calculate_true_net_carbs
# ==========================================

def test_true_net_carbs_normal():
    assert calculate_true_net_carbs(25.0, 5.0, 3.0) == 17.0


def test_true_net_carbs_no_fiber_polyols():
    assert calculate_true_net_carbs(30.0) == 30.0


def test_true_net_carbs_keto_bar():
    assert calculate_true_net_carbs(20.0, 8.0, 10.0) == 2.0


def test_true_net_carbs_clamped_at_zero():
    assert calculate_true_net_carbs(5.0, 10.0, 3.0) == 0.0


def test_true_net_carbs_all_none():
    assert calculate_true_net_carbs(None) == 0.0


def test_true_net_carbs_fiber_polyols_none():
    assert calculate_true_net_carbs(20.0, None, None) == 20.0


# ==========================================
# 1.5 compute_all_metrics Integration
# ==========================================

def test_compute_all_metrics_single_serve_no_platform_prices():
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
    assert metrics.protein_density_pct == 37.74
    assert metrics.true_net_carbs_g == 14.0
    assert metrics.best_price_inr is None
    assert metrics.best_cost_per_g_protein is None


def test_compute_all_metrics_multi_serve_with_platform_prices():
    nutrition = NutritionPerPack(calories_kcal=118.0, protein_g=25.0, total_fat_g=1.0, total_carbs_g=2.0)
    metrics = compute_all_metrics(
        mrp_inr=3499.0,
        nutrition=nutrition,
        net_weight_g=1000.0,
        serving_size_g=31.0,
        platform_prices=[3199.0, None, 3249.0],
    )
    assert metrics.cost_per_g_protein == 4.34
    assert metrics.best_price_inr == 3199.0
    assert metrics.best_cost_per_g_protein == 3.97
    assert metrics.protein_density_pct == 84.75


def test_compute_all_metrics_empty_platform_prices():
    nutrition = NutritionPerPack(calories_kcal=100.0, protein_g=20.0, total_fat_g=1.0, total_carbs_g=2.0)
    metrics = compute_all_metrics(mrp_inr=100.0, nutrition=nutrition, platform_prices=[])
    assert metrics.best_price_inr is None


def test_compute_all_metrics_non_positive_platform_prices():
    nutrition = NutritionPerPack(calories_kcal=100.0, protein_g=20.0, total_fat_g=1.0, total_carbs_g=2.0)
    metrics = compute_all_metrics(mrp_inr=100.0, nutrition=nutrition, platform_prices=[0.0, -10.0, None])
    assert metrics.best_price_inr is None
    assert metrics.best_cost_per_g_protein is None
