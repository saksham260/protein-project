"""Domain models and Pydantic schemas for The Protein Discovery Engine ETL."""

from __future__ import annotations
import re
from typing import Literal, Optional
from pydantic import BaseModel, Field, model_validator


def slugify(text: str) -> str:
    """Generate a clean URL-friendly slug from arbitrary text."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


class NutritionPerPack(BaseModel):
    """Nutritional values for a single packaged product or labeled serving."""
    calories_kcal: float = Field(ge=0, description="Calories in kcal per pack")
    protein_g: float = Field(ge=0, description="Protein in grams per pack")
    total_fat_g: float = Field(ge=0, description="Total fat in grams per pack")
    saturated_fat_g: float = Field(default=0.0, ge=0)
    trans_fat_g: float = Field(default=0.0, ge=0)
    cholesterol_mg: float = Field(default=0.0, ge=0)
    total_carbs_g: float = Field(ge=0, description="Total carbohydrates in grams per pack")
    dietary_fiber_g: float = Field(default=0.0, ge=0)
    total_sugars_g: float = Field(default=0.0, ge=0)
    added_sugars_g: float = Field(default=0.0, ge=0)
    sodium_mg: float = Field(default=0.0, ge=0)
    non_glycemic_polyols_g: float = Field(default=0.0, ge=0, description="Erythritol, allulose, etc.")
    additional_nutrients: dict = Field(default_factory=dict, description="Vitamins, minerals, BCAAs")


class RedFlagItem(BaseModel):
    """An identified nutritional or ingredient red flag."""
    flag_type: str
    flag_severity: Literal["high", "amber", "info"]
    flag_label: str
    flag_description: str
    matched_ingredient: Optional[str] = None
    ins_number: Optional[str] = None


class ProteinProfile(BaseModel):
    """Protein quality classification derived from the ingredient deck."""
    primary_protein_source: Optional[str] = None
    protein_tier: Optional[str] = None
    has_added_free_form_aminos: bool = False


class ComputedMetrics(BaseModel):
    """Derived efficiency and nutritional metrics calculated from raw inputs."""
    cost_per_g_protein: Optional[float] = None
    protein_density_pct: Optional[float] = None
    true_net_carbs_g: Optional[float] = None


class RedirectLinkItem(BaseModel):
    """Outbound purchase destination link."""
    platform: Literal["amazon", "blinkit", "zepto", "instamart", "d2c"]
    url: str
    platform_price_inr: Optional[float] = None


class VariantCreate(BaseModel):
    """Product variant data model for creation and ETL upsert."""
    variant_name: str
    slug: Optional[str] = None
    sku: Optional[str] = None
    barcode_ean: Optional[str] = None
    mrp_inr: float = Field(gt=0, description="Maximum retail price in INR")
    net_weight_g: float = Field(gt=0, description="Net pack weight in grams")
    serving_size_g: float = Field(gt=0, description="Single serving weight in grams")
    servings_per_pack: int = Field(default=1, ge=1)
    serving_size_label: Optional[str] = None
    nutrition: NutritionPerPack
    ingredient_list: list[str] = Field(default_factory=list, description="Normalized lowercase tokens")
    ingredient_deck_raw: list[dict] = Field(default_factory=list, description="Raw parsed structures")
    allergens: list[str] = Field(default_factory=list)
    dietary_tags: list[str] = Field(default_factory=list)
    image_url: Optional[str] = None
    redirect_links: list[RedirectLinkItem] = Field(default_factory=list)
    computed_metrics: Optional[ComputedMetrics] = None
    red_flags: list[RedFlagItem] = Field(default_factory=list)
    protein_profile: Optional[ProteinProfile] = None

    @model_validator(mode="after")
    def populate_slug_if_missing(self) -> VariantCreate:
        if not self.slug:
            self.slug = slugify(self.variant_name)
        return self


class ProductCreate(BaseModel):
    """Parent product representation containing 1 or more variants."""
    name: str
    brand_name: str
    category_slug: str
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    variants: list[VariantCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def populate_slug_if_missing(self) -> ProductCreate:
        if not self.slug:
            self.slug = slugify(f"{self.brand_name}-{self.name}")
        return self
