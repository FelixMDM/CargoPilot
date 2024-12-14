"use client";
import React, { useEffect, useState } from "react";
import { useSelectedCells } from "../loadUnload/SelectedCellsContext";

interface ContainersProps {
  selectable?: boolean; }

const Containers: React.FC<ContainersProps> = ({ selectable }) => {
  //const { selectedCells, setSelectedCells } = useSelectedCells();
  const { selectedCellsId, setSelectedCellsId } = useSelectedCells(); // cell IDs to handle same name selections
  const [gridNames, setGridNames] = useState<string[][]>([]); //store container names 
  const [loading, setLoading] = useState<boolean>(true); 

  useEffect(() => { //get grid names from server endpoint
    const fetchGridNames = async () => {
      try {
        const response = await fetch("http://localhost:8080/getGridNames");
        const data = await response.json();

        console.log("Server Response:", data);
        if (data.gridNames) {
          setGridNames(data.gridNames);
        }
      } catch (error) {
        console.error("Error fetching grid names:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchGridNames();
  }, []);

  // Handle cell click
  const handleCellClick = (row: number, col: number, index: number) => {
    if (!selectable) return;

    const cellId = `${index}, (${row}, ${col})`; 
    const cellTitle = gridNames[row]?.[col] || "Loading..."; 

    setSelectedCellsId((prevSelectedIds) => {
      const newSelectedIds = new Set(prevSelectedIds);
      if (prevSelectedIds.has(cellId)) {
        newSelectedIds.delete(cellId);
      }
      else {
        newSelectedIds.add(cellId); // select the cell in the ID set
      }
      return newSelectedIds;
    });
  }

  return (
    <div className="flex flex-col items-center">
      <div className="grid grid-cols-12 grid-rows-8">
        {Array.from({ length: 96 }).map((_, index: number) => {
          const col = index % 12;
          const row = 7 - Math.floor(index / 12);

          const cellId = `${index}, (${row}, ${col})`;
          const cellTitle = gridNames[row]?.[col] || "Loading..."; // Use grid title if available
          const isSelected = selectedCellsId.has(cellId); // Check selection by ID

          const cellBgColor = selectable
            ? isSelected
              ? "bg-green-500" // Selected cells are green
              : "bg-gray-300" // Non-selected cells are gray
            : "bg-gray-300"; // Default for non-selectable

          return (
            <button
              key={index}
              className={`cell m-auto p-2 border border-black ${cellBgColor}`}
              onClick={() => handleCellClick(row, col, index)}
              disabled={!selectable} // Disable for non-selectable
            >
              {cellTitle} {/* Display the grid name */}
            </button>
          );
        })}
      </div>
      {loading && <p>Loading grid names...</p>} {/* Show loading message */}
    </div>
  );
};

export default Containers;
