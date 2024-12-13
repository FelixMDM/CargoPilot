"use client";
import React, { useState } from "react";
import Containers from "../containers/containersLoadUnload";
import { useSelectedCells } from "./SelectedCellsContext";

const Unload = () => {
  const [unload, setUnload] = useState(false);
  const { getSelectedCells } = useSelectedCells();

  const handleUnload = async () => {
    setUnload(true);
    const selectedCellsArray = getSelectedCells();
  
    try {
      const response = await fetch("http://localhost:8080/unloadAction", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ selectedCells: selectedCellsArray }), // send selectedCells in the request body
      });
  
      const data = await response.json();
      console.log(data.message); // Log the server message
      const isConfirmed = window.confirm(data.message); //show alert with confirmation message

      if (isConfirmed) {
        // Send a second request to actually unload the data (write to the file)
        const confirmResponse = await fetch("http://localhost:8080/confirmUnload", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ selectedCells: selectedCellsArray }),
        });
  
        const confirmData = await confirmResponse.json();
      } else {
        alert("Unload action canceled.");
      }
  
    } catch (error) {
      // Catch and log any errors during the fetch
      console.error("Error:", error);
    }
  };
  

  return (
    <div className="flex flex-col items-center">
      <div className="w-full bg-blue-100 text-blue-900 text-center py-4 font-bold text-xl">
        Please select all containers to unload
      </div>

      <div className="flex flex-row mt-[5%] justify-evenly">
        <Containers />
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
    </div>
  );
};

export default Unload;
