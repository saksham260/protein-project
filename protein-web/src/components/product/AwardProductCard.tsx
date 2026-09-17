import React from "react";
import { ProductWithVariants } from "@/types/product";
import { AwardCategory } from "@/lib/topPicksConfig";
import { ProductCard } from "@/components/product/ProductCard";

export interface AwardProductCardProps {
  product: ProductWithVariants;
  award: AwardCategory;
  editorialBlurb?: string;
}

export const AwardProductCard: React.FC<AwardProductCardProps> = ({
  product,
  award,
}) => {
  return (
    <div className="group relative flex flex-col h-full">
      {/* Card Wrapper with Dynamic Glow Ring */}
      <div
        className="relative flex-1 rounded-2xl transition-all duration-300 group-hover:scale-[1.01]"
        style={{
          boxShadow: `0 0 0 1.5px ${award.glowColor}55, 0 0 28px ${award.glowColor}25, 0 12px 32px rgba(0,0,0,0.7)`,
        }}
      >
        <ProductCard product={product} />
      </div>
    </div>
  );
};
