"use client";
import { useState } from "react";

const Containers = ()  => {
    return (
        <div className="flex flex-col items-center">
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