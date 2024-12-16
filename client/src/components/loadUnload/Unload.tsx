"use client";
import React from "react"; 
import { useState, useEffect } from "react";
import Containers from "../containers/containersLoadUnload";
import { useSelectedCells } from "./SelectedCellsContext";

type Matrix = string[][]
type Move = [number, number, number]
const Unload = ({ nextStepsPage }) => {

  const [moves, setGrid] = useState<Matrix[]>([Array(8).fill(Array(12).fill("UNUSED"))]);

  useEffect(() => {
    // const fetchSteps = async () => {
    //   try {
    //     fetch("http://localhost:8080/getLUSteps", {
    //       method: "GET",
    //   }).then((response) => response.json()).then((data) => {
    //     setGrid(data[0].steps);
  
    //     // if you need to know what's receieved from this request, look here first
    //     console.log("haiiiiiiiii");
    //     console.log(data);
    //     console.log(data[0]);
    //     console.log(data[1]);
    //     console.log("steps: ", data[0].steps);
    //   });
    //   } catch (error) {
    //     console.error("Full error details:", error);
    //     alert("There was an error retrieving the steps for load/unload");
    //   }
    // };
    // fetchSteps()
    try {
      fetch("http://localhost:8080/getLoadGrid", {
        method: "GET",
    }).then((response) => response.json()).then((data) => {
      setGrid(data[0].steps);

      // if you need to know what's receieved from this request, look here first
      console.log("haiiiiiiiii");
      console.log(data);
      console.log(data[0]);
      console.log("steps: ", data[0].steps);
    });
    } catch (error) {
      console.error("Full error details:", error);
      alert("There was an error retrieving the steps for load/unload");
    }
  }, []);

  // const moves = [
  //   [
  //     ["NAN", "Cat", "Dog", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "NAN"],
  //     ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
  //     ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
  //     ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
  //     ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
  //     ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
  //     ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
  //     ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
  //   ],
  //   [
  //     ["NAN", "Cat", "UNUSED", "UNUSED", "Dog", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "NAN"],
  //     ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
  //     ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
  //     ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
  //     ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
  //     ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
  //     ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
  //     ["UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED", "UNUSED"],
  //   ],
  // ];
  
  const [unload, setUnload] = useState(false);
  const [numLoad, setNumLoad] = useState<number>(0); // For the number of containers
  const [askNumLoad, setAskNumLoad] = useState(false); // To control visibility of popup
  const { selectedCellsId } = useSelectedCells(); // Use selectedCellsId directly 

  const continueProcess = () => {
      alert("Containers submitted successfully!");
      nextStepsPage();
      setAskNumLoad(false); // Close the popup after submission
  }

  const handleUnload = async () => {
    setUnload(true);

    const selectedCellsArray = Array.from(selectedCellsId); // Convert Set to array for the API

    try {
      const response = await fetch(`http://localhost:8080/confirmUnload?loadSize=${numLoad}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ selectedCells: selectedCellsArray }), // Send selectedCells in the request body
      });

      const data = await response.json();
      console.log(data.message); // Log the server message
      const isConfirmed = window.confirm(data.message); // Show confirmation pop-up

      if (isConfirmed) {
        // Send a second request to actually unload the data (write to the file)
        const confirmResponse = await fetch(`http://localhost:8080/confirmUnload?loadSize=${numLoad}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ selectedCells: selectedCellsArray }),
        });

        const confirmData = await confirmResponse.json();
        console.log(confirmData.message); // Log the confirm message

        setAskNumLoad(true);
      } else {
        alert("Unload action canceled.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // const handleSubmitContainers = async () => {
  //   try {
  //     const response = await fetch("http://localhost:8080/submitLoad", {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify({ numLoad }),
  //     });

  //     const data = await response.json();
  //     console.log(data.message);
  //     alert("Containers submitted successfully!");
  //     nextStepsPage();
  //     setAskNumLoad(false); // Close the popup after submission
  //   } catch (error) {
  //     console.error("Error submitting number of containers:", error);
  //   }
  // };

  return (
    <div className="flex flex-col items-center">
      <div className="w-full bg-blue-100 text-blue-900 text-center py-4 font-bold text-xl">
        Please select all containers to unload
      </div>

      <div className="flex flex-row mt-[5%] justify-evenly">
        <Containers selectable={true} grid={moves} currentMove={0} />
        <div className="flex flex-col w-[10%] space-y-[15%] items-center">
          <button
            onClick={handleUnload}
            style={{ width: "100px", marginLeft: "47%" }}
            className="w-[100%] h-[10%] mt-[15%] bg-blue-600 rounded-md font-bold text-white"
          >
            UNLOAD
          </button>
        </div>
      </div>

      {/* Modal for number of containers */}
      {askNumLoad && (
        <div className="fixed inset-0 flex justify-center items-center bg-black bg-opacity-50">
          <div className="bg-white p-6 rounded-md shadow-md">
            <h2 className="text-xl font-bold mb-4">How many containers will you load?</h2>
            <input
              type="number"
              value={numLoad}
              onChange={(e) => setNumLoad(Number(e.target.value))}
              className="p-2 border rounded-md mb-4"
              placeholder="Enter number of containers"
            />
            <div className="flex justify-end space-x-4">
              <button
                onClick={handleUnload}
                className="bg-blue-600 text-white px-4 py-2 rounded-md"
              >
                Submit Containers
              </button>
              <button
                onClick={continueProcess}
                className="bg-gray-300 px-4 py-2 rounded-md"
              >
                Continue
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Unload;
