"use client";
import { useEffect, useState } from "react";
import Containers from "./Containers";
import Link from "next/link";

interface FormElements extends HTMLFormControlsCollection {
    comments: HTMLInputElement
}

interface CommentFormElement extends HTMLFormElement {
    readonly elements: FormElements
}

type Matrix = string[][]
type Move = [number, number, number, number]

const ContainersPanel = ()  => {

    const [grid, setGrid] = useState<Matrix[]>([Array(8).fill(Array(12).fill("UNUSED"))]);
    const [moves, setMoves] = useState<Move[]>(Array(2).fill(Array(5).fill(0)));
    const [currentIndex, setCurrentIndex] = useState(0);

    const [comments, setComments] = useState<string>("");
    const [manifestDownloaded, setManifestDownloaded] = useState(false);
    
    const [startCell, setStartCell] = useState("None");
    const [currentMoveIndex, setCurrentMoveIndex] = useState(0);

    const [cost, setCost] = useState(0);

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

    const updateGridForMove = (moveIndex: number) => {
        if (!grid.length || !moves.length || moveIndex < 0 || moveIndex >= moves.length) return;

        const [startX, startY] = moves[moveIndex];
        setStartCell(grid[moveIndex][startX][startY]);
    };

    const nextGrid = () => {
        if (currentMoveIndex < moves.length - 1) {
            updateGridForMove(currentMoveIndex + 1);
            setCurrentMoveIndex((prev) => prev + 1);
            setCost(cost - moves[currentMoveIndex][4])
        }
    
        if (currentIndex < grid.length - 1) {
            setCurrentIndex((prev) => prev + 1);
        }
    };

    const prevGrid = () => {
        if (currentMoveIndex > 0) {
            updateGridForMove(currentMoveIndex - 1);
            setCurrentMoveIndex((prev) => prev - 1);
        }
    
        if (currentIndex > 0) {
            setCurrentIndex((prev) => prev - 1);
        }
    };

    const handleSubmit = async (event: React.FormEvent<CommentFormElement>) => {
        event.preventDefault();
        const commentValue = event.currentTarget.elements.comments.value;
        await logToServer(`User submitted comment: "${commentValue}"`, 'info');
        setComments("");
    };

    const handleDownload = () => {
        // Clear save state before downloading
        fetch('http://localhost:8080/clearStepState', {
            method: 'POST'
        }).then(() => {
            window.location.href = 'http://localhost:8080/downloadManifest';
            setManifestDownloaded(true);
        });
    }

    // Save state when steps change
    useEffect(() => {
        if (grid.length > 1 && moves.length > 0) {
            fetch('http://localhost:8080/saveStepState', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    currentIndex,
                    grid,
                    moves
                })
            }).catch(error => console.error('Failed to save state:', error));
        }
    }, [currentIndex, grid, moves]);

    useEffect(() => {
        try {
            fetch('http://localhost:8080/loadStepState')
                .then((response) => response.json())
                .then((stateData) => {
                    if (stateData.exists && stateData.grid.length > 1) {
                        setGrid(stateData.grid);
                        setMoves(stateData.moves);
                        setCurrentIndex(stateData.currentStep);
                        setCurrentMoveIndex(stateData.currentStep);
                        const [startX, startY] = stateData.moves[stateData.currentStep];
                        setStartCell(stateData.grid[stateData.currentStep][startX][startY+1]);
                    } else {
                        fetch("http://localhost:8080/uploadManifest", {
                            method: "GET",
                        }).then((response) => response.json()).then((data) => {
                            setGrid(data[0].steps);
                            setMoves(data[1].moves);
                            setCost(data[2].cost);
                            console.log("haiiiiiiiii");
                            console.log(data);
                            console.log(data[0]);
                            console.log(data[1]);
                            {
                                if (grid.length > 0 && moves.length > 0) {
                                    const [startX, startY] = moves[currentMoveIndex];
                                    // console.log("yolo",data[0].steps[currentMoveIndex])
                                    setStartCell(data[0].steps[currentMoveIndex][startX][startY+1]);
                                }
                            }
                        })
                    }
                })
        } catch (error) {
            console.error("Full error details:", error);
            alert("There was an error getting manifest.");
        }
    }, []);

    // Clear state when reaching end of steps
    useEffect(() => {
        if (currentIndex === moves.length) {
            fetch('http://localhost:8080/clearStepState', { 
                method: 'POST' 
            });
        }
    }, [currentIndex, moves.length]);

    return (
        <div className="flex flex-col items-center">
            <div className="w-full bg-blue-100 text-blue-900 text-center py-4 font-bold text-xl">
                Estimated Cost: {cost} STEPS: {currentIndex}/{moves.length}
            </div>
            <div className="flex flex-row mt-[5%] justify-evenly">
                <div className="flex flex-col w-[10%] space-y-[15%] items-center">
                    <button 
                        onClick={prevGrid} 
                        disabled={currentIndex === 0}
                        className="w-[100%] h-[10%] mt-[15%] bg-blue-600 rounded-md font-bold text-white">
                        PREV
                    </button>
                    {currentIndex >= 0 && currentIndex < moves.length && 
                        <p className="bg-gray-50 border p-2 border-gray-300 text-gray-900 text-sm rounded-md">
                            Move {startCell} from ({moves[currentMoveIndex][0]}, {moves[currentMoveIndex][1]}) to ({moves[currentMoveIndex][2]}, {moves[currentMoveIndex][3]}). Cost: {moves[currentIndex][4]}
                        </p>
                    }
                </div> 
                <div className="flex flex-col">
                    {currentIndex === moves.length && 
                        <div className="absolute flex flex-col h-[50%] w-[50%] left-[25%] rounded-md opacity-95 bg-slate-500 text-white font-bold text-center justify-center items-center">
                            <div className="">
                                Balance finished. Please download and email outbound manifest.  
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
                    }
                    <Containers grid={grid[currentIndex]} steps={moves[currentIndex]}/>
                </div>
                <div className="flex flex-col w-[10%] space-y-[15%] items-center">
                    <button 
                        onClick={nextGrid} 
                        disabled={currentIndex === grid.length - 1}
                        className="w-[100%] h-[10%] mt-[15%] bg-blue-600 rounded-md font-bold text-white">
                        NEXT
                    </button>
                    <form onSubmit={handleSubmit} className="w-full">
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
            <div className="w-[80%] text-white p-2 font-bold text-2xl bg-blue-950">
                TITANIC
            </div>
            <div className="w-[80%] h-[300px] p-2 text-white font-bold text-2xl bg-red-950">
                TITANIC 
            </div>
        </div>
    );
}

export default ContainersPanel;