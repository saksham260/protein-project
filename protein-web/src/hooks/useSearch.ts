"use client";

import { useState, useEffect } from "react";
import { ProductWithVariants } from "@/types/product";
import { getProducts } from "@/lib/data";

export function useSearch(query: string, debounceMs = 300) {
  const [debouncedQuery, setDebouncedQuery] = useState(query);
  const [results, setResults] = useState<ProductWithVariants[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedQuery(query);
    }, debounceMs);

    return () => clearTimeout(handler);
  }, [query, debounceMs]);

  useEffect(() => {
    let isMounted = true;

    const timer = setTimeout(() => {
      if (!debouncedQuery.trim()) {
        setResults([]);
        setIsLoading(false);
        return;
      }

      setIsLoading(true);
      getProducts({ searchQuery: debouncedQuery })
        .then((data) => {
          if (isMounted) {
            setResults(data);
            setIsLoading(false);
          }
        })
        .catch(() => {
          if (isMounted) {
            setResults([]);
            setIsLoading(false);
          }
        });
    }, 0);

    return () => {
      isMounted = false;
      clearTimeout(timer);
    };
  }, [debouncedQuery]);

  return { results, isLoading, debouncedQuery };
}
