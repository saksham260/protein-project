"use client";

import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { Product, ProductVariant } from "@/types/product";
import { fetchCatalog } from "@/lib/catalogClient";
import { getPreferredDefaultVariantIndex } from "@/lib/utils";

export interface CartItem {
  /** The variant id, or the product id for the rare product with no variant. Each pack size is its own item. */
  key: string;
  productId: string;
  variantId?: string;
  product: Product;
  variant?: ProductVariant;
  addedAt: number;
}

interface CartContextType {
  items: CartItem[];
  itemCount: number;
  isCartOpen: boolean;
  openCart: () => void;
  closeCart: () => void;
  toggleCart: () => void;
  addItem: (product: Product, variant?: ProductVariant) => void;
  removeItem: (productId: string, variantId?: string) => void;
  isInCart: (productId: string, variantId?: string) => boolean;
  clearCart: () => void;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

const CART_STORAGE_KEY = "protein-engine-cart";

function itemKey(productId: string, variantId?: string): string {
  return variantId ?? productId;
}

/** Saved carts hold a copy of the product, so swap in today's prices and links. */
function withFreshData(items: CartItem[], catalog: Product[]): CartItem[] {
  return items.map((item) => {
    const product = catalog.find((p) => p.id === item.productId);
    if (!product) return item;
    const variant = product.variants?.find((v) => v.id === item.variantId) ?? item.variant;
    return { ...item, product, variant };
  });
}

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [items, setItems] = useState<CartItem[]>([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem(CART_STORAGE_KEY);
      const parsed: unknown = saved ? JSON.parse(saved) : null;
      if (Array.isArray(parsed) && parsed.length > 0) {
        const restored = (parsed as CartItem[]).map((item) => ({
          ...item,
          key: item.key ?? itemKey(item.productId, item.variantId),
        }));
        // eslint-disable-next-line react-hooks/set-state-in-effect -- localStorage isn't readable during server render
        setItems(restored);
      }
    } catch (e) {
      console.error("Failed to load cart from localStorage", e);
    } finally {
      setIsInitialized(true);
    }
  }, []);

  // Save to localStorage on change
  useEffect(() => {
    if (!isInitialized) return;
    try {
      localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items));
    } catch (e) {
      console.error("Failed to save cart to localStorage", e);
    }
  }, [items, isInitialized]);

  // The catalog is only worth downloading once someone actually looks at their cart.
  useEffect(() => {
    if (!isCartOpen) return;
    fetchCatalog()
      .then((catalog) => setItems((current) => withFreshData(current, catalog)))
      .catch(() => {
        // Keep the saved copy; the product pages still show current details.
      });
  }, [isCartOpen]);

  const openCart = useCallback(() => setIsCartOpen(true), []);
  const closeCart = useCallback(() => setIsCartOpen(false), []);
  const toggleCart = useCallback(() => setIsCartOpen((prev) => !prev), []);

  const addItem = useCallback((product: Product, variant?: ProductVariant) => {
    setItems((prev) => {
      const effectiveVariant =
        variant ||
        (product.variants &&
          (product.variants[getPreferredDefaultVariantIndex(product.variants)] ||
            product.variants[0]));
      const key = itemKey(product.id, effectiveVariant?.id);
      if (prev.some((item) => item.key === key)) return prev;
      return [
        ...prev,
        {
          key,
          productId: product.id,
          variantId: effectiveVariant?.id,
          product,
          variant: effectiveVariant,
          addedAt: Date.now(),
        },
      ];
    });
  }, []);

  const removeItem = useCallback((productId: string, variantId?: string) => {
    const key = itemKey(productId, variantId);
    setItems((prev) => prev.filter((item) => item.key !== key));
  }, []);

  const isInCart = useCallback(
    (productId: string, variantId?: string) => {
      const key = itemKey(productId, variantId);
      return items.some((item) => item.key === key);
    },
    [items]
  );

  const clearCart = useCallback(() => {
    setItems([]);
  }, []);

  return (
    <CartContext.Provider
      value={{
        items,
        itemCount: items.length,
        isCartOpen,
        openCart,
        closeCart,
        toggleCart,
        addItem,
        removeItem,
        isInCart,
        clearCart,
      }}
    >
      {children}
    </CartContext.Provider>
  );
};

export const useCart = (): CartContextType => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
};
