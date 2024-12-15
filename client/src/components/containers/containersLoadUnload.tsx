"use client";
import React, { useState, useEffect } from "react";
import { useSelectedCells } from "../loadUnload/SelectedCellsContext";

interface ContainersProps {
  selectable?: boolean;
  grid: string[][][]; // Array of grids for each move
  currentMove: number; // Index of the current move
}

const Containers: React.FC<ContainersProps> = ({ selectable, grid, currentMove }) => {
  const { selectedCellsId, setSelectedCellsId } = useSelectedCells();
  const [gridNames, setGridNames] = useState<string[][]>([]);

  useEffect(() => {
    if (grid && grid[currentMove]) {
      setGridNames(grid[currentMove]); // update the gridNames based on the current move
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
          const cellTitle = gridNames[row]?.[col] || "Loading...";
          const isSelected = selectedCellsId.has(cellId);

          const cellBgColor = selectable
            ? isSelected
              ? "bg-green-500"
              : "bg-gray-300"
            : "bg-gray-300";

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
