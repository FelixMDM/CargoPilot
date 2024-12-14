"use client";
import React, { createContext, useContext, useState } from "react";

// Define the context type
interface SelectedCellsContextType {
  selectedCells: Set<string>;
  setSelectedCells: React.Dispatch<React.SetStateAction<Set<string>>>;
  getSelectedCells: () => string[];
}

// create the context
const SelectedCellsContext = createContext<SelectedCellsContextType | undefined>(undefined);

// context provider component
export const SelectedCellsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [selectedCells, setSelectedCells] = useState<Set<string>>(new Set());

  const getSelectedCells = () => {
    return Array.from(selectedCells); // convert set to array
  };

  return (
    <SelectedCellsContext.Provider value={{ selectedCells, setSelectedCells, getSelectedCells }}>
      {children}
    </SelectedCellsContext.Provider>
  );
};

// custom hook to use the context
export const useSelectedCells = () => {
  const context = useContext(SelectedCellsContext);
  if (!context) {
    throw new Error("useSelectedCells must be used within a SelectedCellsProvider");
  }
  return context;
};