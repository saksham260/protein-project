import json
from pathlib import Path

REPO = Path("c:/Users/Saksham/Documents/new-project")
with open(REPO / "protein-etl/data/seed_products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

print(f"Auditing prices across {len(products)} products...")

zero_prices = []
mrp_less_than_price = []
cost_per_g_anomalies = []
valid_prices = 0

for p in products:
    for v in p.get("variants", []):
        mrp = v.get("mrp_inr")
        metrics = v.get("computed_metrics") or {}
        cost_per_g = metrics.get("cost_per_g_protein")
        best_price = metrics.get("best_price_inr")
        
        name = f"{p.get('name')} [{v.get('variant_name')}]"
        
        if not mrp or mrp <= 0:
            zero_prices.append((name, f"Invalid MRP: {mrp}"))
        else:
            valid_prices += 1
            
        if best_price and mrp and best_price > mrp * 1.05:
            mrp_less_than_price.append((name, f"Best price {best_price} > MRP {mrp}"))
            
        if cost_per_g is not None:
            if cost_per_g <= 0.2:
                cost_per_g_anomalies.append((name, f"Suspiciously low cost/g: ₹{cost_per_g}/g"))
            elif cost_per_g > 30.0:
                cost_per_g_anomalies.append((name, f"High cost/g: ₹{cost_per_g}/g"))

print("\n=== Pricing & Cost-Per-Gram Audit ===")
print(f"Valid Priced Variants:       {valid_prices}")
print(f"Zero / Null MRPs:            {len(zero_prices)}")
print(f"Price > MRP Inconsistencies: {len(mrp_less_than_price)}")
print(f"Cost/g Protein Outliers:     {len(cost_per_g_anomalies)}")

if zero_prices:
    print("\nZero/Null MRPs:")
    for item in zero_prices[:10]:
        print(" ", item[0], item[1])

if mrp_less_than_price:
    print("\nPrice > MRP:")
    for item in mrp_less_than_price[:10]:
        print(" ", item[0], item[1])

if cost_per_g_anomalies:
    print("\nCost/g Outliers (sample):")
    for item in cost_per_g_anomalies[:10]:
        print(" ", item[0], item[1])
