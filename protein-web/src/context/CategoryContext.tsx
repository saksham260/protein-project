"use client";

import React, { createContext, useContext, useState } from "react";

interface CategoryContextType {
  activeCategory: string;
  setActiveCategory: (cat: string) => void;
}

const CategoryContext = createContext<CategoryContextType>({
  activeCategory: "all",
  setActiveCategory: () => {},
});

export const CategoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [activeCategory, setActiveCategory] = useState<string>("all");

  return (
    <CategoryContext.Provider value={{ activeCategory, setActiveCategory }}>
      {children}
    </CategoryContext.Provider>
  );
};

export const useCategory = () => useContext(CategoryContext);
