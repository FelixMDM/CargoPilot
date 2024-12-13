"use client";
import { useState } from "react";

type Matrix = string[]

interface ContainerProps {
    grid: Matrix[]
}

const Containers = ({ grid }: ContainerProps)  => {
    const gridData = grid.length > 0 
    ? grid.flat().map(item => String(item)) 
    : Array(96).fill("NAN");

    // here maybe we can process and flatten this grid

    return (
        <div className="flex flex-col items-center">
            <div className="grid grid-cols-12 grid-rows-8">
                {gridData.map((cellValue, index) => (
                    <div
                        key={index}
                        className={`
                            cell m-auto 
                            ${cellValue === 1 
                                ? 'bg-blue-500 text-white' 
                                : 'bg-gray-100 text-gray-500'}
                        `}
                    >
                        {cellValue}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Containers;