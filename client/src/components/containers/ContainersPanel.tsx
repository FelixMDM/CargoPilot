"use client";
import { useState } from "react";
import Containers from "./Containers";

const ContainersPanel = ()  => {
    const [instruction, setInstruction] = useState("No steps generated")

    return (
        <div className="flex flex-col items-center">
            <div className="flex flex-row mt-[5%] justify-evenly">
                <div className="flex flex-col w-[10%] space-y-[15%] items-center">
                    <button className="w-[100%] h-[10%] mt-[15%] bg-blue-600 rounded-md font-bold text-white">
                        PREV
                    </button>
                    <div className="border rounded-md">
                        <p className="m-2">
                            {/* This should be dynamically updated based on the array map */}
                            {instruction}
                        </p>
                    </div>
                </div> 
                <Containers />
                <div className="flex flex-col w-[10%] space-y-[15%] items-center">
                    <button className="w-[100%] h-[10%] mt-[15%] bg-blue-600 rounded-md font-bold text-white">
                        NEXT
                    </button>
                    <div>
                        <input type="text" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-md focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" placeholder="Comments" required />
                    </div>
                    <button className="w-[100%] h-[10%] mt-[15%] bg-blue-600 rounded-md font-bold text-white">
                        SUBMIT
                    </button>
                </div>
            </div>
            <div className="w-[80%] bg-blue-950 h-[20%]">
                
            </div>
        </div>
    );
}

export default ContainersPanel;