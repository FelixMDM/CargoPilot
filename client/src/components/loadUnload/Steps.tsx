"use client";
import React, { useState, useEffect } from "react";
import Containers from "../containers/containersLoadUnload";

const Steps = () => {
  const moves = [
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

  // Set highlighted cell based on the current move
  useEffect(() => {
    if (currentMove > 0) { // Only execute path logic after step 0
      const currentAction = moves[currentMove][0]; // First row of the current move
      const row = 0; // Assuming you want the first row
      const col = currentAction.findIndex(cell => cell !== "UNUSED" && cell !== "NAN");
      const action = path[currentMove][2]; // use the action from the path array
    
      const bgColor = action === -1 ? "green" : action === -2 ? "red" : "";
    
      setHighlightedCell({ row, col, bgColor });
    }
  }, [currentMove]);

  const handlePrev = () => {
    if (currentMove > 0) {
      setCurrentMove((prevMove) => prevMove - 1);
    }
  };

  const handleNext = () => {
    if (currentMove < moves.length - 1) {
      setCurrentMove((prevMove) => prevMove + 1);
    }
  };

  return (
    <div className="flex flex-col items-center">
      <div className="w-full bg-blue-100 text-blue-900 text-center py-4 font-bold text-xl">
        STEPS: {currentMove}/{moves.length - 1} {/* Show steps as 0/2, 1/2, 2/2 */}
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
          grid={moves}
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
    </div>
  );
};

export default Steps;
