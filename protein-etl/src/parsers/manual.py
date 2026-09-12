"""Manual entry parser and ingredient deck tokenizer."""

from __future__ import annotations
import re
import questionary
try:
    from src.links import SEARCH_URL_TEMPLATES, build_search_url
    from src.models import NutritionPerPack, ProductCreate, VariantCreate, RedirectLinkItem
except (ImportError, ModuleNotFoundError):
    from links import SEARCH_URL_TEMPLATES, build_search_url
    from models import NutritionPerPack, ProductCreate, VariantCreate, RedirectLinkItem

NUMBER_PATTERN = r"^-?\d+(\.\d+)?$"


def parse_raw_ingredient_deck(raw_text: str) -> list[str]:
    """Tokenize an ingredient string into distinct ingredients while respecting parentheses.

    For example:
        'Whey Protein Isolate, Dark Chocolate (Cocoa Mass, Sugar, Cocoa Butter), Almonds, Sea Salt.'
    Becomes:
        ['Whey Protein Isolate', 'Dark Chocolate (Cocoa Mass, Sugar, Cocoa Butter)', 'Almonds', 'Sea Salt']
    """
    if not raw_text:
        return []

    cleaned = raw_text.strip().rstrip(".")
    tokens: list[str] = []
    current_token: list[str] = []
    paren_depth = 0

    for char in cleaned:
        if char in "([{":
            paren_depth += 1
            current_token.append(char)
        elif char in ")]}":
            if paren_depth > 0:
                paren_depth -= 1
            current_token.append(char)
        elif char in ",;\n" and paren_depth == 0:
            token_str = "".join(current_token).strip()
            if token_str:
                tokens.append(token_str)
            current_token = []
        else:
            current_token.append(char)

    last_token = "".join(current_token).strip()
    if last_token:
        tokens.append(last_token)

    # Clean leading bullet points or numbers (e.g. "1. Whey Isolate" -> "Whey Isolate")
    final_tokens = []
    for t in tokens:
        cleaned_t = re.sub(r"^[•\-\*\d\.\)]+\s*", "", t).strip()
        if cleaned_t:
            final_tokens.append(cleaned_t)

    return final_tokens


def prompt_float(prompt_text: str, default: float = 0.0) -> float:
    """Prompt user for a positive float value with fallback."""
    val = questionary.text(
        prompt_text,
        default=str(default),
        validate=lambda text: True if re.match(NUMBER_PATTERN, text.strip()) else "Please enter a valid number",
    ).ask()
    return float(val.strip()) if val else default


def prompt_optional_float(prompt_text: str, default: float | None = None) -> float | None:
    """Prompt for a number that may be left blank."""
    val = questionary.text(
        prompt_text,
        default="" if default is None else str(default),
        validate=lambda text: True if not text.strip() or re.match(NUMBER_PATTERN, text.strip()) else "Please enter a number or leave blank",
    ).ask()
    return float(val.strip()) if val and val.strip() else None


def prompt_manual_entry(initial_data: dict | None = None) -> ProductCreate:
    """Run interactive CLI wizard prompting for complete product and nutrition facts."""
    data = initial_data or {}

    print("\n📦 Product Information")
    brand_name = questionary.text(
        "Brand name:",
        default=data.get("brand_name", "The Whole Truth"),
    ).ask()

    product_name = questionary.text(
        "Product name:",
        default=data.get("title", "Double Cocoa Protein Bar"),
    ).ask()

    categories = [
        "protein-bars",
        "protein-powders",
        "rtd-drinks",
        "savory-snacks",
    ]
    category_slug = questionary.select(
        "Select Category:",
        choices=categories,
        default=data.get("category_slug", "protein-bars"),
    ).ask()

    description = questionary.text(
        "Product description (optional):",
        default=data.get("description", ""),
    ).ask()

    print("\n⚖️ Variant & Pricing Details")
    default_variant = data.get("variants", [{}])[0] if data.get("variants") else {}
    variant_name = questionary.text(
        "Variant / Flavor name:",
        default=default_variant.get("variant_name", "Standard / Single Pack"),
    ).ask()

    mrp_inr = prompt_float(
        "MRP in INR (₹) — the printed label price:",
        default=default_variant.get("mrp_inr") or 150.0,
    )

    if default_variant.get("weight_source") == "shipping":
        print("⚠️  Shopify only gave a shipping weight for this variant — check the net weight on the pack.")
    net_weight_g = prompt_float(
        "Net pack weight in grams (g):",
        default=default_variant.get("weight_g") or 52.0,
    )

    serving_size_g = prompt_float(
        "Serving size in grams (g) — same as pack weight for single bars/bottles:",
        default=net_weight_g,
    )

    servings_per_pack = int(prompt_float(
        "Servings per pack:",
        default=max(1, round(net_weight_g / serving_size_g)) if serving_size_g > 0 else 1,
    ))

    print(f"\n🥗 Nutrition Facts (per serving of {serving_size_g:g}g)")
    calories_kcal = prompt_float("Calories (kcal):", 212.0)
    protein_g = prompt_float("Protein (g):", 20.0)
    total_fat_g = prompt_float("Total Fat (g):", 8.0)
    saturated_fat_g = prompt_float("Saturated Fat (g):", 2.5)
    trans_fat_g = prompt_float("Trans Fat (g):", 0.0)
    cholesterol_mg = prompt_float("Cholesterol (mg):", 5.0)
    total_carbs_g = prompt_float("Total Carbohydrates (g):", 20.0)
    dietary_fiber_g = prompt_float("Dietary Fiber (g):", 6.0)
    total_sugars_g = prompt_float("Total Sugars (g):", 3.0)
    added_sugars_g = prompt_float("Added Sugars (g):", 0.0)
    sodium_mg = prompt_float("Sodium (mg):", 95.0)
    polyols_g = prompt_float("Non-glycemic Polyols (g):", 0.0)

    nutrition = NutritionPerPack(
        calories_kcal=calories_kcal,
        protein_g=protein_g,
        total_fat_g=total_fat_g,
        saturated_fat_g=saturated_fat_g,
        trans_fat_g=trans_fat_g,
        cholesterol_mg=cholesterol_mg,
        total_carbs_g=total_carbs_g,
        dietary_fiber_g=dietary_fiber_g,
        total_sugars_g=total_sugars_g,
        added_sugars_g=added_sugars_g,
        sodium_mg=sodium_mg,
        non_glycemic_polyols_g=polyols_g,
    )

    print("\n📜 Ingredient Deck")
    ingredient_paste = questionary.text(
        "Paste the raw ingredient list from the pack:",
        default="Whey Protein Isolate, Raw Almonds, Chicory Root Fiber, Cocoa Butter, Dark Chocolate (Cocoa Mass), Stevia Leaf Extract",
    ).ask()

    ingredient_list = parse_raw_ingredient_deck(ingredient_paste)

    allergens_input = questionary.text(
        "Allergens (comma-separated, e.g. milk, nuts, soy):",
        default="milk, tree nuts",
    ).ask()
    allergens = [a.strip().lower() for a in allergens_input.split(",") if a.strip()]

    dietary_tags_input = questionary.text(
        "Dietary tags (comma-separated, e.g. Gluten-Free, No Added Sugar, Vegetarian):",
        default="Gluten-Free, No Added Sugar, Vegetarian",
    ).ask()
    dietary_tags = [t.strip() for t in dietary_tags_input.split(",") if t.strip()]

    print("\n🔗 Redirect & Purchase Links")
    redirect_links = []

    amazon_url = questionary.text("Amazon product URL (optional):").ask()
    if amazon_url and amazon_url.strip():
        amazon_price = prompt_optional_float("Amazon selling price in ₹ (blank if unknown):")
        redirect_links.append(RedirectLinkItem(platform="amazon", url=amazon_url.strip(), platform_price_inr=amazon_price))

    d2c_url = questionary.text("D2C / Brand Website URL (optional):", default=data.get("url", "")).ask()
    if d2c_url and d2c_url.strip():
        d2c_price = prompt_optional_float(
            "Brand website selling price in ₹ (blank if unknown):",
            default=default_variant.get("price_inr"),
        )
        redirect_links.append(RedirectLinkItem(platform="d2c", url=d2c_url.strip(), platform_price_inr=d2c_price))

    if questionary.confirm(
        "Add Amazon / Blinkit / Zepto / Instamart search links for platforms without a product URL?",
        default=True,
    ).ask():
        linked_platforms = {link.platform for link in redirect_links}
        query = f"{brand_name} {product_name}"
        for platform in SEARCH_URL_TEMPLATES:
            if platform not in linked_platforms:
                redirect_links.append(RedirectLinkItem(platform=platform, url=build_search_url(platform, query)))

    variant = VariantCreate(
        variant_name=variant_name,
        sku=default_variant.get("sku"),
        barcode_ean=default_variant.get("barcode"),
        mrp_inr=mrp_inr,
        net_weight_g=net_weight_g,
        serving_size_g=serving_size_g,
        servings_per_pack=servings_per_pack,
        nutrition=nutrition,
        ingredient_list=ingredient_list,
        ingredient_deck_raw=[{"name": ing} for ing in ingredient_list],
        allergens=allergens,
        dietary_tags=dietary_tags,
        redirect_links=redirect_links,
    )

    return ProductCreate(
        name=product_name,
        brand_name=brand_name,
        category_slug=category_slug,
        description=description,
        image_url=(data.get("images") or [None])[0],
        variants=[variant],
    )
