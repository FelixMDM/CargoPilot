"use client";
import { useState } from "react";
import Containers from "./Containers";

interface FormElements extends HTMLFormControlsCollection {
    comments: HTMLInputElement
}

interface CommentFormElement extends HTMLFormElement {
    readonly elements: FormElements
}

const ContainersPanel = ()  => {
    const [instruction, setInstruction] = useState("No steps generated")
    const [comments, setComments] = useState<string>("");
    const [currentIndex, setCurrentIndex] = useState(0);
    
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

    const handleSubmit = (event: React.FormEvent<CommentFormElement>) => {
        event.preventDefault();
        const commentValue = event.currentTarget.elements.comments.value;
        console.log("Submitted Comment:", commentValue);
        setComments("");
    };

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
                    <div className="border rounded-md">
                        <p className="m-2">
                            {/* This should be dynamically updated based on the array map */}
                            {instruction}
                        </p>
                    </div>
                </div> 
                <Containers grid={grids[currentIndex]}/>
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
            <div className="w-[80%] bg-blue-950">
                tita?   
            </div>
            <div className="w-[80%] h-[300px] bg-red-950">
                tita?   
            </div>
        </div>
    );
}

export default ContainersPanel;