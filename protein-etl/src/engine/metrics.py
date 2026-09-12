"""Calculated Metrics Engine for The Protein Discovery Engine.

Label nutrition is per serving, so pack-level metrics first scale protein up to the whole pack.

Formulas:
- Protein per Pack (g): protein_g * net_weight_g / serving_size_g
- Cost per Gram of Protein (₹/g): mrp_inr / protein_per_pack
- Best Cost per Gram (₹/g): lowest known platform price / protein_per_pack
- Protein Density (%): (protein_g * 4) / calories_kcal * 100
- True Net Carbs (g): total_carbs_g - dietary_fiber_g - non_glycemic_polyols_g
"""

from typing import Optional

try:
    from src.models import ComputedMetrics, NutritionPerPack
except (ImportError, ModuleNotFoundError):
    from models import ComputedMetrics, NutritionPerPack


def calculate_protein_per_pack(
    protein_g: float,
    net_weight_g: Optional[float] = None,
    serving_size_g: Optional[float] = None,
) -> Optional[float]:
    """Total grams of protein in the whole pack.

    Args:
        protein_g: Grams of protein per labelled serving.
        net_weight_g: Net pack weight in grams. Omit for single-serve items.
        serving_size_g: Labelled serving size in grams. Omit for single-serve items.

    Returns:
        Unrounded protein per pack, or None if protein_g is missing or negative.
    """
    if protein_g is None or protein_g < 0:
        return None
    if not net_weight_g or not serving_size_g or net_weight_g <= 0 or serving_size_g <= 0:
        return float(protein_g)
    return float(protein_g) * float(net_weight_g) / float(serving_size_g)


def calculate_cost_per_g_protein(mrp_inr: float, protein_g: float) -> Optional[float]:
    """Calculate the economic efficiency metric (₹ per gram of protein).

    Args:
        mrp_inr: Price in Indian Rupees for the whole pack.
        protein_g: Grams of protein in the whole pack.

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
        protein_g: Grams of protein per serving.
        calories_kcal: Total calories in kcal per serving.

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


def compute_all_metrics(
    mrp_inr: float,
    nutrition: NutritionPerPack,
    net_weight_g: Optional[float] = None,
    serving_size_g: Optional[float] = None,
    platform_prices: Optional[list[Optional[float]]] = None,
) -> ComputedMetrics:
    """Run all metric calculations for a given product price and nutrition panel.

    Args:
        mrp_inr: Printed MRP for the whole pack.
        nutrition: Per-serving nutrition label values.
        net_weight_g / serving_size_g: Used to scale per-serving protein to the whole pack.
        platform_prices: Known selling prices (Amazon, D2C, ...); None entries are ignored.
    """
    protein_per_pack = calculate_protein_per_pack(nutrition.protein_g, net_weight_g, serving_size_g)
    cost_per_g = calculate_cost_per_g_protein(mrp_inr, protein_per_pack)

    known_prices = [p for p in (platform_prices or []) if p is not None and p > 0]
    best_price = min(known_prices) if known_prices else None
    best_cost_per_g = (
        calculate_cost_per_g_protein(best_price, protein_per_pack) if best_price is not None else None
    )

    density = calculate_protein_density(nutrition.protein_g, nutrition.calories_kcal)
    net_carbs = calculate_true_net_carbs(
        nutrition.total_carbs_g,
        nutrition.dietary_fiber_g,
        nutrition.non_glycemic_polyols_g,
    )
    return ComputedMetrics(
        cost_per_g_protein=cost_per_g,
        best_price_inr=best_price,
        best_cost_per_g_protein=best_cost_per_g,
        protein_density_pct=density,
        true_net_carbs_g=net_carbs,
    )
