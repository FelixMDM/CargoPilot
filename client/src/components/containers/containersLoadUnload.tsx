"use client";
import React from "react";
import { useSelectedCells } from "../loadUnload/SelectedCellsContext";
import numberToString from "../loadUnload/numToString";

const Containers = () => {
  const { selectedCells, setSelectedCells } = useSelectedCells();

  // Function to handle cell selection
  const handleCellClick = (row: number, col: number, index: number) => {
    const cellId = `${index}, (${row}, ${col})`; // Store index and (x, y) as a string

    setSelectedCells((prevSelectedCells) => {
      const newSelectedCells = new Set(prevSelectedCells);
      if (newSelectedCells.has(cellId)) {
        newSelectedCells.delete(cellId); // Remove if already selected (unselect)
      } else {
        newSelectedCells.add(cellId); // Add if not selected (select)
      }
      return newSelectedCells;
    });
  };

  return (
    <div className="flex flex-col items-center">
      <div className="grid grid-cols-12 grid-rows-8">
        {Array.from({ length: 96 }).map((_, index: number) => {
          const col = index % 12;
          const row = 7 - Math.floor(index / 12);

          const cellId = `${index}, (${row}, ${col})`;
          const isSelected = selectedCells.has(cellId);

          return (
            <button
              key={index}
              className={`cell m-auto p-2 border border-black ${isSelected ? "bg-green-500" : "bg-gray-300"}`}
              onClick={() => handleCellClick(row, col, index)}
            >
              {numberToString(index)}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default Containers;
