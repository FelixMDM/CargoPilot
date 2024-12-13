"use client";
import { useState } from "react";
import numberToString from "../loadUnload/numToString";

const Containers = () => {
  const [selectedCells, setSelectedCells] = useState<Set<string>>(new Set());

  // handle cell selection
  const handleCellClick = (row: number, col: number, index: number) => {
    const indexString = numberToString(index); // right now this just turns the index value to a string value for testing purposes, but should handle title names from manifest
    const cellId = `${indexString}, (${row}, ${col})`; 
    
    // the above line stores the cellId as a string, this will eventually be the title, i could have it just be the id number (index selected) and have that send instead. commented the line out so it sends the index #

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

          const indexString = numberToString(index); // Convert index to string representation
          const cellId = `${indexString}, (${row}, ${col})`; // Unique ID for each cell with string index

          const isSelected = selectedCells.has(cellId); // Check if the cell is selected

          return (
            <button
              key={index}
              className={`cell m-auto p-2 border border-black ${isSelected ? 'bg-green-500' : 'bg-gray-300'}`}
              onClick={() => handleCellClick(row, col, index)} // Pass index to handle click
            >
              {indexString}  {/* Display index as a word */}
            </button>
          );
        })}
      </div>

      {/* Display selected cells at the bottom */}
      {selectedCells.size > 0 && (
        <div className="mt-4">
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
