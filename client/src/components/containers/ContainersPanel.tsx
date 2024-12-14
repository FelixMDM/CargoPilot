"use client";
import { useEffect, useState } from "react";
import Containers from "./Containers";

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
    const [moves, setMoves] = useState<Move[]>(Array(2).fill(Array(4).fill(0)));
    const [comments, setComments] = useState<string>("");
    const [currentIndex, setCurrentIndex] = useState(0);

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

    const grids: number[][][] = [
        [
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1],
        ],
        [
            [1, 0, 0],
            [0, 1, 1],
            [1, 0, 0],
        ],
        [
            [0, 0, 1],
            [1, 0, 1],
            [1, 1, 0],
        ],
    ];

    const nextGrid = () => {
        setCurrentIndex((prevIndex) => (prevIndex + 1) % grids.length);
    };

    const prevGrid = () => {
        setCurrentIndex((prevIndex) => (prevIndex - 1 + grids.length) % grids.length);
    };

    const handleSubmit = async (event: React.FormEvent<CommentFormElement>) => {
        event.preventDefault();
        const commentValue = event.currentTarget.elements.comments.value;
        
        await logToServer(`User submitted comment: "${commentValue}"`, 'info');
        setComments("");
    };

    useEffect(() => {
        try {
            fetch("http://localhost:8080/uploadManifest", {
                method: "GET",
            }).then((response) => response.json()).then((data) => {
                setGrid(data[0].steps);
                setMoves(data[1].moves);
                console.log("haiiiiiiiii");
                console.log(data);
                console.log(data[0]);
                console.log(data[1]);
            })

        } catch (error) {
            console.error("Full error details:", error);
            alert("There was an error getting manifest.");
        }
    }, []);

    return (
        <div className="flex flex-col items-center">
            <div className="flex flex-row mt-[5%] justify-evenly">
                <div className="flex flex-col w-[10%] space-y-[15%] items-center">
                    <button 
                        onClick={prevGrid} 
                        disabled={currentIndex === 0}
                        className="w-[100%] h-[10%] mt-[15%] bg-blue-600 rounded-md font-bold text-white">
                        PREV
                    </button>
                </div> 
                <Containers grid={grid[currentIndex]} steps={moves[currentIndex]}/>
                <div className="flex flex-col w-[10%] space-y-[15%] items-center">
                    <button 
                        onClick={nextGrid} 
                        disabled={currentIndex === grids.length - 1}
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