"use client";
import React, { useState } from "react";
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

  const [currentMove, setCurrentMove] = useState(0);

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
        STEPS: {currentMove + 1}/{moves.length}
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

        <Containers selectable={false} grid={moves} currentMove={currentMove} />

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
