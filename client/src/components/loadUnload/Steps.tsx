"use client";
import React from "react";
import Link from "next/link";
import { useState, useEffect } from "react";
import Containers from "../containers/containersLoadUnload";

type Matrix = string[][]
type Move = [number, number, number, number]

interface FormElements extends HTMLFormControlsCollection {
  comments: HTMLInputElement
}

interface CommentFormElement extends HTMLFormElement {
  readonly elements: FormElements
}

const Steps = () => {
  const [moves, setGrid] = useState<Matrix[]>([Array(8).fill(Array(12).fill("UNUSED"))]);
  const [path, setMovesFelix] = useState<Move[]>(Array(2).fill(Array(4).fill(0)));
  const [currentLoadIndex, setCurrentLoadIndex] = useState(96);
  const [loadedCellsInfo, setLoadedCellsInfo] = useState<Array<{ posX: number; posY: number; weight: number; label: string }>>([
    { posX: 0, posY: 0, weight: 0, label: "test" },
  ]);
  
  // const [currentMoveIndex, setCurrentMoveIndex] = useState(0);
  //const [currentIndex, setCurrentIndex] = useState(0);
  //const [currentMoveIndex, setCurrentMoveIndex] = useState(0);


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


  //const moves = grid;
  //const path = movesX; // Path with cell coordinates and actions

  const [currentMove, setCurrentMove] = useState(0);
  const [highlightedCell, setHighlightedCell] = useState<{ row: number; col: number; bgColor: string } | undefined>(undefined);
  const [highlightedCell2, setHighlightedCell2] = useState<{ row: number; col: number; bgColor: string } | undefined>(undefined);

  
  const [showComplete, setShowComplete] = useState(false);
  const [askLoadInfo, setAskLoadInfo] = useState(false);
  const [showDownload, setShowDownload] = useState(false);
  const [manifestDownloaded, setManifestDownloaded] = useState(false);
  const [containerName, setContainerName] = useState("");
  const [containerWeight, setContainerWeight] = useState(0);

  const [comments, setComments] = useState<string>("");
  
  useEffect(() => {
    // Only attempt to process path when currentMove is greater than 0 and path exists
    console.log(currentMove);
    console.log("grid", moves)
    console.log("path:", path);
    if (currentMove > 0 && path) {
      const currentAction = moves[currentMove][0];
      const row = path[currentMove - 1][0];
      const col = path[currentMove - 1][1];
      const action = path[currentMove - 1][2]; // use the action from the path array
      const row2 = path[currentMove - 1][2]
      const col2 = path[currentMove - 1][3]

      if(action > -1){
        setHighlightedCell({ row: row, col: col, bgColor: "red" });
        setHighlightedCell2({ row: row2, col: col2, bgColor: "green"});
      } else{
        const bgColor = action === -1 ? "green" : action === -2 ? "red" : "";
        if (action === -1) {
          setAskLoadInfo(true);
        }
        setHighlightedCell({ row, col, bgColor });
        setHighlightedCell2(undefined);
      }
      }
    else if (currentMove === 0) {
      setHighlightedCell(undefined);
      setHighlightedCell2(undefined);
  }
  }, [currentMove, path]);
  
  
  const handlePrev = () => {
    if (currentMove > 0) {
      setCurrentMove((prevMove) => prevMove - 1);
      setAskLoadInfo(false);
    }
  };
  
  const handleNext = () => {
    if (currentMove < moves.length - 1) {
      setCurrentMove((prevMove) => prevMove + 1);
      setAskLoadInfo(false);
    } else if (currentMove === moves.length - 1) {
      setShowComplete(true);
    }
  };
  

  const handleAskLoadInfoSubmit = () => {
    if (highlightedCell || highlightedCell2) {
      let updatedGrid = [...moves];
      for(let i = 0; i < updatedGrid.length; i++){
        for(let j = 0; j < 8; j++){
          for(let k = 0; k < 12; k++){
            if(updatedGrid[i][j][k] === currentLoadIndex.toString()){
              updatedGrid[i][j][k] = containerName;
            }
          }
        }
      }
      setGrid(updatedGrid);
      setCurrentLoadIndex(currentLoadIndex + 1);
  
      setLoadedCellsInfo((prev) => {
        const updatedLoadedCellsInfo = [
          ...prev,
          {
            posX: highlightedCell.row,
            posY: highlightedCell.col,
            weight: containerWeight,
            label: containerName,
          }
        ];

        const currItem = updatedLoadedCellsInfo[updatedLoadedCellsInfo.length - 1];
        console.log(`Updated Container: ${currItem.posX}, ${currItem.posY} Weight: ${currItem.weight}, Title ${currItem.label}`);
        return updatedLoadedCellsInfo;
      });
  
      setAskLoadInfo(false);
      setContainerName("");
      setContainerWeight(0);
    }
  };
  
  const handleConfirm = () => {
    try {
      fetch("http://localhost:8080/saveLoadedCellsInfo", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(loadedCellsInfo)
      })
      .then((data) => {
        console.log("Loaded cells info saved successfully:", data);
        // Optionally reset the state or show a success message
        setShowComplete(false);
        setShowDownload(true);
      })
      .catch((error) => {
        console.error("Error saving loaded cells info:", error);
        // Optionally show an error message to the user
        alert("Failed to save loaded cells information");
      });
    } catch (error) {
      console.error("Full error details:", error);
      alert("There was an error saving the loaded cells information");
    }
  };

  const handleDownload = () => {
    window.location.href = 'http://localhost:8080/downloadManifest';
    setManifestDownloaded(true);
  };

  const logToServer = async (message: string, level: string) => {
    try {
        await fetch('http://localhost:8080/log', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message,
                level,
                component: 'ContainersPanel',
                timestamp: new Date().toISOString()
            })
        });
    } catch (error) {
        console.error('Failed to send log to server:', error);
    }
  };

  const handleSubmit = async (event: React.FormEvent<CommentFormElement>) => {
    event.preventDefault();
    const commentValue = event.currentTarget.elements.comments.value;
    await logToServer(`User submitted comment: "${commentValue}"`, 'info');
    setComments("");
  };

  let [xPos, yPos, dxPos, dyPos] = [0, 0, 0, 0]

  if (currentMove < moves.length - 1) {
    let [xPos, yPos, dxPos, dyPos] = path[currentMove + 1]
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
          {currentMove >= 0 && currentMove < moves.length - 1 && (
            <>
              {dxPos === -1 && (
                  <p className="bg-gray-50 border p-2 border-gray-300 text-gray-900 text-sm rounded-md">
                    Load container {moves[currentMove][xPos][yPos]} to ({xPos}, {yPos})
                  </p>
                )}
                {dxPos === -2 && (
                  <p className="bg-gray-50 border p-2 border-gray-300 text-gray-900 text-sm rounded-md">
                    Unload container at ({xPos}, {yPos}, {moves[currentMove][xPos][yPos]})
                  </p>
                )}
                {dxPos >= 0 && (
                  <p className="bg-gray-50 border p-2 border-gray-300 text-gray-900 text-sm rounded-md">
                    Move starting cell from ({xPos}, {yPos}) to ({dxPos}, {dyPos}).
                  </p>
                )}
            </>
          )}
        </div>

        <Containers
          selectable={false}
          grid={moves}
          currentMove={currentMove}
          highlightedCell={highlightedCell} // pass the highlighted cell prop
          highlightedCell2={highlightedCell2}
        />

        <div className="flex flex-col w-[10%] space-y-[15%] items-center">
          <button
            style={{ width: "100px", marginLeft: "47%" }}
            className="w-[100%] h-[10%] mt-[15%] bg-blue-600 rounded-md font-bold text-white"
            onClick={handleNext}
            disabled={currentMove === moves.length}
          >
            NEXT
          </button>

          <form onSubmit={handleSubmit} className="w-full ml-[39%]">
            <div className="flex flex-col">
                <input
                    id="comments"
                    name="comments"
                    type="text"
                    value={comments}
                    onChange={(e) => setComments(e.target.value)}
                    className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-md focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                    placeholder="Comments"
                    required
                />
            </div>
            <button
                type="submit"   
                className="w-full mt-[15%] py-1 bg-blue-600 rounded-md font-bold text-white"
            >
                SUBMIT
            </button>
          </form>
        </div>
      </div>
      
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
                onChange={(e) => setContainerName(e.target.value)} // e.target.value
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
      
      {showComplete && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
          <div className="bg-white rounded-lg p-6 w-[30%]">
            <h2 className="text-lg font-bold mb-4"> Congrats All Steps Complete!</h2>
            <div className="flex justify-end space-x-4">
              <button
                className="bg-gray-500 text-white rounded-md px-4 py-2"
                onClick={() => setShowComplete(false)}
              >
                Cancel
              </button>
              <button
                className="bg-blue-600 text-white rounded-md px-4 py-2"
                onClick={handleConfirm}
              >
                Confirm
              </button>
            </div>
          </div>
        </div>
      )}

      {showDownload && (
        <div className="absolute flex flex-col h-[50%] w-[50%] left-[25%] rounded-md opacity-95 bg-slate-500 text-white font-bold text-center justify-center items-center">
        <div className="">
            Load Unload finished. Please download and email outbound manifest.  
        </div>
        <button
            onClick={handleDownload}
            className="w-[300px] p-4 m-2 bg-green-600 rounded-2xl hover:text-white cursor-pointer"
        >
            Download Manifest
        </button>
        {manifestDownloaded && 
            <Link
                href="/options"
            >
                Back to options
            </Link>
        }
    </div>
      )}

    </div>
  );
};

export default Steps;
