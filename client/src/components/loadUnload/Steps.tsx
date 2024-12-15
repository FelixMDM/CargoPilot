"use client";
import React from "react";
import { useState, useEffect } from "react";
import Containers from "../containers/containersLoadUnload";

type Matrix = string[][]
type Move = [number, number, number, number]

const Steps = () => {
  const [grid, setGrid] = useState<Matrix[]>([Array(8).fill(Array(12).fill("UNUSED"))]);
  const [moves, setMoves] = useState<Move[]>(Array(2).fill(Array(4).fill(0)));

  useEffect(() => {
    try {
      fetch("http://localhost:8080/getLUSteps", {
        method: "GET",
    }).then((response) => response.json()).then((data) => {
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

  return (
    <div className="flex flex-col items-center">
      <div className="w-full bg-blue-100 text-blue-900 text-center py-4 font-bold text-xl">
        STEPS: 
      </div>

      <div className="flex flex-row mt-[5%] justify-evenly">
        <div className="flex flex-col w-[10%] space-y-[15%] items-center">
          <button
            style={{ width: "100px", marginRight: "47%" }}
            className="w-[100%] h-[10%] mt-[15%] bg-blue-600 rounded-md font-bold text-white"
          >
            PREV
          </button>
        </div>
        
        <Containers selectable={false}/>

        <div className="flex flex-col w-[10%] space-y-[15%] items-center">
          <button
            style={{ width: "100px", marginLeft: "47%" }}
            className="w-[100%] h-[10%] mt-[15%] bg-blue-600 rounded-md font-bold text-white"
          >
            NEXT
          </button>
        </div>
      </div>
    </div>
  );
};

export default Steps;
