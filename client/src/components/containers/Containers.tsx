"use client";
import { useState } from "react";

interface ContainerProps {
    grid: number[][]
}

const Containers = ({ grid }: ContainerProps)  => {
    return (
        <div className="flex flex-col items-center">
            <div>
                {grid}
            </div>
            <div className="grid grid-cols-12 grid-rows-8">
                {Array.from({ length: 96 }).map((_, index: number) => (
                    <div key={index} className="cell m-auto">
                        {String(index % 12 + 1)}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Containers;