"use client";
import React, { createContext, useContext, useState } from "react";

// Create Context for selectedCellsId
const SelectedCellsContext = createContext<{
  selectedCellsId: Set<string>;
  setSelectedCellsId: React.Dispatch<React.SetStateAction<Set<string>>>;
} | null>(null);

// Provider Component
export const SelectedCellsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [selectedCellsId, setSelectedCellsId] = useState<Set<string>>(new Set());

  return (
    <SelectedCellsContext.Provider value={{ selectedCellsId, setSelectedCellsId }}>
      {children}
    </SelectedCellsContext.Provider>
  );
};

// Hook for consuming the context
export const useSelectedCells = () => {
  const context = useContext(SelectedCellsContext);
  if (!context) {
    throw new Error("useSelectedCells must be used within a SelectedCellsProvider");
  }
  return context;
};
