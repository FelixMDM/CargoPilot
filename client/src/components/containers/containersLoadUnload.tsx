"use client";
import { useState } from "react";

const Containers = () => {
  // State to store selected cell positions
  const [selectedCells, setSelectedCells] = useState<Set<string>>(new Set());

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
          // Calculate row and column for each cell
          const col = index % 12;
          const row = 7 - Math.floor(index / 12); // Reverse the row calculation to start from bottom (7 - index)

          const cellId = `${index}, (${row}, ${col})`; // Unique ID for each cell with index and (x, y)
          const isSelected = selectedCells.has(cellId); // Check if the cell is selected

          return (
            <button
              key={index}
              className={`cell m-auto p-2 border border-black ${isSelected ? 'bg-green-500' : 'bg-gray-300'}`}
              onClick={() => handleCellClick(row, col, index)} // Pass index to handle click
            >
              {index}
            </button>
          );
        })}
      </div>
      {selectedCells.size > 0 && (
        <div>
          <p>Selected Positions:</p>
          {Array.from(selectedCells).map((cellId) => {
            return <p key={cellId}>{cellId}</p>; // Display the stored cellId
          })}
        </div>
      )}
    </div>
  );
};

export default Containers;
