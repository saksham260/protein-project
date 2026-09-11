"""Calculated Metrics Engine for The Protein Discovery Engine.

Formulas:
- Cost per Gram of Protein (₹/g): mrp_inr / protein_g
- Protein Density (%): (protein_g * 4) / calories_kcal * 100
- True Net Carbs (g): total_carbs_g - dietary_fiber_g - non_glycemic_polyols_g
"""

from typing import Optional
from src.models import ComputedMetrics, NutritionPerPack


def calculate_cost_per_g_protein(mrp_inr: float, protein_g: float) -> Optional[float]:
    """Calculate the economic efficiency metric (₹ per gram of protein).

    Args:
        mrp_inr: Maximum retail price in Indian Rupees.
        protein_g: Grams of protein per pack.

    Returns:
        Rounded float to 2 decimals, or None if protein_g <= 0 or mrp_inr < 0.
    """
    if protein_g is None or protein_g <= 0 or mrp_inr is None or mrp_inr < 0:
        return None
    return round(float(mrp_inr) / float(protein_g), 2)


def calculate_protein_density(protein_g: float, calories_kcal: float) -> Optional[float]:
    """Calculate protein density as percentage of total calories derived from protein.

    Each gram of protein provides 4 kcal of metabolic energy.

    Args:
        protein_g: Grams of protein per pack.
        calories_kcal: Total calories in kcal per pack.

    Returns:
        Percentage (0-100) rounded to 2 decimals, or None if calories_kcal <= 0.
    """
    if calories_kcal is None or calories_kcal <= 0 or protein_g is None or protein_g < 0:
        return None
    density = (float(protein_g) * 4.0 / float(calories_kcal)) * 100.0
    return round(density, 2)


def calculate_true_net_carbs(
    total_carbs_g: float,
    dietary_fiber_g: float = 0.0,
    polyols_g: float = 0.0,
) -> float:
    """Calculate true net carbs subtracting dietary fiber and non-glycemic polyols.

    Args:
        total_carbs_g: Total carbohydrates labeled in grams.
        dietary_fiber_g: Dietary fiber in grams.
        polyols_g: Non-glycemic sugar alcohols (e.g. erythritol, allulose) in grams.

    Returns:
        Net carbs in grams rounded to 2 decimals, minimum 0.0.
    """
    carbs = float(total_carbs_g or 0.0)
    fiber = float(dietary_fiber_g or 0.0)
    polyols = float(polyols_g or 0.0)
    net_carbs = max(0.0, carbs - fiber - polyols)
    return round(net_carbs, 2)


def compute_all_metrics(mrp_inr: float, nutrition: NutritionPerPack) -> ComputedMetrics:
    """Run all metric calculations for a given product price and nutrition panel."""
    cost_per_g = calculate_cost_per_g_protein(mrp_inr, nutrition.protein_g)
    density = calculate_protein_density(nutrition.protein_g, nutrition.calories_kcal)
    net_carbs = calculate_true_net_carbs(
        nutrition.total_carbs_g,
        nutrition.dietary_fiber_g,
        nutrition.non_glycemic_polyols_g,
    )
    return ComputedMetrics(
        cost_per_g_protein=cost_per_g,
        protein_density_pct=density,
        true_net_carbs_g=net_carbs,
    )
