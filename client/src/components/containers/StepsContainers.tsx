"use client";
import React from "react";
import numberToString from "../loadUnload/numToString";

const StepsContainers = () => {
  return (
    <div className="flex flex-col items-center">
      <div className="grid grid-cols-12 grid-rows-8">
        {Array.from({ length: 96 }).map((_, index: number) => {
          const col = index % 12;
          const row = 7 - Math.floor(index / 12);

          const cellTitle = `${numberToString(index)}`;

          return (
            <div
              key={index}
              className={`cell m-auto p-2 border border-black bg-gray-300 flex items-center justify-center`}
            >
              {cellTitle}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default StepsContainers;
