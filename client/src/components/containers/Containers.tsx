"use client";

type Matrix = string[][]

interface ContainerProps {
    grid?: string[][]
    steps?: [number, number, number, number]
}

const Containers = ({ grid, steps }: ContainerProps)  => {
    console.log("This is the grid that is passed into container component")
    console.log(grid)
    console.log("These are the corresponding steps for the operator to execute")
    console.log(steps)
    const defaultGrid: Matrix = Array.from({ length: 8 }, () =>
        Array.from({ length: 12 }, () => "UNUSED")
    );

    const renderGrid = grid?.length ? grid : defaultGrid;

    return (
        <div className="flex flex-col items-center">
            <div className="grid grid-cols-12 grid-rows-8">
                {renderGrid.map((row, rowIndex) =>
                    row.map((name, colIndex) => {
                        let cellClass = "cell m-auto text-center";

                        if (steps) {
                            const [startX, startY, endX, endY] = steps;
                            if (rowIndex === startX && colIndex === startY) {
                                cellClass += " bg-red-500";
                            } else if (rowIndex === endX && colIndex === endY) {
                                cellClass += " bg-green-500";
                            }
                        }

                        if (name === "NAN") {
                            cellClass += " bg-black text-white";
                        }

                        return (
                            <div
                                key={`${rowIndex}-${colIndex}`}
                                className={cellClass}
                            >
                                {name}
                            </div>
                        );
                    })
                )}
            </div>
        </div>
    );
}

export default Containers;