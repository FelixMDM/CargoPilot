import React, { useState, useEffect } from "react";
import { useSelectedCells } from "../loadUnload/SelectedCellsContext";

interface ContainersProps {
  selectable?: boolean;
  grid: string[][][]; // Array of grids for each move
  currentMove: number; // Index of the current move
  highlightedCell?: { row: number; col: number; bgColor: string }; // prop for highlighted cell
  cellTitleOverride?: { row: number; col: number; title: string };
}

const Containers: React.FC<ContainersProps> = ({ selectable, grid, currentMove, highlightedCell, cellTitleOverride }) => {
  const { selectedCellsId, setSelectedCellsId } = useSelectedCells();
  const [gridNames, setGridNames] = useState<string[][]>([]);

  useEffect(() => {
    console.log('Current Move:', currentMove);
    console.log('Current Grid:', grid[currentMove]);
    if (grid && grid[currentMove]) {
      setGridNames(grid[currentMove]);
    }
  }, [grid, currentMove]);

  const handleCellClick = (row: number, col: number, index: number) => {
    if (!selectable) return;

    const cellId = `${index}, (${row}, ${col})`;

    setSelectedCellsId((prevSelectedIds) => {
      const newSelectedIds = new Set(prevSelectedIds);
      if (prevSelectedIds.has(cellId)) {
        newSelectedIds.delete(cellId);
      } else {
        newSelectedIds.add(cellId);
      }
      return newSelectedIds;
    });
  };

  return (
    <div className="flex flex-col items-center">
      <div className="grid grid-cols-12 grid-rows-8">
        {Array.from({ length: 96 }).map((_, index: number) => {
          const col = index % 12;
          const row = 7 - Math.floor(index / 12);

          const cellId = `${index}, (${row}, ${col})`;
          let cellTitle = gridNames[row]?.[col] || "UNUSED";
          if (
            cellTitleOverride &&
            cellTitleOverride.row === row &&
            cellTitleOverride.col === col
          ) {
            cellTitle = cellTitleOverride.title; // Override the title
          }

          const isSelected = selectedCellsId.has(cellId);

          // Determine background color for the cell
          let cellBgColor = "bg-gray-300"; // Default background color

          // Check if the current cell is the highlighted one and apply the bgColor (green or red)
          if (highlightedCell && highlightedCell.row === row && highlightedCell.col === col) {
            if (highlightedCell.bgColor === "green") {
              cellBgColor = "bg-green-500"; // Apply green background color
            } else if (highlightedCell.bgColor === "red") {
              cellBgColor = "bg-red-500"; // Apply red background color
            }
          } else if (selectable) {
            cellBgColor = isSelected ? "bg-green-500" : "bg-gray-300";
          }

          return (
            <button
              key={index}
              className={`cell m-auto p-2 border border-black ${cellBgColor}`}
              onClick={() => handleCellClick(row, col, index)}
              disabled={!selectable}
            >
              {cellTitle}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default Containers;
