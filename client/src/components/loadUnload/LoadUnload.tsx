"use client";
import { useState } from "react";
import Containers from "../containers/containersLoadUnload";

const Unload = () => {
    const [unload, setUnload] = useState(false);

    const handleUnload = () => {
        setUnload(true);
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
                        style={{ width: '100px', marginLeft: '47%' }} 
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
