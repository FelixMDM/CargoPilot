"use client";
import React from "react";
import { useState, useEffect } from "react";
import Containers from "../containers/containersLoadUnload";

type Matrix = string[][]
type Move = [number, number, number]

const Steps = () => {
  const [grid, setGrid] = useState<Matrix[]>([Array(8).fill(Array(12).fill("UNUSED"))]);
  const [moves, setMovesFelix] = useState<Move[]>(Array(2).fill(Array(3).fill(0)));
  const [currentIndex, setCurrentIndex] = useState(0);
  const [currentMoveIndex, setCurrentMoveIndex] = useState(0);

  useEffect(() => {
    try {
      fetch("http://localhost:8080/getLUSteps", {
        method: "GET",
    }).then((response) => response.json()).then((data) => {
      setGrid(data[0].steps);
      setMovesFelix(data[1].moves);

      // if you need to know what's receieved from this request, look here first
      console.log("haiiiiiiiii");
      console.log(data);
      console.log(data[0]);
      console.log(data[1]);
      console.log("steps: ", data[0].steps);
      console.log("moves", data[1].moves);
    });
    } catch (error) {
      console.error("Full error details:", error);
      alert("There was an error retrieving the steps for load/unload");
    }
  }, []);
  const movesX = [
    [
      ["NAN", "Cat", "Dog", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "NAN"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
    ],
    [
      ["NAN", "Cat", "Dog", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "NAN"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
    ],
    [
      ["NAN", "Cat", "Dog", "UNUSED", "Dog", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "NAN"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
    ],
    [
      ["NAN", "Cat", "UNUSED", "UNUSED", "Dog", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "NAN"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
      ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
    ],
  ];

  const path = [[4, 0, -1], [2, 0, -2]]; // Path with cell coordinates and actions

  const [currentMove, setCurrentMove] = useState(0);
  const [highlightedCell, setHighlightedCell] = useState<{ row: number; col: number; bgColor: string } | undefined>(undefined);
  const [showComplete, setShowComplete] = useState(false);

  const [askLoadInfo, setAskLoadInfo] = useState(false);
  const [containerName, setContainerName] = useState("");
  const [containerWeight, setContainerWeight] = useState(0);
  
  useEffect(() => {
    if (currentMove === moves.length - 1) {
      setHighlightedCell(undefined);
    } 
    else if (currentMove > 0) { 
      const row = path[currentMove - 1]?.[1] ?? 0;
      const col = path[currentMove - 1]?.[0] ?? 0;
      const action = path[currentMove - 1]?.[2] || 0;
      
      const bgColor = action === -1 ? "green" : action === -2 ? "red" : "";
      
      setHighlightedCell({ row, col, bgColor });

      if (action === -1) {
        setAskLoadInfo(true); // Show modal if action = -1 (load)
      }

    }
  }, [currentMove]);
  
  
  const handlePrev = () => {
    if (currentMove > 0) {
      setCurrentMove((prevMove) => prevMove - 1);
      setAskLoadInfo(false);
  
      if (currentMove - 1 > 0) {
        const pathIndex = currentMove - 2; // Map step to path index
        const [row, col, action] = path[pathIndex];
        const bgColor = action === -1 ? "green" : action === -2 ? "red" : "";
        setHighlightedCell({ row, col, bgColor });
      } else {
        setHighlightedCell(undefined);
      }
    }
  };
  
  
  const handleNext = () => {
    if (currentMove < moves.length - 1) {
      setCurrentMove((prevMove) => prevMove + 1);
  
      if (currentMove + 1 > 0 && currentMove + 1 < moves.length - 1) {
        const pathIndex = currentMove; // Map step to path index
        const [row, col, action] = path[pathIndex];
        const bgColor = action === -1 ? "green" : action === -2 ? "red" : "";
        setHighlightedCell({ row, col, bgColor });
      } else if (currentMove + 1 === moves.length - 1) {
        setHighlightedCell(undefined);
      }
    } else if (currentMove === moves.length - 1) {
      setShowComplete(true);
    }
    setAskLoadInfo(false);
  };

  const handleAskLoadInfoSubmit = () => {
    console.log(`Container Name: ${containerName}, Weight: ${containerWeight}`);
    setAskLoadInfo(false); // Close the modal after submission
    setContainerName("");
    setContainerWeight(0);
  }
  

  return (
    <div className="flex flex-col items-center">
      <div className="w-full bg-blue-100 text-blue-900 text-center py-4 font-bold text-xl">
        STEPS: {currentMove}/{moves.length - 1}
      </div>

      <div className="flex flex-row mt-[5%] justify-evenly">
        <div className="flex flex-col w-[10%] space-y-[15%] items-center">
          <button
            style={{ width: "100px", marginRight: "47%" }}
            className="w-[100%] h-[10%] mt-[15%] bg-blue-600 rounded-md font-bold text-white"
            onClick={handlePrev}
            disabled={currentMove === 0}
          >
            PREV
          </button>
        </div>

        <Containers
          selectable={false}
          grid={grid}
          currentMove={currentMove}
          highlightedCell={highlightedCell} // Pass the highlighted cell prop
        />

        <div className="flex flex-col w-[10%] space-y-[15%] items-center">
          <button
            style={{ width: "100px", marginLeft: "47%" }}
            className="w-[100%] h-[10%] mt-[15%] bg-blue-600 rounded-md font-bold text-white"
            onClick={handleNext}
            disabled={currentMove === moves.length - 1}
          >
            NEXT
          </button>
        </div>
      </div>
      {/* Modal */}
      
      {askLoadInfo && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
          <div className="bg-white rounded-lg p-6 w-[30%]">
            <h2 className="text-lg font-bold mb-4">Load Container</h2>
            <div className="mb-4">
              <label className="block text-sm font-bold mb-2">Container Name:</label>
              <input
                type="text"
                className="w-full border rounded-lg p-2"
                value={containerName}
                onChange={(e) => setContainerName(e.target.value)}
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-bold mb-2">Container Weight:</label>
              <input
                type="text"
                className="w-full border rounded-lg p-2"
                value={containerWeight}
                onChange={(e) => setContainerWeight(Number(e.target.value))}
              />
            </div>
            <div className="flex justify-end space-x-4">
              <button
                className="bg-gray-500 text-white rounded-md px-4 py-2"
                onClick={() => setAskLoadInfo(false)}
              >
                Cancel
              </button>
              <button
                className="bg-blue-600 text-white rounded-md px-4 py-2"
                onClick={handleAskLoadInfoSubmit}
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Steps;

