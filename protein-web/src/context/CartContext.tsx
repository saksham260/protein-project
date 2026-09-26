"use client";

import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { Product, ProductVariant } from "@/types/product";

export interface CartItem {
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
  removeItem: (productId: string) => void;
  toggleItem: (product: Product, variant?: ProductVariant) => void;
  isInCart: (productId: string) => boolean;
  clearCart: () => void;
  syncToAccount: () => Promise<void>;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

const CART_STORAGE_KEY = "protein-engine-cart";

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [items, setItems] = useState<CartItem[]>([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem(CART_STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed)) {
          setItems(parsed);
        }
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

  const openCart = useCallback(() => setIsCartOpen(true), []);
  const closeCart = useCallback(() => setIsCartOpen(false), []);
  const toggleCart = useCallback(() => setIsCartOpen((prev) => !prev), []);

  const addItem = useCallback((product: Product, variant?: ProductVariant) => {
    setItems((prev) => {
      const existing = prev.find((item) => item.productId === product.id);
      if (existing) return prev;
      const effectiveVariant = variant || (product.variants && product.variants[0]);
      return [
        ...prev,
        {
          productId: product.id,
          variantId: effectiveVariant?.id,
          product,
          variant: effectiveVariant,
          addedAt: Date.now(),
        },
      ];
    });
  }, []);

  const removeItem = useCallback((productId: string) => {
    setItems((prev) => prev.filter((item) => item.productId !== productId));
  }, []);

  const isInCart = useCallback(
    (productId: string) => {
      return items.some((item) => item.productId === productId);
    },
    [items]
  );

  const toggleItem = useCallback(
    (product: Product, variant?: ProductVariant) => {
      setItems((prev) => {
        const exists = prev.some((item) => item.productId === product.id);
        if (exists) {
          return prev.filter((item) => item.productId !== product.id);
        }
        const effectiveVariant = variant || (product.variants && product.variants[0]);
        return [
          ...prev,
          {
            productId: product.id,
            variantId: effectiveVariant?.id,
            product,
            variant: effectiveVariant,
            addedAt: Date.now(),
          },
        ];
      });
    },
    []
  );

  const clearCart = useCallback(() => {
    setItems([]);
  }, []);

  const syncToAccount = useCallback(async () => {
    // Stub for future cloud/auth sync
    console.log("Syncing cart to account (stub)...", items);
  }, [items]);

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
        toggleItem,
        isInCart,
        clearCart,
        syncToAccount,
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
