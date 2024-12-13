"use client";
import { useState } from "react";

type Matrix = string[]

interface ContainerProps {
    grid: string[][]
}

const Containers = ({ grid }: ContainerProps)  => {
    console.log("this is the current step", grid)

    return (
        <div className="flex flex-col items-center">
            <div className="grid grid-cols-12 grid-rows-8">
                {/* {grid?.map((row, index) =>
                    row.map((name, colIndex) => (
                        <div 
                            key={index}
                            className="cell m-auto">
                            {name}
                        </div>
                    ))
                )} */}

                {grid?.map((name, index) =>
                    <div 
                        key={index}
                        className="cell m-auto">
                        {name}
                    </div>
                )}
            </div>
        </div>
    );
}

export default Containers;